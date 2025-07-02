from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.llm_handler import get_code_response
from backend.database.db_connection import get_db
from backend.database import db_models
from backend.schemas import PromptRequest, ContinueChatRequest
from sqlalchemy.orm import Session
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, restrict later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Emzyking AI Backend is Running 🚀"}

@app.post("/new-chat")
def new_chat(db: Session = Depends(get_db)):
    chat_id = str(uuid.uuid4())
    new_session = db_models.ChatSession(chat_id=chat_id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {"chat_id": chat_id, "message": "New chat created."}

@app.post("/continue-chat")
async def continue_chat(request: ContinueChatRequest, db: Session = Depends(get_db)):
    chat_id = request.chat_id
    user_prompt = request.prompt

    chat_session = db.query(db_models.ChatSession).filter(db_models.ChatSession.chat_id == chat_id).first()

    if not chat_session:
        return {"error": "Chat session not found."}

    # Save user message
    user_message = db_models.ChatMessage(chat_id=chat_id, role='user', content=user_prompt)
    db.add(user_message)
    db.commit()

    # Generate response
    response = await get_code_response(user_prompt)

    # Save assistant response
    assistant_message = db_models.ChatMessage(chat_id=chat_id, role='assistant', content=response)
    db.add(assistant_message)
    db.commit()

    return {"chat_id": chat_id, "response": response}

@app.post("/generate-code")
async def generate_code(request: PromptRequest):
    user_prompt = request.prompt

    response = await get_code_response(user_prompt)
    return {"code": response}

# Endpoint to Get Chat History
@app.get("/chat-history/{chat_id}")
def get_chat_history(chat_id: str, db: Session = Depends(get_db)):
    chat_session = db.query(db_models.ChatSession).filter(db_models.ChatSession.chat_id == chat_id).first()

    if not chat_session:
        return {"error": "Chat session not found."}

    messages = db.query(db_models.ChatMessage).filter(db_models.ChatMessage.chat_id == chat_id).order_by(db_models.ChatMessage.id).all()

    chat_history = []
    for message in messages:
        chat_history.append({
            "role": message.role,
            "content": message.content
        })

    return {"chat_id": chat_id, "history": chat_history}
