from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.schemas.schemas import ChatRequest, ChatResponse
import asyncio

from src.agents.mathematician import run_mathematician
from src.agents.writer import run_writer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    user_prompt = payload.message
    chat_history = payload.chat_history or ""

    try:
        calc_result = await asyncio.to_thread(run_mathematician, user_prompt, chat_history)
        final_response = await asyncio.to_thread(run_writer, user_prompt, calc_result)
        return ChatResponse(response=final_response)
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return ChatResponse(response=f"BACKEND ERROR: {str(e)}")