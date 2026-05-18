"""Real environment exploration strategy.

Strategy that explores in real environment via EnvClient,
as opposed to LLM-simulated exploration.
"""

import re
import uuid
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base import ExplorationStrategy, TaskObjective

logger = logging.getLogger(__name__)


# Prompts for real environment exploration
REAL_EXPLORE_SYSTEM_PROMPT = """You are an AI assistant exploring an environment to discover useful API combinations.

You will interact with a real environment that provides actual API responses.
Your goal is to:
1. Explore available APIs by making calls
2. Observe the real responses
3. Discover useful API combinations for common tasks

Be exploratory - try different APIs and parameter combinations.
Focus on finding novel patterns that could be useful for users.

{additional_guidance}
"""

SUMMARIZE_SYSTEM_PROMPT = """You are an AI assistant that generates task descriptions from exploration trajectories.

Given an exploration trajectory showing real API interactions, generate new task descriptions that:
1. Could be solved using the discovered API combinations
2. Are realistic user requests
3. Cover the observed API patterns

For each task, provide:
- A confidence score (0.0-1.0) based on how well-defined the task is
- An action sequence showing how to solve it"""

SUMMARIZE_USER_PROMPT = """## Original Task
{seed_task}

## Exploration Trajectory (Real Environment)
{trajectory}

## Instructions
Based on the real API interactions observed, generate 1-3 new task descriptions.

Output format:
<tasks>
<task>
<query>Natural language task description</query>
<confidence>0.0-1.0</confidence>
<action_sequence>Step-by-step solution using the observed APIs</action_sequence>
</task>
...
</tasks>
"""


