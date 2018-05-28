import os
import json
import re
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


def read_excel_with_emai(filename):
    rl = requestsloader.RequestsLoader()
    rl.load_workbook(filename)
    excel_content = rl.get_requests_str()
    email_addr = rl.get_email()
    return excel_content, email_addr

def read_excel(filename):
    rl = requestsloader.RequestsLoader()
    rl.load_workbook(filename)
    excel_content = rl.get_requests_str()
    return excel_content

def verify_email_format(addr):
    if not addr:
        return False
    RE_EMAIL = re.compile(r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$')
    return RE_EMAIL.match(addr)

def verify_select_level(rpt_level, sel_cty_comp):
    RE_CTY_CODE = re.compile(r'.*\d{3}.*')
    if rpt_level == 'Company Level' and RE_CTY_CODE.search(sel_cty_comp):
        return True

def verify_date(start_date, end_date):
    RE_DATE = re.compile('\d{4}[-/]\d{2}[-/]\d{2}')
    if RE_DATE.match(start_date) and RE_DATE.match(end_date):
        return True

def verify_input(input_val):
    if not input_val:
        return False
    elif '\n' in input_val:
        return False
    return True

if __name__ == '__main__':
    print(verify_email_format('huang__lmw@@c1n.ibm.com 23'))
    print(verify_select_level('Company Level', 'China Ons21hare'))
    print(verify_date('1024-12-12','1234/12/31'))