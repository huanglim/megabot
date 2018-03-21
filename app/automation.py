import os
import json
from json2html import *
from threading import Thread
from flask import current_app
from automation import requestsloader,download_BI_report


def send_async_request(app, filename):
    with app.app_context():
        os.chdir(current_app.config['UPLOAD_FOLDER'])
        download_BI_report.download_report(parameter_file=filename)
        return None


def send_request(filename):
    app = current_app._get_current_object()
    thr = Thread(target=send_async_request,args=[app,filename])
    thr.start()
    return thr


def convert_2_html(excel_content):
    excel_json = json.dumps(excel_content)
    excel_html = json2html.convert(json=excel_json, table_attributes="id=\"table-7\"")
    return excel_html


def read_excel(filename):
    rl = requestsloader.RequestsLoader()
    rl.load_workbook(filename)
    excel_content = rl.get_requests_str()
    return excel_content
