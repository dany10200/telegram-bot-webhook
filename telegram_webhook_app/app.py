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
