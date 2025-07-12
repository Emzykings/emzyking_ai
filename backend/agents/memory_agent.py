"""
This module defines the MemoryAgent, which stores and retrieves relevant
context, facts, and preferences from user conversations.

Author: Emzyking AI
"""

from backend.agents.base_agent import BaseAgent
from backend.database.db_connection import SessionLocal
from backend.database.db_models import MemoryStore
from typing import Dict, Any
import re


class MemoryAgent(BaseAgent):
    """
    Agent that manages memory storage and retrieval for user sessions.
    Useful for personalization, remembering preferences, or task context.
    """

    def __init__(self):
        super().__init__(
            name="MemoryAgent",
            description="Stores or retrieves memories such as facts, preferences, or tasks per session."
        )

    def can_handle(self, prompt: str) -> bool:
        """
        Determines if the prompt suggests a memory-related action.

        Args:
            prompt (str): User input.

        Returns:
            bool: True if memory action keywords are detected.
        """
        keywords = ["remember", "forget", "recall", "remind", "store this", "what did I", "what was my"]
        return any(kw in prompt.lower() for kw in keywords)

    async def handle(self, prompt: str, context: Dict[str, Any] = {}) -> str:
        """
        Executes a memory action: store or retrieve memory for a chat session.

        Args:
            prompt (str): User request.
            context (Dict): Should include 'chat_id'.

        Returns:
            str: Memory action result.
        """
        chat_id = context.get("chat_id")
        if not chat_id:
            return "❌ Chat session ID is required to manage memory."

        db = SessionLocal()

        try:
            prompt_lower = prompt.lower()

            # Example: "remember my favorite language is Python"
            if "remember" in prompt_lower or "store this" in prompt_lower:
                memory_type = "fact"
                memory_content = self._extract_memory_fact(prompt)
                if not memory_content:
                    return "⚠️ Could not extract any memory to store. Please be more specific."

                new_memory = MemoryStore(chat_id=chat_id, memory_type=memory_type, content=memory_content)
                db.add(new_memory)
                db.commit()
                return f"✅ Got it. I've remembered: '{memory_content}'"

            # Example: "what did I say", "recall", "remind me"
            elif any(word in prompt_lower for word in ["recall", "what did", "remind", "what was"]):
                memories = (
                    db.query(MemoryStore)
                    .filter(MemoryStore.chat_id == chat_id)
                    .order_by(MemoryStore.updated_at.desc())
                    .limit(5)
                    .all()
                )

                if not memories:
                    return "🤷‍♂️ I don't have anything stored for this session yet."

                response = "🧠 Here's what I remember:\n"
                for i, mem in enumerate(memories, start=1):
                    response += f"{i}. {mem.content} (last updated: {mem.updated_at.strftime('%Y-%m-%d %H:%M')})\n"
                return response.strip()

            return "❌ I couldn't identify a valid memory action in your prompt."

        except Exception as e:
            return f"❌ Error accessing memory: {str(e)}"
        finally:
            db.close()

    def _extract_memory_fact(self, prompt: str) -> str:
        """
        Extracts the actual memory content from a user's statement.

        Example: "Remember my name is John" → "my name is John"

        Args:
            prompt (str): Full user message.

        Returns:
            str: Parsed memory content.
        """
        match = re.search(r"(remember|store this)\s*(that\s*)?(.*)", prompt, re.IGNORECASE)
        return match.group(3).strip() if match else ""
