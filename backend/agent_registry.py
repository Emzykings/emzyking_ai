"""
This module serves as a centralized registry for all AI agents
used in Emzyking AI. It supports both direct and dynamic access
to agent instances, enabling consistent imports and flexible routing.

Author: Emzyking AI
"""

from typing import List
from backend.agents.base_agent import BaseAgent
from backend.agents.code_generator import CodeGeneratorAgent
from backend.agents.bug_fixer import BugFixerAgent
from backend.agents.code_explainer import CodeExplainerAgent
from backend.agents.memory_agent import MemoryAgent

# --- Instantiate Core Agents ---
code_generator_agent = CodeGeneratorAgent()
bug_fixer_agent = BugFixerAgent()
code_explainer_agent = CodeExplainerAgent()
memory_agent = MemoryAgent()

# --- Registry Without Router for Circular Safety ---
AGENT_REGISTRY = {
    "code_generator": code_generator_agent,
    "bug_fixer": bug_fixer_agent,
    "code_explainer": code_explainer_agent,
    "memory": memory_agent,
}

def get_all_agents() -> List[BaseAgent]:
    """
    Returns a list of all agents that can directly handle user prompts.
    Excludes RouterAgent itself to avoid recursion.

    Returns:
        List[BaseAgent]: All applicable user-facing AI agents.
    """
    return list(AGENT_REGISTRY.values())

# --- Import and Add RouterAgent After get_all_agents is Defined ---
from backend.agents.router_agent import RouterAgent
router_agent = RouterAgent()
AGENT_REGISTRY["router"] = router_agent
