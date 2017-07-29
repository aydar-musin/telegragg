__author__ = 'aydar'

from EmailMessage import EmailMessage
from EmailServices.EmailServices import EmailServices

est_host_map={'gmail':'imap.gmail.com'}


def get_unseen(email_settings):
    service = EmailServices.get_service(email_settings.type, email_settings.auth_data)

    messages = service.get_unread_emails()

    for msg in messages:
        if isinstance(msg.email, str):
            msg.email = msg.decode('utf-8')
        if isinstance(msg.subject, str):
            msg.subject = msg.subject.decode('utf-8')
        if isinstance(msg.from_email, str):
            msg.from_email = msg.from_email.decode('utf-8')
        if isinstance(msg.message, str):
            msg.message = msg.message.decode('utf-8')

    return  messages