import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)

from openai import OpenAI

# تأكد من وجود المتغير في البيئة
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables.")

bot_app = ApplicationBuilder().token(TOKEN).build()


# أمر بدء المحادثة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أنا بوت الذكاء الاصطناعي. أرسل أي سؤال.")

# أمر gpt لرد ذكي
async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("يرجى كتابة سؤال بعد الأمر /gpt")
        return

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

# تسجيل الأوامر
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("gpt", gpt))


# مسار /webhook
@app.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        await bot_app.update_queue.put(Update.de_json(request.get_json(force=True), bot_app.bot))
        return "Webhook received!"
    return "Invalid request", 400


# لتشغيله على render
if __name__ == "__main__":
    import asyncio
    bot_app.run_polling()
