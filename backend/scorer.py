"""
This module ranks available AI agents by how well they match the user’s prompt,
based on basic keyword heuristics or more advanced NLP models (extensible).

Author: Emzyking AI
"""

from typing import List, Tuple
from backend.agents.base_agent import BaseAgent


def keyword_match_score(prompt: str, keywords: List[str]) -> int:
    """
    Scores a prompt based on the number of matching keywords.

    Args:
        prompt (str): The user input prompt.
        keywords (List[str]): Keywords that define an agent's expertise.

    Returns:
        int: A score representing keyword match strength.
    """
    prompt_lower = prompt.lower()
    return sum(1 for kw in keywords if kw in prompt_lower)


def rank_agents(prompt: str) -> List[Tuple[BaseAgent, int]]:
    """
    Ranks all registered agents by their relevance to the prompt using
    keyword heuristics or can_handle() confidence.

    Args:
        prompt (str): The user input string.

    Returns:
        List[Tuple[BaseAgent, int]]: Agents ranked by descending match score.
    """
    # 🛠️ Lazy import to break circular dependency
    from backend.agent_registry import AGENT_REGISTRY

    ranked: List[Tuple[BaseAgent, int]] = []

    for agent_name, agent in AGENT_REGISTRY.items():
        if isinstance(agent, BaseAgent):
            try:
                score = keyword_match_score(prompt, agent.keywords())
                if score > 0:
                    ranked.append((agent, score))
            except Exception:
                continue

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked
