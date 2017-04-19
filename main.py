import re
import threading

import telebot

from Database import dataStorage
import UserData
import config
import email_checker
import texts
from botan import botan
import logger


database = dataStorage.Database()
bot = telebot.TeleBot(config.token)

user_temp_emails = {}
user_states = {}


@bot.message_handler(content_types=['text'])
def message_handler(message):
    try:
        user_id = message.chat.id
        state = None

        if user_id in user_states:
            state = user_states[user_id]

        result = react(state, user_id, message.text)
        user_states[user_id] = result[0]
        bot.send_message(user_id, result[1])

        botan.track(config.botan_api_key, user_id, {'input': message.text, 'reponse': result[1]}, message.text)

    except Exception as e:
        bot.send_message(user_id, texts.get_text(texts.error))
        logger.error(str(e))


# available states:
WAIT_EMAIL = 'WAIT_EMAIL'
WAIT_PASSWORD = 'WAIT_PASSWORD'


def react(state, user_id, message):
    if message == '/start':
        return None, texts.get_text(texts.start_txt)
    if message == '/help':
        return None, texts.get_text(texts.help_txt)
    elif message == '/add':
        return WAIT_EMAIL, texts.get_text(texts.add_txt)
    elif message == '/list':
        emails = database.get_emails(user_id)
        if emails:
            result = ''
            for email in emails:
                result = result + '\n' + email.email
            return None, texts.get_text(texts.list_txt)+result
    else:
        if state == WAIT_EMAIL:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', message):
                return WAIT_EMAIL, texts.get_text(texts.not_valid_email)
            elif database.get_user(user_id) and message in [obj.email for obj in database.get_emails(user_id)]:
                return WAIT_EMAIL, texts.get_text(texts.email_already_added)
            else:
                email = UserData.EmailSettings()
                email.email = message
                user_temp_emails[user_id] = email

                return WAIT_PASSWORD, texts.get_text(texts.wait_password)
        elif state == WAIT_PASSWORD:
            temp_email = None

            if user_temp_emails.has_key(user_id):
                temp_email = user_temp_emails[user_id]
            else:
                return None, texts.get_text(texts.error)

            temp_email.password = message
            temp_email.imap_host = 'imap.'+temp_email.email.split('@')[1]

            if not email_checker.check_settings(temp_email):
                return None, texts.get_text(texts.email_check_error)

            user = database.get_user(user_id)

            if user:
                database.add_email(user.id, temp_email)
            else:
                user = UserData.User()
                user.id = user_id
                database.create_user(user)
                database.add_email(user.id, temp_email)

            return None, texts.get_text(texts.email_successfully_added)


def check_event():
    try:

        users = database.get_all_users()

        for user in users:
            for email_setting in user.emails:
                new_emails = email_checker.get_unseen(email_setting)
                for email in new_emails.values():
                    bot.send_message(user.id, u'New email on: '+email.email.decode('utf-8')+u'\r\n-------\r\nFrom: '+email.from_email.decode('utf-8')+u'\r\n-------- \r\n\r\n '+ clean_str(get_unicode_str(email.message)))
    except Exception as e:
        print('error in check event '+e.message)

    threading.Timer(10, check_event).start()


def get_unicode_str(str):
    try:
        return str.decode('utf-8')
    except:
        return str


def clean_str(str):
    try:
        result= []
        lines = str.split('\n')
        lastLine = 'initial str'

        for line in lines:
            if not (re.match(r'^\s*$', line) and re.match(r'^\s*$', lastLine)):
                result.append(line.strip())
            lastLine = line

        return '\n'.join(result)
    except Exception as e:
        print e.message
        return  str

print 'starting...'
check_event()

if(__name__=='__main__'):
    bot.polling(none_stop=True)

