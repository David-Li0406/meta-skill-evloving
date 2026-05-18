"""Experience-guided exploration strategy.

Based on AgentEvolver's exploration pattern that uses:
1. Experience from previous rollouts to guide API exploration
2. API checklist to avoid redundant exploration
3. Skill library coverage analysis
"""

import re
import uuid
import json
import random
import logging
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
from collections import defaultdict

from .base import ExplorationStrategy, TaskObjective

logger = logging.getLogger(__name__)


# Prompts for experience-guided exploration
EXPERIENCE_GUIDED_SYSTEM_PROMPT = """You are an AI assistant exploring an environment to discover useful API combinations.

Given a seed task, available tools, and experience information (APIs that work well vs. APIs that often fail),
generate a realistic exploration trajectory that:
1. Prioritizes unexplored or underutilized APIs
2. Avoids APIs that have been frequently failing
3. Discovers new, useful API combinations for solving real user tasks

Your exploration should help expand the skill library by finding novel API usage patterns."""

EXPERIENCE_GUIDED_USER_PROMPT = """## Seed Task
{seed_task}

## Available Tools
{available_tools}

## Experience Guidance
{experience_guidance}

## Instructions
Generate an exploration trajectory that:
1. Uses 3-5 API calls
2. Explores APIs NOT in the already-covered list when possible
3. Avoids APIs that frequently fail
4. Discovers meaningful API combinations

Output your exploration as a series of steps:
<exploration>
<step>
<action>API call with parameters</action>
<observation>Expected response</observation>
</step>
...
</exploration>
"""

EXPERIENCE_SUMMARIZE_SYSTEM_PROMPT = """You are an AI assistant that generates task descriptions from exploration trajectories.

Given an exploration trajectory showing API interactions and existing tasks to avoid duplicates,
generate new task descriptions that:
1. Could be solved using the discovered API combinations
2. Are realistic user requests
3. Are different from existing tasks
4. Test novel API usage patterns

For each task, provide:
- A confidence score (0.0-1.0) based on how well-defined the task is
- An action sequence showing how to solve it"""

EXPERIENCE_SUMMARIZE_USER_PROMPT = """## Seed Task
{seed_task}

## Exploration Trajectory
{trajectory}

## Existing Tasks (avoid generating similar ones)
{existing_tasks}

## Instructions
Generate 1-3 new task descriptions based on this exploration.
Ensure they are distinct from existing tasks.

Output format:
<tasks>
<task>
<query>Natural language task description</query>
<confidence>0.0-1.0</confidence>
<action_sequence>Step-by-step solution</action_sequence>
</task>
...
</tasks>
"""


class ExperienceTracker:
    """
    Tracks API usage experience across trajectories.

    Identifies:
    - Stable APIs: consistently successful
    - Risky APIs: frequently failing
    - Uncovered APIs: not yet explored
    """

    def __init__(self):
        self.api_success_count: Dict[str, int] = defaultdict(int)
        self.api_failure_count: Dict[str, int] = defaultdict(int)
        self.all_available_apis: Set[str] = set()
        self.skill_covered_apis: Set[str] = set()

    def load_from_trajectories(self, trajectories: List[Dict]) -> None:
        """Load experience from trajectory data."""
        for traj in trajectories:
            reward = traj.get("reward", 0)
            is_success = reward > 0.99

            # Extract tools used in trajectory
            task_history = traj.get("task_history", [])
            for step in task_history:
                if step.get("role") == "assistant" and step.get("tool_calls"):
                    for tool_call in step["tool_calls"]:
                        api_name = tool_call.get("name", "")
                        if api_name:
                            if is_success:
                                self.api_success_count[api_name] += 1
                            else:
                                self.api_failure_count[api_name] += 1

    def load_from_skills(self, skills: List[Dict]) -> None:
        """Load covered APIs from skill library."""
        for skill_item in skills:
            skill = skill_item.get("skill", skill_item)
            tools = skill.get("tools", [])
            self.skill_covered_apis.update(tools)

    def set_available_apis(self, apis: List[str]) -> None:
        """Set all available APIs for the domain."""
        self.all_available_apis = set(apis)

    def get_stable_apis(self, min_success_ratio: float = 0.7) -> Set[str]:
        """Get APIs that are consistently successful."""
        stable = set()
        for api in self.api_success_count:
            total = self.api_success_count[api] + self.api_failure_count[api]
            if total > 0 and self.api_success_count[api] / total >= min_success_ratio:
                stable.add(api)
        return stable

    def get_risky_apis(self, min_failure_ratio: float = 0.5) -> Set[str]:
        """Get APIs that frequently fail."""
        risky = set()
        for api in self.api_failure_count:
            total = self.api_success_count.get(api, 0) + self.api_failure_count[api]
            if total > 0 and self.api_failure_count[api] / total >= min_failure_ratio:
                risky.add(api)
        return risky

    def get_uncovered_apis(self) -> Set[str]:
        """Get APIs not yet covered by skill library."""
        return self.all_available_apis - self.skill_covered_apis

    def get_exploration_guidance(self) -> str:
        """Generate exploration guidance text."""
        stable = self.get_stable_apis()
        risky = self.get_risky_apis()
        uncovered = self.get_uncovered_apis()

        guidance_parts = []

        if stable:
            guidance_parts.append(
                f"**Stable APIs** (work well, avoid over-exploring):\n{', '.join(list(stable)[:20])}"
            )

        if risky:
            guidance_parts.append(
                f"**Risky APIs** (often fail, use carefully):\n{', '.join(list(risky)[:10])}"
            )

        if uncovered:
            guidance_parts.append(
                f"**Unexplored APIs** (prioritize these):\n{', '.join(list(uncovered)[:15])}"
            )

        return "\n\n".join(guidance_parts) if guidance_parts else "No prior experience available."


