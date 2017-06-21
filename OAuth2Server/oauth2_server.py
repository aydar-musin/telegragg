import json

import flask
from oauth2client import client
from oauth2client.client import OAuth2WebServerFlow
import os
import sys
from UserData import EmailSettings
from Database.dataStorage import Database


app = flask.Flask(__name__)

db = Database()

@app.route('/oa2redirect/<es_type>/<user_id>')
def oa2redirect(es_type, user_id):
    if es_type == 'gmail':
        flow = get_google_flow(user_id)
        auth_uri = flow.step1_get_authorize_url()
        flask.session['user_id'] = user_id
        flask.session['es_type'] = es_type

        return flask.redirect(auth_uri)

    return "Unknown es_type"

@app.route('/oa2callback')
def oa2callback():
    if 'code' in flask.request.args and 'es_type' in flask.session and 'user_id' in flask.session:
        auth_code = flask.request.args.get('code')
        es_type = flask.session['es_type']
        user_id = flask.session['user_id']

        flask.session.pop('es_type', None)
        flask.session.pop('user_id', None)

        if es_type == 'gmail':
            flow = get_google_flow(user_id)
            credentials = flow.step2_exchange(auth_code)

            email_stngs = EmailSettings()
            email_stngs.user_id = user_id
            email_stngs.type = es_type
            email_stngs.token = credentials.access_token
            email_stngs.expire_time = credentials.token_expiry
            email_stngs.refresh_token = credentials.refresh_token

            db.add_email(user_id, email_stngs)

            return "Successfully logged in"
        else:
            return "Unknown es_type"
    else:
        return "Authorization error"


def get_google_flow(user_id):
    return client.flow_from_clientsecrets(
        os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'EmailServices/secrets/google.json')),
        scope='https://www.googleapis.com/auth/gmail.readonly',
        redirect_uri=flask.url_for('oa2callback', _external=True))
"""   return OAuth2WebServerFlow(client_id='1048164942148-j779t9t942gfsai79fhu8fq43cvk6i6e.apps.googleusercontent.com',
                           client_secret='sqpZVGgSB812NqD2a3v2OX8L',
                           scope='https://www.googleapis.com/auth/gmail.readonly',
                           redirect_uri=flask.url_for('oa2callback', es_type='gmail', user_id=user_id ,_external=True),
                               )
"""


if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = True
  app.run()