from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

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

@app.post("/chat")
async def chat_with_gpt(msg: Message):
    full_prompt = PROMPT_TEMPLATE + "\n" + msg.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти дружній психологічний GPT-бот."},
                {"role": "user", "content": full_prompt},
            ]
        )
        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"Виникла помилка: {str(e)}"}
