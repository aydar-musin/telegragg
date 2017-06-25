import config
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import client
import httplib2
import json
import os

class GmailService:
    def __init__(self):
        self.name = 'gmail'


    @staticmethod
    def get_flow():
        return client.flow_from_clientsecrets(os.path.dirname(os.path.abspath(__file__))+'/secrets/google.json',
            scope='https://www.googleapis.com/auth/gmail.readonly https://mail.google.com',
            redirect_uri=config.callback_url)

    @staticmethod
    def get_user_email(credentials):
        http = credentials.authorize(httplib2.Http())
        resp, content = http.request('https://www.googleapis.com/gmail/v1/users/me/profile', 'GET')

        if not content:
            raise Exception('error fetching user email address')

        response = json.loads(content)
        return response['emailAddress']
