import os
from app import create_app, cloudant_nosql_db

# app = create_app(os.getenv('MEGABOT_CONFIG') or 'default')
app = create_app(os.getenv('MEGABOT_CONFIG') or 'production')
if __name__ == '__main__':
    PORT = int(os.getenv('VCAP_APP_PORT', '8080'))
    HOST = str(os.getenv('VCAP_APP_HOST', 'localhost'))
    # app.run(host=HOST, port=PORT)
    app.run(host=HOST, port=PORT, ssl_context='adhoc')
        # app.run()

    # db = cloudant_nosql_db
    # approved_list = [
    #     'China Onshore',
    #     'IBM Australia(616-IBMA)',
    #     'IBM CHINA GDC DL(641-GDCDL)',
    # ]
    # db.write_to_user('huanglmw@cn.ibm.com', approved_list)
    # assert db.is_authorized('huanglmw@cn.ibm.com', 'China Onshore')