__author__ = 'aydar'

import email
import imaplib

from EmailMessage import EmailMessage
from EmailServices.EmailServices import EmailServices

est_host_map={'gmail':'imap.gmail.com'}


def get_unseen(email_settings):
    service = EmailServices.get_service(email_settings.type, email_settings.auth_data)

    return service.get_unread_emails()
