from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # خزن التوكن من .env

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    
    # اختبر إن فيه رسالة داخلة فعلًا
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = "تم استلام رسالتك ✅"
        
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": text}
            )

    return {"ok": True}
