import telebot
import json
import os
import time
import requests
from telebot import types
from utils import save_url, handle_instagram, handle_facebook, handle_youtube, handle_tiktok
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Welcome, send your URL to download.')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.lower()
    if "instagram" in url:
        handle_instagram(bot, message)
    elif "youtu.be" in url or "youtube" in url:
        handle_youtube(bot, message)
    elif "tiktok" in url:
        handle_tiktok(bot, message)
    elif "facebook" in url:
        handle_facebook(bot, message)
    else:
        bot.reply_to(message, "Unsupported URL.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    quality = call.data

    with open(f'{chat_id}-urls.json', 'r') as f:
        urls = json.load(f)

    video_url = urls.get(str(chat_id), {}).get(quality)
    if video_url:
        response = requests.get(video_url, stream=True)            
        msg = bot.reply_to(call.message, "جاري التنزيل تحلى بالصبر..!")
        video_file = f'{int(time.time())}-video.mp4'
        with open(video_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        bot.send_video(call.message.chat.id, open(video_file, 'rb'), caption="Dev : @l_abani 🍃")
        os.remove(video_file)
    else:
        bot.reply_to(call.message, "Error: URL not found.")
    os.remove(f'{chat_id}-urls.json')

def start_bot():
    while True:
        try:
            bot.infinity_polling()
        except:
            pass
