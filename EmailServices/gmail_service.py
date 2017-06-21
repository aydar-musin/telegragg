import config
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import client

class GmailService:
    def __init__(self):
        self.name = 'gmail'


    @staticmethod
    def get_flow():
        return client.flow_from_clientsecrets('./EmailServices/secrets/google.json',
            scope='https://www.googleapis.com/auth/gmail.readonly',
            redirect_uri=config.callback_url)

    def get_auth_link(self, user_id, redirect_uri):
        flow = GmailService.get_flow(user_id)
        return flow.step1_get_authorize_url()