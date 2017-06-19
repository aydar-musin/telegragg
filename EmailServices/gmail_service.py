import config
from oauth2client.client import OAuth2WebServerFlow


class GmailService:
    def __init__(self):
        self.name = 'gmail'


    @staticmethod
    def get_flow(user_id):
        return OAuth2WebServerFlow(client_id='1048164942148-j779t9t942gfsai79fhu8fq43cvk6i6e.apps.googleusercontent.com',
                           client_secret='sqpZVGgSB812NqD2a3v2OX8L',
                           scope='https://www.googleapis.com/auth/gmail.readonly',
                           redirect_uri=config.redirect_url.format({'user_id':user_id}))

    def get_auth_link(self, user_id):
        flow = GmailService.get_flow(user_id)
        return flow.step1_get_authorize_url()