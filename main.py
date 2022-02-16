import telebot
import time

TOKEN = '5159960474:AAH26K6_EjDc-GgeFclKIRbmaPc9hbGTPA4'
bot = telebot.TeleBot(TOKEN)


def getargs(text):
    _args = text.split()[1:]
    return _args


@bot.message_handler(commands=["start"])
def sayhello(message):
    bot.send_message(message.chat.id, "hello good morning")


@bot.message_handler(commands=["help"])
def sayhelp(message):
    bot.send_message(message.chat.id, "what do you want")


bot.polling()
