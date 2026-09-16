import os, json, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 8651676357

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Running! ✅"

def load_users():
    try:
        with open("users.json","r") as f:
            return json.load(f)
    except: return {}

def save_users(d):
    with open("users.json","w") as f:
        json.dump(d,f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users=load_users()
    uid=str(update.effective_user.id)
    if uid not in users:
        users[uid]={"balance":0,"refers":0}
        save_users(users)
    await update.message.reply_text(f"Bot is Alive! ✅ ID: {uid}")

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
