__author__ = 'aydar'

import re
import dataStorage
import UserData
import config
import telebot

database = dataStorage.Database()
bot = telebot.TeleBot(config.token)

user_temp_emails = {}
user_states = {}


@bot.message_handler(content_types=['text'])
def message_handler(message):
    user_id = message.chat.id
    state = None

    if user_id in user_states:
        state = user_states[user_id]

    result = react(state, user_id, message.text)
    user_states[user_id] = result[0]
    bot.send_message(user_id, result[1])

# available states:
WAIT_EMAIL = 'WAIT_EMAIL'
WAIT_PASSWORD = 'WAIT_PASSWORD'


def react(state, user_id, message):
    if message == '/start':
        return None, 'Welcome. Use /add to add email'
    elif message == '/add':
        return WAIT_EMAIL, 'OK, send me your email address'
    elif message == '/list':
        user = database.get_user(user_id)
        if user:
            result = ''
            for email in user.emails:
                result = result + '\n' + email.email
            return None, 'Here is your added emails:\n'+result
    else:
        if state == WAIT_EMAIL:
            if not re.match(r'[^@]+@[^@]+\.[^@]+', message):
                return WAIT_EMAIL, 'Not valid email address. Try again'
            elif database.get_user(user_id) and message in [obj.email for obj in database.get_user(user_id).emails]:
                return WAIT_EMAIL, 'This email is already added. Try again'
            else:
                email = UserData.EmailSettings()
                email.email = message
                user_temp_emails[user_id] = email

                return WAIT_PASSWORD, 'OK, send me the password. It\'s secure :)'
        elif state == WAIT_PASSWORD:
            user = database.get_user(user_id)

            temp_email = None

            if user_temp_emails.has_key(user_id):
                temp_email = user_temp_emails[user_id]
            else:
                return None, 'Session was interrupted. Try to start again by typing /add'

            temp_email.password = message

            if user:
                user.emails.append(temp_email)
                database.update_user(user)
            else:
                user = UserData.User()
                user.id = user_id
                user.emails.append(temp_email)

            database.update_user(user)
            return None, 'Email successfully added!'


if(__name__=='__main__'):
    bot.polling(none_stop=True)

