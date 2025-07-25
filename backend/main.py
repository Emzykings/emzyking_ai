from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import uuid
import traceback

from backend.schemas import PromptRequest, ContinueChatRequest, FeedbackRequest
from backend.database.db_connection import get_db
from backend.database import db_models
from backend.utils import extract_keywords
from backend.agent_registry import router_agent
from backend.context.context_builder import build_context
from backend.feedback_handler import save_feedback_from_request

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    try:
        chat_id = request.chat_id
        user_prompt = request.prompt

        chat_session = db.query(db_models.ChatSession).filter(
            db_models.ChatSession.chat_id == chat_id
        ).first()

        if not chat_session:
            raise HTTPException(status_code=404, detail="Chat session not found.")

        user_msg = db_models.ChatMessage(chat_id=chat_id, role="user", content=user_prompt)
        db.add(user_msg)
        db.commit()
        db.refresh(user_msg)

        context = build_context(chat_id, db)

        response_text, thought, tool_calls, agent_name, confidence = await router_agent.route(
            chat_id=chat_id, user_input=user_prompt, context=context
        )

        assistant_msg = db_models.ChatMessage(
            chat_id=chat_id, role="assistant", content=response_text
        )
        db.add(assistant_msg)
        db.commit()
        db.refresh(assistant_msg)

        if thought:
            agent_thought = db_models.AgentThought(
                message_id=assistant_msg.id,
                reasoning=thought.get("reasoning"),
                tool_invoked=thought.get("tool_invoked"),
                observation=thought.get("observation"),
            )
            db.add(agent_thought)

        for tool in tool_calls or []:
            db.add(
                db_models.ToolUsage(
                    message_id=assistant_msg.id,
                    tool_name=tool.get("tool_name"),
                    input_params=tool.get("input"),
                    output_result=tool.get("output"),
                )
            )

        db.commit()

        return {
            "chat_id": chat_id,
            "response": response_text,
            "agent_thought": thought,
            "tools_used": tool_calls,
            "routed_agent": agent_name,
            "confidence_score": confidence
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")

@app.post("/generate-code")
async def generate_code(request: PromptRequest):
    result, _, _, _, _ = await router_agent.route(
        chat_id=str(uuid.uuid4()), user_input=request.prompt
    )
    return {"code": result}

@app.get("/chat-history/{chat_id}")
def get_chat_history(chat_id: str, db: Session = Depends(get_db)):
    session = db.query(db_models.ChatSession).filter_by(chat_id=chat_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found.")

    messages = (
        db.query(db_models.ChatMessage)
        .filter_by(chat_id=chat_id)
        .order_by(db_models.ChatMessage.id)
        .all()
    )

    return {
        "chat_id": chat_id,
        "history": [{"role": m.role, "content": m.content} for m in messages],
    }

@app.get("/all-chat-history")
def get_all_chat_history(db: Session = Depends(get_db)):
    try:
        all_chats = (
            db.query(db_models.ChatSession)
            .order_by(db_models.ChatSession.created_at.desc())
            .all()
        )

        print(f"🗂️ Total chat sessions: {len(all_chats)}")

        chat_histories = []
        for chat in all_chats:
            messages = (
                db.query(db_models.ChatMessage)
                .filter(db_models.ChatMessage.chat_id == chat.chat_id)
                .order_by(db_models.ChatMessage.id)
                .all()
            )

            user_texts = [m.content for m in messages if m.role == "user"]

            try:
                summary = extract_keywords(user_texts)
            except Exception as e:
                print(f"⚠️ Failed to extract keywords for chat {chat.chat_id}: {e}")
                summary = "Keyword summary failed"

            chat_histories.append(
                {
                    "chat_id": chat.chat_id,
                    "created_at": chat.created_at,
                    "summary": summary,
                    "messages": [{"role": m.role, "content": m.content} for m in messages],
                }
            )

        return {"chats": chat_histories}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback")
def submit_feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    try:
        save_feedback_from_request(db, request)
        return {"message": "Feedback received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
