import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Watson Conversation
    WATSON_CONV_USER = os.environ.get('WATSON_CONV_USER') \
                       or '22d58649-2f7c-4635-83e4-19ffdcc114c0'
    WATSON_CON_PASS = os.environ.get('WATSON_CON_PASS') or 'xKTet3ftXwGa'
    WATSON_CON_VER = os.environ.get('WATSON_CON_VER') or '2018-02-16'
    WATSON_CON_WORKSPACE_ID = os.environ.get('WATSON_CON_WORKSPACE_ID') \
                              or '52211d79-6da3-490e-a1d4-e801f9a031ea'
    WASTON_CON_URL = 'https://gateway-s.watsonplatform.net/assistant/api'

    # File path
    UPLOAD_FOLDER = os.path.join(basedir,'app/doc/upload')
    DOWNLOAD_FOLDER = os.path.join(basedir,'app/doc/download')
    ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'}

    # Cloudant NoSql DB
    CLOUDANT_NOSQL_DB_DATABASE_NAME = \
        os.environ.get('CLOUDANT_NOSQL_DB_DATABASE_NAME') \
        or 'megabot_db'
    CLOUDANT_NOSQL_DB_USER_NAME = \
        os.environ.get('CLOUDANT_NOSQL_DB_USER_NAME') \
        or "0d0ab079-7631-442d-8355-a466779cb63d-bluemix"
    CLOUDANT_NOSQL_DB_PASSWORD = \
        os.environ.get('CLOUDANT_NOSQL_DB_PASSWORD') \
        or "45e643fcad1755a4828ff390196db82cb01d480537d99367cfbeaa3f39acddf5"
    CLOUDANT_NOSQL_DB_URL = \
        os.environ.get('CLOUDANT_NOSQL_DB_URL') \
        or "https://0d0ab079-7631-442d-8355-a466779cb63d-bluemix:45e643fcad1755a4828ff390196" \
            "db82cb01d480537d99367cfbeaa3f39acddf5@0d0ab079-7631-442d-8355-a466779cb63d-bluemix.cloudant.com"

    # SSO Self-Service Provisioner
    HOME_URL = 'https://tstmegabot.mybluemix.net/'
    # OIDC_CALLBACK = 'auth/oidcclient'
    OIDC_CALLBACK = ''
    # CLIENT_SECRETS_JSON = os.path.join(basedir,
    #                                    'app\doc\sso\client_secrets.json')
    CLIENT_SECRETS_JSON = os.path.join(basedir,
                                       'app/doc/sso/client_secrets.json')

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