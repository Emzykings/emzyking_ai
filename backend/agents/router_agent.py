"""
This module defines the RouterAgent, responsible for routing user prompts
to the most appropriate specialized agent based on intent, confidence scoring,
and contextual memory.

Author: Emzyking AI
"""

from typing import List, Dict, Any, Optional, Tuple
from backend.agents.base_agent import BaseAgent
from backend.scorer import rank_agents


class RouterAgent(BaseAgent):
    """
    Central dispatcher that determines which specialized agent is best suited
    to respond to a given user prompt based on intent and context scoring.
    """

    def __init__(self):
        # Lazy import to avoid circular import at top-level
        from backend.agent_registry import get_all_agents
        self.agents: List[BaseAgent] = [
            agent for agent in get_all_agents()
            if agent.__class__.__name__ != "RouterAgent"
        ]

    def keywords(self) -> List[str]:
        return ["route", "dispatch", "redirect"]

    def can_handle(self, user_input: str) -> int:
        """
        Always return 0 — RouterAgent is not designed to directly handle prompts.
        """
        return 0

    async def handle(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Optional[Dict[str, str]], List[Dict[str, Any]]]:
        """
        Enables the RouterAgent to behave like other agents, primarily for consistency.
        """
        response, thought, tools, agent, score = await self.route(user_input=user_input, context=context)
        return response, thought, tools

    async def route(
        self,
        user_input: str,
        chat_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Optional[Dict[str, str]], List[Dict[str, Any]], str, float]:
        """
        Main routing function. Scores and selects the best agent.
        """
        context = context or {}

        # Step 1: Score agents by relevance using rank_agents()
        ranked: List[Tuple[BaseAgent, int]] = rank_agents(user_input)

        # Step 2: Pick the best agent
        if ranked:
            best_agent, score = ranked[0]
            response, thought, tool_calls = await best_agent.handle(user_input, context)
            return response, thought, tool_calls, best_agent.__class__.__name__, float(score)

        # Step 3: Fallback response
        fallback_msg = (
            "🤖 I'm not sure how to help with that.\n"
            "Try one of the following:\n"
            "• 'Generate a Python function to sort a list'\n"
            "• 'Fix this broken JavaScript code'\n"
            "• 'Explain what this SQL query does'\n"
            "• 'Remember that I prefer Python over Java'"
        )
        return fallback_msg, None, [], "router", 0.0