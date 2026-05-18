"""AppWorld agent implementation with skill support."""

from typing import Dict, Optional, List, Set
from ..base import BaseAgent
from ..skill_usage import SkillUsageService


class AppWorldAgent(BaseAgent):
    """
    Agent for AppWorld benchmark with skill-enhanced inference.

    Supports modes:
    - vanilla: No skill assistance
    - plan_only: Use plan retrieval and rewriting
    - skill_only: Use skill retrieval only
    - plan_with_skill: Both plans and skills (default)
    """

    HUMAN_SKILLS = [
        {
            "name": "Get the list of available apps",
            "document": """Use this at the start of a new task to review all available apps.

Parameters
----------
None

Outputs
-------
List of available apps with descriptions.

Notes
-----
1. Call this to discover apps that might help with the task.""",
            "content": "apis.api_docs.show_app_descriptions()",
            "tools": ["apis.api_docs.show_app_descriptions"]
        },
        {
            "name": "List all APIs in an app",
            "document": """Use this to explore APIs under a specific app.

Parameters
----------
app_name: str - The name of the app to inspect.

Outputs
-------
List of APIs available within the app.

Notes
-----
1. Use when you need to discover what APIs are available.
2. Do not invent APIs - always call this first.""",
            "content": "apis.api_docs.show_api_descriptions(app_name=app_name)",
            "tools": ["apis.api_docs.show_api_descriptions"]
        },
        {
            "name": "Get detailed API documentation",
            "document": """Get full documentation for a specific API.

Parameters
----------
app_name: str - The app that the API belongs to.
api_name: str - The name of the API to inspect.

Outputs
-------
Detailed API documentation with parameters and return fields.

Notes
-----
1. Use when an API seems relevant and you need exact specs.
2. Do not invent parameters - always verify here first.""",
            "content": "apis.api_docs.show_api_doc(app_name=app_name, api_name=api_name)",
            "tools": ["apis.api_docs.show_api_doc"]
        },
        {
            "name": "Complete the task",
            "document": """Call this when you have fully completed the user's request.

Parameters
----------
answer: Optional - The final result to return (string or number).

Outputs
-------
None

Notes
-----
1. If the task requires returning info, provide it via `answer`.
2. Many tasks don't need a return value - just call with no args.""",
            "content": """# If you need to return information:
apis.supervisor.complete_task(answer=<answer>)

# If no answer is required:
apis.supervisor.complete_task()""",
            "tools": ["apis.supervisor.complete_task"]
        }
    ]

    def __init__(
        self,
        llm,
        skill_service: Optional[SkillUsageService] = None,
        mode: str = "plan_with_skill"
    ):
        """
        Initialize AppWorld agent.

        Args:
            llm: LLM instance
            skill_service: SkillUsageService for skill retrieval
            mode: Agent mode
        """
        super().__init__(
            llm=llm,
            skill_retriever=None,
            benchmark="appworld",
            mode=mode
        )
        self.skill_service = skill_service
        self._task = None
        self._system_prompt = None
        self._metadata = {}

    async def prepare(
        self,
        task: str,
        app_descriptions: str,
        supervisor: str,
        datetime_str: str
    ) -> Dict:
        """
        Prepare agent for a task.

        Args:
            task: Task description
            app_descriptions: Available app descriptions
            supervisor: Supervisor info
            datetime_str: Current datetime

        Returns:
            Dict with system_prompt and metadata
        """
        self._task = task

        base_prompt = f"""Available Apps:
{app_descriptions}

Current DateTime: {datetime_str}
Supervisor Info: {supervisor}"""

        if self.skill_service and self.mode != "vanilla":
            result = await self.skill_service.prepare_prompt(
                task=task,
                base_prompt=base_prompt,
                max_skills=10,
                rewrite_plan=True
            )

            if result["metadata"].get("selected_skills"):
                result["metadata"]["selected_skills"].extend(self.HUMAN_SKILLS)

            self._system_prompt = result["system_prompt"]
            self._metadata = result["metadata"]
        else:
            self._system_prompt = base_prompt
            self._metadata = {"mode": "vanilla"}

        return {
            "system_prompt": self._system_prompt,
            "metadata": self._metadata
        }

    async def step(self, observation: str) -> str:
        """Execute one agent step."""
        raise NotImplementedError("Use run() for full execution")

    async def run(self, task: str) -> Dict:
        """Run agent on a task."""
        raise NotImplementedError("AppWorld execution requires environment integration")
