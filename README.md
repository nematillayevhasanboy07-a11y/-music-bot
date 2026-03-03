import telebot
import os
import yt_dlp
from flask import Flask
import threading

# 1. BOT SOZLAMALARI
# Tokenni Render'da 'Environment Variables'ga qo'shasiz (pastda tushuntiraman)
API_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# 2. RENDER UCHUN "UYG'OTGICH"
@app.route('/')
def home():
    return "Bot tirik!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# 3. MUSIQA QIDIRISH FUNKSIYASI (Youtube orqali)
def download_music(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1:',
        'outtmpl': 'music.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        title = info['entries'][0]['title'] if 'entries' in info else info['title']
        return title

# 4. BOT BUYRUQLARI
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎵 Salom! Qo'shiq nomi yoki ijrochisini yozing, men topib beraman.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    qidiruv = message.text
    msg = bot.send_message(message.chat.id, "🔎 Qidiryapman...")
    
    try:
        title = download_music(qidiruv)
        with open('music.mp3', 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption=f"✅ {title}")
        os.remove('music.mp3')
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ Topilmadi. Xato: {str(e)}", message.chat.id, msg.message_id)

# 5. ISHGA TUSHIRISH
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