class ExperienceGuidedExplorationStrategy(ExplorationStrategy):
    """
    Experience-guided exploration strategy.

    This strategy:
    1. Tracks API usage patterns from past trajectories
    2. Guides exploration towards unexplored or underutilized APIs
    3. Avoids redundant exploration of well-covered APIs
    4. Prevents repeated failures by avoiding risky APIs

    Based on AgentEvolver's exploration approach.
    """

    def __init__(
        self,
        llm,
        env_client: Optional[Any] = None,
        max_steps: int = 5,
        max_tasks_per_trajectory: int = 3,
        available_tools: Optional[List[Dict]] = None,
        experience_tracker: Optional[ExperienceTracker] = None,
        existing_queries: Optional[Set[str]] = None,
        verbose: bool = True
    ):
        """
        Initialize experience-guided exploration strategy.

        Args:
            llm: LLM instance
            env_client: Optional environment client
            max_steps: Maximum exploration steps
            max_tasks_per_trajectory: Maximum tasks per trajectory
            available_tools: List of available tool schemas
            experience_tracker: Tracker for API usage experience
            existing_queries: Set of existing task queries to avoid
            verbose: Whether to output verbose logs
        """
        super().__init__(llm, env_client, verbose)
        self.max_steps = max_steps
        self.max_tasks_per_trajectory = max_tasks_per_trajectory
        self.available_tools = available_tools or []
        self.experience_tracker = experience_tracker or ExperienceTracker()
        self.existing_queries = existing_queries or set()

    def set_available_tools(self, tools: List[Dict]) -> None:
        """Set available tools and update experience tracker."""
        self.available_tools = tools
        api_names = [
            t["function"]["name"]
            for t in tools
            if "function" in t
        ]
        self.experience_tracker.set_available_apis(api_names)

    def load_experience(
        self,
        trajectories: Optional[List[Dict]] = None,
        skills: Optional[List[Dict]] = None
    ) -> None:
        """Load experience from trajectories and skills."""
        if trajectories:
            self.experience_tracker.load_from_trajectories(trajectories)
        if skills:
            self.experience_tracker.load_from_skills(skills)

    def add_existing_query(self, query: str) -> None:
        """Add query to existing set."""
        self.existing_queries.add(query.lower().strip())

    async def explore(
        self,
        seed_task: Dict,
        **kwargs
    ) -> List[Dict]:
        """
        Explore using experience-guided LLM interaction.

        Args:
            seed_task: Seed task to explore from

        Returns:
            List of trajectory dictionaries
        """
        task_id = seed_task.get("task_id", str(uuid.uuid4())[:8])
        user_task = seed_task.get("user_task", "")

        # Format available tools
        tools_str = self._format_tools(self.available_tools)

        # Get experience guidance
        experience_guidance = self.experience_tracker.get_exploration_guidance()

        # Build exploration prompt
        user_prompt = EXPERIENCE_GUIDED_USER_PROMPT.format(
            seed_task=user_task,
            available_tools=tools_str,
            experience_guidance=experience_guidance
        )

        try:
            if hasattr(self.llm, 'chat'):
                response = await self.llm.chat([
                    {"role": "system", "content": EXPERIENCE_GUIDED_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ])
            else:
                response = await self.llm.ainvoke(messages=[
                    ("system", EXPERIENCE_GUIDED_SYSTEM_PROMPT),
                    ("user", user_prompt)
                ])

            if isinstance(response, dict):
                response_content = response.get("content", "")
            else:
                response_content = str(response)

            # Parse exploration trajectory
            trajectory = self._parse_exploration(response_content)
            trajectory["trajectory_id"] = f"explore_{task_id}_{uuid.uuid4().hex[:8]}"
            trajectory["seed_task_id"] = task_id
            trajectory["timestamp"] = datetime.now().isoformat()
            trajectory["experience_guided"] = True

            if self.verbose:
                step_count = len(trajectory.get('steps', []))
                logger.info(f"Generated experience-guided trajectory with {step_count} steps")

            return [trajectory]

        except Exception as e:
            logger.error(f"Experience-guided exploration failed: {e}")
            return []

    async def summarize(
        self,
        seed_task: Dict,
        trajectory: Dict
    ) -> List[Dict]:
        """
        Summarize exploration to generate task objectives.

        Includes deduplication against existing tasks.
        """
        user_task = seed_task.get("user_task", "")

        # Format trajectory
        trajectory_str = self._format_trajectory(trajectory)

        # Format existing tasks for deduplication
        existing_tasks_str = self._format_existing_tasks()

        # Build summarization prompt
        user_prompt = EXPERIENCE_SUMMARIZE_USER_PROMPT.format(
            seed_task=user_task,
            trajectory=trajectory_str,
            existing_tasks=existing_tasks_str
        )

        try:
            if hasattr(self.llm, 'chat'):
                response = await self.llm.chat([
                    {"role": "system", "content": EXPERIENCE_SUMMARIZE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ])
            else:
                response = await self.llm.ainvoke(messages=[
                    ("system", EXPERIENCE_SUMMARIZE_SYSTEM_PROMPT),
                    ("user", user_prompt)
                ])

            if isinstance(response, dict):
                response_content = response.get("content", "")
            else:
                response_content = str(response)

            # Parse and deduplicate
            objectives = self._parse_tasks(response_content)
            objectives = self._deduplicate_objectives(objectives)
            objectives = objectives[:self.max_tasks_per_trajectory]

            # Add to existing queries
            for obj in objectives:
                self.add_existing_query(obj.get("query", ""))

            if self.verbose:
                logger.info(f"Generated {len(objectives)} unique task objectives")

            return objectives

        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return []

    def _format_tools(self, tools: List[Dict]) -> str:
        """Format tools for prompt."""
        if not tools:
            return "No tools available."

        formatted = []
        for tool in tools:
            if "function" in tool:
                func = tool["function"]
                name = func.get("name", "unknown")
                desc = func.get("description", "No description")
                formatted.append(f"- {name}: {desc}")

        return "\n".join(formatted)

    def _format_trajectory(self, trajectory: Dict) -> str:
        """Format trajectory for prompt."""
        steps = trajectory.get("steps", [])
        if not steps:
            return "No steps recorded."

        formatted = []
        for i, step in enumerate(steps, 1):
            action = step.get("action", "Unknown action")
            observation = step.get("observation", "No observation")
            formatted.append(f"Step {i}:\n  Action: {action}\n  Observation: {observation}")

        return "\n\n".join(formatted)

    def _format_existing_tasks(self) -> str:
        """Format existing tasks for deduplication prompt."""
        if not self.existing_queries:
            return "No existing tasks."

        sample = list(self.existing_queries)[:10]
        return "\n".join(f"- {q}" for q in sample)

    def _parse_exploration(self, response: str) -> Dict:
        """Parse exploration response into trajectory format."""
        trajectory = {"steps": [], "raw_response": response}

        try:
            exploration_match = re.search(
                r"<exploration>(.*?)</exploration>",
                response,
                re.DOTALL
            )

            if exploration_match:
                exploration_content = exploration_match.group(1)
                step_matches = re.findall(
                    r"<step>(.*?)</step>",
                    exploration_content,
                    re.DOTALL
                )

                for step_content in step_matches:
                    action_match = re.search(
                        r"<action>(.*?)</action>",
                        step_content,
                        re.DOTALL
                    )
                    observation_match = re.search(
                        r"<observation>(.*?)</observation>",
                        step_content,
                        re.DOTALL
                    )

                    step = {
                        "action": action_match.group(1).strip() if action_match else "",
                        "observation": observation_match.group(1).strip() if observation_match else ""
                    }
                    trajectory["steps"].append(step)

        except Exception as e:
            logger.debug(f"Error parsing exploration: {e}")

        return trajectory

    def _parse_tasks(self, response: str) -> List[Dict]:
        """Parse task objectives from response."""
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
                            metadata={"source": "experience_guided_exploration"}
                        )
                        objectives.append(objective.to_dict())

        except Exception as e:
            logger.debug(f"Error parsing tasks: {e}")

        return objectives

    def _deduplicate_objectives(self, objectives: List[Dict]) -> List[Dict]:
        """Remove objectives with queries similar to existing ones."""
        unique = []
        for obj in objectives:
            query = obj.get("query", "").lower().strip()
            if query and query not in self.existing_queries:
                unique.append(obj)
        return unique
