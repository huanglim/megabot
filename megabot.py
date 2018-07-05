import os
from app import create_app

# Init the flask app with the config setting
# Checking the environment, if it is cloud environment, then use production setting
# Otherwise use default setting
if os.getenv('VCAP_APP_HOST'):
    app = create_app(os.getenv('MEGABOT_CONFIG', 'production'))
else:
    app = create_app(os.getenv('MEGABOT_CONFIG', 'default'))

if __name__ == '__main__':

    # Get the PORT & HOST
    PORT = int(os.getenv('VCAP_APP_PORT', '8080'))
    HOST = str(os.getenv('VCAP_APP_HOST', 'localhost'))

    # Run the Flask server
    if app.config.get('PRODUCTION'):
        app.run(host=HOST, port=PORT)
    else:
        app.run(host=HOST, port=PORT, ssl_context='adhoc')
