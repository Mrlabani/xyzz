import os
import requests
import telebot
import json
import time
import psutil
from telebot import types
from flask import Flask, request

token = os.getenv('7250959737:AAEoq5PaAlZU5e83utVh6QUEX75NTgiYpIQ')
bot = telebot.TeleBot(token)
app = Flask(__name__)

start_photo_path = 'start_photo.jpg'

@app.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://YOUR_APP_NAME.onrender.com/' + token)
    return "!", 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)

bot.infinity_polling()

@bot.message_handler(commands=['start'])
def start(message):
    if os.path.exists(start_photo_path):
        with open(start_photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption='Welcome, send your URL to download. \n\nScript Credit: @l_abani 🍃 Developer')
    else:
        bot.reply_to(message, 'Welcome, send your URL to download. \n\nScript Credit: @l_abani 🍃 Developer')

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, '🏓 Pong!')

@bot.message_handler(commands=['status'])
def status(message):
    bot.reply_to(message, 'Bot is running!')

@bot.message_handler(commands=['stats'])
def stats(message):
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    bot.reply_to(message, f'📊 CPU Usage: {cpu}%\n📈 Memory Usage: {memory}%\n💾 Disk Usage: {disk}%')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.lower()
    if "instagram" in url:
        Instagram(message)
    elif "youtu.be" in url or "youtube" in url:
        YouTube(message)
    elif "tiktok" in url:
        TikTok(message)
    elif "facebook" in url:
        Facebook(message)
    else:
        bot.reply_to(message, "Unsupported URL.")

def save_url(url, quality, chat_id):
    urls_file = f'{chat_id}-urls.json'
    if not os.path.exists(urls_file):
        with open(urls_file, 'w') as f:
            json.dump({}, f)

    with open(urls_file, 'r') as f:
        urls = json.load(f)

    if str(chat_id) not in urls:
        urls[str(chat_id)] = {}
    urls[str(chat_id)][quality] = url

    with open(urls_file, 'w') as f:
        json.dump(urls, f)

def Instagram(message):
    bot.reply_to(message, 'جاري البــحث انتظر')
    link = message.text

    headers = {
        'authority': 'www.y2mate.com',
        'accept': '*/*',
        'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.y2mate.com',
        'referer': 'https://www.y2mate.com/instagram-downloader',
        'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'k_query': link,
        'k_page': 'Instagram',
        'hl': 'en',
        'q_auto': '1',
    }

    res = requests.post('https://www.y2mate.com/mates/analyzeV2/ajax', headers=headers, data=data)
    if "ok" in res.text:
        video_url = res.json().get('links', {}).get('video', [{}])[0].get('url')
        save_url(video_url, 'insta', message.chat.id)
        markup = types.InlineKeyboardMarkup()
        if video_url:
            btn_high = types.InlineKeyboardButton("High Quality", callback_data='insta')
            markup.add(btn_high)
            bot.send_message(message.chat.id, "Choose the video quality:", reply_markup=markup)
    else:
        bot.reply_to(message, "Unsupported URL.")

def Facebook(message):
    bot.reply_to(message, 'جاري البــحث انتظر')
    link = message.text
    headers = {
        'authority': 'social-downloader.vercel.app',
        'accept': 'application/json, text/plain, */*',
        'referer': 'https://social-downloader.vercel.app/facebook',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    req = requests.get(f'https://social-downloader.vercel.app/api/facebook?url={link}', headers=headers).json()

    high = req.get('links', {}).get('Download High Quality', '')
    low = req.get('links', {}).get('Download Low Quality', '')

    if high:
        save_url(high, 'high', message.chat.id)
    if low:
        save_url(low, 'low', message.chat.id)

    markup = types.InlineKeyboardMarkup()
    if high:
        btn_high = types.InlineKeyboardButton("High Quality", callback_data='high')
        markup.add(btn_high)
    if low:
        btn_low = types.InlineKeyboardButton("Low Quality", callback_data='low')
        markup.add(btn_low)

    bot.send_message(message.chat.id, "Choose the video quality:", reply_markup=markup)

def YouTube(message):
    bot.reply_to(message, 'جاري البــحث انتظر')
    link = message.text
    headers = {
        'authority': 'www.y2mate.com',
        'accept': '*/*',
        'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.y2mate.com',
        'referer': 'https://www.y2mate.com/en858/download-youtube',
        'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'k_query': link,
        'k_page': 'youtube',
        'hl': 'en',
        'q_auto': '1',
    }

    res = requests.post('https://www.y2mate.com/mates/analyzeV2/ajax', headers=headers, data=data)
    if "ok" in res.text:
        cut = res.json()['result']['id']
        markup = types.InlineKeyboardMarkup()

        qualities = res.json().get('result', {}).get('links', {}).get('mp4', {}).keys()
        for quality in qualities:
            k = res.json().get('result', {}).get('links', {}).get('mp4', {}).get(quality, {}).get('k')
            size = res.json().get('result', {}).get('links', {}).get('mp4', {}).get(quality, {}).get('size')

            da = {
                'vid': cut,
                'k': k,
            }

            response = requests.post('https://www.y2mate.com/mates/convertV2/index', headers=headers, data=da).json()
            video_url = response.get('dlink', '')

            if video_url:
                save_url(video_url, quality, message.chat.id)
                button = types.InlineKeyboardButton(f'{quality} - {size}', callback_data=quality)
                markup.add(button)

        bot.send_message(message.chat.id, "Choose the video quality:", reply_markup=markup)
    else:
        bot.reply_to(message, "Unsupported URL.")

def TikTok(message):
    bot.reply_to(message, 'جاري البــحث انتظر')
    link = message.text

    headers = {
        'accept': 'application/json, text/plain, */*',
        'origin': 'https://tikcd.vercel.app',
        'referer': 'https://tikcd.vercel.app/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    response = requests.get(f'https://tikcd.vercel.app/api?url={link}', headers=headers).json()

    if 'result' in response:
        download_link = response['result']['nowm']
        save_url(download_link, 'tik', message.chat.id)
        bot.send_message(message.chat.id, "Download Link", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Download", url=download_link)))
    else:
        bot.reply_to(message, "Unsupported URL.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    urls_file = f'{chat_id}-urls.json'

    if not os.path.exists(urls_file):
        bot.answer_callback_query(call.id, "Error: URL data not found.")
        return

    with open(urls_file, 'r') as f:
        urls = json.load(f)

    quality = call.data
    if quality in urls.get(str(chat_id), {}):
        download_url = urls[str(chat_id)][quality]
        if call.message.text != download_url:
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=download_url)
        else:
            bot.answer_callback_query(call.id, "The content is already updated.")
    else:
        bot.answer_callback_query(call.id, "Error: URL not found.")

# Infinite polling for Telegram bot to handle incoming messages
bot.infinity_polling()
