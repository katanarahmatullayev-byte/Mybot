import telebot
import json
import os

TOKEN = "8924567785:AAGuMRII3jKzNkgkRSyw3ip8vIpWCxwK67c"
ADMIN_ID = 1048620269

bot = telebot.TeleBot(TOKEN)
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_user(user):
    users = load_users()
    ids = [u["id"] for u in users]
    if user.id not in ids:
        users.append({
            "id": user.id,
            "name": user.first_name,
            "username": f"@{user.username}" if user.username else "yo'q"
        })
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)
        bot.send_message(ADMIN_ID,
            f"🆕 Yangi foydalanuvchi!\n"
            f"👤 Ism: {user.first_name}\n"
            f"🔗 Username: @{user.username}\n"
            f"👥 Jami: {len(users)} ta")

@bot.message_handler(commands=["start"])
def start(message):
    save_user(message.from_user)
    bot.send_message(message.chat.id, "Xush kelibsiz! 👋")

@bot.message_handler(commands=["stats"])
def stats(message):
    if message.from_user.id == ADMIN_ID:
        users = load_users()
        bot.send_message(ADMIN_ID, f"👥 Jami foydalanuvchilar: {len(users)} ta")

bot.polling()
