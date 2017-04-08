__author__ = 'aydar'

import email
from bs4 import BeautifulSoup
import imaplib

from EmailMessage import EmailMessage


def from_html(html):
    soup = BeautifulSoup(html)
    return soup.get_text()


def get_unseen(email_settings):
    m = imaplib.IMAP4_SSL(email_settings.imap_host)
    m.login(email_settings.email, email_settings.password)
    m.select("Inbox")
    status, unreadcount = m.status('INBOX', "(UNSEEN)")
    unreadcount = int(unreadcount[0].split()[2].strip(').,]'))

    if unreadcount == 0:
        return {}

    items = m.search(None, "UNSEEN")
    items = str(items[1]).strip('[\']').split(' ')

    result = {}

    for index, emailid in enumerate(items):
        uid = m.fetch(emailid, "UID")[1][0]
        message = None
        resp, data = m.fetch(emailid, "(RFC822)")
        email_body = data[0][1]
        mail = email.message_from_string(email_body)

        if mail.is_multipart():
            for part in mail.get_payload():
                if part.get_content_type() == 'text/plain':
                    message = part.get_payload(decode=True)
                else:
                    message = from_html(part.get_payload(decode=True))

                if message and message != '':
                    break
        else:
            if mail.get_content_type() == 'text/plain':
                message = mail.get_payload(decode=True)
            else:
                message = from_html(mail.get_payload(decode=True))

        email_msg = EmailMessage()
        email_msg.id = uid
        email_msg.email = email_settings.email
        email_msg.from_email = mail['from']
        email_msg.message = message

        result[uid] = email_msg

    return result