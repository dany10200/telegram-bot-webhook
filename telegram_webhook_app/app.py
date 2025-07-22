from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Telegram bot
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Flask app
flask_app = Flask(__name__)

# Telegram command
async def start(update: Update, context):
    await update.message.reply_text("مرحبًا! البوت شغال عبر Webhook ✨")

application.add_handler(CommandHandler("start", start))

# Webhook endpoint
@flask_app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    asyncio.run(application.process_update(update))
    return "ok"

# This variable must be called `app` for Gunicorn to load it
app = flask_app
import requests

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Received data:", data)

    # استخراج الرسالة والنص
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "✅ مرحبًا بك في PowerX! البوت شغال تمام 🔥")

    return "ok", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)
