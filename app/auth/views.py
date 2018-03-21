from flask import current_app,redirect,request,g,abort,render_template
from . import auth
from oauth2client.client import flow_from_clientsecrets,FlowExchangeError

@auth.before_app_request
def loging():
    redirect_uri = current_app.config['HOME_URL'] + \
                   current_app.config['OIDC_CALLBACK']
    g.flow = flow_from_clientsecrets(current_app.config['CLIENT_SECRETS_JSON'],
                                   scope='openid',
                                   redirect_uri=redirect_uri)
    auth_uri = g.flow.step1_get_authorize_url()

    return redirect(auth_uri)

@auth.route('/oidcclient')
def oidcclient():
    code = request.args.get('code')
    if 'id_token' not in g and code is not None:
        try:
            credentials = g.flow.step2_exchange(code)
            id_token = credentials.id_token
            g['id_token'] = id_token
        except FlowExchangeError:
            abort(401)
        finally:
            return redirect(current_app.config['HOME_URL'])
    else:
        return render_template('index.html', name=g['id_token']['firstName'].replace('%20', ' '))
