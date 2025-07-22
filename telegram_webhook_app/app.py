from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import os
import openai

# تأكد إنك استوردت التحديث
from telegram.ext import Dispatcher, MessageHandler, filters

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# بوت تليجرام
telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put(update)
    return "ok", 200

# نقطة انطلاق بسيطة للتأكد من أن السيرفر شغال
@app.route('/', methods=['GET'])
def index():
    return 'Telegram bot is running!', 200

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلًا! أنا شغال.")

telegram_app.add_handler(CommandHandler('start', start))

# لا تنسَ run_app
if __name__ == "__main__":
    telegram_app.run_polling()
