"""
This module defines the CodeExplainerAgent, which explains code snippets 
or defines programming terms in simple terms for better understanding.

Author: Emzyking AI
"""

from backend.agents.base_agent import BaseAgent
from typing import Any, Dict, Tuple, List
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class CodeExplainerAgent(BaseAgent):
    """
    Agent responsible for explaining code functionality or programming concepts
    in plain English.
    """

    def __init__(self):
        super().__init__(
            name="CodeExplainer",
            description="Explains code behavior or programming terms clearly in a human-readable format."
        )

    def can_handle(self, prompt: str) -> int:
        """
        Determines how suitable this agent is for the prompt.

        Returns:
            int: Relevance score (0–10)
        """
        keywords = [
            "explain", "understand", "describe", "what does", "meaning of",
            "comment this", "what is", "define", "purpose of", "how does"
        ]
        matches = sum(keyword in prompt.lower() for keyword in keywords)
        return 10 if matches else 0

    async def handle(self, prompt: str, context: Dict[str, Any] = {}) -> Tuple[str, Dict[str, str], List[Dict[str, Any]]]:
        """
        Processes the user request and provides a clear explanation of code or a programming term.

        Returns:
            - response: The explanation or definition
            - thought: Explanation meta (reasoning and source)
            - tool_calls: Tool usage metadata (empty for now)
        """
        explanation_prompt = (
            "You are Emzyking AI, a helpful programming assistant.\n"
            "If the prompt is a code snippet, explain what the code does using bullet points and examples.\n"
            "If the prompt is a question about a programming concept (e.g., 'What is polymorphism?'), give a simple, concise explanation suitable for beginners.\n\n"
            f"Prompt:\n{prompt}\n\n"
            "Explanation:"
        )

        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(explanation_prompt)
            return (
                response.text.strip(),
                {
                    "reasoning": "Identified as a code explanation or programming definition request.",
                    "tool_invoked": "gemini-2.5-flash",
                    "observation": "Response successfully generated using Gemini."
                },
                []  # no tool calls
            )

        except Exception as e:
            if "Quota" in str(e) or "429" in str(e):
                return (
                    "⚠️ Emzyking AI quota exceeded. Please try again later.",
                    {
                        "reasoning": "API quota exceeded.",
                        "tool_invoked": "gemini-2.5-flash",
                        "observation": "Could not generate explanation due to usage limits."
                    },
                    []
                )
            return (
                f"❌ Error while explaining: {str(e)}",
                {
                    "reasoning": "Gemini API call failed.",
                    "tool_invoked": "gemini-2.5-flash",
                    "observation": "An exception occurred while generating explanation."
                },
                []
            )
