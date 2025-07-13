"""
This module defines the CodeGeneratorAgent, a specialized agent
that handles user requests for generating code.

Author: Emzyking AI
"""

from backend.agents.base_agent import BaseAgent
from typing import Any, Dict, List
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

    def keywords(self) -> List[str]:
        """
        Returns a list of keywords relevant to code generation tasks.
        Used by rank_agents() to score match confidence.
        """
        return [
            "build", "generate", "create", "code", "script", "function",
            "write", "api", "class", "loop", "if statement", "program",
            "multiply", "sort", "calculate", "output", "print", "return",
            "syntax", "python", "javascript", "sql", "c++", "java"
        ]

    def can_handle(self, prompt: str) -> int:
        """
        Scores how well this agent can handle the given prompt.

        Args:
            prompt (str): The user input.

        Returns:
            int: Match score based on keyword occurrences.
        """
        prompt_lower = prompt.lower()
        return sum(1 for kw in self.keywords() if kw in prompt_lower)

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
            "You are Emzyking AI, a smart and concise code generation assistant.\n"
            "Your task is to generate clean, correct, and efficient code for the following user request.\n"
            "Respond ONLY with the code. Use comments where needed but no extra text.\n\n"
            f"User Request: {prompt.strip()}\n\n"
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
