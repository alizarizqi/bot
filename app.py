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
            # textsplit = sp.split()
            # doc = nlp(sp)
            # poss = " ".join(token.pos_ for token in doc)
            # possplit = poss.split()
            # bot.send_message(chat_id, possplit)
            # bot.send_message(chat_id, sp)
            bot.send_message(chat_id, sp)
            # grammartenses = [
            # {
            #     "pattern":r"every day",
            #     "pesan":"simple present tense",
            # "err_id":1
            # },
            # {
            #         "pattern":r"every month",
            #         "pesan":"simple present tense",
            #     "err_id":2
            #     },
            # {
            #         "pattern":r"every week",
            #         "pesan":"simple present tense",
            #     "err_id":3
            #     },
            # {
            #         "pattern":r"every year",
            #         "pesan":"simple present tense",
            #     "err_id":4
            #     },
            # {
            #         "pattern":r"always",
            #         "pesan":"simple present tense",
            #     "err_id":5
            #     },
            # {
            #         "pattern":r"frequently",
            #         "pesan":"simple present tense",
            #     "err_id":6
            #     },
            # {
            #         "pattern":r"sometimes",
            #         "pesan":"simple present tense",
            #     "err_id":7
            #     },
            # {
            #         "pattern":r"are",
            #         "pesan":"present continuous tense",
            #     "err_id":8
            #     },
            # {
            #         "pattern":r"am",
            #         "pesan":"present continuous tense",
            #     "err_id":9
            #     },
            # {
            #         "pattern":r"is",
            #         "pesan":"present continuous tense",
            #     "err_id":10
            #     },
            # {
            #         "pattern":r"now",
            #         "pesan":"present continuous tense",
            #     "err_id":11
            #     },
            # {
            #         "pattern":r"right now",
            #         "pesan":"present continuous tense",
            #     "err_id":12
            #     },
            # {
            #         "pattern":r"at this moment",
            #         "pesan":"present continuous tense",
            #     "err_id":13
            #     },
            # {
            #         "pattern":r"will",
            #         "pesan":"simple future tense",
            #     "err_id":14
            #     },
            # {
            #         "pattern":r"tomorrow",
            #         "pesan":"simple future tense",
            #     "err_id":15
            #     },
            # {
            #         "pattern":r"next week",
            #         "pesan":"simple future tense",
            #     "err_id":16
            #     },
            # {
            #         "pattern":r"next month",
            #         "pesan":"simple future tense",
            #     "err_id":17
            #     },
            # {
            #         "pattern":r"next year",
            #         "pesan":"simple future tense",
            #     "err_id":18
            #     },
            # {
            #         "pattern":r"next monday",
            #         "pesan":"simple future tense",
            #     "err_id":19
            #     },
            # {
            #         "pattern":r"next tuesday",
            #         "pesan":"simple future tense",
            #     "err_id":20
            #     },
            # {
            #         "pattern":r"next wednesday",
            #         "pesan":"simple future tense",
            #     "err_id":21
            #     },
            # {
            #         "pattern":r"next thursday",
            #         "pesan":"simple future tense",
            #     "err_id":22
            #     },
            # {
            #         "pattern":r"next friday",
            #         "pesan":"simple future tense",
            #     "err_id":23
            #     },
            # {
            #         "pattern":r"next saturday",
            #         "pesan":"simple future tense",
            #     "err_id":24
            #     },
            # {
            #         "pattern":r"next sunday",
            #         "pesan":"simple future tense",
            #     "err_id":25
            #     },
            # {
            #         "pattern":r"this week",
            #         "pesan":"simple future tense",
            #     "err_id":26
            #     },
            # {
            #         "pattern":r"this month",
            #         "pesan":"simple future tense",
            #     "err_id":27
            #     },
            # {
            #         "pattern":r"this year",
            #         "pesan":"simple future tense",
            #     "err_id":28
            #     }
            # ]
            # for err in grammartenses:
            #     found = re.search(err["pattern"], sp)
            #     if found:
            #         if err["err_id"] == 1 or err["err_id"] == 2 or err["err_id"] == 3 or err["err_id"] == 4 or err["err_id"] == 5 or err["err_id"] == 6 or err["err_id"] == 7:
            #             bot.send_message(chat_id,"simple present tense")
            #         elif err["err_id"] == 8 or err["err_id"] == 9 or err["err_id"] == 10:
            #             bot.send_message(chat_id,"present continuous tense")
            #         elif err["err_id"] == 11 or err["err_id"] == 12 or err["err_id"] == 13:
            #             bot.send_message(chat_id,"present continuous tense 2")
            #         elif err["err_id"] == 14:
            #             bot.send_message(chat_id,"simple future tense")
            #         elif err["err_id"] == 15 or err["err_id"] == 16 or err["err_id"] == 17 or err["err_id"] == 18 or err["err_id"] == 19 or err["err_id"] == 20 or err["err_id"] == 21 or err["err_id"] == 22 or err["err_id"] == 23 or err["err_id"] == 24 or err["err_id"] == 25 or err["err_id"] == 26 or err["err_id"] == 27 or err["err_id"] == 28:
            #             bot.send_message(chat_id,"simple future tense 2")

            # grammar = [
            #     {
            #         "pattern": ["VERB", "PRON"],
            #         "pesan":"Kata kerja ditempatkan setelah kata ganti",
            #         "koreksi":[1, 0],  # PRON, VERB
            #         "contoh":"we read",
            #         "status":"error1",
            #         "err_id":1},
            #     {
            #         "pattern": ["PRON", "VERB", "NOUN", "DET"],
            #         "pesan":"Kata kerja ditempatkan setelah kata ganti",
            #         "koreksi":[0, 1, 3, 2],  # PRON, VERB, DET, NOUN
            #         "contoh":"i read the book",
            #         "status":"error2",
            #         "err_id":2},
            #     {
            #         "pattern": ["PRON", "VERB", "AUX", "NOUN"],
            #         "pesan":"Kata kerja ditempatkan setelah kata ganti",
            #         "koreksi":[0, 2, 1, 3],  # PRON, AUX, VERB
            #         "contoh":"i am reading book",
            #         "status":"error3",
            #         "err_id":3},
            #     {
            #         "pattern": ["PRON", "AUX", "VERB", "NOUN", "DET"],
            #         "pesan":"Noun after Determinan",
            #         "koreksi":[0, 1, 2, 4, 3],  # PRON, AUX, VERB, DET, NOUN
            #         "contoh":"i am reading the book",
            #         "status":"error4",
            #         "err_id":4},
            #     {
            #         "pattern": ["PRON", "AUX", "VERB", "NOUN", "PRON"],
            #         "pesan":"Noun after Determinan",
            #         "koreksi":[0, 1, 2, 4, 3],  # PRON, AUX, VERB, DET, NOUN
            #         "contoh":"i am reading the book",
            #         "status":"error5",
            #         "err_id":5},
            #     {
            #         "pattern": ["PRON", "ADV", "VERB"],
            #         "pesan":"adv after verb",
            #         "koreksi":[0, 2, 1],  # PRON, AUX, VERB, DET, NOUN
            #         "contoh":"i come here",
            #         "status":"error6",
            #         "err_id":6}

            # ]

            # def grammar_checker(testing, testing_list, testing_pos):

            #     check = 0

            #     # iterate through possible errors
            #     for err in grammar:
            #         indexes = []

            #         # look for error patterns in the list of POS tags
            #         for i in range(len(testing_pos)):

            #             # i += check

            #             # found a match
            #             if testing_pos[i:i+len(err["pattern"])] == err["pattern"]:
            #                 indexes.append((i, i+len(err["pattern"])))

            #                 koreksi_pos = [
            #                     testing_pos[i:i+len(err["pattern"])][a] for a in err["koreksi"]]
            #                 koreksi = [
            #                     testing_list[i:i+len(err["pattern"])][a] for a in err["koreksi"]]

            #                 for j in range(len(indexes)):
            #                     testing_list[i:indexes[j][1]] = koreksi
            #                     testing_pos[indexes[j][0]                                            :indexes[j][1]] = koreksi_pos

            #                 grammar_id.extend(range(i, i+len(err["pattern"])))

            # grammar_checker(" ".join(textsplit), textsplit, possplit)
            # output2 = textsplit
            # output3 = ' '.join(output2)
            # doc2 = nlp(output3)
            # poss2 = " ".join(token.pos_ for token in doc2)
            # poss2split = poss2.split()
            # # bot.send_message(chat_id, poss2split)
            # # bot.send_message(chat_id, output3)

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
            #         "err_id":3},
            #     {
            #         "pattern": ["PRON", "VERB", "NOUN", "ADJ", "NOUN"],
            #         "pesan":"Simple Past Tense",
            #         "err_id":4}

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
            #                     return "Tense is Simple Present Tense"
            #                 if err["err_id"] == 2:
            #                     return "Tense is Simple Present Tense 2"
            #                 if err["err_id"] == 3:
            #                     return "Tense is Present Continuous Tense"
            #                 if err["err_id"] == 4:
            #                     return "Tense is Simple Past Tense"

            # bot.send_message(chat_id, detect_tense(poss2split))

        return 'ok'
    return 'error'


def index():
    return webhook()
