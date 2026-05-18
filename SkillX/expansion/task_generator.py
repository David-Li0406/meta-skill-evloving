"""Task generation from trajectories."""

import re
import logging
import uuid
from typing import List, Dict, Optional, Set
from datetime import datetime

try:
    from ..prompts.expansion_prompts import (
        TASK_SUMMARIZE_SYSTEM_PROMPT,
        TASK_SUMMARIZE_USER_PROMPT,
        _format_trajectory_for_summarize,
    )
except ImportError:
    from prompts.expansion_prompts import (
        TASK_SUMMARIZE_SYSTEM_PROMPT,
        TASK_SUMMARIZE_USER_PROMPT,
        _format_trajectory_for_summarize,
    )

logger = logging.getLogger(__name__)


class TaskGenerator:
    """
    Generate new tasks from exploration trajectories.

    Creates task descriptions for unexplored API combinations.
    Output format matches the trajectory format for downstream processing.
    """

    def __init__(self, llm, verbose: bool = True):
        """
        Initialize task generator.

        Args:
            llm: LLM instance
            verbose: Whether to output verbose logs
        """
        self.llm = llm
        self.verbose = verbose

    async def generate(
        self,
        trajectories: List[Dict],
        num_tasks: int = 10,
        existing_tasks: Optional[List[str]] = None
    ) -> List[str]:
        """
        Generate new task descriptions.

        Args:
            trajectories: Source trajectories
            num_tasks: Number of tasks to generate
            existing_tasks: List of existing task descriptions to avoid duplicates

        Returns:
            List of task descriptions
        """
        if not trajectories:
            logger.warning("No trajectories provided for task generation")
            return []

        all_tasks = []
        existing = set(existing_tasks or [])

        for traj in trajectories:
            if len(all_tasks) >= num_tasks:
                break

            tasks = await self._generate_from_trajectory(traj, existing)
            for task in tasks:
                if len(all_tasks) >= num_tasks:
                    break
                if task not in existing:
                    all_tasks.append(task)
                    existing.add(task)

        if self.verbose:
            logger.info(f"Generated {len(all_tasks)} tasks from {len(trajectories)} trajectories")

        return all_tasks

    async def _generate_from_trajectory(
        self,
        trajectory: Dict,
        existing_tasks: Set[str]
    ) -> List[str]:
        """Generate tasks from a single trajectory."""
        # Format trajectory content
        trajectory_content = _format_trajectory_for_summarize(trajectory)

        user_prompt = TASK_SUMMARIZE_USER_PROMPT.format(
            trajectory_content=trajectory_content,
            old_objectives="\n".join(f"- {t}" for t in existing_tasks) if existing_tasks else "None",
            task_preference="Generate realistic, everyday user tasks."
        )

        try:
            response = await self.llm.chat([
                {"role": "system", "content": TASK_SUMMARIZE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ])

            if isinstance(response, dict):
                response_content = response.get("content", "")
            else:
                response_content = str(response)

            return self._parse_queries_from_response(response_content)

        except Exception as e:
            logger.error(f"Failed to generate tasks: {e}")
            return []

    def _parse_queries_from_response(self, response: str) -> List[str]:
        """Extract query strings from LLM response."""
        queries = []

        try:
            task_matches = re.findall(r"<task>(.*?)</task>", response, re.DOTALL)

            for task_content in task_matches:
                query_match = re.search(
                    r"<query>(.*?)</query>", task_content, re.DOTALL
                )
                if query_match:
                    query = query_match.group(1).strip()
                    if query:
                        queries.append(query)

        except Exception as e:
            logger.error(f"Error parsing queries: {e}")

        return queries


class TaskSynthesizer:
    """
    Synthesize complete task objects from exploration results.

    Converts exploration trajectories and task descriptions into
    full task objects ready for execution.
    """

    def __init__(
        self,
        llm,
        benchmark: str = "appworld",
        verbose: bool = True
    ):
        """
        Initialize synthesizer.

        Args:
            llm: LLM instance
            benchmark: Benchmark name for metadata
            verbose: Whether to output verbose logs
        """
        self.llm = llm
        self.benchmark = benchmark
        self.verbose = verbose
        self.task_generator = TaskGenerator(llm, verbose)

    async def synthesize(
        self,
        trajectories: List[Dict],
        existing_tasks: Optional[List[str]] = None,
        max_tasks: int = 10
    ) -> List[Dict]:
        """
        Synthesize complete task objects from trajectories.

        Output format:
        {
            "task_id": "synthetic_<uuid>",
            "user_task": "Natural language task description",
            "query": "Natural language task description",
            "confidence": 0.0-1.0,
            "action_sequence": "Expected solution steps",
            "source": "exploration",
            "epoch": N,
            "benchmark": "appworld",
            "metadata": {...}
        }

        Args:
            trajectories: Exploration trajectories
            existing_tasks: Tasks to avoid duplicating
            max_tasks: Maximum number of tasks to generate

        Returns:
            List of synthesized task dictionaries
        """
        all_tasks = []
        existing = set(existing_tasks or [])

        for traj in trajectories:
            if len(all_tasks) >= max_tasks:
                break

            tasks = await self._synthesize_from_trajectory(traj, existing)

            for task in tasks:
                if len(all_tasks) >= max_tasks:
                    break
                query = task.get("query", "")
                if query and query not in existing:
                    all_tasks.append(task)
                    existing.add(query)

        if self.verbose:
            logger.info(f"Synthesized {len(all_tasks)} tasks")

        return all_tasks

    async def _synthesize_from_trajectory(
        self,
        trajectory: Dict,
        existing_tasks: Set[str]
    ) -> List[Dict]:
        """Synthesize tasks from a single trajectory."""
        # Format trajectory content
        trajectory_content = _format_trajectory_for_summarize(trajectory)

        user_prompt = TASK_SUMMARIZE_USER_PROMPT.format(
            trajectory_content=trajectory_content,
            old_objectives="\n".join(f"- {t}" for t in existing_tasks) if existing_tasks else "None",
            task_preference="Generate realistic, everyday user tasks that could be solved with these APIs."
        )

        try:
            response = await self.llm.chat([
                {"role": "system", "content": TASK_SUMMARIZE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ])

            if isinstance(response, dict):
                response_content = response.get("content", "")
            else:
                response_content = str(response)

            return self._parse_full_tasks(response_content, trajectory)

        except Exception as e:
            logger.error(f"Failed to synthesize tasks: {e}")
            return []

    def _parse_full_tasks(self, response: str, source_trajectory: Dict) -> List[Dict]:
        """Parse complete task objects from LLM response."""
        tasks = []

        try:
            task_matches = re.findall(r"<task>(.*?)</task>", response, re.DOTALL)

            for task_content in task_matches:
                try:
                    query_match = re.search(
                        r"<query>(.*?)</query>", task_content, re.DOTALL
                    )
                    confidence_match = re.search(
                        r"<confidence>(.*?)</confidence>", task_content, re.DOTALL
                    )
                    action_match = re.search(
                        r"<action_sequence>(.*?)</action_sequence>", task_content, re.DOTALL
                    )

                    if query_match and confidence_match and action_match:
                        query = query_match.group(1).strip()
                        confidence = float(confidence_match.group(1).strip())
                        action_sequence = action_match.group(1).strip()

                        task = {
                            "task_id": f"synthetic_{uuid.uuid4().hex[:8]}",
                            "user_task": query,
                            "query": query,
                            "confidence": confidence,
                            "action_sequence": action_sequence,
                            "source": "exploration",
                            "benchmark": self.benchmark,
                            "metadata": {
                                "synthesized_at": datetime.now().isoformat(),
                                "source_trajectory_id": source_trajectory.get(
                                    "trajectory_id", "unknown"
                                ),
                                "evaluator": "synthetic"
                            }
                        }
                        tasks.append(task)

                except (ValueError, AttributeError) as e:
                    logger.debug(f"Failed to parse task: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing tasks: {e}")

        return tasks

    def tasks_to_trajectories(
        self,
        tasks: List[Dict],
        epoch: int = 1
    ) -> List[Dict]:
        """
        Convert synthesized tasks to trajectory format.

        This allows synthesized tasks to be used as input for
        skill extraction in the next epoch.

        Args:
            tasks: List of synthesized tasks
            epoch: Current epoch number

        Returns:
            List of trajectory-formatted dictionaries
        """
        trajectories = []

        for task in tasks:
            trajectory = {
                "trajectory_id": task.get("task_id", f"synthetic_{uuid.uuid4().hex[:8]}"),
                "benchmark": self.benchmark,
                "task_id": task.get("task_id", ""),
                "user_task": task.get("user_task", task.get("query", "")),
                "task_history": [],  # Empty - to be filled by agent execution
                "reward": None,  # Not yet executed
                "metadata": {
                    "source": "exploration",
                    "epoch": epoch,
                    "confidence": task.get("confidence", 0.5),
                    "action_sequence": task.get("action_sequence", ""),
                    "synthesized_at": task.get("metadata", {}).get(
                        "synthesized_at", datetime.now().isoformat()
                    )
                }
            }
            trajectories.append(trajectory)

        return trajectories
