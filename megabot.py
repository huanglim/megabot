import os
from app import create_app

app = create_app(os.getenv('MEGABOT_CONFIG') or 'default')
# app = create_app(os.getenv('MEGABOT_CONFIG') or 'production')
if __name__ == '__main__':
    app.run('0.0.0.0'
            ,port=8080
            # ,ssl_context='adhoc'
            )
