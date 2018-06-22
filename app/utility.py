import os
import json
import re
import http.client
import logging
from flask import render_template
from json2html import *
from threading import Thread
from flask import current_app
from flask_mail import Message
from . import mail
from . import watson_conversion,cloudant_nosql_db
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

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, confirm_link, template=None ):
    app = current_app._get_current_object()
    msg = Message(subject,
                  sender=app.config['MAIL_SENDER'],
                  recipients=[to])
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', confirm_link=confirm_link)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def send_email_api(to, sender, subject, confirm_link):

    conn = http.client.HTTPSConnection("w3.api.ibm.com")

    payload = "{\"to\":[\"%s\"]," \
              "\"from\":\"%s\"," \
              "\"subject\":\"%s\"," \
              "\"body\":" \
              "\"Hi, <br> You are receiving an email to confirm the access request. The link is : <br> %s\"}" \
              % (to, sender, subject, confirm_link)

    headers = {
        'x-ibm-client-id': "352c77cc-68cc-4d73-a5e5-ef10866719ed",
        'x-ibm-client-secret': "I0qT0tJ3vE7vB7oS7eX1dM5sP0oY7rP1hW1sN3mE2yB2eX5uM1",
        'content-type': "application/json",
        'accept': "application/json"
    }

    conn.request("POST", "/common/run/email/sendmail", payload, headers)
    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

def get_approver(emailAddress):
    return emailAddress

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
    print(rpt_level, sel_cty_comp)
    if rpt_level == 'Company Level' and not RE_CTY_CODE.search(sel_cty_comp):
        return False
    else:
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

def convert_country(country):
    re_country = re.split(': ', country)
    return '{}'.format(re_country[1])
#
def convert_company(company):
    re_comp = re.split(': ', company)
    return '{}({})'.format(re_comp[1], re_comp[0])