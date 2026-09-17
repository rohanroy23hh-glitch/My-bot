import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is Live!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ref = context.args[0] if context.args else "No refer"
    await update.message.reply_text(f"Hello {user.first_name}! ✅\nYour Refer: {ref}\nBot is Finally Working!")

def run_bot():
    if not BOT_TOKEN:
        print("BOT_TOKEN missing!")
        return
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot polling started...")
    app.run_polling()

if __name__ == "__main__":
    Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
