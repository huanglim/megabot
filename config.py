import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # Watson Conversation
    WATSON_CONV_USER = os.environ.get('WATSON_CONV_USER') \
                       or '61f4632f-8f8c-4292-b9b8-95382d8ef3d8'
    WATSON_CON_PASS = os.environ.get('WATSON_CON_PASS') or 'D14UJNo02KCP'
    WATSON_CON_VER = os.environ.get('WATSON_CON_VER') or '2017-05-26'
    WATSON_CON_WORKSPACE_ID = os.environ.get('WATSON_CON_WORKSPACE_ID') \
                              or '1c9b588c-8b0e-4ae3-a7e1-83588a30ae81'

    # File path
    UPLOAD_FOLDER = os.path.join(basedir,'app\doc\/upload')
    DOWNLOAD_FOLDER = os.path.join(basedir,'app\doc\download')
    ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG',
                              'xlsx', 'gif', 'GIF'])

    # Cloudant NoSql DB
    CLOUDANT_NOSQL_DB_DATABASE_NAME = \
        os.environ.get('CLOUDANT_NOSQL_DB_DATABASE_NAME') \
        or 'user_parameter_files'
    CLOUDANT_NOSQL_DB_USER_NAME = \
        os.environ.get('CLOUDANT_NOSQL_DB_USER_NAME') \
        or 'd390fba6-2dee-4b7b-bb9b-16e0037ac410-bluemix'
    CLOUDANT_NOSQL_DB_PASSWORD = \
        os.environ.get('CLOUDANT_NOSQL_DB_PASSWORD') \
        or '30cd32cb535e285b89593851d785f76d538c35692053394ef831f3849b5ff277'
    CLOUDANT_NOSQL_DB_URL = \
        os.environ.get('CLOUDANT_NOSQL_DB_URL') \
        or 'https://d390fba6-2dee-4b7b-bb9b-16e0037ac410-bluemix:30cd32cb5' \
           '35e285b89593851d785f76d538c35692053394ef831f3849b5ff277@d390fb' \
           'a6-2dee-4b7b-bb9b-16e0037ac410-bluemix.cloudant.com'

    # SSO Self-Service Provisioner
    HOME_URL = 'https://megabot.au-syd.mybluemix.net/'
    OIDC_CALLBACK = 'oidcclient'
    CLIENT_SECRETS_JSON = os.path.join(basedir,
                                       'app\doc\sso\client_secrets.json')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    @classmethod
    def init_app(cls,app):
        Config.init_app(app)
        # email errors to admin


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}




