import telebot
import os
from flask import Flask
from threading import Thread

# Render-da bot o'chib qolmasligi uchun veb-server
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run(): app.run(host='0.0.0.0', port=10000)
def keep_alive(): Thread(target=run).start()

# Tokenni Render-dan olamiz
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Bot Render-da muvaffaqiyatli ishga tushdi.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
