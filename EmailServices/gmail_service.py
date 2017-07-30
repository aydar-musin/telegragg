import config
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from oauth2client import client
import httplib2
import json
import os
from apiclient import discovery
from EmailMessage import EmailMessage
import email_parser


class GmailService:
    def __init__(self, credentials):
        self.credentials = OAuth2Credentials.from_json(credentials)
        self.name = 'gmail'
        self.gmail = discovery.build('gmail', 'v1', http=self.credentials.authorize(http=httplib2.Http()))

    @staticmethod
    def get_flow():
        return client.flow_from_clientsecrets(os.path.dirname(os.path.abspath(__file__))+'/secrets/google.json',
            scope='https://mail.google.com https://www.googleapis.com/auth/gmail.readonly',
            redirect_uri=config.callback_url)

    def refresh_auth_data(self):
        if self.credentials.access_token_expired:
            self.credentials.refresh(http=httplib2.Http())
            return True, self.credentials.to_json()

        return False, self.credentials.to_json()

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

        if 'messages' not in response:
            return result

        for msg in response['messages']:
            message = self.gmail.users().messages().get(userId='me', id=msg['id']).execute()
            parsed_message = GmailService.parse_message(message)
            parsed_message.id = msg['id']
            result.append(parsed_message)

            #mark the message as read
            self.gmail.users().messages().modify(userId='me', id=msg['id'], body={ 'removeLabelIds': ['UNREAD']}).execute()

        return result

    @staticmethod
    def parse_message(msg):
        email = EmailMessage()

        for header in msg['payload']['headers']:
            if header['name'] == 'From':
                email.from_email = header['value']
            elif header['name'] == 'Subject':
                email.subject = header['value']
            elif header['name'] == 'To':
                email.email = header['value']

        email.message = GmailService.get_payload_message(msg['payload'])

        return email

    @staticmethod
    def get_payload_message(payload):
        transfer_encoding = None
        mime_type = payload['mimeType']

        for header in payload['headers']:
            if header['name'] == 'Content-Transfer-Encoding':
                transfer_encoding = header['value']
                break

        if 'multipart' in payload['mimeType']:
            payload['parts'].sort()
            for part in payload['parts']:
                res = GmailService.get_payload_message(part)
                if res:
                    return res
        elif mime_type == 'text/html':
            return email_parser.from_html(payload['body']['data'].encode('UTF-8'), transfer_encoding)
        elif mime_type == 'text/plain':
            if transfer_encoding == 'base64':
                return email_parser.from_base64(payload['body']['data'].encode('UTF-8'))
            elif transfer_encoding == 'quoted-printable':
                return email_parser.from_quoted_printable(email_parser.from_base64(payload['body']['data'].encode('UTF-8')))
            elif transfer_encoding == '8bit':
                return email_parser.from_quoted_printable(email_parser.from_base64(payload['body']['data'].econde('UTF-8')))
            elif not transfer_encoding:
                return email_parser.clean_str(payload['body']['data'].encode('UTF-8'))
            else:
                raise Exception('Not supported transfer encoding')
        else:
            return None