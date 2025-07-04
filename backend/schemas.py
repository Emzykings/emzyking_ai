# backend/schemas.py
from pydantic import BaseModel

class PromptRequest(BaseModel):
    prompt: str

class ContinueChatRequest(BaseModel):
    chat_id: str
    prompt: str
