"""
This module serves as a centralized registry for all AI agents
used in Emzyking AI. It supports both direct and dynamic access
to agent instances, enabling consistent imports and flexible routing.

Author: Emzyking AI
"""

from typing import List, Dict
from backend.agents.base_agent import BaseAgent
from backend.agents.code_generator import CodeGeneratorAgent
from backend.agents.bug_fixer import BugFixerAgent
from backend.agents.code_explainer import CodeExplainerAgent
from backend.agents.memory_agent import MemoryAgent

# --- Agent Name Constants ---
CODE_GENERATOR = "code_generator"
BUG_FIXER = "bug_fixer"
CODE_EXPLAINER = "code_explainer"
MEMORY = "memory"
ROUTER = "router"

# --- Instantiate Core Agents ---
code_generator_agent = CodeGeneratorAgent()
bug_fixer_agent = BugFixerAgent()
code_explainer_agent = CodeExplainerAgent()
memory_agent = MemoryAgent()

# --- Registry Without Router for Circular Safety ---
AGENT_REGISTRY: Dict[str, BaseAgent] = {
    CODE_GENERATOR: code_generator_agent,
    BUG_FIXER: bug_fixer_agent,
    CODE_EXPLAINER: code_explainer_agent,
    MEMORY: memory_agent,
}

def get_all_agents() -> List[BaseAgent]:
    """
    Returns a list of all agents that can directly handle user prompts.
    Excludes RouterAgent to avoid recursion.

    Returns:
        List[BaseAgent]: All user-facing AI agents.
    """
    return list(AGENT_REGISTRY.values())

# --- Import and Add RouterAgent After get_all_agents is Defined ---
from backend.agents.router_agent import RouterAgent
router_agent = RouterAgent()
AGENT_REGISTRY[ROUTER] = router_agent

__all__ = ["AGENT_REGISTRY", "get_all_agents"]
