from flask import Flask, request
from dotenv import load_dotenv
import os
import openai
import requests

# تحميل المتغيرات
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)  # Gunicorn uses this

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def get_saved_reply(text):
    text = text.lower()
    if "الباقات" in text:
        return "💼 الباقات: باقة أساسية – VIP – رجال أعمال. للتفاصيل راسلنا."
    elif "السعر" in text or "الأسعار" in text:
        return "💰 الأسعار تبدأ من 250 ريال حسب نوع السيارة والخدمة."
    elif "الموقع" in text or "العنوان" in text:
        return "📍 الدمام – حي الزهور\nرابط: https://maps.google.com/"
    elif "مواعيد" in text or "العمل" in text:
        return "🕐 من 1 ظهرًا إلى 10 مساءً يوميًا."
    return None

def get_gpt_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد افتراضي لخدمة PowerX للسيارات. رد باحتراف وبلغة واضحة باللهجة السعودية."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return "❌ حدث خطأ في الاتصال بـ GPT."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text.startswith("/start"):
            send_message(chat_id, "مرحبًا بك! البوت شغال عبر Webhook ✅")
        else:
            saved_reply = get_saved_reply(text)
            if saved_reply:
                send_message(chat_id, saved_reply)
            else:
                gpt_reply = get_gpt_response(text)
                send_message(chat_id, gpt_reply)

    return "ok", 200

@app.route("/", methods=["GET"])
def index():
    return "بوت PowerX يعمل ✅", 200
