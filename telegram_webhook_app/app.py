from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Webhook data:", data)
    return "OK", 200

    
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
