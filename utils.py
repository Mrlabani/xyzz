import os
import json
import requests
from telebot import types

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

def handle_instagram(bot, message):
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

def handle_facebook(bot, message):
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

def handle_youtube(bot, message):
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
                'referer': 'https://www.y2mate.com/youtube-downloader',
                'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }
            dat = {
                'vid': cut,
                'k': k,
                'ftype': 'mp4',
            }
            res = requests.post('https://www.y2mate.com/mates/convertV2/index', headers=he, data=dat).json()
            save_url(res['result']['url'], video_id, message.chat.id)
            btn = types.InlineKeyboardButton(f'{quality} ({size})', callback_data=video_id)
            markup.add(btn)
        bot.send_message(message.chat.id, "Choose the video quality:", reply_markup=markup)
    else:
        bot.reply_to(message, "Unsupported URL.")

def handle_tiktok(bot, message):
    bot.reply_to(message, 'جاري البــحث انتظر')
    link = message.text
    headers = {
        'authority': 'social-downloader.vercel.app',
        'accept': 'application/json, text/plain, */*',
        'referer': 'https://social-downloader.vercel.app/tiktok',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    req = requests.get(f'https://social-downloader.vercel.app/api/tiktok?url={link}', headers=headers).json()
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
      
