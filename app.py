# from textblob import TextBlob
from flask import Flask, request
from autocorrect import Speller
import os
import telegram
import re
from langdetect import detect
import spacy
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def webhook():
    bot = telegram.Bot(token=os.environ["YOURAPIKEY"])
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.effective_chat.id
        text = update.message.text
        # check = Speller(lang='en')
        # spell = check(text)
        # bot.send_message(chat_id, spell)

        pat = re.compile(r'([A-Z|a-z][^\.!?]*[\.!?])')
        patt = pat.findall(text)
        # lang = detect(patt)
        for i in patt:
            langg = detect(i)
            if langg == 'en':
                check = Speller(lang='en')
                spelll = check(i)
                doc = nlp(spelll)
                pos = " ".join(token.tag_ for token in doc)
                for word in pos:
                    bot.send_message(chat_id, word)
            break

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
