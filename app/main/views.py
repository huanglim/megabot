import os,time,json, logging
from flask import render_template,request,jsonify,send_from_directory,\
    current_app,session,redirect,g, abort, url_for, flash
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from . import main
from .. import watson_conversion,cloudant_nosql_db
from ..auth.views import login
from .forms import RegistrationForm
from wtforms import SelectField
from threading import current_thread
from ..utility import read_excel,  \
                        verify_select_level, verify_email_format, \
                        verify_template, verify_input,  \
                        get_approver, convert_country, convert_company

from werkzeug.utils import secure_filename
from json2html import *

from pprint import pprint

logging.basicConfig(level=logging.INFO)

@main.route('/',methods=['GET','POST'])
@login
def index():
    logging.info('in index')
    #
    # if current_app.config['DEBUG'] or current_app.config['TESTING']:
    #     return render_template('index.html')
    # else:
    #     # if 'id_token' not in request.cookies:
    #     if 'id_token' not in session:
    #         redirect_uri = current_app.config['OIDC_CALLBACK']
    #         current_app.flow = flow_from_clientsecrets(current_app.config['CLIENT_SECRETS_JSON'],
    #                                          scope='openid',
    #                                          redirect_uri=redirect_uri)
    #         auth_uri = current_app.flow.step1_get_authorize_url()
    #         return redirect(auth_uri)
    #     else:
    #         return render_template('index.html', name=session['id_token']['firstName'].replace('%20', ' '))
    return render_template('index.html', name=session['id_token']['firstName'].replace('%20', ' '))

@main.route('/oidc_callback')
def oidc_callback():
    logging.info('in callback')
    code = request.args.get('code')
    if 'id_token' not in session and code is not None:
        try:
            logging.info('in init id_token')
            credentials = current_app.flow.step2_exchange(code)
            id_token = credentials.id_token
            logging.info('id token is {}'.format(id_token))
            id_token['firstName'] = id_token['firstName'].replace('%20',' ')
            id_token['lastName'] = id_token['lastName'].replace('%20', ' ')
            session['id_token'] = id_token
            # response = current_app.make_response\
            #     (render_template('index.html', name=session['id_token']['firstName']))
            response = current_app.make_response\
                (redirect(current_app.config['next']))
            response.set_cookie('id_token',id_token)
        except FlowExchangeError:
            abort(401)
        finally:
            # return redirect(current_app.config['HOME_URL'])
            return response
    else:
        return redirect(current_app.config['next'])
        # return render_template('index.html', name=session['id_token']['firstName'].replace('%20', ' '))

@main.route('/userinfo', methods=['GET'])
def userinfo():
    if session.get('id_token'):
        try:
            user = cloudant_nosql_db.get_user_info(session['id_token']['emailAddress'])
            # pprint(user)
        except IndexError:
            cloudant_nosql_db.init_user(session['id_token'])
            user = cloudant_nosql_db.get_user_info(session['id_token']['emailAddress'])
    else:
        abort(404)
    return render_template('userinfo.html', user=user)

@main.route('/edit_access', methods=['GET','POST'])
def edit_access():

    if request.method == 'POST':
        _country = request.values.getlist('country')
        country_access = list(map(convert_country, _country))

        _company = request.values.getlist('company')
        company_access = list(map(convert_company, _company))

        doc = cloudant_nosql_db.get_user_info(session['id_token']['emailAddress'])
        if country_access:
            cloudant_nosql_db.update_pending_country_accesses(doc.get('_id'), country_access)

        if company_access:
            cloudant_nosql_db.update_pending_company_accesses(doc.get('_id'), company_access)
        # return redirect(url_for('main.userinfo'))
        doc = cloudant_nosql_db.get_user_info(session['id_token']['emailAddress'])

        # Send the email for approval
        to =  get_approver(session['id_token']['emailAddress'])
        subject = 'Access request for {}'.format(doc.get('emailAddress'))
        confirm_link = current_app.config['HOME_URL']+'confirm_access/'+session['id_token']['emailAddress']
        sender = current_app.config['MAIL_SENDER']
        # send_email(approver, subject, 'mail_confirm_access', confirm_link)
        cloudant_nosql_db.write_to_mail(to, sender, subject, confirm_link, doc.get('emailAddress'))
        # send_email_api(to, sender, subject, confirm_link)
        return render_template('userinfo.html', user=doc)

    return render_template('edit_access.html')

