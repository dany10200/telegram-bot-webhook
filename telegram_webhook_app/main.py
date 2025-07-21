from flask import Flask, request
from dotenv import load_dotenv
import os

load_dotenv()  

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN") 


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Webhook is running!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received data:", data)
    return "ok", 200
