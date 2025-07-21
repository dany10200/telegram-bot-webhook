from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler
)
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # تأكد إن التوكن في ملف .env

# أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا بك في البوت!")

# أنشئ التطبيق
app = ApplicationBuilder().token(BOT_TOKEN).build()

# أضف الأمر start
app.add_handler(CommandHandler("start", start))

# ابدأ البوت باستخدام polling
if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