@main.route('/confirm_access/<emailAddress>', methods=['GET','POST'])
@login
def confirm_access(emailAddress):

    # emailAddress = request.args.get('emailAddress')
    if not emailAddress:
        abort(404)

    approver = session['id_token']['firstName']

    approver_mailaddr = session['id_token']['emailAddress']
    if approver_mailaddr != get_approver(emailAddress):
        abort(401)

    try:
        requester = cloudant_nosql_db.get_user_info(emailAddress)
    except Exception as e:
        abort(404)

    if request.method == 'POST':
        logging.info('in the update pending process')
        if requester.get('pending_country_accesses'):
            try:
                cloudant_nosql_db.update_approved_country_accesses(requester.get('_id'),
                                                                   requester.get('pending_country_accesses'))
            except Exception as e:
                raise
            else:
                cloudant_nosql_db.update_pending_country_accesses(requester.get('_id'),
                                                                   None)
        if requester.get('pending_company_accesses'):
            try:
                cloudant_nosql_db.update_approved_company_accesses(requester.get('_id'),
                                                                   requester.get('pending_company_accesses'))
            except Exception as e:
                raise
            else:
                cloudant_nosql_db.update_pending_company_accesses(requester.get('_id'),
                                                                   None)

        if 'https://' not in request.url:
            _url = request.url.replace('http://', 'https://')
        else:
            _url = request.url

        return redirect(_url)
        # return render_template('confirm_access.html', user=user)
    return render_template('confirm_access.html', approver=approver, requester=requester)

@main.route("/ask",methods=['POST'])
def ask():
    input = str(request.form['messageText'])
    return jsonify({'status': 'OK',
                    'answer': watson_conversion.get_response(input)})

@main.route("/enable_schedule",methods=['GET'])
def enable_schedule():

    _id = request.args['id']
    if not _id:
        render_template('404')

    try:
        cloudant_nosql_db.update_schedule_status(_id, 'active')
    except Exception as e:
        logging.error(e)
        raise
    else:
        return jsonify({'status': True})

@main.route("/disable_schedule",methods=['GET'])
def disable_schedule():

    _id = request.args['id']
    if not _id:
        render_template('404')

    try:
        cloudant_nosql_db.update_schedule_status(_id, 'disable')
    except Exception as e:
        logging.error(e)
        raise
    else:
        return jsonify({'status': True})

@main.route("/schedule", methods=["GET", "POST"])
@login
def schedule():
    emailAddress = session['id_token']['emailAddress']
    try:
        schedules = cloudant_nosql_db.get_user_schedules(emailAddress)
    except IndexError as e:
        logging.info('There is no schedule for the user {}'.format(emailAddress))
        schedules = None
    return render_template('schedule.html', schedules=schedules)

@main.route("/task", methods=["GET", "POST"])
@login
def task():
    emailAddress = session['id_token']['emailAddress']
    try:
        tasks = cloudant_nosql_db.get_user_tasks(emailAddress)
        logging.info(tasks)
    except IndexError as e:
        logging.info('There is no task for the user {}'.format(emailAddress))
        tasks = None
    return render_template('task.html', tasks=tasks)

@main.route("/edit_schedule", methods=["GET","POST"])
def edit_schedule():
    form = RegistrationForm(request.form)
    # user = cloudant_nosql_db.get_user_info(session['id_token']['emailAddress'])
    # fix bug for -502 when use directly add schedule before init user information.
    try:
        user = cloudant_nosql_db.get_user_info(session['id_token']['emailAddress'])
        # pprint(user)
    except IndexError:
        cloudant_nosql_db.init_user(session['id_token'])
        user = cloudant_nosql_db.get_user_info(session['id_token']['emailAddress'])

    if request.method == 'POST' and form.validate():
        logging.info('{}'.format(request.form.get('sel_cty_comp')))
        schedule_record = {
            "user": session['id_token']['emailAddress'],
            "Select Report Level": form.sel_rpt_lvl.data,
            "Select Country/Company": request.form.get('sel_cty_comp'),
            "Account / Employee": form.sel_acc_emp.data,
            "Weekending Date Range Start date": str(form.wk_date_start.data),
            "Weekending Date Range End date": str(form.wk_date_end.data),
            "Select Report Criteria": form.sel_rpt_crit.data,
            "Select Report Format": form.sel_rpt_format.data,
            "Input Field": form.input_field.data,
            "run date":str(form.run_date.data),
            "schedule cycle":form.schedule_cycle.data
        }
        cloudant_nosql_db.write_to_schedule(schedule_record)
        redirect_url = url_for('main.schedule')
        if 'https://' not in redirect_url:
            # to fix redirect issue for bluemix
            _url = current_app.config['HOME_URL'][:-1]+redirect_url
        else:
            _url = redirect_url
        logging.info('The redirect url is {}, the old one is {}'.format(_url, redirect_url))
        print(_url, redirect_url)

        return redirect(_url)

    return render_template('edit_schedule.html', form=form, user=user)

