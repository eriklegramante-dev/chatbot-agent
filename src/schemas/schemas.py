"""
Pydantic schemas for the Chatbot API endpoints.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ChatRequest(BaseModel):
    """
    Schema representing the incoming user chat payload from the frontend.
    """

    session_id: str = Field(
        ...,
        description="Unique identifier for the user session to retrieve context.",
        min_length=1,
    )
    message: str = Field(
        ...,
        description="The prompt or mathematical command sent by the user.",
        min_length=1,
    )
    chat_history: Optional[str] = ""

    @field_validator("message", "session_id")
    @classmethod
    def sanitize_strings(cls, value: str) -> str:
        """
        Ensures the incoming strings are stripped of leading/trailing whitespaces.
        """
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Fields cannot be empty or contain only whitespace.")
        return cleaned


class ChatResponse(BaseModel):
    """
    Schema representing the structured response sent back to the client.
    """

    response: str = Field(
        ..., description="The final localized string returned by the assistant."
    )
