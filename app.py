import os
import time
import json
import requests
import telebot
from telebot import types

# Telegram bot token
token = "YOUR_BOT_TOKEN"  # Replace with your actual bot token
bot = telebot.TeleBot(token)

# Bot start image URL
start_image_url = "https://example.com/start_image.jpg"  # Replace with your actual start image URL

# Ping, status, and stats commands
@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, '🏓 Pong!')

@bot.message_handler(commands=['status'])
def status(message):
    bot.reply_to(message, '🟢 The bot is running!')

@bot.message_handler(commands=['stats'])
def stats(message):
    bot.reply_to(message, '📊 Here are some stats...')

# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_photo(message.chat.id, start_image_url, caption='Welcome to the bot! Send your URL to download.')

# URL processing
@bot.message_handler(func=lambda message: True)
def process_url(message):
    url = message.text.lower()
    if "instagram" in url:
        download_instagram(message)
    elif "youtu.be" in url or "youtube" in url:
        download_youtube(message)
    elif "tiktok" in url:
        download_tiktok(message)
    elif "facebook" in url:
        download_facebook(message)
    else:
        bot.reply_to(message, "Unsupported URL.")

# Save URL function
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

# Instagram downloader
def download_instagram(message):
    bot.reply_to(message, '🔍 Searching, please wait...')
    link = message.text
    headers = {
        'authority': 'www.y2mate.com',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.y2mate.com',
        'referer': 'https://www.y2mate.com/instagram-downloader',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    }
    data = {'k_query': link, 'k_page': 'Instagram', 'hl': 'en', 'q_auto': '1'}
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

# Facebook downloader
def download_facebook(message):
    bot.reply_to(message, '🔍 Searching, please wait...')
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

# YouTube downloader
def download_youtube(message):
    bot.reply_to(message, '🔍 Searching, please wait...')
    link = message.text
    headers = {
        'authority': 'www.y2mate.com',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.y2mate.com',
        'referer': 'https://www.y2mate.com/en858/download-youtube',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    }
    data = {'k_query': link, 'k_page': 'Youtube Downloader', 'hl': 'en', 'q_auto': '0'}
    response = requests.post('https://www.y2mate.com/mates/en858/analyzeV2/ajax', headers=headers, data=data).json()
    if response['status'] == 'ok':
        cut = response["vid"]
        video_links = response.get('links', {}).get('mp4', {})
        markup = types.InlineKeyboardMarkup()
        for video_id, video_info in video_links.items():
            size = video_info.get('size', '')
            quality = video_info.get('q', '')
            k = video_info.get('k', '')
            he = {
                'authority': 'www.y2mate.com',
                'accept': '*/*',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://www.y2mate.com',
                'referer': 'https://www.y2mate.com/download-youtube/',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
            }
            da = {'vid': cut, 'k': k}
            req = requests.post('https://www.y2mate.com/mates/convertV2/index', headers=he, data=da)
            try:
                go = req.json()["dlink"]
            except:
                go = ""
            save_url(go, quality, message.chat.id)
            btn = types.InlineKeyboardButton(f"Quality: {quality} - Size: {size}", callback_data=quality)
            markup.add(btn)
        bot.send_message(message.chat.id, "Choose the video quality:", reply_markup=markup)
    else:
        bot.reply_to(message, "Unsupported URL.")

# TikTok downloader
def download_tiktok(message):
    bot.reply_to(message, '🔍 Searching, please wait...')
    link = message.text
    headers = {
        'authority': 'api.tikmate.app',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://tikmate.app',
        'referer': 'https://tikmate.app/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    }
    data = {'url': link}
    req = requests.post('https://api.tikmate.app/api/lookup', headers=headers, data=data).json()
    if not req['success']:
        bot.reply_to(message, 'Error URL')
    else:
        id = req['id']
        tok = req['token']
        url = f'https://tikmate.app/download/{tok}/{id}.mp4?hd=1'
        bot.send_video(message.chat.id, url, reply_to_message_id=message.message_id)

# Callback query handler for quality selection
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    quality = call.data
    urls_file = f'{chat_id}-urls.json'
    with open(urls_file, 'r') as f:
        urls = json.load(f)
    video_url = urls.get(str(chat_id), {}).get(quality)
    if video_url:
        response = requests.get(video_url, stream=True)
        msg = bot.reply_to(call.message, "⬇️ Downloading, please wait...")
        total_length = int(response.headers.get('content-length', 0))
        dl = 0
        start_time = time.time()
        for chunk in response.iter_content(chunk_size=4096):
            dl += len(chunk)
            bot.edit_message_text(
                f"⬇️ Downloading... {dl / 1024 / 1024:.2f}MB of {total_length / 1024 / 1024:.2f}MB",
                chat_id, msg.message_id)
        end_time = time.time()
        duration = end_time - start_time
        bot.send_video(chat_id, video_url)
        bot.reply_to(call.message, f"✅ Downloaded! Total time: {duration:.2f} seconds.\n📊 Download speed: {dl / duration / 1024:.2f} KB/s")

# Bot polling
if __name__ == '__main__':
    print("Bot is running...")
    bot.polling(none_stop=True)

# Script Credit @l_abani 🍃 Devloper
