import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.agents_config import execute_agent_flow
from src.schemas import ChatRequest, ChatResponse

load_dotenv()

app = FastAPI(title="Math Agent Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    try:
        user_message = payload.message
        chat_history = payload.history or ""

        ai_response = await execute_agent_flow(
            user_prompt=user_message,
            chat_history=chat_history
        )

        return ChatResponse(response=ai_response)

    except Exception as e:
        print("\n--- DETAILED ERROR TRACEBACK ---")
        import traceback
        traceback.print_exc() 
        print("--------------------------------\n")
        
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the agents: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)