class RealEnvironmentExplorationStrategy(ExplorationStrategy):
    """
    Strategy that explores in real environment.

    Key difference from Random/ExperienceGuided strategies:
    - Those use LLM to SIMULATE exploration (fake observations)
    - This uses LLM to DRIVE exploration in REAL environment (real observations)

    The trajectory contains actual API responses from the environment.
    """

    def __init__(
        self,
        llm,
        env_client=None,
        env_type: str = "appworld",
        max_steps: int = 10,
        max_tasks_per_trajectory: int = 3,
        tools: Optional[List[Dict]] = None,
        additional_guidance: str = "",
        verbose: bool = True
    ):
        """
        Initialize real environment exploration strategy.

        Args:
            llm: LLM instance for agent decisions
            env_client: EnvClient for environment interaction
            env_type: Environment type (appworld, bfcl, tau2bench)
            max_steps: Maximum exploration steps
            max_tasks_per_trajectory: Maximum tasks to generate per trajectory
            tools: Available tool schemas
            additional_guidance: Additional system prompt guidance
            verbose: Whether to log verbose output
        """
        super().__init__(llm, env_client, verbose)
        self.env_type = env_type
        self.max_steps = max_steps
        self.max_tasks_per_trajectory = max_tasks_per_trajectory
        self.tools = tools or []
        self.additional_guidance = additional_guidance
        self._explorer = None

    def _get_explorer(self):
        """Lazy initialization of explorer."""
        if self._explorer is None:
            from ..env_explorer import RealEnvironmentExplorer
            self._explorer = RealEnvironmentExplorer(
                env_client=self.env_client,
                llm=self.llm,
                env_type=self.env_type,
                tools=self.tools,
                verbose=self.verbose
            )
        return self._explorer

    def _build_exploration_prompt(self) -> str:
        """Build system prompt for exploration."""
        return REAL_EXPLORE_SYSTEM_PROMPT.format(
            additional_guidance=self.additional_guidance or "Explore freely."
        )

    async def explore(
        self,
        seed_task: Dict,
        **kwargs
    ) -> List[Dict]:
        """
        Explore real environment from seed task.

        Args:
            seed_task: Seed task with task_id and optional user_task

        Returns:
            List containing single trajectory from real environment
        """
        task_id = seed_task.get("task_id", str(uuid.uuid4())[:8])

        if self.env_client is None:
            logger.error("No env_client provided, cannot explore real environment")
            return []

        explorer = self._get_explorer()
        system_prompt = self._build_exploration_prompt()

        try:
            trajectory = await explorer.explore_task(
                task_id=task_id,
                system_prompt=system_prompt,
                max_steps=self.max_steps
            )

            if self.verbose:
                step_count = len(trajectory.get("steps", []))
                logger.info(f"Real environment exploration: {step_count} steps, "
                           f"reward={trajectory.get('reward')}")

            return [trajectory]

        except Exception as e:
            logger.error(f"Real environment exploration failed: {e}")
            return []

    async def summarize(
        self,
        seed_task: Dict,
        trajectory: Dict
    ) -> List[Dict]:
        """
        Summarize real exploration trajectory into task objectives.

        Args:
            seed_task: Original seed task
            trajectory: Trajectory from real environment

        Returns:
            List of task objective dictionaries
        """
        user_task = seed_task.get("user_task", seed_task.get("task_id", "unknown"))
        trajectory_str = self._format_trajectory(trajectory)

        user_prompt = SUMMARIZE_USER_PROMPT.format(
            seed_task=user_task,
            trajectory=trajectory_str
        )

        try:
            if hasattr(self.llm, 'chat'):
                response = await self.llm.chat([
                    {"role": "system", "content": SUMMARIZE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ])
            else:
                response = await self.llm.ainvoke(messages=[
                    {"role": "system", "content": SUMMARIZE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ])

            if isinstance(response, dict):
                response_content = response.get("content", "")
            else:
                response_content = str(response)

            objectives = self._parse_tasks(response_content)
            objectives = objectives[:self.max_tasks_per_trajectory]

            if self.verbose:
                logger.info(f"Generated {len(objectives)} task objectives from real trajectory")

            return objectives

        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return []

    def _format_trajectory(self, trajectory: Dict) -> str:
        """Format trajectory for prompt."""
        parts = []

        # Include task info
        parts.append(f"Task ID: {trajectory.get('task_id', 'unknown')}")
        parts.append(f"Environment: {trajectory.get('env_type', 'unknown')}")

        # Format steps
        steps = trajectory.get("steps", [])
        if steps:
            parts.append("\n## Steps:")
            for i, step in enumerate(steps, 1):
                action = step.get("action", {})
                observation = step.get("observation", [])

                # Format action
                if isinstance(action, dict):
                    action_str = action.get("content", "")
                    if action.get("tool_calls"):
                        tool_calls = action["tool_calls"]
                        action_str += f"\nTool calls: {tool_calls}"
                else:
                    action_str = str(action)

                # Format observation
                if isinstance(observation, list):
                    obs_str = "\n".join(
                        f"  - {msg.get('role', 'unknown')}: {msg.get('content', '')[:200]}"
                        for msg in observation
                    )
                else:
                    obs_str = str(observation)

                parts.append(f"\nStep {i}:")
                parts.append(f"  Action: {action_str[:300]}")
                parts.append(f"  Observation: {obs_str[:300]}")

        # Include reward if available
        if trajectory.get("reward") is not None:
            parts.append(f"\nFinal reward: {trajectory['reward']}")

        return "\n".join(parts)

    def _parse_tasks(self, response: str) -> List[Dict]:
        """Parse task objectives from LLM response."""
        objectives = []

        try:
            tasks_match = re.search(
                r"<tasks>(.*?)</tasks>",
                response,
                re.DOTALL
            )

            if tasks_match:
                tasks_content = tasks_match.group(1)
                task_matches = re.findall(
                    r"<task>(.*?)</task>",
                    tasks_content,
                    re.DOTALL
                )

                for task_content in task_matches:
                    query_match = re.search(
                        r"<query>(.*?)</query>",
                        task_content,
                        re.DOTALL
                    )
                    confidence_match = re.search(
                        r"<confidence>(.*?)</confidence>",
                        task_content,
                        re.DOTALL
                    )
                    action_match = re.search(
                        r"<action_sequence>(.*?)</action_sequence>",
                        task_content,
                        re.DOTALL
                    )

                    if query_match:
                        try:
                            confidence = float(confidence_match.group(1).strip()) if confidence_match else 0.5
                        except ValueError:
                            confidence = 0.5

                        objective = TaskObjective(
                            query=query_match.group(1).strip(),
                            confidence=confidence,
                            action_sequence=action_match.group(1).strip() if action_match else "",
                            metadata={"source": "real_environment_exploration"}
                        )
                        objectives.append(objective.to_dict())

        except Exception as e:
            logger.debug(f"Error parsing tasks: {e}")

        return objectives


class ExperienceGuidedRealStrategy(ExplorationStrategy):
    """
    Experience-guided exploration in real environment.

    Combines experience tracking with real environment interaction:
    1. Uses past experience to guide exploration
    2. Executes in real environment
    3. Collects real trajectories for skill extraction
    """

    def __init__(
        self,
        llm,
        env_client=None,
        env_type: str = "appworld",
        experience_tracker=None,
        max_steps: int = 10,
        max_tasks_per_trajectory: int = 3,
        tools: Optional[List[Dict]] = None,
        verbose: bool = True
    ):
        super().__init__(llm, env_client, verbose)
        self.env_type = env_type
        self.experience_tracker = experience_tracker
        self.max_steps = max_steps
        self.max_tasks_per_trajectory = max_tasks_per_trajectory
        self.tools = tools or []
        self._explorer = None

    def _get_explorer(self):
        """Lazy initialization of explorer."""
        if self._explorer is None:
            from ..env_explorer import RealEnvironmentExplorer
            self._explorer = RealEnvironmentExplorer(
                env_client=self.env_client,
                llm=self.llm,
                env_type=self.env_type,
                tools=self.tools,
                verbose=self.verbose
            )
        return self._explorer

    def set_experience_tracker(self, tracker) -> None:
        """Set or update experience tracker."""
        self.experience_tracker = tracker

    def _build_guided_prompt(self) -> str:
        """Build system prompt with experience guidance."""
        base_prompt = """You are an AI assistant exploring an environment to discover useful API combinations.

You will interact with a real environment that provides actual API responses.
"""
        if self.experience_tracker:
            guidance = self.experience_tracker.get_exploration_guidance()
            return f"{base_prompt}\n\n## Experience Guidance\n{guidance}"

        return base_prompt

    async def explore(
        self,
        seed_task: Dict,
        **kwargs
    ) -> List[Dict]:
        """Explore real environment with experience guidance."""
        task_id = seed_task.get("task_id", str(uuid.uuid4())[:8])

        if self.env_client is None:
            logger.error("No env_client provided, cannot explore real environment")
            return []

        explorer = self._get_explorer()
        system_prompt = self._build_guided_prompt()

        try:
            trajectory = await explorer.explore_task(
                task_id=task_id,
                system_prompt=system_prompt,
                max_steps=self.max_steps
            )

            if self.verbose:
                step_count = len(trajectory.get("steps", []))
                logger.info(f"Experience-guided real exploration: {step_count} steps")

            return [trajectory]

        except Exception as e:
            logger.error(f"Experience-guided exploration failed: {e}")
            return []

    async def summarize(
        self,
        seed_task: Dict,
        trajectory: Dict
    ) -> List[Dict]:
        """Summarize exploration into task objectives."""
        # Reuse the summarization from RealEnvironmentExplorationStrategy
        real_strategy = RealEnvironmentExplorationStrategy(
            llm=self.llm,
            max_tasks_per_trajectory=self.max_tasks_per_trajectory,
            verbose=self.verbose
        )
        return await real_strategy.summarize(seed_task, trajectory)
