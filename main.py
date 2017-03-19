__author__ = 'aydar'

import config
import telebot
import re
import UserData
import dataStorage

database = dataStorage.Database()

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=['text'])
def repeat_all_messages(message):
    react_to_message(message)
    # bot.send_message(message.chat.id, message.text)


userStates = {}
userTempEmails = {}


def react_to_message(message):
    print message.text

    if message.text == '/start':
        bot.send_message(message.chat.id, 'Welcome to Email Aggregator Bot! Here you can aggregate all your email inbox')
    elif message.text == '/add':
        bot.send_message(message.chat.id, 'Ok, send me your email address')

        userStates[message.chat.id] = 'wait_email_addr'
    elif message.text == '/list':
        user = database.get_user(message.chat.id)
        if user:
            result = ''
            for email in user.emails:
                result = result + '\n' + email.email
            bot.send_message(message.chat.id, 'Here is your added emails:\n'+result)

    elif message.chat.id in userStates:

        userState = userStates[message.chat.id]

        if userState == 'wait_email_addr':
            if not re.match(r'[^@]+@[^@]+\.[^@]+', message.text):
                bot.send_message(message.chat.id, 'Not valid email address. Try again')
            elif database.get_user(message.chat.id) and message.text in [obj.email for obj in database.get_user(message.chat.id).emails]:
                bot.send_message(message.chat.id, 'This email is already added. Try again')
            else:
                userStates[message.chat.id] = 'wait_password'
                email = UserData.EmailSettings()
                email.email = message.text
                userTempEmails[message.chat.id] = email

                bot.send_message(message.chat.id, 'Now, send me password. It\'s secure :)')

        elif userState == 'wait_password':
            userStates[message.chat.id] = None

            user = database.get_user(message.chat.id)
            if user:
                user.emails.append(userTempEmails[user.id])
                database.update_user(user)
            else:
                user = UserData.User()
                user.id = message.chat.id
                user.emails.append(userTempEmails[user.id])

            database.update_user(user)
            bot.send_message(user.id, 'Email successfully added!')

