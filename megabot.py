import os
from app import create_app, cloudant_nosql_db

# app = create_app(os.getenv('MEGABOT_CONFIG','default'))
app = create_app(os.getenv('MEGABOT_CONFIG', 'production'))

if __name__ == '__main__':
    PORT = int(os.getenv('VCAP_APP_PORT', '8080'))
    HOST = str(os.getenv('VCAP_APP_HOST', 'localhost'))
    if app.config.get('PRODUCTION'):
        app.run(host=HOST, port=PORT)
    else:
        app.run(host=HOST, port=PORT, ssl_context='adhoc')
        # app.run()
    # #
    # db = cloudant_nosql_db
    # approved_accesses = [
    #     'China Onshore',
    #     'IBM Australia(616-IBMA)',
    #     'IBM CHINA GDC DL(641-GDCDL)',
    # ]
    # user = db.get_user_info('huanglmw@cn.ibm.com')
    # db.update_user_info(user['_id'], 'approved_accesses', approved_accesses)