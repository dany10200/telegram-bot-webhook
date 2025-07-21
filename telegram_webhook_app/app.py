from flask import Flask, request
import telegram
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Webhook data:", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            bot.send_message(chat_id=chat_id, text="هلا! أنا بوت PowerX. كيف أقدر أساعدك؟")
        elif "السعر" in text or "بكم" in text:
            bot.send_message(chat_id=chat_id, text="الباقة الأساسية تبدأ من ١٠٠ ريال. تبغى التفاصيل؟")
        else:
            bot.send_message(chat_id=chat_id, text="ما فهمتك تمام، جرب تكتب /start")

    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
