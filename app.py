from flask import Flask, request

# webhook heroku - this tutorial works on cloud.
#   to run flask on local server
#       export FLASK_APP=tutorial6
#       flask run
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Where-to-host-Telegram-Bots#vps
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks
# https://python-telegram-bot.readthedocs.io/
# https://seminar.io/2018/09/03/building-serverless-telegram-bot/
# https://www.heroku.com/

import os
import telegram
# import spacy
# from spacy_langdetect import LanguageDetector
# nlp = spacy.load("en_core_web_sm")
# language_detector = LanguageDetector()
# nlp.add_pipe(language_detector)


# from langdetect import detect
from langdetect import detect

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def webhook():
    bot = telegram.Bot(token=os.environ["YOURAPIKEY"])
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.effective_chat.id
        text = update.message.text
        lang = detect(text)
        kalimat = text.split()
        spam2 = len(kalimat)
        if(spam2 <= 10):
            if lang == "en":
                bot.send_message(chat_id, "good")
            else:
                bot.send_message(chat_id, "not good")
        else:
            bot.send_message(
                chat_id, "Sorry, your text is too much. Please write the simple text")


# first_name = update.effective_chat.first_name
# Reply with the same message

# kalimat = text.split()
# spam2 = len(kalimat)
# if(spam2 <= 10):
# lang = detect(text)
# if(lang == 'en'):
# lang = detect(text)

# bot.send_message(chat_id, lang)
# else:
#     bot.send_message(
#         chat_id, "Sorry, your text is too much. Please write the simple text")

# if text == '/start':
#     bot.send_message(chat_id, "halo")
# else:
#     bot.sendMessage(chat_id=chat_id, text=f"{text} {first_name}")

        return 'ok'
    return 'error'


def index():
    return webhook()
