from typing import Optional
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    history: Optional[str] = ""


class ChatResponse(BaseModel):
    response: str