from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler
import os
from dotenv import load_dotenv
import asyncio
import requests

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

application = ApplicationBuilder().token(BOT_TOKEN).build()
flask_app = Flask(__name__)
app = flask_app  # for Gunicorn

async def start(update: Update, context):
    await update.message.reply_text("مرحبًا! البوت شغال عبر Webhook ✨")

application.add_handler(CommandHandler("start", start))

# Webhook endpoint - فقط واحدة
@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.get_json(force=True)
    
    # Telegram built-in processing
    update = Update.de_json(json_data, application.bot)
    asyncio.run(application.process_update(update))

    # استخراج يدوي للرسالة (اختياري)
    if "message" in json_data:
        chat_id = json_data["message"]["chat"]["id"]
        text = json_data["message"].get("text", "")
        if text == "/start":
            send_message(chat_id, "✅ مرحبًا بك في PowerX! البوت شغال تمام 🔥")

    return "ok", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)
