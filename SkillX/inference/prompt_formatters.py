"""Prompt formatters for skill-enhanced inference."""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


class BasePromptFormatter(ABC):
    """Base class for prompt formatting."""

    @abstractmethod
    def format_skill_library(self, skills: List[Dict]) -> str:
        """Format skills for prompt injection."""
        pass

    @abstractmethod
    def format_system_prompt(
        self,
        base_prompt: str,
        skill_library: str,
        plan: Optional[str] = None
    ) -> str:
        """Format complete system prompt."""
        pass


class AppWorldPromptFormatter(BasePromptFormatter):
    """Prompt formatter for AppWorld benchmark."""

    SYSTEM_TEMPLATE = """You are a helpful AI assistant that can interact with apps to complete tasks.

{base_prompt}

{skill_section}

{plan_section}

Important Notes:
1. The Skill Library provides reference implementations, not callable functions.
2. Always verify API documentation before using skills.
3. Use `apis.api_docs.show_api_doc(app_name, api_name)` to check exact API specs.
"""

    SKILL_SECTION = """# Skill Library
The following skills provide guidance on how to accomplish common tasks:

{skill_library}

Note: Skills are for reference only. Use the actual APIs for implementation."""

    def format_skill_library(self, skills: List[Dict]) -> str:
        """Format skills for AppWorld prompt."""
        if not skills:
            return ""

        lines = []
        for idx, skill in enumerate(skills, 1):
            lines.append(f"# Skill {idx}: {skill['name']}")
            lines.append(f"\nDescription:\n{skill.get('document', '')}")
            lines.append(f"\nContent:\n{skill.get('content', '')}")
            lines.append("")

        return "\n".join(lines)

    def format_system_prompt(
        self,
        base_prompt: str,
        skill_library: str,
        plan: Optional[str] = None
    ) -> str:
        """Format AppWorld system prompt."""
        skill_section = ""
        if skill_library:
            skill_section = self.SKILL_SECTION.format(skill_library=skill_library)

        plan_section = ""
        if plan:
            plan_section = f"# Reference Plan\n{plan}\n\nNote: Adapt the plan to the specific task."

        return self.SYSTEM_TEMPLATE.format(
            base_prompt=base_prompt,
            skill_section=skill_section,
            plan_section=plan_section
        )


class BFCLPromptFormatter(BasePromptFormatter):
    """Prompt formatter for BFCL benchmark."""

    SYSTEM_TEMPLATE = """You are a helpful assistant. You are provided with a set of tools to help users complete tasks.

Additionally, a skill library (if available) will be provided for your reference. While solving the tasks, you may use the provided functions from the skill library.
{skill_library}

Please note that the skill library is for reference only; for actual usage, follow the specifications of the provided tools."""

    def format_skill_library(self, skills: List[Dict]) -> str:
        """Format skills for BFCL prompt."""
        if not skills:
            return ""

        lines = []
        for idx, skill in enumerate(skills, 1):
            lines.append(f"# Skill {idx}:")
            lines.append(f"Description:\n{skill.get('document', '')}")
            lines.append(f"\nContent:\n{skill.get('content', '')}")
            lines.append("")

        return "\n".join(lines)

    def format_system_prompt(
        self,
        base_prompt: str,
        skill_library: str,
        plan: Optional[str] = None
    ) -> str:
        """Format BFCL system prompt."""
        return self.SYSTEM_TEMPLATE.format(skill_library=skill_library)


class Tau2BenchPromptFormatter(BasePromptFormatter):
    """Prompt formatter for τ²-Bench benchmark."""

    SYSTEM_TEMPLATE = """<instructions>
{agent_instruction}
</instructions>
<policy>
{domain_policy}
</policy>
{skill_section}"""

    AGENT_INSTRUCTION = """You are a customer service agent that helps the user according to the <policy> provided below.
In each turn you can either:
- Send a message to the user.
- Make a tool call.
You cannot do both at the same time.

Try to be helpful and always follow the policy. Always make sure you generate valid JSON only.

{skill_note}"""

    SKILL_SECTION = """<skill_library>
The following skills provide guidance on using tools effectively:

{skill_library}

Note: Skills describe how to use tools. Follow the tool specifications for actual calls.
</skill_library>"""

    def format_skill_library(self, skills: List[Dict]) -> str:
        """Format skills for τ²-Bench prompt."""
        if not skills:
            return ""

        lines = []
        for skill in skills:
            lines.append(f"## {skill['name']}")
            lines.append(f"{skill.get('document', '')}")
            if skill.get('content'):
                lines.append(f"\nExamples:\n{skill['content']}")
            lines.append("")

        return "\n".join(lines)

    def format_system_prompt(
        self,
        base_prompt: str,
        skill_library: str,
        plan: Optional[str] = None
    ) -> str:
        """Format τ²-Bench system prompt."""
        skill_note = ""
        skill_section = ""

        if skill_library:
            skill_note = "Before using tools, consult the skill library for best practices."
            skill_section = self.SKILL_SECTION.format(skill_library=skill_library)

        agent_instruction = self.AGENT_INSTRUCTION.format(skill_note=skill_note)

        return self.SYSTEM_TEMPLATE.format(
            agent_instruction=agent_instruction,
            domain_policy=base_prompt,
            skill_section=skill_section
        )


def get_formatter(benchmark: str) -> BasePromptFormatter:
    """Get formatter for a benchmark."""
    formatters = {
        "appworld": AppWorldPromptFormatter,
        "bfcl": BFCLPromptFormatter,
        "tau2bench": Tau2BenchPromptFormatter,
        "tau2-bench": Tau2BenchPromptFormatter,
    }

    formatter_cls = formatters.get(benchmark.lower())
    if formatter_cls is None:
        raise ValueError(f"Unknown benchmark: {benchmark}")

    return formatter_cls()
