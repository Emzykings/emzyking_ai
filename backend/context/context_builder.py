"""
This module builds a structured context string from historical data for use by
the LLM or routing agents. It combines long-term memory (facts, preferences)
with recent conversation history.

Author: Emzyking AI
"""

from sqlalchemy.orm import Session
from backend.database import db_models


def build_context(chat_id: str, db: Session, max_messages: int = 5) -> str:
    """
    Builds a context string for the LLM or RouterAgent based on:
      1. Memory items (long-term knowledge like user preferences)
      2. Most recent N chat messages (for short-term conversational flow)

    Args:
        chat_id (str): The unique chat session ID.
        db (Session): SQLAlchemy session instance.
        max_messages (int): Number of most recent messages to include (default: 5).

    Returns:
        str: A multi-section context string formatted for LLM input.
    """

    context_parts = []

    # === 1. Load memory store entries for this chat session ===
    memories = (
        db.query(db_models.MemoryStore)
        .filter(db_models.MemoryStore.chat_id == chat_id)
        .order_by(db_models.MemoryStore.updated_at.desc())
        .all()
    )

    if memories:
        context_parts.append("🧠 Memory:")
        for mem in memories:
            context_parts.append(f"- ({mem.memory_type}) {mem.content}")
        context_parts.append("")  # Add blank line after memory block

    # === 2. Load most recent chat messages ===
    messages = (
        db.query(db_models.ChatMessage)
        .filter(db_models.ChatMessage.chat_id == chat_id)
        .order_by(db_models.ChatMessage.id.desc())  # Get latest first
        .limit(max_messages)
        .all()
    )

    # Reverse to maintain chronological order (oldest → newest)
    messages.reverse()

    if messages:
        context_parts.append("💬 Recent Conversation:")
        for msg in messages:
            speaker = "User" if msg.role == "user" else "Emzyking AI"
            context_parts.append(f"{speaker}: {msg.content}")

    # Combine all parts
    return "\n".join(context_parts).strip()
