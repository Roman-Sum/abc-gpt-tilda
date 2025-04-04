from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # ← тут обирається модель

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

PROMPT_TEMPLATE = os.getenv("GPT_PROMPT")
START_OPTIONS = (
    "🔹 З чого почнемо?\n"
    "1. Почати роботу з думками\n"
    "2. Як це працює"
)

START_INSTRUCTION = (
    "Якщо Ви хочете почати працювати з думками, просто напишіть «1» або «Почати».\n"
    "Якщо спочатку хочете дізнатися, як це працює — напишіть «2» або «Як це працює».\n"
    "Обидва шляхи правильні — виберіть той, що підходить саме Вам. "
    "І пам’ятайте: навіть якщо щось не згадається відразу, це абсолютно нормально."
)


@app.post("/chat")
async def chat_with_gpt(msg: Message):
    user_input = msg.text.strip().lower()

    # 🔹 Якщо це стартове повідомлення — повертаємо інструкцію
    if user_input in ["почати", "1", "hi", "hello", "start", "як це працює", "2"]:
        return {"reply": START_OPTIONS + "\n\n" + START_INSTRUCTION}

    # 🔹 Інакше — працюємо як звичайно
    full_prompt = PROMPT_TEMPLATE + "\n" + msg.text

    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Ти дружній психологічний GPT-бот."},
                {"role": "user", "content": full_prompt},
            ]
        )
        reply = response.choices[0].message.content
        return {"reply": reply}
    except Exception as e:
        return {"reply": f"Виникла помилка: {str(e)}"}
