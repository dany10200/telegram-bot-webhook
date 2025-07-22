from fastapi import FastAPI, Request
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    data = await req.json()

    try:
        message = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]

        # رد بسيط + ممكن تربطه بـ GPT لو عايز
        reply = f"إنت قلت: {message}"

        async with httpx.AsyncClient() as client:
            await client.post(TELEGRAM_API_URL, json={
                "chat_id": chat_id,
                "text": reply
            })

    except Exception as e:
        print("Error handling message:", e)

    return {"ok": True}

# احذف app.run()
