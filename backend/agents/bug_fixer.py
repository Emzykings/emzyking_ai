"""
This module defines the BugFixerAgent, which identifies and fixes bugs
in code snippets provided by the user.

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


class BugFixerAgent(BaseAgent):
    """
    Agent responsible for detecting and fixing bugs in user-provided code.
    """

    def __init__(self):
        super().__init__(
            name="BugFixer",
            description="Detects and fixes bugs in broken or error-prone code."
        )

    def can_handle(self, prompt: str) -> bool:
        """
        Determines whether this agent should handle the given prompt.

        Args:
            prompt (str): The user input.

        Returns:
            bool: True if the prompt likely involves bug fixing.
        """
        keywords = ["fix", "bug", "error", "issue", "debug", "troubleshoot", "broken"]
        return any(keyword in prompt.lower() for keyword in keywords)

    async def handle(self, prompt: str, context: Dict[str, Any] = {}) -> str:
        """
        Processes the prompt and returns a fixed version of the code.

        Args:
            prompt (str): The user input.
            context (Dict[str, Any]): Optional context (e.g., language, history).

        Returns:
            str: The debugged or corrected code snippet.
        """
        bug_fixing_prompt = (
            "You are Emzyking AI, a powerful code debugging assistant.\n"
            "Your job is to detect and fix any errors in the user's code.\n"
            "Only return the corrected version of the code without additional explanations.\n\n"
            f"User Code with Issue:\n{prompt}\n\n"
            "Fixed Code:"
        )

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(bug_fixing_prompt)
            return response.text.strip()

        except Exception as e:
            if "Quota" in str(e) or "429" in str(e):
                return "⚠️ Emzyking AI quota exceeded. Please try again later."
            return f"❌ Error debugging code: {str(e)}"
