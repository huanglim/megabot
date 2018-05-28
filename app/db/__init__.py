from cloudant.client import Cloudant
from cloudant.database import CloudantDatabase
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

    def write_to_user(self, user=None, approved_list=None ):
        if approved_list is None:
            approved_list = []

        database = CloudantDatabase(self.client, self.app.config['CLOUDANT_NOSQL_DB_USER_DATABASE_NAME'])
        doc = {"user":user,
                       "approved_accesses":approved_list,
                       "last update time": time.ctime()}
        if database.exists():
            database.create_document(doc)
        else:
            database = self.client.create_database(self.app.config['CLOUDANT_NOSQL_DB_USER_DATABASE_NAME'])
            database.create_document(doc)

    def write_to_request(self, document, user=None, status=None):
        database = CloudantDatabase(self.client, self.app.config['CLOUDANT_NOSQL_DB_REQUEST_DATABASE_NAME'])
        append_info = {"user":user,
                       "status": status,
                       "insert time": time.ctime()}
        new_document = document.copy()
        new_document.update(append_info)
        if database.exists():
            database.create_document(new_document)
        else:
            database = self.client.create_database(self.app.config['CLOUDANT_NOSQL_DB_REQUEST_DATABASE_NAME'])
            database.create_document(new_document)

    def is_authorized(self, user, request_access):
        database = CloudantDatabase(self.client, self.app.config['CLOUDANT_NOSQL_DB_USER_DATABASE_NAME'])
        selector = {'user':{'$eq':user}}
        res = database.get_query_result(selector)[0]

        if request_access in res[0]['approved_accesses']:
            return True
        else:
            return False

    def db_disconnect(self):
        self.client.disconnect()

if __name__ == '__main__':
    pass
