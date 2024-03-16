import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

app = FastAPI()


openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_api_key)

class Message:
    content: str

class Request:
    headers: dict

@app.post("/message")
async def post_message(message: Message, request: Request, background_tasks: BackgroundTasks):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message.content,
        max_tokens=150
    )