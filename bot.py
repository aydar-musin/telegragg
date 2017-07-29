import re
import threading

import telebot

from Database import dataStorage
import UserData
import config
from EmailServices.EmailServices import EmailServices
import texts
from botan import botan
import logger
import email_checker

database = dataStorage.Database()
bot = telebot.TeleBot(config.token)


user_temp_emails = {}
user_states = {}

@bot.message_handler(content_types=['text'])
def message_handler(message):
    try:
        user_id = message.chat.id


        react(user_id, message.text)

        botan.track(config.botan_api_key, user_id, {'input': message.text}, message.text)
    except Exception as e:
        bot.send_message(user_id, texts.get_text(texts.error))
        logger.error(str(e))


def react(user_id, message):
    if message == '/start':
        bot.send_message(user_id, texts.get_text(texts.start_txt))
    if message == '/help':
        bot.send_message(user_id, texts.get_text(texts.help_txt))
    elif message == '/add':
        bot.send_message(user_id, texts.get_text(texts.add_txt), reply_markup=get_es_markup(user_id))
    elif message == '/list':
        emails = database.get_emails(user_id)
        if emails:
            result = ''
            for email in emails:
                result = result + '\n' + email.email

            bot.send_message(user_id, texts.get_text(texts.list_txt)+result)


# get email services markup
def get_es_markup(user_id):
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    es_types = EmailServices.get_service_types()

    for es_type in es_types:
        markup.add(
            telebot.types.InlineKeyboardButton(text=es_type,
                                                      url=config.redirect_url
                                               .replace('es_type', es_type).replace('user_id', str(user_id))))

    return markup


def get_message_text(msg):
    return u'\r\n'+msg.subject+\
           u'\r\nNew email on: ' +\
           msg.email+u'\r\nFrom: '+msg.from_email+\
           u'\r\n-------- \r\n\r\n '+ msg.message[:3800]


def check_event():
    try:

        users = database.get_all_users()

        for user in users:
            for email_setting in user.emails:
                new_emails = email_checker.get_unseen(email_setting)
                for email in new_emails:
                    bot.send_message(user.id, get_message_text(email))
                    botan.track(config.botan_api_key, user.id, {'email':email.email}, 'email received')
    except Exception as e:
        print('error in check event '+e.message)
        logger.error(str(e))

    threading.Timer(10, check_event).start()



print 'starting...'
check_event()
print 'starting...'
# check_event()

if(__name__=='__main__'):
    bot.polling(none_stop=True)