# download template file
@main.route('/download/<filename>')
def download_template(filename):
    logging.debug('In the function: {}, the file is {}'.\
                  format('download_template',current_app.config['DOWNLOAD_FOLDER']))
    if os.path.isfile(os.path.join(current_app.config['DOWNLOAD_FOLDER'],
                                   filename)):
        logging.debug('Has the file{} '.format(os.path.join(current_app.config['DOWNLOAD_FOLDER'],
                                   filename)))
        return send_from_directory(current_app.config['DOWNLOAD_FOLDER'],
                                   filename, as_attachment=True)

# upload parameters file
@main.route('/upload', methods=['POST'], strict_slashes=False)
def upload():
    logging.info('start upload')

    status = True
    status_message = ''
    user_addr = session['id_token']['emailAddress']

    file_dir = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    # get the file object from request
    f = request.files['file']
    # check if allowed file format
    allowed_file = lambda x : '.' in x and x.rsplit('.',1)[1] \
                              in current_app.config['ALLOWED_EXTENSIONS']

    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        # get the filename and file extension
        filename,ext = fname.rsplit('.', 1)
        seconds = str(time.time()).replace('.','_')
        # renamed file name with adding time(the seconds)
        new_filename = filename + '_' + seconds + '.' + ext
        # save file to upload folder
        f.save(os.path.join(file_dir, new_filename))
        full_file_name = os.path.join(file_dir, new_filename)
        #read template
        logging.info('complete save %s' %full_file_name)

        try:
            excel_content = read_excel(full_file_name)
        except Exception as e:
            logging.error('Error in read execl! %s' %e)
            status = False
            status_message = 'Please upload latest version of template and upload the correct one." \
            "Your report is not running. '

        logging.debug('The email address is %s, type is %s' %(user_addr, type(user_addr)))

        if not verify_template(excel_content):
            status = False
            status_message = "Your template is not up to date. Please download the latest one! "

            return jsonify({'status': status,
                            'request_status': status_message
                            })

        if status:
            for index, request_record in enumerate(excel_content):
                logging.info('loop & verify request record %s' %request_record)
                if not verify_select_level(request_record.get('Select Report Level'),
                    request_record.get('Select Country/Company')):
                    status = False
                    status_message = "Invalid report level or country/company level, " \
                    "Please double check your input, Your input is: "
                    break
                # elif not verify_date(request_record['Weekending Date Range Start date'],
                #                      request_record['Weekending Date Range End date']):
                #     status = False
                #     status_message = 'Invalid Weekending Date Range Start or End date, Please double check your input, \
                #     Your input is: '
                #     break
                elif not cloudant_nosql_db.is_authorized(user_addr,
                                                         request_record['Select Report Level'],
                                                         request_record['Select Country/Company']):
                    status = False
                    status_message = "Your privilege checking is failed. Please go to userinfo to confirm your access. " \
                    "Userinfo is in the right-top of screen."
                    return jsonify({'status': 'failed',
                        'request_status':status_message
                        })
                elif not verify_input(request_record['Input Field']):
                    # logging.debug(request_record['Input Field'])
                    status = False
                    status_message = "Invalid Input Field, please double check your input,"\
                     "use COMMA to seprate your account or sn and ensure there is " \
                     "no Enter in your input. \nYour input is: "
                    break
                else:
                    status_message = "Your {} record is now in process, the email will send to {}," \
                                     "please wait for a while!".format(index+1, user_addr)
                    cloudant_nosql_db.write_to_request(request_record, user=user_addr, status='submitted')

        # convert excel to html table
        excel_json = json.dumps(excel_content)
        excel_html = json2html.convert(json=excel_json,
                                       table_attributes="id=\"table-7\"")

        # save parameters file to db
        # for document in excel_content:
        #     # can get the intranet id from sso token
        #     # which can be stored in session or g
        #     cloudant_nosql_db.write_to_db(document,user=None)

        return jsonify({'status': 'OK', 'excelHTML':excel_html,
                        'filename':new_filename,
                        'request_status':status_message
                        })
    else:
        return jsonify({'status':'Not OK'})