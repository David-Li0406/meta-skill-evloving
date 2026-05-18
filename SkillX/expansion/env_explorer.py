"""Environment exploration interface for skill expansion.

Provides abstract interface for real environment interaction,
separate from LLM-simulated exploration.
"""

import json
import uuid
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class EnvironmentExplorer(ABC):
    """Abstract interface for environment exploration."""

    @abstractmethod
    async def create_instance(self, task_id: str) -> Dict:
        """Create environment instance for task.

        Returns:
            Dict with 'instance_id' and 'initial_state'
        """
        pass

    @abstractmethod
    async def step(self, instance_id: str, action: Dict) -> Dict:
        """Execute action in environment.

        Args:
            instance_id: Environment instance ID
            action: Action to execute (typically messages)

        Returns:
            Dict with 'state', 'done', 'reward' (optional)
        """
        pass

    @abstractmethod
    async def release(self, instance_id: str) -> None:
        """Release environment instance."""
        pass

    @abstractmethod
    async def explore_task(
        self,
        task_id: str,
        system_prompt: str,
        max_steps: int = 10,
        **kwargs
    ) -> Dict:
        """Run full exploration on a task.

        Args:
            task_id: Task to explore
            system_prompt: System prompt for LLM agent
            max_steps: Maximum interaction steps

        Returns:
            Trajectory dictionary
        """
        pass


class RealEnvironmentExplorer(EnvironmentExplorer):
    """
    Explores real environment via EnvClient.

    Uses LLM to drive agent interactions in actual environment,
    collecting real trajectories for skill expansion.
    """

    def __init__(
        self,
        env_client,
        llm,
        env_type: str,
        tools: Optional[List[Dict]] = None,
        timeout: float = 180.0,
        verbose: bool = True
    ):
        """
        Initialize real environment explorer.

        Args:
            env_client: EnvClient instance for environment interaction
            llm: LLM instance for agent decisions
            env_type: Environment type (appworld, bfcl, tau2bench)
            tools: Available tool schemas for the environment
            timeout: Request timeout in seconds
            verbose: Whether to log verbose output
        """
        self.env_client = env_client
        self.llm = llm
        self.env_type = env_type
        self.tools = tools or []
        self.timeout = timeout
        self.verbose = verbose

    async def create_instance(self, task_id: str) -> Dict:
        """Create environment instance."""
        try:
            response = self.env_client.create(self.env_type, task_id)
            instance_id = response.get("info", {}).get("instance_id", "")
            initial_state = response.get("state", [])

            return {
                "instance_id": instance_id,
                "initial_state": initial_state,
                "task_id": task_id
            }
        except Exception as e:
            logger.error(f"Failed to create instance for task {task_id}: {e}")
            raise

    async def step(self, instance_id: str, action: Dict) -> Dict:
        """Execute step in environment."""
        try:
            response = self.env_client.step(instance_id, action)
            return {
                "state": response.get("state", []),
                "done": response.get("done", False),
                "reward": response.get("reward", None)
            }
        except Exception as e:
            logger.error(f"Step failed for instance {instance_id}: {e}")
            raise

    async def release(self, instance_id: str) -> None:
        """Release environment instance."""
        try:
            self.env_client.release(instance_id)
        except Exception as e:
            logger.warning(f"Failed to release instance {instance_id}: {e}")

    async def explore_task(
        self,
        task_id: str,
        system_prompt: str,
        max_steps: int = 10,
        **kwargs
    ) -> Dict:
        """
        Run exploration in real environment.

        Flow:
        1. Create environment instance
        2. Get initial state (usually user message)
        3. Loop: LLM generates action -> step in env -> observe
        4. Return collected trajectory
        """
        trajectory = {
            "trajectory_id": f"real_explore_{uuid.uuid4().hex[:8]}",
            "task_id": task_id,
            "env_type": self.env_type,
            "timestamp": datetime.now().isoformat(),
            "steps": [],
            "task_history": [],
            "done": False,
            "reward": None
        }

        instance_id = None

        try:
            # Step 1: Create instance
            instance = await self.create_instance(task_id)
            instance_id = instance["instance_id"]
            initial_state = instance["initial_state"]

            if self.verbose:
                logger.info(f"Created instance {instance_id} for task {task_id}")

            # Initialize conversation with system prompt
            messages = [{"role": "system", "content": system_prompt}]

            # Add initial state (user message)
            for msg in initial_state:
                messages.append(msg)
                trajectory["task_history"].append(msg)

            # Step 2: Exploration loop
            for step_num in range(max_steps):
                # Get LLM response
                llm_response = await self._get_llm_action(messages)

                if llm_response is None:
                    logger.warning(f"LLM returned no response at step {step_num}")
                    break

                # Add assistant message to history
                assistant_msg = {
                    "role": "assistant",
                    "content": llm_response.get("content", ""),
                }
                if llm_response.get("tool_calls"):
                    assistant_msg["tool_calls"] = llm_response["tool_calls"]

                messages.append(assistant_msg)
                trajectory["task_history"].append(assistant_msg)

                # Record step
                trajectory["steps"].append({
                    "step": step_num,
                    "action": assistant_msg,
                    "observation": None  # Will be filled by env response
                })

                # Execute in environment
                step_result = await self.step(instance_id, messages[-1:])

                # Add environment response
                env_response = step_result.get("state", [])
                for resp in env_response:
                    messages.append(resp)
                    trajectory["task_history"].append(resp)

                # Update step observation
                if trajectory["steps"]:
                    trajectory["steps"][-1]["observation"] = env_response

                # Check if done
                if step_result.get("done", False):
                    trajectory["done"] = True
                    trajectory["reward"] = step_result.get("reward")
                    break

                if self.verbose:
                    logger.debug(f"Completed step {step_num + 1}/{max_steps}")

            # Get final evaluation if not done
            if not trajectory["done"]:
                try:
                    reward = self.env_client.evaluate(instance_id)
                    trajectory["reward"] = reward
                except Exception:
                    pass

            if self.verbose:
                logger.info(f"Exploration completed: {len(trajectory['steps'])} steps, "
                           f"reward={trajectory.get('reward')}")

        except Exception as e:
            logger.error(f"Exploration failed: {e}")
            trajectory["error"] = str(e)

        finally:
            if instance_id:
                await self.release(instance_id)

        return trajectory

    async def _get_llm_action(self, messages: List[Dict]) -> Optional[Dict]:
        """Get LLM action for current state."""
        try:
            # Use LLM's chat method
            if hasattr(self.llm, 'chat'):
                response = await self.llm.chat(messages, tools=self.tools)
            elif hasattr(self.llm, 'ainvoke'):
                response = await self.llm.ainvoke(messages=messages)
            else:
                logger.error("LLM has no supported method (chat/ainvoke)")
                return None

            # Parse response
            if isinstance(response, str):
                return {"content": response}
            elif isinstance(response, dict):
                return response
            else:
                return {"content": str(response)}

        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return None


