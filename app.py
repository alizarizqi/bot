from flask import Flask, request
import os
import telegram
import re
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
        pat = re.compile(r'([A-Z|a-z][^\.!?]*[\.!?])')
        patt = pat.findall(text)
        bot.send_message(chat_id, patt)
        # kalimat = text.split()
        # spam2 = len(kalimat)
        # if(spam2 <= 10):
        #     bot.send_message(chat_id, "okee")

        # match_dot = re.compile((?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s)
        # dotInText = match_dot.search(text)
        # if dotInText.group:
        #     bot.send_message(
        #         chat_id, "Sorry, your text is too much. Please write the simple text")
        # else:
        #     lang = detect(text)
        #     if lang == "en":
        #         bot.send_message(chat_id, "good")
        #     else:
        #         bot.send_message(chat_id, "not good")

        #


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

        return 'ok'
    return 'error'


def index():
    return webhook()
