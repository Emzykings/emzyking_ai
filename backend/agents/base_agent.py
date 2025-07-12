"""
This module defines the BaseAgent class, which serves as the parent
class for all task-specific agents (e.g., CodeGenerator, BugFixer, etc.).
Each agent must implement the `can_handle` and `handle` methods.

Author: Emzyking AI
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """
    Abstract base class for all agents.

    Subclasses must implement:
    - can_handle(): Determines if the agent can process the given request.
    - handle(): Performs the actual task and returns the response.
    """

    def __init__(self, name: str, description: str):
        """
        Initializes the agent with a name and description.

        Args:
            name (str): Name of the agent.
            description (str): Short description of what the agent does.
        """
        self.name = name
        self.description = description

    @abstractmethod
    def can_handle(self, prompt: str) -> bool:
        """
        Checks whether the agent can handle the given prompt.

        Args:
            prompt (str): The user input.

        Returns:
            bool: True if the agent can handle it, False otherwise.
        """
        pass

    @abstractmethod
    async def handle(self, prompt: str, context: Dict[str, Any] = {}) -> str:
        """
        Handles the prompt and returns a response.

        Args:
            prompt (str): The user input.
            context (Dict): Optional context information.

        Returns:
            str: The agent's response.
        """
        pass

    def get_info(self) -> Dict[str, str]:
        """
        Returns basic info about the agent.

        Returns:
            Dict[str, str]: Dictionary with name and description.
        """
        return {
            "name": self.name,
            "description": self.description
        }
