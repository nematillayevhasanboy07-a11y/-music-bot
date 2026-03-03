from telebot import TeleBot
import yt_dlp
import os

# 🔑 Sizning tokeningiz va Shazam/AcrCloud API key
TOKEN = "8757036858:AAEMiFRwq-amw8gyYcyX78b2xPEoR_zJasc"


bot = TeleBot(TOKEN)

# --- Start komandiya ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎵 Salom! Qo‘shiq nomini yozing yoki video yuboring. Men topib beraman!")

# --- Qo‘shiq nomi orqali ---
@bot.message_handler(commands=['music'])
def music_command(message):
    query = message.text.replace('/music', '').strip()
    if not query:
        bot.reply_to(message, "⚠️ Qo‘shiq nomini yozing. Masalan: /music Shape of You")
        return
    download_and_send(message, query)

# --- Video yuborilganda ---
@bot.message_handler(content_types=['video'])
def identify_video(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("temp.mp4", 'wb') as f:
        f.write(downloaded_file)
    
    # 🔹 Bu yerda Shazam/AcrCloud API orqali aniqlash
    # misol funksiyasi: result = identify_music("temp.mp4")
    result = "Qo‘shiq nomi: Example Song\nIjrochi: Example Artist"  # bu faqat misol
    bot.reply_to(message, f"🎵 Topildi:\n{result}")
    
    os.remove("temp.mp4")

# --- YouTube audio yuklash funksiyasi ---
def download_and_send(message, query):
    bot.reply_to(message, f"🔎 {query} qidirilmoqda...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': 'music.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            file_name = ydl.prepare_filename(info['entries'][0])
            audio_file = file_name.rsplit('.', 1)[0] + ".mp3"

        with open(audio_file, 'rb') as f:
            bot.send_audio(message.chat.id, f)
        os.remove(audio_file)
    except:
        bot.reply_to(message, "❌ Musiqa topilmadi yoki xatolik yuz berdi.")

bot.polling()
