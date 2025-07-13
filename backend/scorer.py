"""
This module ranks available AI agents by how well they match the user’s prompt,
based on keyword heuristics and/or agent-specific scoring logic.

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
    either keyword heuristics or custom can_handle scoring.

    Returns:
        List[Tuple[BaseAgent, int]]: Sorted list of (agent, score)
    """
    from backend.agent_registry import AGENT_REGISTRY

    ranked: List[Tuple[BaseAgent, int]] = []

    for agent_name, agent in AGENT_REGISTRY.items():
        if not isinstance(agent, BaseAgent):
            continue

        try:
            # Try agent-defined logic
            score = agent.can_handle(prompt)
            if isinstance(score, int) and score > 0:
                ranked.append((agent, score))
                continue

            # Try keyword fallback if .keywords() exists
            if hasattr(agent, "keywords"):
                keywords = agent.keywords()
                kw_score = keyword_match_score(prompt, keywords)
                if kw_score > 0:
                    ranked.append((agent, kw_score))

        except Exception as e:
            print(f"[Ranker] Error scoring agent '{agent_name}': {e}")
            continue

    # Sort by score descending
    ranked.sort(key=lambda x: x[1], reverse=True)

    # Debugging output
    print("[Router] Agent Ranking:", [(a.name, s) for a, s in ranked])

    return ranked
