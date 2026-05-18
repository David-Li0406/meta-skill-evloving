"""BFCL agent implementation with skill support."""

from typing import Dict, Optional, List, Set
from ..base import BaseAgent
from ..skill_usage import SkillUsageService


class BFCLAgent(BaseAgent):
    """
    Agent for BFCL benchmark with skill-enhanced inference.

    Key differences from other benchmarks:
    - Tools are provided per task
    - Skills are filtered by available tools
    - Uses function calling format
    """

    def __init__(
        self,
        llm,
        skill_service: Optional[SkillUsageService] = None,
        mode: str = "plan_with_skill"
    ):
        """
        Initialize BFCL agent.

        Args:
            llm: LLM instance
            skill_service: SkillUsageService for skill retrieval
            mode: Agent mode
        """
        super().__init__(
            llm=llm,
            skill_retriever=None,
            benchmark="bfcl",
            mode=mode
        )
        self.skill_service = skill_service
        self._tools = None
        self._tool_names = set()
        self._system_prompt = None
        self._metadata = {}

    def set_tools(self, tools: List[Dict]) -> None:
        """
        Set available tools for this task.

        Args:
            tools: List of tool schemas in OpenAPI format
        """
        self._tools = tools
        self._tool_names = set()

        for tool in tools:
            if "function" in tool:
                self._tool_names.add(tool["function"]["name"])
            elif "name" in tool:
                self._tool_names.add(tool["name"])

        if self.skill_service:
            self.skill_service.set_available_tools(self._tool_names)

    async def prepare(self, query: str) -> Dict:
        """
        Prepare agent for a query.

        Args:
            query: User query

        Returns:
            Dict with system_prompt and metadata
        """
        if self.skill_service and self.mode != "vanilla":
            result = await self.skill_service.prepare_prompt(
                task=query,
                base_prompt="",
                max_skills=10,
                rewrite_plan=True
            )

            self._system_prompt = result["system_prompt"]
            self._metadata = result["metadata"]
        else:
            self._system_prompt = "You are a helpful assistant."
            self._metadata = {"mode": "vanilla"}

        return {
            "system_prompt": self._system_prompt,
            "tools": self._tools,
            "metadata": self._metadata
        }

    async def step(self, observation: str) -> str:
        """Execute one agent step."""
        raise NotImplementedError("Use run() for full execution")

    async def run(self, task: str) -> Dict:
        """Run agent on a task."""
        raise NotImplementedError("BFCL execution requires environment integration")
