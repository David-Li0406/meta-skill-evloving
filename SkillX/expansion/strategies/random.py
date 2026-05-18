"""Random sampling exploration strategy.

Based on AgentEvolver's LlmRandomSamplingExploreStrategy.
"""

import re
import uuid
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base import ExplorationStrategy, TaskObjective

logger = logging.getLogger(__name__)

# Prompts for exploration and summarization
EXPLORE_SYSTEM_PROMPT = """You are an AI assistant exploring an environment to discover useful API combinations.

Given a seed task and available tools, generate a realistic exploration trajectory by:
1. Identifying relevant APIs for the task
2. Simulating a sequence of API calls
3. Recording the expected responses

Your exploration should discover new, useful API combinations that could solve real user tasks."""

EXPLORE_USER_PROMPT = """## Seed Task
{seed_task}

## Available Tools
{available_tools}

## Instructions
Generate an exploration trajectory that:
1. Uses 3-5 API calls
2. Discovers meaningful API combinations
3. Could lead to useful new tasks

Output your exploration as a series of steps:
<exploration>
<step>
<action>API call with parameters</action>
<observation>Expected response</observation>
</step>
...
</exploration>
"""

SUMMARIZE_SYSTEM_PROMPT = """You are an AI assistant that generates task descriptions from exploration trajectories.

Given an exploration trajectory showing API interactions, generate new task descriptions that:
1. Could be solved using the discovered API combinations
2. Are realistic user requests
3. Are different from the seed task

For each task, also provide:
- A confidence score (0.0-1.0) based on how well-defined the task is
- An action sequence showing how to solve it"""

SUMMARIZE_USER_PROMPT = """## Seed Task
{seed_task}

## Exploration Trajectory
{trajectory}

## Instructions
Generate 1-3 new task descriptions based on this exploration.

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


class RandomExplorationStrategy(ExplorationStrategy):
    """
    Random sampling exploration strategy.

    This strategy:
    1. Explore: Uses LLM to simulate random exploration of available APIs
    2. Summarize: Uses LLM to generate task descriptions from trajectories

    Suitable when:
    - No real environment is available
    - Want to generate diverse training tasks
    - Bootstrapping a skill library
    """

    def __init__(
        self,
        llm,
        env_client: Optional[Any] = None,
        max_steps: int = 5,
        max_tasks_per_trajectory: int = 3,
        available_tools: Optional[List[Dict]] = None,
        verbose: bool = True
    ):
        """
        Initialize random exploration strategy.

        Args:
            llm: LLM instance for exploration and summarization
            env_client: Optional environment client (not required for LLM-based exploration)
            max_steps: Maximum exploration steps per trajectory
            max_tasks_per_trajectory: Maximum tasks to generate per trajectory
            available_tools: List of available tool schemas
            verbose: Whether to output verbose logs
        """
        super().__init__(llm, env_client, verbose)
        self.max_steps = max_steps
        self.max_tasks_per_trajectory = max_tasks_per_trajectory
        self.available_tools = available_tools or []

    def set_available_tools(self, tools: List[Dict]) -> None:
        """Set available tools for exploration."""
        self.available_tools = tools

    async def explore(
        self,
        seed_task: Dict,
        **kwargs
    ) -> List[Dict]:
        """
        Explore using LLM-simulated API interactions.

        Args:
            seed_task: Seed task containing task_id and user_task

        Returns:
            List of trajectory dictionaries
        """
        task_id = seed_task.get("task_id", str(uuid.uuid4())[:8])
        user_task = seed_task.get("user_task", "")

        # Format available tools
        tools_str = self._format_tools(self.available_tools) if self.available_tools else "No specific tools provided."

        # Build exploration prompt
        user_prompt = EXPLORE_USER_PROMPT.format(
            seed_task=user_task,
            available_tools=tools_str
        )

        try:
            if hasattr(self.llm, 'chat'):
                response = await self.llm.chat([
                    {"role": "system", "content": EXPLORE_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ])
            else:
                response = await self.llm.ainvoke(messages=[
                    ("system", EXPLORE_SYSTEM_PROMPT),
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

            if self.verbose:
                logger.info(f"Generated exploration trajectory with {len(trajectory.get('steps', []))} steps")

            return [trajectory]

        except Exception as e:
            logger.error(f"Exploration failed: {e}")
            return []

    async def summarize(
        self,
        seed_task: Dict,
        trajectory: Dict
    ) -> List[Dict]:
        """
        Summarize exploration to generate task objectives.

        Args:
            seed_task: Original seed task
            trajectory: Exploration trajectory

        Returns:
            List of task objective dictionaries
        """
        user_task = seed_task.get("user_task", "")

        # Format trajectory
        trajectory_str = self._format_trajectory(trajectory)

        # Build summarization prompt
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
                    ("system", SUMMARIZE_SYSTEM_PROMPT),
                    ("user", user_prompt)
                ])

            if isinstance(response, dict):
                response_content = response.get("content", "")
            else:
                response_content = str(response)

            # Parse task objectives
            objectives = self._parse_tasks(response_content)

            # Limit number of tasks
            objectives = objectives[:self.max_tasks_per_trajectory]

            if self.verbose:
                logger.info(f"Generated {len(objectives)} task objectives from trajectory")

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

    def _parse_exploration(self, response: str) -> Dict:
        """Parse exploration response into trajectory format."""
        trajectory = {
            "steps": [],
            "raw_response": response
        }

        try:
            # Find exploration block
            exploration_match = re.search(
                r"<exploration>(.*?)</exploration>",
                response,
                re.DOTALL
            )

            if exploration_match:
                exploration_content = exploration_match.group(1)

                # Find all steps
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
            # Find tasks block
            tasks_match = re.search(
                r"<tasks>(.*?)</tasks>",
                response,
                re.DOTALL
            )

            if tasks_match:
                tasks_content = tasks_match.group(1)

                # Find all tasks
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
                            metadata={"source": "random_exploration"}
                        )
                        objectives.append(objective.to_dict())

        except Exception as e:
            logger.debug(f"Error parsing tasks: {e}")

        return objectives
