import os
from app import create_app

app = create_app(os.getenv('MEGABOT_CONFIG') or 'default')

if __name__ == '__main__':
    app.run()


