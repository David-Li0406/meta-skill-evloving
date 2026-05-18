"""Base classes for inference."""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any


class BaseSkillRetriever(ABC):
    """Base class for skill retrieval."""

    @abstractmethod
    async def retrieve_plan(
        self,
        task: str,
        top_k: int = 3
    ) -> List[Dict]:
        """
        Retrieve relevant plans for a task.

        Args:
            task: Task description
            top_k: Number of plans to retrieve

        Returns:
            List of plan dictionaries
        """
        pass

    @abstractmethod
    async def retrieve_skills(
        self,
        query: str,
        skill_type: str = "functional",
        top_k: int = 5
    ) -> List[Dict]:
        """
        Retrieve relevant skills.

        Args:
            query: Query text
            skill_type: Type of skills to retrieve
            top_k: Number of skills to retrieve

        Returns:
            List of skill dictionaries
        """
        pass


class BaseAgent(ABC):
    """Base class for benchmark-specific agents."""

    def __init__(
        self,
        llm,
        skill_retriever: Optional[BaseSkillRetriever] = None,
        benchmark: str = "appworld",
        mode: str = "plan_with_skill"
    ):
        """
        Initialize agent.

        Args:
            llm: LLM instance
            skill_retriever: Skill retrieval service
            benchmark: Benchmark name
            mode: Agent mode (vanilla, plan_only, plan_with_skill, skill_only)
        """
        self.llm = llm
        self.skill_retriever = skill_retriever
        self.benchmark = benchmark
        self.mode = mode

    @abstractmethod
    async def step(self, observation: str) -> str:
        """
        Execute one agent step.

        Args:
            observation: Current observation

        Returns:
            Agent action
        """
        pass

    @abstractmethod
    async def run(self, task: str) -> Dict:
        """
        Run agent on a task.

        Args:
            task: Task description

        Returns:
            Trajectory dictionary
        """
        pass
