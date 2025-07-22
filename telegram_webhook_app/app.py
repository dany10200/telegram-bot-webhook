import os
import asyncio
import requests
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes

# تحميل متغيرات البيئة
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_TOKEN = BOT_TOKEN  # لتستخدمه في send_message()

# إعداد تطبيق Telegram
application = ApplicationBuilder().token(BOT_TOKEN).build()

# إعداد تطبيق Flask
flask_app = Flask(__name__)

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ مرحبًا بك في PowerX! البوت شغال تمام 🔥")

# إضافة الأمر للبوت
application.add_handler(CommandHandler("start", start))

# نقطة Webhook
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)

    async def process():
        if not application.initialized:
            await application.initialize()
        await application.process_update(update)

    asyncio.run(process())
    return "ok", 200

# (اختياري) نقطة لجلب معلومات أساسية للتجربة
@flask_app.route("/", methods=["GET"])
def index():
    return "✅ PowerX Telegram Webhook Bot is Live", 200

# دالة إرسال رسالة (يمكنك استخدامها لأي غرض يدوي)
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

# تعريف المتغير المطلوب لـ gunicorn
app = flask_app
