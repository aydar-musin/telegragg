import re
import threading

import telebot

from Database import dataStorage
import UserData
import config
from EmailServices import EmailServices
import texts
from botan import botan
import logger


database = dataStorage.Database()
bot = telebot.TeleBot(config.token)

email_services = EmailServices.EmailServices()

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
    es_types = email_services.get_service_types()

    for es_type in es_types:
        markup.add(
            telebot.types.InlineKeyboardButton(text=es_type,
                                                      url=config.redirect_url
                                               .replace('es_type', es_type).replace('user_id', str(user_id))))

    return markup

print 'starting...'
# check_event()

if(__name__=='__main__'):
    bot.polling(none_stop=True)
