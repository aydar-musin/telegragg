import json

import flask
import httplib2

from apiclient import discovery
from oauth2client.client import OAuth2WebServerFlow
from EmailServices import EmailServices
import os
import sys

app = flask.Flask(__name__)


@app.route('/oa2redirect/<es_type>/<user_id>')
def oa2redirect(es_type, user_id):
    if es_type == 'gmail':
        flow = get_google_flow(user_id)
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)

    return "Unknown es_type"

@app.route('/oa2callback')
def oa2callback():
    if 'code' in flask.request.args and 'es_type' in flask.request.args and 'user_id' in flask.request.args:
        auth_code = flask.request.args.get('code')
        es_type =flask.request.args.get('es_type')
        user_id = flask.request.args.get('user_id')

        if es_type == 'gmail':
            flow = get_google_flow(user_id)
            credentials = flow.step2_exchange(auth_code)
            return credentials.to_json()
        else:
            return "Unknown es_type"


def get_google_flow(user_id):
    return OAuth2WebServerFlow(client_id='1048164942148-j779t9t942gfsai79fhu8fq43cvk6i6e.apps.googleusercontent.com',
                           client_secret='sqpZVGgSB812NqD2a3v2OX8L',
                           scope='https://www.googleapis.com/auth/gmail.readonly',
                           redirect_uri=flask.url_for('oa2callback', es_type='gmail', user_id=user_id ,_external=True).replace('127.0.0.1', 'lvh.me'))
#
#    return client.flow_from_clientsecrets(
#                    os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'EmailServices/secrets/google.json')),
#                    scope='https://www.googleapis.com/auth/gmail.readonly',
#                    redirect_uri=flask.url_for('oa2callback', es_type='gmail', user_id=user_id ,_external=True))

if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = True
  app.run()