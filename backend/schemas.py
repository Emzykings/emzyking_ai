# backend/schemas.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PromptRequest(BaseModel):
    prompt: str = Field(..., description="The user's input prompt or coding request.")


class ContinueChatRequest(BaseModel):
    chat_id: str = Field(..., description="Unique ID of the chat session.")
    prompt: str = Field(..., description="The user's follow-up message or query.")


# Response model for structured output
class ChatMessageSchema(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None


class ChatHistoryResponse(BaseModel):
    chat_id: str
    history: List[ChatMessageSchema]


class AllChatSummarySchema(BaseModel):
    chat_id: str
    created_at: datetime
    summary: Optional[str]
    messages: List[ChatMessageSchema]

class FeedbackRequest(BaseModel):
    message_id: int = Field(..., description="ID of the assistant's message")
    rating: int = Field(..., ge=1, le=5, description="Rating between 1 and 5")
    comment: Optional[str] = Field(None, description="Optional user feedback comment")