from fastapi import FastAPI, Request
import uvicorn
import os
import requests

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.post("/")
async def telegram_webhook(req: Request):
    data = await req.json()
    message = data.get("message", {}).get("text", "")
    chat_id = data.get("message", {}).get("chat", {}).get("id")

    if message and chat_id:
        reply = "أهلًا! هذا رد تلقائي ✨"
        requests.post(f"{TELEGRAM_API_URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": reply
        })

    return {"ok": True}
