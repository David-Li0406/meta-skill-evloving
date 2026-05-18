"""τ²-Bench agent implementation with skill support."""

from typing import Dict, Optional, List, Set
from ..base import BaseAgent
from ..skill_usage import SkillUsageService


class Tau2BenchAgent(BaseAgent):
    """
    Agent for τ²-Bench benchmark with skill-enhanced inference.

    Key differences from other benchmarks:
    - Domain-specific policies (airline, retail, telecom)
    - Skills are atomic (tool-centric)
    - User simulation is part of the task
    """

    DOMAINS = ["airline", "retail", "telecom"]

    def __init__(
        self,
        llm,
        skill_service: Optional[SkillUsageService] = None,
        domain: str = "airline",
        mode: str = "skill_only"
    ):
        """
        Initialize τ²-Bench agent.

        Args:
            llm: LLM instance
            skill_service: SkillUsageService for skill retrieval
            domain: Domain name (airline, retail, telecom)
            mode: Agent mode (typically skill_only for tau2bench)
        """
        super().__init__(
            llm=llm,
            skill_retriever=None,
            benchmark="tau2bench",
            mode=mode
        )
        self.skill_service = skill_service
        self.domain = domain
        self._tools = None
        self._policy = None
        self._system_prompt = None
        self._metadata = {}

    def set_domain_context(
        self,
        tools: List[Dict],
        policy: str
    ) -> None:
        """
        Set domain-specific context.

        Args:
            tools: List of tool schemas for this domain
            policy: Domain policy text
        """
        self._tools = tools
        self._policy = policy

        tool_names = set()
        for tool in tools:
            if "function" in tool:
                tool_names.add(tool["function"]["name"])
            elif "name" in tool:
                tool_names.add(tool["name"])

        if self.skill_service:
            self.skill_service.set_available_tools(tool_names)

    async def prepare(self, task: str = "") -> Dict:
        """
        Prepare agent for a task.

        For τ²-Bench, skills are injected into system prompt.
        Task is typically the user's first message.

        Args:
            task: Initial task/context (optional)

        Returns:
            Dict with system_prompt and metadata
        """
        if self.skill_service and self.mode != "vanilla":
            result = await self.skill_service.prepare_prompt(
                task=task or self.domain,
                base_prompt=self._policy or "",
                max_skills=10,
                rewrite_plan=False
            )

            self._system_prompt = result["system_prompt"]
            self._metadata = result["metadata"]
        else:
            self._system_prompt = f"""<instructions>
You are a customer service agent that helps the user according to the <policy> provided below.
In each turn you can either:
- Send a message to the user.
- Make a tool call.
You cannot do both at the same time.

Try to be helpful and always follow the policy. Always make sure you generate valid JSON only.
</instructions>
<policy>
{self._policy or ''}
</policy>"""
            self._metadata = {"mode": "vanilla", "domain": self.domain}

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
        raise NotImplementedError("τ²-Bench execution requires environment integration")
