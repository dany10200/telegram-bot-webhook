from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import asyncio
from dotenv import load_dotenv
import requests
import openai

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# عميل GPT الرسمي
client = openai.OpenAI(api_key=OPENAI_API_KEY)

application = ApplicationBuilder().token(BOT_TOKEN).build()
flask_app = Flask(__name__)
app = flask_app  # لـ Gunicorn

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبا! البوت شغال ✅ Webhook 🎯")

application.add_handler(CommandHandler("start", start))


# ردود محفوظة
def get_saved_reply(text):
    text = text.lower()
    if "الباقة" in text:
        return "رش الحماية الشاملة يتضمن 👇:\n- الفئة: VIP\n- الشفافية: لمعة أو مطفي\n- السعر يبدأ من 1250 ريال"
    elif "السعر" in text or "كم" in text:
        return "الأسعار تبدأ من 250 ريال حسب نوع السيارة والمكان 👇"
    elif "الموقع" in text:
        return "📍 موقعنا على الخريطة: https://maps.google.com/"
    elif "الحجز" in text:
        return "للحجز أرسل بيانات السيارة ورقم الجوال وسنتواصل معك."

    return None


@flask_app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        reply = get_saved_reply(text)
        if reply:
            send_message(chat_id, reply)
        else:
            try:
                # استخدام GPT للردود العامة
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "أنت بوت دعم ذكي لشركة حماية سيارات."},
                        {"role": "user", "content": text}
                    ]
                )
                response = completion.choices[0].message.content.strip()
                send_message(chat_id, response)
            except Exception as e:
                print("GPT Error:", e)
                send_message(chat_id, "❌ حدث خطأ في الاتصال بـ GPT.")

    return "OK"


def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)
