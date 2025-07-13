"""
This module defines the BugFixerAgent, which identifies and fixes bugs
in code snippets provided by the user.

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


class BugFixerAgent(BaseAgent):
    """
    Agent responsible for detecting and fixing bugs in user-provided code.
    """

    def __init__(self):
        super().__init__(
            name="BugFixer",
            description="Detects and fixes bugs in broken or error-prone code."
        )

    def keywords(self) -> List[str]:
        """
        Returns a list of keywords relevant to bug fixing tasks.
        """
        return [
            "fix", "bug", "error", "issue", "debug", "troubleshoot",
            "broken", "fails", "throws", "unexpected", "wrong", "doesn't work", "not working"
        ]

    def can_handle(self, prompt: str) -> int:
        """
        Scores how well this agent can handle the prompt.

        Args:
            prompt (str): The user input.

        Returns:
            int: Match score based on keyword matches.
        """
        prompt_lower = prompt.lower()
        return sum(1 for kw in self.keywords() if kw in prompt_lower)

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
            "Return only the corrected version of the code without extra explanations.\n\n"
            f"User Code with Issue:\n{prompt.strip()}\n\n"
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
