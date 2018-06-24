from cloudant.client import Cloudant
from cloudant.database import CloudantDatabase
from cloudant.document import Document
import logging
from cloudant.error import CloudantException
import time

class Cloundant_NoSQL_DB(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self,app):
        self.app = app
        self.client = Cloudant(app.config['CLOUDANT_NOSQL_DB_USER_NAME'],
                               app.config['CLOUDANT_NOSQL_DB_PASSWORD'],
                               url=app.config['CLOUDANT_NOSQL_DB_URL'])
        self.client.connect()

    def write_to_request(self, document, user=None, status=None):
        database = CloudantDatabase(self.client, self.app.config['CLOUDANT_NOSQL_DB_REQUEST_DATABASE_NAME'])
        append_info = {"user":user,
                       "status": status,
                       "submit time": time.ctime()}
        new_document = document.copy()
        new_document.update(append_info)
        if database.exists():
            database.create_document(new_document)
        else:
            database = self.client.create_database(self.app.config['CLOUDANT_NOSQL_DB_REQUEST_DATABASE_NAME'])
            database.create_document(new_document)


    def write_to_schedule(self, schedule_record):
        database = CloudantDatabase(self.client, self.app.config['CLOUDANT_NOSQL_DB_SCHEDULE_DATABASE_NAME'])
        append_info = {"status": 'active',
                       "submit time": time.ctime()}
        new_document = schedule_record.copy()
        new_document.update(append_info)
        if database.exists():
            database.create_document(new_document)
        else:
            database = self.client.create_database(self.app.config['CLOUDANT_NOSQL_DB_SCHEDULE_DATABASE_NAME'])
            database.create_document(new_document)

    def is_authorized(self, emailAddress, report_level, request_access):
        database = CloudantDatabase(self.client, self.app.config['CLOUDANT_NOSQL_DB_USER_DATABASE_NAME'])
        selector = {'emailAddress':{'$eq':emailAddress}}
        try:
            res = database.get_query_result(selector)[0]
        except Exception:
            return False
        else:
            if res and \
                    ((res[0]['approved_country_accesses'] and \
                    request_access in res[0]['approved_country_accesses']) \
                    or (res[0]['approved_company_accesses'] and \
                    request_access in res[0]['approved_company_accesses'])):
                return True
            else:
                return False

    def write_to_mail(self, to, sender, subject, confirm_link, requester):
        database = CloudantDatabase(self.client, self.app.config['CLOUDANT_NOSQL_DB_MAIL_DATABASE_NAME'])
        doc = { "to": to,
                "sender":sender,
                        "subject": subject,
                        "confirm_link": confirm_link,
                        "requester": requester,
                        "status": 'submitted',
                        "submit time": time.ctime()}
        if database.exists():
            database.create_document(doc)
        else:
            database = self.client.create_database(self.app.config['CLOUDANT_NOSQL_DB_MAIL_DATABASE_NAME'])
            database.create_document(doc)

    def init_user(self, userinfo, status='active'):

        database = CloudantDatabase(self.client, self.app.config['CLOUDANT_NOSQL_DB_USER_DATABASE_NAME'])
        doc = { "emailAddress": userinfo.get('emailAddress'),
                        "firstName": userinfo.get('firstName'),
                        "lastName": userinfo.get('lastName'),
                        "uid": userinfo.get('uid'),
                        "approved_country_accesses": None,
                        "approved_company_accesses": None,
                        "pending_country_accesses": None,
                        "pending_company_accesses": None,
                        "status": status,
                        "init time": time.ctime()}
        if database.exists():
            database.create_document(doc)
        else:
            return False

    def get_user_info(self, emailAddress):
        database = CloudantDatabase(self.client, self.app.config['CLOUDANT_NOSQL_DB_USER_DATABASE_NAME'])
        selector = {'emailAddress':{'$eq':emailAddress}}
        try:
            res = database.get_query_result(selector)[0]
        except Exception as e:
            raise
        else:
            return res[0]

    def get_user_schedules(self, emailAddress):
        database = CloudantDatabase(self.client, self.app.config['CLOUDANT_NOSQL_DB_SCHEDULE_DATABASE_NAME'])
        if not database.exists():
            database = self.client.create_database(self.app.config['CLOUDANT_NOSQL_DB_SCHEDULE_DATABASE_NAME'])

        selector = {'user':{'$eq':emailAddress}}
        try:
            res = database.get_query_result(selector)
        except Exception as e:
            raise
        else:
            return res

    def get_user_tasks(self, emailAddress):
        database = CloudantDatabase(self.client, self.app.config['CLOUDANT_NOSQL_DB_REQUEST_DATABASE_NAME'])
        if not database.exists():
            database = self.client.create_database(self.app.config['CLOUDANT_NOSQL_DB_REQUEST_DATABASE_NAME'])
        selector = {'user': {'$eq': emailAddress}}
        try:
            res = database.get_query_result(selector)
        except Exception as e:
            raise
        else:
            return res

    def get_doc_id(self, emailAddress):
        return self.get_user_info(emailAddress)['_id']

    def update_user_info(self, doc_id, update_field, to_value):
        database = CloudantDatabase(self.client, self.app.config['CLOUDANT_NOSQL_DB_SCHEDULE_DATABASE_NAME'])
        remote_doc = Document(database, doc_id)
        remote_doc.update_field(
            action=remote_doc.field_set,
            field=update_field,
            value=to_value)

    def update_schedule_status(self, doc_id, to_value):
        database = CloudantDatabase(self.client, self.app.config['CLOUDANT_NOSQL_DB_SCHEDULE_DATABASE_NAME'])
        remote_doc = Document(database, doc_id)
        remote_doc.update_field(
            action=remote_doc.field_set,
            field='status',
            value=to_value)

    def update_pending_country_accesses(self, doc_id, to_value):
        update_field = 'pending_country_accesses'
        return self.update_user_info(doc_id, update_field, to_value)

    def update_pending_company_accesses(self, doc_id, to_value):
        update_field = 'pending_company_accesses'
        return self.update_user_info(doc_id, update_field, to_value)

    def update_approved_company_accesses(self, doc_id, to_value):
        update_field = 'approved_company_accesses'
        return self.update_user_info(doc_id, update_field, to_value)

    def update_approved_country_accesses(self, doc_id, to_value):
        update_field = 'approved_country_accesses'
        return self.update_user_info(doc_id, update_field, to_value)

    def db_disconnect(self):
        self.client.disconnect()

if __name__ == '__main__':
    pass
