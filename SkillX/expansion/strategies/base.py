"""Base class for exploration strategies.

Based on AgentEvolver's TaskExploreStrategy design pattern.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ExplorationStrategy(ABC):
    """
    Abstract base class for exploration strategies.

    An exploration strategy defines how to:
    1. Explore an environment from a seed task
    2. Summarize exploration trajectories into new tasks

    Subclasses must implement:
    - explore(): Generate trajectories from seed tasks
    - summarize(): Convert trajectories to task objectives
    """

    def __init__(
        self,
        llm,
        env_client: Optional[Any] = None,
        verbose: bool = True
    ):
        """
        Initialize exploration strategy.

        Args:
            llm: LLM instance for task generation
            env_client: Optional environment client for interaction
            verbose: Whether to output verbose logs
        """
        self.llm = llm
        self.env_client = env_client
        self.verbose = verbose

    @abstractmethod
    async def explore(
        self,
        seed_task: Dict,
        **kwargs
    ) -> List[Dict]:
        """
        Explore environment from a seed task.

        This method generates exploration trajectories by interacting
        with the environment or using the LLM to simulate interactions.

        Args:
            seed_task: Seed task to explore from
                - task_id: Unique task identifier
                - user_task: Task description
                - metadata: Additional task metadata

        Returns:
            List of trajectory dictionaries, each containing:
                - trajectory_id: Unique trajectory identifier
                - steps: List of (action, observation) pairs
                - metadata: Additional trajectory metadata
        """
        pass

    @abstractmethod
    async def summarize(
        self,
        seed_task: Dict,
        trajectory: Dict
    ) -> List[Dict]:
        """
        Summarize exploration trajectory to generate new task objectives.

        This method analyzes an exploration trajectory and generates
        new task descriptions that could be solved using the discovered
        API combinations.

        Args:
            seed_task: Original seed task
            trajectory: Exploration trajectory to summarize

        Returns:
            List of task objective dictionaries, each containing:
                - query: Natural language task description
                - confidence: Confidence score (0.0-1.0)
                - action_sequence: Expected solution steps
                - metadata: Additional metadata
        """
        pass

    def set_env_client(self, env_client: Any) -> None:
        """Set or update the environment client."""
        self.env_client = env_client

    def inject_dependencies(
        self,
        llm: Optional[Any] = None,
        env_client: Optional[Any] = None,
        **kwargs
    ) -> None:
        """
        Inject dependencies after initialization.

        Useful for delayed initialization or configuration updates.
        """
        if llm is not None:
            self.llm = llm
        if env_client is not None:
            self.env_client = env_client


class TaskObjective:
    """
    Represents a synthesized task objective.

    Attributes:
        query: Natural language task description
        confidence: Confidence score for task quality
        action_sequence: Expected solution steps
        ground_truth: Optional expected answer
        metadata: Additional metadata
    """

    def __init__(
        self,
        query: str,
        confidence: float = 0.5,
        action_sequence: str = "",
        ground_truth: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.query = query
        self.confidence = confidence
        self.action_sequence = action_sequence
        self.ground_truth = ground_truth
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "query": self.query,
            "confidence": self.confidence,
            "action_sequence": self.action_sequence,
            "ground_truth": self.ground_truth,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskObjective":
        """Create from dictionary representation."""
        return cls(
            query=data.get("query", ""),
            confidence=data.get("confidence", 0.5),
            action_sequence=data.get("action_sequence", ""),
            ground_truth=data.get("ground_truth"),
            metadata=data.get("metadata", {}),
        )
