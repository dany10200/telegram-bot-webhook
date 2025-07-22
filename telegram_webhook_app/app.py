import os
import asyncio
import requests
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes

# تحميل المتغيرات من .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# إعداد تطبيق Telegram
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Flask app
flask_app = Flask(__name__)

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ مرحبًا بك! البوت شغال بنجاح عبر Webhook.")

# أضف الأمر
application.add_handler(CommandHandler("start", start))

# Webhook endpoint
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)

    async def process_update():
        await application.initialize()   # بدون أي شرط
        await application.process_update(update)

    asyncio.run(process_update())
    return "ok", 200

# صفحة رئيسية بسيطة
@flask_app.route("/", methods=["GET"])
def home():
    return "✅ Webhook Bot is Live", 200

# تعريف متغير Gunicorn
app = flask_app
