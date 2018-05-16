import os
from app import create_app, cloudant_nosql_db

app = create_app(os.getenv('MEGABOT_CONFIG') or 'default')
# app = create_app(os.getenv('MEGABOT_CONFIG') or 'production')
if __name__ == '__main__':
    PORT = int(os.getenv('VCAP_APP_PORT', '5050'))
    HOST = str(os.getenv('VCAP_APP_HOST', 'localhost'))
    app.run(host=HOST, port=PORT)