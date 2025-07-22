from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)
application = ApplicationBuilder().token(BOT_TOKEN).build()

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Webhook شغال تمام، أهلاً بيك!")

# الرد الذكي بناءً على المحتوى
def get_saved_reply(text):
    text = text.lower()
    if "العنوان" in text:
        return "📍 العنوان: https://maps.google.com/"
    elif "الباقة" in text:
        return "💎 باقة VIP تشمل الغسيل والتلميع والحماية."
    elif "سعر" in text:
        return "💰 السعر يبدأ من 250 ريال حسب نوع الخدمة."
    else:
        return "🤖 مرحبًا! كيف أقدر أساعدك؟"

# رد تلقائي على أي رسالة
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    reply = get_saved_reply(text)
    await update.message.reply_text(reply)

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", start))
application.add_handler(CommandHandler("webhook", start))
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("home", start))

from telegram.ext import MessageHandler, filters
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# تشغيل مع Flask
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.update_queue.put_nowait(update)
        return "ok"
