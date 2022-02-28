import time
from telebot import types
import os
import telebot
from flask import Flask, request
import telegram

# token position and bot declaration
token = 'api_code'
server = Flask(__name__)
bot = telebot.TeleBot(token)
bot.settings = dict()
bot.buffers = dict()

# handlers


@bot.message_handler(commands=['start'])
def start(message):
    name = str(message.from_user.first_name)
    bot.reply_to(message, fr"Hi {name}! I'm a pomodoro timer🍅⏰" +
                 "\n"+"Let's do some 𝙥𝙪𝙢𝙢𝙖𝙧𝙤𝙡𝙖 together!")


@bot.message_handler(commands=['setup'])
def setup1(message):
    cid = message.chat.id
    markup = types.ForceReply(selective=False)
    res1 = bot.send_message(cid, "Send me Work Time and Rest Time in this format:" +
                            "\n"+"%minutes - %minutes".center(50), reply_markup=markup)
    bot.register_next_step_handler(res1, setup2)


def setup2(message):
    if '-' in message.text:
        userID = str(message.from_user.id)
        x = ''.join(message.text.split())
        mid = x.find('-')
        wTime = x[0:mid]
        rTime = x[mid+1::]
        if '.' not in wTime and '.' not in rTime and wTime != '0' and rTime != '0':
            setting = dict()
            setting["wTime"] = wTime
            setting["rTime"] = rTime
            bot.settings[userID] = setting
            markup = types.ForceReply(selective=False)
            res2 = bot.reply_to(message, fr"Whoa {setting['wTime']} for working and {setting['rTime']} for resting are a good choice!" +
                                "\n"+'How many pomodori do you want to crush?🍅', reply_markup=markup)
            bot.register_next_step_handler(res2, setup3)
        else:
            bot.reply_to(message, 'Sorry but you insert a strange values.' +
                         '\n'+'Please try again with two integers!')
    else:
        bot.reply_to(
            message, 'Sorry but you insert an invalid format.'+'\n'+'Please try again!')


def setup3(message):
    if message.text.isalpha() == False and '-' not in message.text:
        userID = str(message.from_user.id)
        bot.settings[userID]['pomodoro'] = int(message.text)
        bot.reply_to(message, fr'Alright then, '+"🍅" *
                     int(bot.settings[userID]['pomodoro'])+" ready to be crushed!")
    else:
        bot.reply_to(message, fr'Sorry, try to insert a number next time!')


@bot.message_handler(commands=['erase'])
def erase(message):
    userID = str(message.from_user.id)
    if userID not in bot.settings.keys():
        bot.reply_to(message, "Sorry but you can't delete something that doesn't exist 🤔" +
                     '\n'+"Tap this -> /setup and you are good!")
    else:
        bot.settings[userID].clear()
        bot.reply_to(message, 'Done! Now you can /setup them again')


@bot.message_handler(commands=['current_session'])
def printSetting(message):
    userID = str(message.from_user.id)
    if userID not in bot.settings.keys():
        bot.reply_to(message, "Sorry but you can't see something that doesn't exist 🤔" +
                     '\n'+"Tap this -> /setup and you are good!")
    else:
        bot.send_message(message.chat.id, fr'Work time: {bot.settings[userID]["wTime"]}'+'\n' +
                         fr'Rest time: {bot.settings[userID]["rTime"]}'+'\n'+fr'Pomodori: {bot.settings[userID]["pomodoro"]}')


@bot.message_handler(commands=['pummarola'])
def pummarolaWorking(message):
    userID = str(message.from_user.id)
    if userID not in bot.settings.keys():
        bot.reply_to(message, "Sorry but you can't 𝙥𝙪𝙢𝙢𝙖𝙧𝙤𝙡𝙖 before setup 🤔" +
                     '\n'+"Tap this -> /setup and you are good!")
    else:
        mins = 0
        secs = 0
        timer = dict()
        bot.buffers[userID] = timer
        workTime = int(bot.settings[userID]['wTime']) * 60
        bot.send_message(
            message.chat.id, fr"Take a look to your progress here /progress")
        while workTime > 0:
            mins, secs = divmod(workTime, 60)
            timer['mins'] = mins
            timer['secs'] = secs
            time.sleep(1)
            workTime -= 1
        bot.buffers.clear()
        markup = types.ForceReply(selective=False)
        res = bot.send_message(
            message.chat.id, fr"Good job! You've finished one session of {bot.settings[userID]['wTime']} min."+"\n"+"When you are ready to relax send me something!", reply_markup=markup)
        bot.register_next_step_handler(res, pummarolaResting)


def pummarolaResting(message):
    userID = str(message.from_user.id)
    restTime = int(bot.settings[userID]['rTime']) * 60
    timer = dict()
    bot.buffers[userID] = timer
    bot.send_message(
        message.chat.id, fr"Now take a glass of water and relax for {bot.settings[userID]['rTime']} min.!"+"\n"+"See how much you have left from /progress")
    while restTime > 0:
        mins, secs = divmod(restTime, 60)
        timer['mins'] = mins
        timer['secs'] = secs
        time.sleep(1)
        restTime -= 1
    bot.settings[userID]['pomodoro'] = int(
        bot.settings[userID]['pomodoro']) - 1
    bot.buffers.clear()
    if int(bot.settings[userID]['pomodoro']) == 0:
        bot.send_message(
            message.chat.id, fr"Good Job buddy! You did a terrific pummarola today!")
    else:
        markup = types.ForceReply(selective=False)
        res = bot.send_message(message.chat.id, fr"Are you ready for the next pomodoro 🍅?"+"\n" +
                               fr"There are only {int(bot.settings[userID]['pomodoro'])} to finish!"+"\n"+"When you are ready for the next 𝙥𝙪𝙢𝙢𝙖𝙧𝙤𝙡𝙖 send me something!", reply_markup=markup)
        bot.register_next_step_handler(res, pummarolaWorking)


@bot.message_handler(commands=['progress'])
def progress(message):
    userID = str(message.from_user.id)
    bot.reply_to(
        message, fr"You're doing great, only {bot.buffers[userID]['mins']} minutes and {bot.buffers[userID]['secs']} seconds left!"+"\n"+"-> /progress")

# Server dump


@server.route('/' + token, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(
        url='https://skripsi2022.herokuapp.com/5159960474:AAH26K6_EjDc-GgeFclKIRbmaPc9hbGTPA4')
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
