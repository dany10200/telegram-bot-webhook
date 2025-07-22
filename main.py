from flask import Flask, request
import requests
import os

app = Flask(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

@app.route('/webhook', methods=["POST"])
def webhook():
    data = request.get_json()
    print("✅ Received data:", data)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            send_message(chat_id, "مرحبًا بك في PowerX! 🛡️")

    return "ok", 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

# احذف app.run()
