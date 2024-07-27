import os
import json
import time
import requests
import telebot
from telebot import types
import psutil  # To get system stats

# Ensure required packages are installed
try:
    import requests
    import telebot
    import psutil
except ImportError:
    os.system("pip install requests telebot psutil")

# Bot token
token = "7250959737:AAEoq5PaAlZU5e83utVh6QUEX75NTgiYpIQ"
bot = telebot.TeleBot(token)

# Global variables
user = None
urls_file = None

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    # Send a welcome picture
    with open('start_photo.jpg', 'rb') as photo:
        bot.send_photo(chat_id, photo, caption="👋 Welcome! Send your URL to download.")
    bot.reply_to(message, 'Send your URL to download.')

@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "🏓 Pong! The bot is online.")

@bot.message_handler(commands=['status'])
def status(message):
    status_msg = "✅ Bot is running smoothly."
    bot.reply_to(message, status_msg)

@bot.message_handler(commands=['stats'])
def stats(message):
    # Get system stats
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    total_memory = memory_info.total / (1024 ** 3)  # GB
    available_memory = memory_info.available / (1024 ** 3)  # GB

    stats_msg = (f"**System Stats:**\n"
                 f"💻 CPU Usage: {cpu_usage}%\n"
                 f"🧠 Total Memory: {total_memory:.2f} GB\n"
                 f"🆓 Available Memory: {available_memory:.2f} GB")
    
    bot.reply_to(message, stats_msg, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
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
        bot.reply_to(message, "❌ Unsupported URL.")

def save_url(url, quality, chat_id):
    global urls_file
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

def calculate_speed(start_time, end_time, bytes_transferred):
    elapsed_time = end_time - start_time
    if elapsed_time > 0:
        speed = bytes_transferred / elapsed_time / 1024 / 1024  # Speed in MB/s
        return speed
    return 0

def update_progress(message_id, chat_id, progress_text):
    bot.edit_message_text(progress_text, chat_id, message_id)

def Instagram(message):
    bot.reply_to(message, '🔍 Searching, please wait...')
    link = message.text

    headers = {
        'authority': 'www.y2mate.com',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.y2mate.com',
        'referer': 'https://www.y2mate.com/instagram-downloader',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'k_query': link,
        'k_page': 'Instagram',
        'hl': 'en',
        'q_auto': '1',
    }

    try:
        res = requests.post('https://www.y2mate.com/mates/analyzeV2/ajax', headers=headers, data=data)
        res.raise_for_status()
        if "ok" in res.text:
            video_url = res.json().get('links', {}).get('video', [{}])[0].get('url')
            save_url(video_url, 'insta', message.chat.id)
            markup = types.InlineKeyboardMarkup()
            if video_url:
                btn_high = types.InlineKeyboardButton("📹 High Quality", callback_data='insta')
                markup.add(btn_high)
                bot.send_message(message.chat.id, "📥 Choose the video quality:", reply_markup=markup)
        else:
            bot.reply_to(message, "❌ Unsupported URL.")
    except requests.RequestException as e:
        bot.reply_to(message, f"❌ An error occurred: {e}")

def Facebook(message):
    bot.reply_to(message, '🔍 Searching, please wait...')
    link = message.text
    headers = {
        'authority': 'social-downloader.vercel.app',
        'accept': 'application/json, text/plain, */*',
        'referer': 'https://social-downloader.vercel.app/facebook',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    try:
        req = requests.get(f'https://social-downloader.vercel.app/api/facebook?url={link}', headers=headers).json()
        high = req.get('links', {}).get('Download High Quality', '')
        low = req.get('links', {}).get('Download Low Quality', '')

        if high:
            save_url(high, 'high', message.chat.id)
        if low:
            save_url(low, 'low', message.chat.id)

        markup = types.InlineKeyboardMarkup()
        if high:
            btn_high = types.InlineKeyboardButton("📹 High Quality", callback_data='high')
            markup.add(btn_high)
        if low:
            btn_low = types.InlineKeyboardButton("🔽 Low Quality", callback_data='low')
            markup.add(btn_low)

        bot.send_message(message.chat.id, "📥 Choose the video quality:", reply_markup=markup)
    except requests.RequestException as e:
        bot.reply_to(message, f"❌ An error occurred: {e}")

def YouTube(message):
    bot.reply_to(message, '🔍 Searching, please wait...')
    link = message.text
    headers = {
        'authority': 'www.y2mate.com',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.y2mate.com',
        'referer': 'https://www.y2mate.com/en858/download-youtube',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'k_query': link,
        'k_page': 'Youtube Downloader',
        'hl': 'en',
        'q_auto': '0',
    }

    try:
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
                    'x-requested-with': 'XMLHttpRequest',
                }

                da = {
                    'vid': cut,
                    'k': k,
                }

                req = requests.post('https://www.y2mate.com/mates/convertV2/index', headers=he, data=da)
                try:
                    go = req.json()["dlink"]
                except (requests.RequestException, KeyError):
                    go = ""
                save_url(go, quality, message.chat.id)
                btn = types.InlineKeyboardButton(f"📹 Quality: {quality} - Size: {size}", callback_data=quality)
                markup.add(btn)

            bot.send_message(message.chat.id, "📥 Choose the video quality:", reply_markup=markup)
        else:
            bot.reply_to(message, "❌ Unsupported URL.")
    except requests.RequestException as e:
        bot.reply_to(message, f"❌ An error occurred: {e}")

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
        start_time = time.time()

        msg = bot.reply_to(call.message, "🔽 Downloading, please wait...")

        video_file = f'{int(time.time())}-video.mp4'
        try:
            with open(video_file, 'wb') as file:
                bytes_transferred = 0
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    bytes_transferred += len(chunk)
                    elapsed_time = time.time() - start_time
                    speed = calculate_speed(start_time, time.time(), bytes_transferred)
                    progress_text = f"🔽 Downloading... {bytes_transferred / (1024 ** 2):.2f} MB - Speed: {speed:.2f} MB/s"
                    update_progress(msg.message_id, chat_id, progress_text)

            bot.send_video(call.message.chat.id, open(video_file, 'rb'), caption="📤 Dev: @l_abani 🍃")
        except Exception as e:
            bot.reply_to(call.message, f"❌ An error occurred: {e}")
        finally:
            os.remove(video_file)
    else:
        bot.reply_to(call.message, "❌ Error: URL not found.")
    os.remove(urls_file)

def TikTok(message):
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

    data = {
        'url': link,
    }

    try:
        req = requests.post('https://api.tikmate.app/api/lookup', headers=headers, data=data).json()
        if not req['success']:
            bot.reply_to(message, '❌ Error URL')
        else:
            id = req['id']
            tok = req['token']
            url = f'https://tikmate.app/download/{tok}/{id}.mp4?hd=1'
            bot.send_video(message.chat.id, url, reply_to_message_id=message.message_id)
    except requests.RequestException as e:
        bot.reply_to(message, f"❌ An error occurred: {e}")

while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(10)  # Wait before restarting polling
