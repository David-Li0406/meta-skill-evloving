"""Base classes for skill expansion."""

from abc import ABC, abstractmethod
from typing import List, Dict, Set, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.skill import SkillLibrary


class BaseExpansionStrategy(ABC):
    """
    Base class for skill expansion strategies.

    Expansion strategies guide the exploration of new APIs and generation
    of new tasks to expand the skill library.
    """

    @abstractmethod
    async def analyze_experience(
        self,
        successful_trajs: List[Dict],
        failed_trajs: List[Dict]
    ) -> Dict[str, Set[str]]:
        """
        Analyze trajectories to identify API usage patterns.

        This method examines successful and failed trajectories to identify:
        - APIs that work reliably (successful_apis)
        - APIs that frequently fail (failed_apis)
        - APIs that are used in failures but not successes (unexplored_apis)

        Args:
            successful_trajs: Trajectories with reward >= threshold
            failed_trajs: Trajectories with reward < threshold

        Returns:
            Dict with keys:
                - successful_apis: Set of API names that worked
                - failed_apis: Set of API names that failed
                - unexplored_apis: Set of APIs needing more exploration
        """
        pass

    @abstractmethod
    async def explore(
        self,
        skill_library: "SkillLibrary",
        env_worker: Any,
        experience: Dict[str, Set[str]]
    ) -> List[Dict]:
        """
        Explore environment guided by experience.

        Uses the experience analysis to guide exploration:
        - Prioritize unexplored and failed APIs
        - Avoid re-exploring stable, successful APIs
        - Collect new trajectories demonstrating API usage

        Args:
            skill_library: Current skill library (to check coverage)
            env_worker: Environment worker for rollout execution
            experience: API usage statistics from analyze_experience()

        Returns:
            List of exploration trajectories
        """
        pass

    @abstractmethod
    async def summarize(self, trajectories: List[Dict]) -> List[Dict]:
        """
        Generate new task descriptions from exploration trajectories.

        Analyzes exploration trajectories to synthesize realistic,
        user-centered task descriptions that can be used to generate
        new training trajectories.

        Args:
            trajectories: Exploration trajectories to analyze

        Returns:
            List of synthesized tasks with format:
            {
                "query": "Natural language task description",
                "confidence": 0.0-1.0,
                "action_sequence": "Expected solution steps",
                "source": "exploration"
            }
        """
        pass
