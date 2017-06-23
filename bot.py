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
import email_checker

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

def check_event():
    try:

        users = database.get_all_users()

        for user in users:
            for email_setting in user.emails:
                new_emails = email_checker.get_unseen(email_setting)
                for email in new_emails.values():
                    bot.send_message(user.id, u'New email on: '+email.email.decode('utf-8')+u'\r\n-------\r\nFrom: '+email.from_email.decode('utf-8')+u'\r\n-------- \r\n\r\n '+ clean_str(get_unicode_str(email.message)))
                    botan.track(config.botan_api_key, user.id, {'email':email.email}, 'email received')
    except Exception as e:
        print('error in check event '+e.message)
        logger.error(str(e))

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
print 'starting...'
# check_event()

if(__name__=='__main__'):
    bot.polling(none_stop=True)

