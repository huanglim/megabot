import os
from app import create_app

# app = create_app(os.getenv('MEGABOT_CONFIG','default'))
app = create_app(os.getenv('MEGABOT_CONFIG', 'production'))

if __name__ == '__main__':
    PORT = int(os.getenv('VCAP_APP_PORT', '8080'))
    HOST = str(os.getenv('VCAP_APP_HOST', 'localhost'))
    if app.config.get('PRODUCTION'):
        app.run(host=HOST, port=PORT)
    else:
        app.run(host=HOST, port=PORT, ssl_context='adhoc')