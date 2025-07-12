"""
This module defines the CodeGeneratorAgent, a specialized agent
that handles user requests for generating code.

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


class CodeGeneratorAgent(BaseAgent):
    """
    Agent responsible for generating code from user prompts.
    """

    def __init__(self):
        super().__init__(
            name="CodeGenerator",
            description="Generates code snippets based on the user's prompt."
        )

    def can_handle(self, prompt: str) -> bool:
        """
        Determines if the prompt is a code generation request.

        Args:
            prompt (str): The user input.

        Returns:
            bool: True if this agent can handle it.
        """
        # Heuristics: basic check for code-like instructions
        keywords = ["build", "generate", "create", "code", "script", "function", "write", "api", "class"]
        return any(keyword in prompt.lower() for keyword in keywords)

    async def handle(self, prompt: str, context: Dict[str, Any] = {}) -> str:
        """
        Handles the prompt by generating code using Gemini API.

        Args:
            prompt (str): The user input.
            context (Dict[str, Any]): Optional context for generation.

        Returns:
            str: Generated code snippet.
        """
        full_prompt = (
            "You are Emzyking AI, a smart code generation assistant. "
            "Only provide the code in your response without extra explanation.\n\n"
            f"User Request: {prompt}\n\n"
            "Generated Code:"
        )

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(full_prompt)
            return response.text.strip()

        except Exception as e:
            if "Quota" in str(e) or "429" in str(e):
                return "⚠️ Emzyking AI quota exceeded. Please try again later."
            return f"❌ Error generating code: {str(e)}"
