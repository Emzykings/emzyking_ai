"""
This module defines the CodeExplainerAgent, which explains code snippets 
in simple terms for better understanding.

Author: Emzyking AI
"""

from backend.agents.base_agent import BaseAgent
from typing import Any, Dict
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class CodeExplainerAgent(BaseAgent):
    """
    Agent responsible for explaining code functionality and logic in plain English.
    """

    def __init__(self):
        super().__init__(
            name="CodeExplainer",
            description="Explains code behavior, logic, and purpose in a clear, human-readable format."
        )

    def can_handle(self, prompt: str) -> bool:
        """
        Determines if this agent should handle the prompt.

        Args:
            prompt (str): The user query.

        Returns:
            bool: True if the prompt includes requests like 'explain', 'understand', or 'what does this do'.
        """
        keywords = ["explain", "understand", "describe", "what does", "meaning of", "comment this"]
        return any(keyword in prompt.lower() for keyword in keywords)

    async def handle(self, prompt: str, context: Dict[str, Any] = {}) -> str:
        """
        Processes the user request and provides a clear explanation of the code.

        Args:
            prompt (str): The code or question from the user.
            context (Dict[str, Any]): Optional context.

        Returns:
            str: A human-readable explanation of the code.
        """
        explanation_prompt = (
            "You are Emzyking AI, a friendly and professional code explainer.\n"
            "Your job is to explain what the following code does in simple, understandable terms.\n"
            "Use clear formatting and bullet points when needed. Do not alter the code.\n\n"
            f"Code to Explain:\n{prompt}\n\n"
            "Explanation:"
        )

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(explanation_prompt)
            return response.text.strip()

        except Exception as e:
            if "Quota" in str(e) or "429" in str(e):
                return "⚠️ Emzyking AI quota exceeded. Please try again later."
            return f"❌ Error while explaining code: {str(e)}"
