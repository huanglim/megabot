from cloudant.client import Cloudant
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

    def write_to_db(self, document, user=None, status=None):
        database = self.client.create_database(self.app.config['CLOUDANT_NOSQL_DB_DATABASE_NAME'])
        append_info = {"user":user,
                       "status": status,
                       "insert time": time.ctime()}
        new_document = document.copy()
        new_document.update(append_info)
        if database.exists():
            database.create_document(new_document)

    def db_disconnect(self):
        self.client.disconnect()