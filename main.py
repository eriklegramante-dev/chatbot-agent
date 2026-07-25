import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.agents.mathematician import run_mathematician
from src.agents.writer import run_writer
from src.utils.validation import is_invalid_mixed_prompt
from src.schemas.schemas import ChatRequest, ChatResponse

load_dotenv()

app = FastAPI(
    title="Math Agent Chatbot API",
    description="API for processing mathematical operations using isolated CrewAI agents.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint to verify API availability."""
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    """
    Orchestrates the modular flow:
    1. Validation Guardrail (Fast-Fail)
    2. Mathematician Agent (Calculation / Intent)
    3. Copywriter Agent (Response Formatting)
    """
    user_prompt = payload.message.strip()

    if is_invalid_mixed_prompt(user_prompt):
        return ChatResponse(
            response="Invalid expression. Please provide valid numbers and mathematical operators."
        )

    chat_history = getattr(payload, "chat_history", "") or ""

    try:
        calc_result = await asyncio.to_thread(
            run_mathematician, user_prompt, chat_history
        )

        final_response = await asyncio.to_thread(run_writer, user_prompt, calc_result)

        return ChatResponse(response=final_response)

    except Exception as e:
        import traceback

        print("=== Error caught in the backend. ===")
        traceback.print_exc()
        print("=================================")

        return ChatResponse(response=f"BACKEND ERROR: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
