import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from openai import OpenAI

# استدعاء API key من environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

# تهيئة OpenAI client
client = OpenAI(api_key=openai_api_key)

# تهيئة Flask app
app = Flask(__name__)

# أمر /start في البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل أي رسالة وسأرد عليك باستخدام GPT.")

# أمر للرد على أي رسالة
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

# إنشاء تطبيق التليجرام
application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("chat", handle_message))

# نقطة البداية لـ webhook
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# تشغيل التطبيق
if __name__ == "__main__":
    app.run(debug=True)
