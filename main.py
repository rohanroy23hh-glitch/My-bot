import os, json, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8800142582:AAFL_qBn7twMzg95agFyOhRvpj6xL2ZulUg
ADMIN_ID = 8651676357

app = Flask(__name__)
@app.route('/')
def home(): return "Bot Running!"

def load_users():
    try:
        with open("users.json","r") as f: return json.load(f)
    except: return {}
def save_users(d):
    with open("users.json","w") as f: json.dump(d,f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users=load_users(); uid=str(update.effective_user.id)
    if uid not in users:
        users[uid]={"balance":0,"refers":0}
        if context.args and context.args[0]!=uid and context.args[0] in users:
            users[context.args[0]]["balance"]+=10; users[context.args[0]]["refers"]+=1
        save_users(users)
    link=f"https://t.me/Clear_master2026_bot?start={uid}"
    txt=f"Balance: {users[uid]['balance']} TK\nRefers: {users[uid]['refers']}\n\nLink:\n{link}"
    kb=[[InlineKeyboardButton("Refer", callback_data="r")],[InlineKeyboardButton("Balance", callback_data="b"), InlineKeyboardButton("Withdraw", callback_data="w")]]
    await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))

async def btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q=update.callback_query; await q.answer(); users=load_users(); uid=str(q.from_user.id)
    if q.data=="b": await q.message.reply_text(f"Balance: {users[uid]['balance']} TK")
    elif q.data=="r": await q.message.reply_text(f"https://t.me/Clear_master2026_bot?start={uid}")
    elif q.data=="w":
        if users[uid]['balance']<100: await q.message.reply_text("100 TK lagbe")
        else: await q.message.reply_text("bKash Number din:"); context.user_data["wait"]=True

async def msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("wait"):
        users=load_users(); uid=str(update.effective_user.id)
        await context.bot.send_message(ADMIN_ID, f"Withdraw\nUser:{uid}\nNum:{update.message.text}\nAmt:{users[uid]['balance']}")
        users[uid]['balance']=0; save_users(users); await update.message.reply_text("✅ Request Sent!"); context.user_data["wait"]=False

def run_bot():
    a=Application.builder().token(BOT_TOKEN).build()
    a.add_handler(CommandHandler("start", start)); a.add_handler(CallbackQueryHandler(btn)); a.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, msg)); a.run_polling()

if __name__=="__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))).start(); run_bot()
