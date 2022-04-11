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
        grammar_id = []
        langgg = detect(text)
        if langgg == 'en':
            checkk = Speller(lang='en')
            sp = checkk(text)
            textsplit = sp.split()
            doc = nlp(sp)
            poss = " ".join(token.pos_ for token in doc)
            possplit = poss.split()

            grammar = [
                {
                    "pattern": ["VERB", "PRON"],
                    "pesan":"Kata kerja ditempatkan setelah kata ganti",
                    "koreksi":[1, 0],  # PRON, VERB
                    "contoh":"we read",
                    "status":"error1",
                    "err_id":1},
                {
                    "pattern": ["VERB", "AUX", "PRON"],
                    "pesan":"Kata kerja ditempatkan setelah kata ganti",
                    "koreksi":[2, 1, 0],  # PRON, AUX, VERB
                    "contoh":"we read",
                    "status":"error1",
                    "err_id":2},
                {
                    "pattern": ["VERB", "NOUN", "DET"],
                    "pesan":"Noun after Determinan",
                    "koreksi":[0, 2, 1],  # VERB, DET, NOUN
                    "contoh":"read the book",
                    "status":"error3",
                    "err_id":3},
                {
                    "pattern": ["AUX", "VERB", "NOUN", "DET"],
                    "pesan":"Noun after Determinan",
                    "koreksi":[0, 1, 3, 2],  # AUX VERB, DET, NOUN
                    "contoh":"I am reading the book",
                    "status":"error4",
                    "err_id":4}
            ]

            def grammar_checker(testing, testing_list, testing_pos):
                check = 0
            # iterate through possible errors
                for err in grammar:
                    indexes = []
                    # look for error patterns in the list of POS tags
                    for i in range(len(testing_pos)):
                        # i += check
                        # found a match
                        if testing_pos[i:i+len(err["pattern"])] == err["pattern"]:
                            indexes.append((i, i+len(err["pattern"])))

                            if err["err_id"] == 1:
                                koreksi_pos = [
                                    testing_pos[i:i+len(err["pattern"])][a] for a in err["koreksi"]]
                                koreksi = [
                                    testing_list[i:i+len(err["pattern"])][a] for a in err["koreksi"]]
                                for j in range(len(indexes)):
                                    testing_list[i:indexes[j][1]] = koreksi
                                    testing_pos[indexes[j][0]                                                :indexes[j][1]] = koreksi_pos
                                    grammar_id.extend([i, i+1])

                            if err["err_id"] == 2 and 3:
                                koreksi_pos = [
                                    testing_pos[i:i+len(err["pattern"])][a] for a in err["koreksi"]]
                                koreksi = [
                                    testing_list[i:i+len(err["pattern"])][a] for a in err["koreksi"]]

                                for j in range(len(indexes)):
                                    testing_list[i:indexes[j][1]] = koreksi
                                    testing_pos[indexes[j][0]                                                :indexes[j][1]] = koreksi_pos
                                    grammar_id.extend(
                                        range(i, i+len(err["pattern"])))

            grammar_checker(" ".join(textsplit), textsplit, possplit)
            output2 = textsplit
            output3 = ' '.join(output2)
            bot.send_message(chat_id, output3)

        return 'ok'
    return 'error'


def index():
    return webhook()
