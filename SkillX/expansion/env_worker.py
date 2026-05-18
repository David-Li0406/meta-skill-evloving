"""Environment worker interface for exploration."""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, Callable
import logging

logger = logging.getLogger(__name__)


class BaseEnvWorker(ABC):
    """
    Base environment worker interface for exploration rollouts.

    This interface defines how the exploration system interacts with
    different environments (AppWorld, BFCL, Tau2Bench, etc.).

    Based on AgentEvolver's EnvWorker pattern.
    """

    @abstractmethod
    async def execute(
        self,
        system_prompt: str,
        max_steps: int = 10,
        temperature: float = 1.0,
        check_list: Optional[List[str]] = None,
        **kwargs
    ) -> Dict:
        """
        Execute an exploration rollout.

        Args:
            system_prompt: System prompt guiding the exploration
            max_steps: Maximum number of interaction steps
            temperature: LLM sampling temperature
            check_list: List of APIs to avoid/discourage

        Returns:
            Trajectory dict with format:
            {
                "task_history": [...],  # List of messages
                "reward": float,         # Final reward
                "task_id": str,          # Task identifier
                "completed": bool        # Whether task completed
            }
        """
        pass

    @abstractmethod
    async def reset(self, task: Optional[Dict] = None) -> Dict:
        """
        Reset the environment.

        Args:
            task: Optional task to initialize with

        Returns:
            Initial observation
        """
        pass


class GenericEnvWorker(BaseEnvWorker):
    """
    Generic environment worker implementation.

    Can be configured with custom LLM and environment interfaces.
    """

    def __init__(
        self,
        llm_chat_fn: Callable,
        env_step_fn: Callable,
        env_reset_fn: Callable,
        tokenizer: Optional[Any] = None,
        max_model_len: int = 102400,
        verbose: bool = True
    ):
        """
        Initialize generic environment worker.

        Args:
            llm_chat_fn: Function to call LLM
                Signature: (messages: List[Dict], **kwargs) -> Dict
                Returns: {"role": "assistant", "content": str}
            env_step_fn: Function to execute action in environment
                Signature: (action: str) -> str
                Returns: Environment observation/feedback
            env_reset_fn: Function to reset environment
                Signature: (task: Optional[Dict]) -> Dict
                Returns: Initial observation
            tokenizer: Tokenizer for length checking (optional)
            max_model_len: Maximum context length
            verbose: Whether to log verbosely
        """
        self.llm_chat_fn = llm_chat_fn
        self.env_step_fn = env_step_fn
        self.env_reset_fn = env_reset_fn
        self.tokenizer = tokenizer
        self.max_model_len = max_model_len
        self.verbose = verbose

    async def reset(self, task: Optional[Dict] = None) -> Dict:
        """Reset the environment."""
        return self.env_reset_fn(task)

    async def execute(
        self,
        system_prompt: str,
        max_steps: int = 10,
        temperature: float = 1.0,
        check_list: Optional[List[str]] = None,
        **kwargs
    ) -> Dict:
        """Execute exploration rollout."""
        messages = [{"role": "system", "content": system_prompt}]
        task_history = list(messages)
        completed = False
        reward = 0.0

        for step in range(max_steps):
            try:
                response = self.llm_chat_fn(
                    messages=messages,
                    custom_sampling_params={"temperature": temperature}
                )

                if response is None or response.get("content", "") == "":
                    if self.verbose:
                        logger.warning(f"Empty LLM response at step {step}")
                    break

                assistant_content = response.get("content", "")
                messages.append({"role": "assistant", "content": assistant_content})
                task_history.append({"role": "assistant", "content": assistant_content})

                # Execute in environment
                observation = self.env_step_fn(assistant_content)

                messages.append({"role": "user", "content": f"Output:\n```\n{observation}```\n\n"})
                task_history.append({"role": "user", "content": f"Output:\n```\n{observation}```\n\n"})

                # Check for task completion signals
                if "complete_task" in assistant_content.lower():
                    completed = True
                    reward = 1.0
                    break

                if "marked the active task complete" in observation.lower():
                    completed = True
                    reward = 1.0
                    break

            except Exception as e:
                logger.error(f"Error at step {step}: {e}")
                break

        return {
            "task_history": task_history,
            "reward": reward,
            "completed": completed,
            "steps": step + 1
        }


class AppWorldEnvWorker(BaseEnvWorker):
    """
    AppWorld-specific environment worker.

    Wraps AppWorld environment for exploration.
    """

    def __init__(
        self,
        appworld_instance: Any,
        llm_chat_fn: Callable,
        verbose: bool = True
    ):
        """
        Initialize AppWorld worker.

        Args:
            appworld_instance: AppWorld environment instance
            llm_chat_fn: LLM chat function
            verbose: Whether to log verbosely
        """
        self.world = appworld_instance
        self.llm_chat_fn = llm_chat_fn
        self.verbose = verbose

    async def reset(self, task: Optional[Dict] = None) -> Dict:
        """Reset AppWorld environment."""
        if task and hasattr(self.world, "reset"):
            self.world.reset(task_id=task.get("task_id"))
        return {"task": getattr(self.world, "task", None)}

    async def execute(
        self,
        system_prompt: str,
        max_steps: int = 10,
        temperature: float = 1.0,
        check_list: Optional[List[str]] = None,
        **kwargs
    ) -> Dict:
        """Execute rollout in AppWorld."""
        import re

        messages = [{"role": "system", "content": system_prompt}]
        task_history = list(messages)

        for step in range(max_steps):
            try:
                response = self.llm_chat_fn(
                    messages=messages,
                    custom_sampling_params={"temperature": temperature}
                )

                if response is None:
                    break

                assistant_content = response.get("content", "")
                messages.append({"role": "assistant", "content": assistant_content})
                task_history.append({"role": "assistant", "content": assistant_content})

                # Extract code from response
                code = self._extract_code(assistant_content)

                # Execute in AppWorld
                output = self.world.execute(code)

                messages.append({"role": "user", "content": f"Output:\n```\n{output}```\n\n"})
                task_history.append({"role": "user", "content": f"Output:\n```\n{output}```\n\n"})

                # Check completion
                if self.world.task_completed():
                    break

            except Exception as e:
                logger.error(f"AppWorld execution error at step {step}: {e}")
                break

        # Get final reward
        reward = 0.0
        if hasattr(self.world, "evaluate"):
            try:
                tracker = self.world.evaluate()
                num_passes = len(tracker.passes)
                num_failures = len(tracker.failures)
                if num_passes + num_failures > 0:
                    reward = num_passes / (num_passes + num_failures)
            except Exception:
                pass

        return {
            "task_history": task_history,
            "reward": reward,
            "completed": self.world.task_completed() if hasattr(self.world, "task_completed") else False,
            "task_id": getattr(self.world.task, "id", "unknown") if hasattr(self.world, "task") else "unknown"
        }

    def _extract_code(self, text: str) -> str:
        """Extract Python code from markdown blocks."""
        import re
        match = re.search(r"```python\n(.*?)```", text, flags=re.DOTALL)
        if match:
            return match.group(1).strip()
        return text
