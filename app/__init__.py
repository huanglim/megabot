from flask import Flask
from config import config
from .watson import WatsonConversion
from .db import Cloundant_NoSQL_DB

watson_conversion = WatsonConversion()
cloudant_nosql_db = Cloundant_NoSQL_DB()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    watson_conversion.init_app(app)
    cloudant_nosql_db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    if config_name == 'production':
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

    return app