from fastapi import FastAPI, Request
import httpx
import os
from dotenv import load_dotenv

load_dotenv()  # تحميل متغيرات البيئة من .env

app = FastAPI()
BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

PRESET_REPLIES = {
    "مواعيد العمل": "من 9 صباحًا إلى 5 مساءً، ما عدا الجمعة.",
    "فين الموقع": "الدمام، حي الزهور.",
    "الأسعار": "الباقة تبدأ من 199 ريال وتشمل الحماية والتلميع الكامل.",
}

@app.post("/webhook")
async def webhook_handler(req: Request):
    data = await req.json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()

    if not chat_id or not text:
        return {"ok": True}

    reply = PRESET_REPLIES.get(text, "اسألني أي شيء عن خدماتنا!")

    async with httpx.AsyncClient() as client:
        await client.post(TELEGRAM_API, json={
            "chat_id": chat_id,
            "text": reply
        })

    return {"ok": True}
