import os,time,json, logging
from flask import render_template,request,jsonify,send_from_directory,\
    current_app,session,redirect,g
from . import main
from .. import watson_conversion,cloudant_nosql_db

from ..automation import read_excel, send_request, \
                        verify_select_level, verify_email_format, \
                        verify_date, verify_input
from werkzeug.utils import secure_filename
from json2html import *

logging.basicConfig(level=logging.DEBUG)

@main.route('/',methods=['GET','POST'])
def index():
    if current_app.config['DEBUG'] or current_app.config['TESTING']:
        return render_template('index.html')
    else:
        if 'id_token' not in session:
            auth_uri = g.flow.step1_get_authorize_url()
            return redirect(auth_uri)
        else:
            return render_template('index.html', name=session['id_token']['firstName'].replace('%20', ' '))


# communicate with watson conversation API
@main.route("/ask",methods=['POST'])
def ask():
    input = str(request.form['messageText'])
    return jsonify({'status': 'OK',
                    'answer': watson_conversion.get_response(input)})


# download template file
@main.route('/download/<filename>')
def download_template(filename):
    if os.path.isfile(os.path.join(current_app.config['DOWNLOAD_FOLDER'],
                                   filename)):
        return send_from_directory(current_app.config['DOWNLOAD_FOLDER'],
                                   filename, as_attachment=True)


# upload parameters file
@main.route('/upload', methods=['POST'], strict_slashes=False)
def upload():
    logging.info('start upload')

    status_code = True
    email_addr = ''

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
            excel_content, email_addr = read_excel(full_file_name)
        except Exception as e:
            logging.error('Error in read execl! %s' %e)
            status_code = False
            status_message = 'Please upload latest version of template and upload the correct one. \
            Your report is not running. '

        logging.debug('The email address is %s, type is %s' %(email_addr, type(email_addr)))

        if not verify_email_format(email_addr):
            status_code = False
            status_message = 'Please input correct email address! Your report is not running, please correct and reupload. \
            Your input is '

        if status_code:
            for request_record in excel_content:
                logging.info('loop & verify request record %s' %request_record)
                if not verify_select_level(request_record['Select Report Level'],
                    request_record['Select Country/Company']):
                    status_code = False
                    status_message = 'Invalid report level or country/company level, Please double check your input, \
                    Your input is: '
                    break
                # elif not verify_date(request_record['Weekending Date Range Start date'], 
                #                      request_record['Weekending Date Range End date']):
                #     status_code = False
                #     status_message = 'Invalid Weekending Date Range Start or End date, Please double check your input, \
                #     Your input is: '
                #     break
                elif not verify_input(request_record['Input Field']):
                    # logging.debug(request_record['Input Field'])
                    status_code = False
                    status_message = 'Invalid Input Field, please double check your input, use COMMA to seprate your \
                    account or sn and ensure there is no Enter in your input. \
                    \nYour input is: '
                    break

        # send request to automation access
        if status_code:
            send_request(full_file_name)
            status_message = 'Your report is now in process, the email will send to {}, \
            please wait for a while!'.format(email_addr)

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