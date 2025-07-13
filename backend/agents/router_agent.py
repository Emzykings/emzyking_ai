"""
This module defines the RouterAgent, responsible for routing user prompts
to the most appropriate specialized agent based on intent, confidence scoring,
and contextual memory.

Author: Emzyking AI
"""

from typing import List, Dict, Any, Optional, Tuple
from backend.agents.base_agent import BaseAgent
from backend.scorer import rank_agents
from backend import llm_handler


class RouterAgent(BaseAgent):
    """
    Central dispatcher that determines which specialized agent is best suited
    to respond to a given user prompt based on intent and context scoring.
    """

    def __init__(self):
        # import to avoid circular import at top-level
        from backend.agent_registry import get_all_agents
        self.agents: List[BaseAgent] = [
            agent for agent in get_all_agents()
            if agent.__class__.__name__ != "RouterAgent"
        ]

    def keywords(self) -> List[str]:
        return ["route", "dispatch", "redirect"]

    def can_handle(self, user_input: str) -> int:
        # RouterAgent doesn't directly handle prompts
        return 0

    async def handle(
        self,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Optional[Dict[str, str]], List[Dict[str, Any]]]:
        response, thought, tools, _, _ = await self.route(user_input=user_input, context=context)
        return response, thought, tools

    async def route(
        self,
        user_input: str,
        chat_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Optional[Dict[str, str]], List[Dict[str, Any]], str, float]:
        """
        Main routing function. Scores and selects the best agent.

        Returns:
            - response: The agent's reply to the prompt
            - thought: Optional thought or internal reasoning
            - tool_calls: Any tool usage or structured actions
            - agent_name: The name of the selected agent
            - confidence_score: Relevance score from ranking
        """
        context = context or {}

        # Step 1: Score agents by relevance
        ranked: List[Tuple[BaseAgent, int]] = rank_agents(user_input)

        # Step 2: Try the best ranked agent (even if score is 0)
        if ranked:
            best_agent, score = ranked[0]
            try:
                result = await best_agent.handle(user_input, context)

                if isinstance(result, str):
                    response = result
                    thought = {
                        "reasoning": f"Handled by {best_agent.__class__.__name__} based on prompt match.",
                        "tool_invoked": "gemini-2.5-flash",
                        "observation": "Returned simple text."
                    }
                    return response, thought, [], best_agent.__class__.__name__, float(score)

                response, thought, tools = result
                return response, thought, tools, best_agent.__class__.__name__, float(score)

            except Exception as e:
                print(f"Agent {best_agent.__class__.__name__} failed: {e}")

        # Step 3: Fallback to direct model handler if all else fails
        try:
            response = await llm_handler.generate(user_input)
            thought = {
                "reasoning": "No specialized agent scored confidently or succeeded. Used LLM handler fallback.",
                "tool_invoked": "gemini-2.5-flash",
                "observation": "Handled via direct LLM call."
            }
            return response, thought, [], "llm_handler", 0.0

        except Exception as e:
            print(f"LLM Handler Fallback failed: {e}")

        # Step 4: Final fallback message
        fallback_msg = (
            "🤖 Hi, I am Emzyking AI your programming Assistant, I'm not sure how to help with that.\n"
            "Try one of the following:\n"
            "• 'Generate a Python function to sort a list'\n"
            "• 'Fix this broken JavaScript code'\n"
            "• 'Explain what this SQL query does'\n"
            "• 'Remember that I prefer Python over Java'"
        )
        return fallback_msg, None, [], "router", 0.0