class SimulatedEnvironmentExplorer(EnvironmentExplorer):
    """
    Simulated exploration using LLM to generate both actions and observations.

    Useful when real environment is not available.
    """

    def __init__(
        self,
        llm,
        env_type: str,
        tools: Optional[List[Dict]] = None,
        verbose: bool = True
    ):
        self.llm = llm
        self.env_type = env_type
        self.tools = tools or []
        self.verbose = verbose
        self._instances: Dict[str, Dict] = {}

    async def create_instance(self, task_id: str) -> Dict:
        """Create simulated instance."""
        instance_id = f"sim_{uuid.uuid4().hex[:8]}"
        self._instances[instance_id] = {
            "task_id": task_id,
            "history": []
        }
        return {
            "instance_id": instance_id,
            "initial_state": [],
            "task_id": task_id
        }

    async def step(self, instance_id: str, action: Dict) -> Dict:
        """Simulate environment step."""
        # In simulation, we just record the action
        if instance_id in self._instances:
            self._instances[instance_id]["history"].append(action)

        return {
            "state": [],
            "done": False,
            "reward": None
        }

    async def release(self, instance_id: str) -> None:
        """Release simulated instance."""
        self._instances.pop(instance_id, None)

    async def explore_task(
        self,
        task_id: str,
        system_prompt: str,
        max_steps: int = 10,
        **kwargs
    ) -> Dict:
        """Run simulated exploration."""
        trajectory = {
            "trajectory_id": f"sim_explore_{uuid.uuid4().hex[:8]}",
            "task_id": task_id,
            "env_type": self.env_type,
            "timestamp": datetime.now().isoformat(),
            "steps": [],
            "simulated": True
        }

        # Use LLM to generate exploration trajectory
        prompt = f"""You are exploring an environment to discover API usage patterns.

Environment: {self.env_type}
Task: {task_id}

{system_prompt}

Generate an exploration trajectory with {max_steps} steps.
For each step, output:
<step>
<action>API call or action</action>
<observation>Expected response</observation>
</step>
"""

        try:
            if hasattr(self.llm, 'chat'):
                response = await self.llm.chat([
                    {"role": "system", "content": "You are an environment simulator."},
                    {"role": "user", "content": prompt}
                ])
            else:
                response = await self.llm.ainvoke(messages=[
                    {"role": "system", "content": "You are an environment simulator."},
                    {"role": "user", "content": prompt}
                ])

            # Parse response
            import re
            if isinstance(response, dict):
                response = response.get("content", "")

            step_matches = re.findall(
                r"<step>(.*?)</step>",
                str(response),
                re.DOTALL
            )

            for i, step_content in enumerate(step_matches[:max_steps]):
                action_match = re.search(r"<action>(.*?)</action>", step_content, re.DOTALL)
                obs_match = re.search(r"<observation>(.*?)</observation>", step_content, re.DOTALL)

                trajectory["steps"].append({
                    "step": i,
                    "action": action_match.group(1).strip() if action_match else "",
                    "observation": obs_match.group(1).strip() if obs_match else ""
                })

            if self.verbose:
                logger.info(f"Simulated exploration: {len(trajectory['steps'])} steps")

        except Exception as e:
            logger.error(f"Simulated exploration failed: {e}")
            trajectory["error"] = str(e)

        return trajectory
