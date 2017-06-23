__author__ = 'aydar'

import email
from bs4 import BeautifulSoup
import imaplib

from EmailMessage import EmailMessage

est_host_map={'gmail':'imap.gmail.com'}

def from_html(html):
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()
    return soup.get_text()


def get_unseen(email_settings):
    m = imaplib.IMAP4_SSL(est_host_map[email_settings.type])
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (email_settings.email, email_settings.token)
    m.authenticate('XOAUTH2',lambda x:auth_string)
    m.select("Inbox")
    status, unreadcount = m.status('INBOX', "(UNSEEN)")
    unreadcount = int(unreadcount[0].split()[2].strip(').,]'))

    if unreadcount == 0:
        return {}

    items = m.search(None, "UNSEEN")
    items = str(items[1]).strip('[\']').split(' ')

    result = {}

    for index, emailid in enumerate(items[:10]):
        uid = m.fetch(emailid, "UID")[1][0]
        message = None
        resp, data = m.fetch(emailid, "(RFC822)")
        email_body = data[0][1]
        mail = email.message_from_string(email_body)

        email_msg = EmailMessage()
        email_msg.id = uid
        email_msg.email = email_settings.email
        email_msg.from_email = mail['from']
        email_msg.message = get_email_text(mail)

        result[uid] = email_msg

    return result


def get_email_text(mail):
    try:
        if mail.is_multipart():
            message = ''
            for part in mail.get_payload():
                message = get_email_text(part)
                if message and message != '':
                    return message
        else:
            if mail.get_content_type() == 'text/plain':
                return mail.get_payload(decode=True)
            elif mail.get_content_type() == 'text/html':
                return from_html(mail.get_payload(decode=True))
    except Exception as e:
        print('get_email_text error '+str(e.message))
        return ''


def check_settings(email_setting):
    try:
        m = imaplib.IMAP4_SSL(email_setting.imap_host)
        m.login(email_setting.email, email_setting.password)
        m.select("Inbox")
        status, unreadcount = m.status('INBOX', "(UNSEEN)")
        unreadcount = int(unreadcount[0].split()[2].strip(').,]'))

        if unreadcount >100: # temp solution
            return False
        else:
            return True
    except Exception as e:
        print 'email check error: '+ str(e.message)
        return False
