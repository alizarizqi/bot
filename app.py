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

        pat = re.compile(r'([A-Z|a-z][^\.!?]*[\.!?])')
        patt = pat.findall(text)
        # lang = detect(patt)

        # def tag_list_component(doc):
        #     tags = [token.tag_ for token in doc]
        #     doc.set_extension('tags_', default=False, force=True)
        #     doc._.tags_ = tags

        #     return doc

        # if(nlp.has_pipe("tag_list_pipe")):
        #     nlp.remove_pipe("tag_list_pipe")
        # nlp.add_pipe(tag_list_component, name="tag_list_pipe")

        for i in patt:
            langgg = detect(i)
            if langgg == 'en':
                check = Speller(lang='en')
                spelllcheck = check(i)

                doc = nlp(spelllcheck)
                # doc2 = doc._.tags_
                # bot.sendMessage(chat_id, doc2)

                poss = " ".join(token.pos_ for token in doc)
                # posstext = " ".join(token.text for token in doc)
                possplit = poss.split()
                if "PRON" and "VERB" in poss:
                    bot.sendMessage(chat_id, possplit)
                else:
                    bot.sendMessage(chat_id, "tidak lengkap")
            else:
                bot.sendMessage(chat_id, "English please")
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
