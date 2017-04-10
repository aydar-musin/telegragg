import re
import threading

import telebot

from Database import dataStorage
import UserData
import config
import email_checker

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
    except Exception as e:
        bot.send_message(user_id, 'Error '+ e.message)

# available states:
WAIT_EMAIL = 'WAIT_EMAIL'
WAIT_PASSWORD = 'WAIT_PASSWORD'


def react(state, user_id, message):
    if message == '/start' or message == '/help':
        return None, 'Welcome! Use /add to add email. Also you can use /list to show all your added emails and /help to see this message.'
    elif message == '/add':
        return WAIT_EMAIL, 'OK, send me your email address'
    elif message == '/list':
        emails = database.get_emails(user_id)
        if emails:
            result = ''
            for email in emails:
                result = result + '\n' + email.email
            return None, 'Here is your added emails:\n'+result
    else:
        if state == WAIT_EMAIL:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', message):
                return WAIT_EMAIL, 'Not valid email address. Try again'
            elif database.get_user(user_id) and message in [obj.email for obj in database.get_emails(user_id)]:
                return WAIT_EMAIL, 'This email is already added. Try again'
            else:
                email = UserData.EmailSettings()
                email.email = message
                user_temp_emails[user_id] = email

                return WAIT_PASSWORD, 'OK, send me the password. It\'s secure :)'
        elif state == WAIT_PASSWORD:
            temp_email = None

            if user_temp_emails.has_key(user_id):
                temp_email = user_temp_emails[user_id]
            else:
                return None, 'Session was interrupted. Try to start again by typing /add'

            temp_email.password = message
            temp_email.imap_host = 'imap.'+temp_email.email.split('@')[1]

            if not email_checker.check_settings(temp_email):
                return None, 'I can not connect to your email box.'

            user = database.get_user(user_id)

            if user:
                database.add_email(user.id, temp_email)
            else:
                user = UserData.User()
                user.id = user_id
                database.create_user(user)
                database.add_email(user.id, temp_email)

            return None, 'Email successfully added!'


def check_event():
    try:

        users = database.get_all_users()

        for user in users:
            for email_setting in user.emails:
                new_emails = email_checker.get_unseen(email_setting)
                for email in new_emails.values():
                    bot.send_message(user.id, u'New email on '+email.email.decode('utf-8')+u'\r\n-------\r\n from '+email.from_email.decode('utf-8')+u'\r\n-------- \r\n\r\n '+ clean_str(get_unicode_str(email.message)))
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

