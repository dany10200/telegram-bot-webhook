from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import asyncio
from dotenv import load_dotenv
import requests
from openai import OpenAI

# تحميل متغيرات البيئة
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# تهيئة GPT client
client = OpenAI(api_key=OPENAI_API_KEY)

# تهيئة البوت
application = ApplicationBuilder().token(BOT_TOKEN).build()
flask_app = Flask(__name__)
app = flask_app  # لـ Gunicorn

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ أهلاً! البوت شغال عبر Webhook 🔌")

application.add_handler(CommandHandler("start", start))

# رد محفوظ
def get_saved_reply(text):
    text = text.lower()
    if "الباقة" in text:
        return "💎 رجاءً أرسل: التلميع الشامل – VIP – الحماية، وسنرد عليك بالتفاصيل."
    elif "سعر" in text or "السعر" in text:
        return "💰 الأسعار تبدأ من 250 ريال حسب نوع السيارة والخدمة."
    elif "الموقع" in text:
        return "📍 العنوان: https://maps.google.com/"
    elif "الخدمة" in text:
        return "🛠️ نقدم: تلميع خارجي – داخلي – حماية نانو – عزل حراري."
    return None

# معالجة الرسائل
@flask_app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data and 'text' in data['message']:
        user_text = data['message']['text']
        chat_id = data['message']['chat']['id']

        saved_reply = get_saved_reply(user_text)
        if saved_reply:
            send_message(chat_id, saved_reply)
        else:
            # استخدام GPT فقط إذا ما في رد محفوظ
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "أجب باللهجة السعودية باختصار وسطرين فقط."},
                        {"role": "user", "content": user_text}
                    ]
                )
                answer = response.choices[0].message.content.strip()
                send_message(chat_id, answer)
            except Exception as e:
                print("🔥 GPT Error:", e)
                send_message(chat_id, "❌ حدث خطأ في الاتصال بـ GPT.")

    return "ok"

# إرسال رسالة لتليجرام
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Telegram Error:", e)
