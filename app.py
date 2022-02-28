import telebot
from flask import Flask, request
import os
API_TOKEN = '5159960474:AAH26K6_EjDc-GgeFclKIRbmaPc9hbGTPA4'

bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)
PORT = int(os.environ.get('PORT', '8443'))

# Handle '/start' and '/help'


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(
        message, "\nHi there, I am EchoBot.\nI am here to echo your words. Just send anything and I'll send the same thing to you!\n")

    # Handle all other messages with content_type 'text' (content_types defaults to ['text'])

    @bot.message_handler(func=lambda message: True)
    def echo_message(message):
        bot.reply_to(message, message.text)

    @server.route('/' + API_TOKEN, methods=['POST'])
    def getMessage():
        bot.process_new_updates(
            [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200

    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url='https://skripsi2022.herokuapp.com/' + API_TOKEN)
        return "!", 200

    if __name__ == "__main__":
        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
