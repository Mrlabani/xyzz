# Script Credit: @l_abani

import os
try:
    import requests
    import telebot
    import json
    import time
    from telebot import types
except ImportError:
    os.system("pip install requests")
    os.system("pip install pyTelegramBotAPI")

import requests
import telebot
import json
import os
import time
from telebot import types

token = "7250959737:AAEoq5PaAlZU5e83utVh6QUEX75NTgiYpIQ"  # Your Token BOT
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Welcome, send your URL to download.')

@bot.message_handler(func=lambda message: True)
def Ahmed(message):
    global user
    user = message.chat.id
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
    global user, urls_file
    urls_file = f'{user}-urls.json'
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
        'k_page': 'Youtube Downloader',
        'hl': 'en',
        'q_auto': '0',
    }

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
                'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://www.y2mate.com',
                'referer': 'https://www.y2mate.com/download-youtube/',
                'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }

            da = {
                'vid': cut,
                'k': k,
            }

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

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global urls_file
    chat_id = call.message.chat.id
    quality = call.data

    with open(urls_file, 'r') as f:
        urls = json.load(f)

    video_url = urls.get(str(chat_id), {}).get(quality)

    if video_url:
        response = requests.get(video_url, stream=True)

        msg = bot.reply_to(call.message, "جاري التنزيل تحلى بالصبر..!")

        viod = f'{int(time.time())}-video.mp4'
        with open(viod, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        bot.send_video(call.message.chat.id, open(viod, 'rb'), caption="Dev : @maho_s9 ~~ AHMED")
        os.remove(viod)
    else:
        bot.reply_to(call.message, "Error: URL not found.")

    os.remove(urls_file)

def TikTok(message):
    bot.reply_to(message, 'جاري البــحث انتظر')
    link = message.text
    headers = {
        'authority': 'api.tikmate.app',
        'accept': '*/*',
        'accept-language': 'ar-YE,ar;q=0.9,en-YE;q=0.8,en-US;q=0.7,en;q=0.6',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://tikmate.app',
        'pragma': 'no-cache',
        'referer': 'https://tikmate.app/',
        'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    }

    data = {
        'url': link,
    }

    req = requests.post('https://api.tikmate.app/api/lookup', headers=headers, data=data).json()
    if not req['success']:
        bot.reply_to(message, 'Error URL')
    else:
        id = req['id']
        tok = req['token']
        url = f'https://tikmate.app/download/{tok}/{id}.mp4?hd=1'
        bot.send_video(message.chat.id, url, reply_to_message_id=message.message_id)

while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)  # Delay before retrying
  
