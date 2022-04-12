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
            # bot.send_message(chat_id, possplit)

            grammar = [
                {
                    "pattern": ["VERB", "PRON"],
                    "pesan":"Kata kerja ditempatkan setelah kata ganti",
                    "koreksi":[1, 0],  # PRON, VERB
                    "contoh":"we read",
                    "status":"error1",
                    "err_id":1},
                {
                    "pattern": ["PRON", "VERB", "NOUN", "DET"],
                    "pesan":"Kata kerja ditempatkan setelah kata ganti",
                    "koreksi":[0, 1, 3, 2],  # PRON, VERB, DET, NOUN
                    "contoh":"i read the book",
                    "status":"error2",
                    "err_id":2},
                {
                    "pattern": ["PRON", "VERB", "AUX", "NOUN"],
                    "pesan":"Kata kerja ditempatkan setelah kata ganti",
                    "koreksi":[0, 2, 1, 3],  # PRON, AUX, VERB
                    "contoh":"i am reading book",
                    "status":"error3",
                    "err_id":3},
                {
                    "pattern": ["PRON", "AUX", "VERB", "NOUN", "DET"],
                    "pesan":"Noun after Determinan",
                    "koreksi":[0, 1, 2, 4, 3],  # PRON, AUX, VERB, DET, NOUN
                    "contoh":"i am reading the book",
                    "status":"error4",
                    "err_id":4},
                {
                    "pattern": ["PRON", "AUX", "VERB", "NOUN", "PRON"],
                    "pesan":"Noun after Determinan",
                    "koreksi":[0, 1, 2, 4, 3],  # PRON, AUX, VERB, DET, NOUN
                    "contoh":"i am reading the book",
                    "status":"error5",
                    "err_id":5},
                {
                    "pattern": ["PRON", "ADV", "VERB"],
                    "pesan":"adv after verb",
                    "koreksi":[0, 2, 1],  # PRON, AUX, VERB, DET, NOUN
                    "contoh":"i come here",
                    "status":"error6",
                    "err_id":6}

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

                            koreksi_pos = [
                                testing_pos[i:i+len(err["pattern"])][a] for a in err["koreksi"]]
                            koreksi = [
                                testing_list[i:i+len(err["pattern"])][a] for a in err["koreksi"]]

                            for j in range(len(indexes)):
                                testing_list[i:indexes[j][1]] = koreksi
                                testing_pos[indexes[j][0]                                            :indexes[j][1]] = koreksi_pos

                            grammar_id.extend(range(i, i+len(err["pattern"])))

            grammar_checker(" ".join(textsplit), textsplit, possplit)
            output2 = textsplit
            output3 = ' '.join(output2)
            # doc2 = nlp(output3)
            # poss2 = " ".join(token.pos_ for token in doc2)
            # poss2split = poss2.split()
            bot.send_message(chat_id, output3)

            # grammarDetectTense = [
            #     {
            #         "pattern": ["PRON", "VERB", "DET", "NOUN"],
            #         "pesan":"Simple Present Tense",
            #         "err_id":1},
            #     {
            #         "pattern": ["PRON", "VERB", "ADP", "NOUN", "DET", "NOUN"],
            #         "pesan":"Simple Present Tense",
            #         "err_id":2},
            #     {
            #         "pattern": ["PRON", "AUX", "VERB", "NOUN", "ADV"],
            #         "pesan":"Present Continuous Tense",
            #         "err_id":3}

            # ]

            # def detect_tense(testing_pos):

            #     # check = 0

            #     # iterate through possible errors
            #     for err in grammarDetectTense:
            #         indexes = []

            #         # look for error patterns in the list of POS tags
            #         for i in range(len(testing_pos)):

            #             # i += check

            #             # found a match
            #             if testing_pos[i:i+len(err["pattern"])] == err["pattern"]:
            #                 # indexes.append((i, i+len(err["pattern"])))
            #                 if err["err_id"] == 1:
            #                     return print("Tense is Simple Present Tense")
            #                 if err["err_id"] == 2:
            #                     return print("Tense is Simple Present Tense 2")
            #                 if err["err_id"] == 3:
            #                     return print("Tense is Present Continuous Tense")
            # out = detect_tense(poss2split)
            # bot.send_message(chat_id, out)

        return 'ok'
    return 'error'


def index():
    return webhook()
