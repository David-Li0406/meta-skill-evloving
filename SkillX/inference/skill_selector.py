"""Skill selector using LLM for relevance filtering."""

import logging
import re
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)

SELECT_SKILL_PROMPT = """Given a user task and a reference plan, select the most relevant skills from the skill library.

# User Task
{user_task}

# Reference Plan
{plan}

# Skill Library
{skill_library}

Select the skills that are most relevant to completing the task according to the plan.
Return the selected skill names as a Python list.

```python
["skill_name_1", "skill_name_2", ...]
```"""


class SkillSelector:
    """
    LLM-based skill selector for plan-guided skill selection.

    Filters retrieved skills based on relevance to task and plan.
    """

    def __init__(self, llm, max_retries: int = 3):
        """
        Initialize skill selector.

        Args:
            llm: LLM instance with generate method
            max_retries: Maximum retries for LLM calls
        """
        self.llm = llm
        self.max_retries = max_retries

    async def select(
        self,
        user_task: str,
        plan: str,
        skill_library: List[Dict],
        max_skills: int = 10
    ) -> List[Dict]:
        """
        Select relevant skills for a task.

        Args:
            user_task: Task description
            plan: Reference plan
            skill_library: List of candidate skills
            max_skills: Maximum skills to return

        Returns:
            List of selected skills
        """
        if not skill_library:
            return []

        if len(skill_library) <= max_skills:
            return skill_library

        skill_desc = self._format_skill_descriptions(skill_library)

        prompt = SELECT_SKILL_PROMPT.format(
            user_task=user_task,
            plan=plan,
            skill_library=skill_desc
        )

        for retry in range(self.max_retries):
            try:
                response = await self.llm.generate(prompt)
                selected_names = self._extract_skill_names(response)

                if selected_names:
                    selected_skills = [
                        s for s in skill_library if s["name"] in selected_names
                    ][:max_skills]
                    return selected_skills

            except Exception as e:
                logger.warning(f"Skill selection retry {retry + 1}: {e}")

        return skill_library[:max_skills]

    def _format_skill_descriptions(self, skills: List[Dict]) -> str:
        """Format skills for prompt."""
        lines = []
        for skill in skills:
            lines.append({
                "skill_name": skill["name"],
                "skill_description": skill.get("document", "")[:200]
            })
        return str(lines)

    def _extract_skill_names(self, response: str) -> List[str]:
        """Extract skill names from LLM response."""
        match = re.search(r"```python\s*(.*?)\s*```", response, re.DOTALL)
        if match:
            try:
                names = eval(match.group(1).strip())
                if isinstance(names, list):
                    return names
            except Exception:
                pass

        match = re.search(r"\[(.*?)\]", response, re.DOTALL)
        if match:
            try:
                names = eval(f"[{match.group(1)}]")
                if isinstance(names, list):
                    return names
            except Exception:
                pass

        return []
