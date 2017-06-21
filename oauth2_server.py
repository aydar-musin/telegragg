import json

import flask
from EmailServices.gmail_service import GmailService
import os
import sys
from UserData import EmailSettings, User

from Database.dataStorage import Database


app = flask.Flask(__name__)

db = Database()

@app.route('/oa2redirect/<es_type>/<user_id>')
def oa2redirect(es_type, user_id):
    if es_type == 'gmail':
        flow = GmailService.get_flow(flask.url_for('oa2callback'))
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
            flow = GmailService.get_flow(flask.url_for('oa2callback'))
            credentials = flow.step2_exchange(auth_code)

            email_stngs = EmailSettings()
            email_stngs.user_id = user_id
            email_stngs.type = es_type
            email_stngs.token = credentials.access_token
            email_stngs.expire_time = credentials.token_expiry
            email_stngs.refresh_token = credentials.refresh_token

            user = db.get_user(user_id)

            if not user:
                user = User()
                user.id = user_id
                db.create_user(user)

            db.add_email(user_id, email_stngs)

            return "Successfully logged in\n\n"+credentials.to_json()
        else:
            return "Unknown es_type"
    else:
        return "Authorization error"


if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = True
  app.run(host='0.0.0.0', port=int(sys.argv[1]))