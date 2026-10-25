import os
from pyrogram import Client, filters
import openai

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
app = Client("my_ai_userbot", api_id=API_ID, api_hash=API_HASH)

SYSTEM_PROMPT = """
Sen ushbu Telegram akkaunt egasining shaxsiy sun'iy intellekt egizagi (dublyori) sanalasan. 
Sening vazifang — egasi band bo'lgan paytda shaxsiy chatlarga samimiy, tabiiy va xuddi o'zidek javob berish.
1. Suhbatdosh qaysi tilda yozsa, o'sha tilda qisqa, do'stona va smayliklar bilan javob ber.
2. Agar muhim ish yoki pul haqida so'rashsa: "Hozir bandlar, bo'shashlari bilan o'zlari aloqaga chiqishadi" deb ayt.
"""

@app.on_message(filters.private & ~filters.me & ~filters.bot)
async def auto_reply(client, message):
    try:
        await client.send_chat_action(message.chat.id, "typing")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7,
            max_tokens=250
        )
        reply_text = response.choices[0].message.content
        await message.reply_text(reply_text)
    except Exception as e:
        print(f"Xatolik: {e}")

if __name__ == "__main__":
    app.run()
