import os,time,json
from flask import render_template,request,jsonify,send_from_directory,\
    current_app,session,redirect,g
from . import main
from .. import watson_conversion,cloudant_nosql_db

from ..automation import read_excel,send_request
from werkzeug.utils import secure_filename
from json2html import *


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

        # send request to automation access
        send_request(new_filename)

        # convert excel to html table
        excel_content = read_excel(new_filename)
        excel_json = json.dumps(excel_content)
        excel_html = json2html.convert(json=excel_json,
                                       table_attributes="id=\"table-7\"")

        # save parameters file to db
        for document in excel_content:
            # can get the intranet id from sso token
            # which can be stored in session or g
            cloudant_nosql_db.write_to_db(document,user=None)

        return jsonify({'status': 'OK', 'excelHTML':excel_html,
                        'filename':new_filename})
    else:
        return jsonify({'status':'Not OK'})