from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    """
    Schema representing the incoming user chat payload.
    """

    message: str = Field(
        ...,
        description="The prompt or mathematical command sent by the user.",
        min_length=1,
    )
    chat_history: Optional[str] = Field(
        default="", description="Optional formatted conversation history."
    )

    @field_validator("message")
    @classmethod
    def sanitize_message(cls, value: str) -> str:
        """
        Ensures the incoming message is stripped of leading/trailing whitespaces.
        """
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Message cannot be empty or contain only whitespace.")
        return cleaned


class ChatResponse(BaseModel):
    """
    Schema representing the structured response sent back to the client.
    """

    response: str = Field(
        ..., description="The final localized string returned by the assistant."
    )
