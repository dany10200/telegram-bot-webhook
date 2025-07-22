from flask import Flask, request
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
import openai

# تحميل متغيرات البيئة
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# إعداد مفتاح OpenAI
openai.api_key = OPENAI_API_KEY

# تهيئة تطبيق Telegram
application = ApplicationBuilder().token(BOT_TOKEN).build()
flask_app = Flask(__name__)
app = flask_app  # مطلوب لـ Gunicorn

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Webhook جاهز الآن بوتك شغال 🎯")

application.add_handler(CommandHandler("start", start))

# ردود محفوظة
def get_saved_reply(text):
    text = text.lower()
    if "الباقة" in text:
        return "رجعنا أقوى.. التلميع شامل – VIP – الباقة كاملة بـ ٥٠٠ ريال."
    elif "السعر" in text or "تكلفة" in text:
        return "الأسعار تبدأ من 250 ريال حسب نوع البوية والخدمة."
    elif "الموقع" in text:
        return "📍 العنوان: https://maps.google.com/"
    elif "العرض" in text:
        return "العرض يشمل تلميع + حماية + هدية مجانية لأول 10 عملاء."

# استقبال الرسائل من Telegram
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data:
        update = Update.de_json(data, application.bot)
        if update.message:
            text = update.message.text
            reply = get_saved_reply(text)
            if reply:
                application.bot.send_message(chat_id=update.message.chat_id, text=reply)
    return "ok"
