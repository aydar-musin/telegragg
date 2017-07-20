import config
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from oauth2client import client
import httplib2
import json
import os
from apiclient import discovery
from EmailMessage import EmailMessage

class GmailService:
    def __init__(self, credentials):
        self.credentials = OAuth2Credentials.from_json(credentials)
        self.name = 'gmail'
        self.gmail = discovery.build('gmail', 'v1', http=self.credentials.authorize(httplib2.Http()))

    @staticmethod
    def get_flow():
        return client.flow_from_clientsecrets(os.path.dirname(os.path.abspath(__file__))+'/secrets/google.json',
            scope='https://mail.google.com https://www.googleapis.com/auth/gmail.readonly',
            redirect_uri=config.callback_url)

    def get_user_email(self):
        http = self.credentials.authorize(httplib2.Http())
        resp, content = http.request('https://www.googleapis.com/gmail/v1/users/me/profile', 'GET')

        if not content:
            raise Exception('error fetching user email address')

        response = json.loads(content)
        return response['emailAddress']

    def get_unread_emails(self):
        result = []
        response = self.gmail.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()

        for msg in response['messages']:
            message = self.gmail.users().messages().get(userId='me', id=msg['id']).execute()
            email = EmailMessage()

