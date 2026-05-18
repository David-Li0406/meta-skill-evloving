"""Experience-guided exploration for skill expansion."""

import re
import logging
from typing import List, Dict, Any, Optional, Set

from .base import BaseExpansionStrategy

try:
    from ..prompts.expansion_prompts import (
        get_exploration_prompt,
        get_task_summarize_prompt,
    )
except ImportError:
    from prompts.expansion_prompts import (
        get_exploration_prompt,
        get_task_summarize_prompt,
    )

logger = logging.getLogger(__name__)


class ExperienceGuidedExplorer(BaseExpansionStrategy):
    """
    Experience-guided exploration strategy.

    Based on AgentEvolver's LlmRandomSamplingExploreStrategy.
    Uses past experience to guide exploration of new tasks.

    Key features:
    - Analyzes successful/failed trajectories to identify API patterns
    - Prioritizes unexplored and failed APIs
    - De-prioritizes already-successful APIs
    - Synthesizes new tasks from exploration trajectories
    """

    def __init__(
        self,
        llm,
        agent=None,
        skill_library=None,
        env_profile: Optional[Any] = None,
        max_explore_steps: int = 10,
        exploration_temperature: float = 1.0,
        verbose: bool = True,
    ):
        """
        Initialize explorer.

        Args:
            llm: LLM instance for task summarization
            agent: Agent for task execution (optional)
            skill_library: Existing skill library
            env_profile: Environment profile with description
            max_explore_steps: Maximum exploration steps per rollout
            exploration_temperature: LLM temperature for exploration
            verbose: Whether to output verbose logs
        """
        self.llm = llm
        self.agent = agent
        self.skill_library = skill_library
        self.env_profile = env_profile
        self.max_explore_steps = max_explore_steps
        self.exploration_temperature = exploration_temperature
        self.verbose = verbose

        # API whitelist - APIs to always allow (login, docs, etc.)
        self.api_whitelist = {"login", "apis.api_docs", "apis.supervisor", "show_account"}

    def _extract_tools_from_trajectory(self, trajectory: Dict) -> Set[str]:
        """Extract all tool names used in a trajectory."""
        tools = set()
        steps = trajectory.get("trajectory", trajectory.get("task_history", []))

        for step in steps:
            # Check for tool_calls in assistant messages
            if step.get("tool_calls"):
                for tc in step["tool_calls"]:
                    if isinstance(tc, dict) and "name" in tc:
                        tools.add(tc["name"])
                    elif isinstance(tc, dict) and "function" in tc:
                        tools.add(tc["function"].get("name", ""))

            # Check for tool responses
            if step.get("role") == "tool" and step.get("name"):
                tools.add(step["name"])

            # Check for Python-style API calls in content
            content = step.get("content", "")
            if content and "apis." in content:
                # Extract API calls like apis.spotify.get_playlists()
                api_matches = re.findall(r"(apis\.\w+\.\w+)", content)
                tools.update(api_matches)

        return tools

    async def analyze_experience(
        self,
        successful_trajs: List[Dict],
        failed_trajs: List[Dict]
    ) -> Dict[str, Set[str]]:
        """
        Analyze successful and failed trajectories.

        Logic (from AgentEvolver):
        1. Collect APIs used in successful trajectories
        2. Collect APIs used in failed trajectories
        3. If mixed success/failure for same task:
           - Find APIs only in successful but not in "hardest" failed
           - These are likely "missing" APIs that cause failures

        Args:
            successful_trajs: Trajectories with reward >= threshold
            failed_trajs: Trajectories with reward < threshold

        Returns:
            Dict with keys: successful_apis, failed_apis, unexplored_apis
        """
        successful_apis = set()
        failed_apis = set()

        # Collect APIs from successful trajectories
        for traj in successful_trajs:
            tools = self._extract_tools_from_trajectory(traj)
            successful_apis.update(tools)

        # Collect APIs from failed trajectories
        for traj in failed_trajs:
            tools = self._extract_tools_from_trajectory(traj)
            failed_apis.update(tools)

        # APIs only in failed trajectories need more exploration
        unexplored_apis = failed_apis - successful_apis

        # Group trajectories by task for detailed analysis
        task_groups = {}
        for traj in successful_trajs + failed_trajs:
            task = traj.get("user_task", traj.get("task_id", "unknown"))
            if task not in task_groups:
                task_groups[task] = {"successful": [], "failed": []}

            reward = traj.get("reward", 0)
            if reward >= 0.999:
                task_groups[task]["successful"].append(traj)
            else:
                task_groups[task]["failed"].append(traj)

        # Advanced analysis: find missing APIs that cause failures
        for task, groups in task_groups.items():
            if groups["successful"] and groups["failed"]:
                # Mixed results - analyze what's different
                success_apis = set()
                for t in groups["successful"]:
                    success_apis.update(self._extract_tools_from_trajectory(t))

                # Find the "hardest" failed trajectory (least APIs)
                hardest_failed_apis = None
                for t in groups["failed"]:
                    apis = self._extract_tools_from_trajectory(t)
                    if hardest_failed_apis is None or len(apis) < len(hardest_failed_apis):
                        hardest_failed_apis = apis

                # APIs in successful but not in hardest failed are "missing"
                if hardest_failed_apis is not None:
                    missing_for_task = success_apis - hardest_failed_apis
                    unexplored_apis.update(missing_for_task)

        if self.verbose:
            logger.info(f"Experience analysis: {len(successful_apis)} successful APIs, "
                        f"{len(failed_apis)} failed APIs, {len(unexplored_apis)} unexplored APIs")

        return {
            "successful_apis": successful_apis,
            "failed_apis": failed_apis,
            "unexplored_apis": unexplored_apis
        }

    def _filter_apis(self, apis: Set[str]) -> Set[str]:
        """Filter out whitelisted APIs."""
        filtered = set()
        for api in apis:
            if not any(w in api for w in self.api_whitelist):
                filtered.add(api)
        return filtered

    async def explore(
        self,
        skill_library: Any,
        env_worker: Any,
        experience: Dict[str, Set[str]]
    ) -> List[Dict]:
        """
        Explore environment guided by experience.

        Guidance strategy:
        1. Build checklist of APIs to explore (unexplored + failed)
        2. Sample some successful APIs to avoid (already covered)
        3. Run agent with exploration system prompt
        4. If agent tries to use already-explored API, prompt to try others

        Args:
            skill_library: Current skill library
            env_worker: Environment worker for rollout
            experience: API usage statistics

        Returns:
            List of exploration trajectories
        """
        if env_worker is None:
            logger.warning("No env_worker provided, skipping exploration")
            return []

        # Build exploration guidance
        apis_to_explore = experience["unexplored_apis"] | experience["failed_apis"]
        apis_to_avoid = experience["successful_apis"]

        # Also check skill library for covered tools
        if skill_library is not None:
            covered_tools = skill_library.get_all_tool_names()
            apis_to_avoid = apis_to_avoid | covered_tools

        # Filter out whitelisted APIs
        apis_to_explore = self._filter_apis(apis_to_explore)
        apis_to_avoid = self._filter_apis(apis_to_avoid)

        # Get environment description
        env_description = "No environment description provided."
        if self.env_profile is not None:
            if hasattr(self.env_profile, "get_instruction"):
                env_description = self.env_profile.get_instruction()
            elif hasattr(self.env_profile, "description"):
                env_description = self.env_profile.description

        # Get exploration system prompt
        system_prompt = get_exploration_prompt(
            environment_description=env_description,
            apis_to_explore=apis_to_explore,
            apis_to_avoid=apis_to_avoid
        )

        if self.verbose:
            logger.info(f"Starting exploration with {len(apis_to_explore)} APIs to explore, "
                        f"{len(apis_to_avoid)} APIs to avoid")

        # Run exploration using env_worker
        try:
            trajectory = await self._run_exploration(
                env_worker=env_worker,
                system_prompt=system_prompt,
                apis_to_avoid=apis_to_avoid
            )
            return [trajectory] if trajectory else []
        except Exception as e:
            logger.error(f"Exploration failed: {e}")
            return []

    async def _run_exploration(
        self,
        env_worker: Any,
        system_prompt: str,
        apis_to_avoid: Set[str]
    ) -> Optional[Dict]:
        """
        Run a single exploration rollout.

        Args:
            env_worker: Environment worker
            system_prompt: Exploration system prompt
            apis_to_avoid: APIs to discourage

        Returns:
            Exploration trajectory or None
        """
        # If env_worker has an execute method, use it
        if hasattr(env_worker, "execute"):
            trajectory = await env_worker.execute(
                system_prompt=system_prompt,
                max_steps=self.max_explore_steps,
                temperature=self.exploration_temperature,
                check_list=list(apis_to_avoid) if apis_to_avoid else None
            )
            return trajectory

        # Otherwise try to use it as an async function
        if callable(env_worker):
            trajectory = await env_worker(
                system_prompt=system_prompt,
                max_steps=self.max_explore_steps
            )
            return trajectory

        logger.warning("env_worker doesn't have expected interface")
        return None

    async def summarize(self, trajectories: List[Dict]) -> List[Dict]:
        """
        Generate task descriptions from exploration trajectories.

        Uses LLM to:
        1. Analyze API interaction sequence
        2. Identify realistic user tasks
        3. Output structured task format

        Args:
            trajectories: Exploration trajectories

        Returns:
            List of synthesized tasks
        """
        all_tasks = []

        for traj in trajectories:
            try:
                # Get prompts
                system_prompt, user_prompt = get_task_summarize_prompt(
                    trajectory=traj,
                    old_objectives=[t.get("query", "") for t in all_tasks],
                    task_preference="Please generate realistic, user-centered tasks."
                )

                # Call LLM
                response = await self.llm.chat([
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ])

                # Parse response
                if isinstance(response, dict):
                    response_content = response.get("content", "")
                else:
                    response_content = str(response)

                parsed_tasks = self._parse_tasks_from_response(response_content)
                all_tasks.extend(parsed_tasks)

                if self.verbose:
                    logger.info(f"Synthesized {len(parsed_tasks)} tasks from trajectory")

            except Exception as e:
                logger.error(f"Failed to summarize trajectory: {e}")
                continue

        return all_tasks

    def _parse_tasks_from_response(self, response: str) -> List[Dict]:
        """
        Parse task descriptions from LLM response.

        Args:
            response: LLM response text

        Returns:
            List of parsed tasks
        """
        tasks = []

        try:
            # Find all <task>...</task> blocks
            task_matches = re.findall(r"<task>(.*?)</task>", response, re.DOTALL)

            for task_content in task_matches:
                try:
                    # Parse individual fields
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

                        tasks.append({
                            "query": query,
                            "confidence": confidence,
                            "action_sequence": action_sequence,
                            "source": "exploration"
                        })

                except (ValueError, AttributeError) as e:
                    logger.debug(f"Failed to parse task block: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing tasks from response: {e}")

        return tasks
