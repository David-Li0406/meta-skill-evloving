"""Base AI client interface."""

from abc import ABC, abstractmethod
from typing import Any


class BaseAIClient(ABC):
    """Base class for AI model clients."""

    def __init__(self, model_name: str):
        """Initialize AI client.

        Args:
            model_name: Name of the AI model (e.g., 'claude-3-5-sonnet', 'gpt-4', 'gemini-pro')
        """
        self.model_name = model_name

    @abstractmethod
    async def analyze(
        self, task: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Analyze task and return structured response.

        Args:
            task: Task description to analyze
            context: Optional context from previous rounds

        Returns:
            dict with keys: analysis, conclusion, confidence
        """
        pass

    @abstractmethod
    async def review(
        self, task: str, peer_analysis: dict[str, Any], own_analysis: dict[str, Any]
    ) -> dict[str, Any]:
        """Review peer analysis and provide feedback.

        Args:
            task: Original task description
            peer_analysis: Peer's analysis to review
            own_analysis: This model's own analysis

        Returns:
            dict with keys: feedback, agreement_points, disagreement_points
        """
        pass

    @abstractmethod
    async def debate(
        self,
        task: str,
        own_position: dict[str, Any],
        opposing_views: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Participate in debate round.

        Args:
            task: Original task description
            own_position: This model's current position
            opposing_views: List of opposing views from other models

        Returns:
            dict with keys: updated_position, rebuttals, concessions
        """
        pass
