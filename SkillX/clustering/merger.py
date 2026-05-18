"""LLM-based skill merging."""

import re
import json
import logging
from typing import List, Dict, Optional, Any

try:
    from ..prompts.registry import PromptRegistry
except ImportError:
    from prompts.registry import PromptRegistry

logger = logging.getLogger(__name__)


class SkillMerger:
    """
    Merge similar skills using LLM.

    Combines skills in the same cluster into a more comprehensive skill.
    """

    def __init__(
        self,
        llm,
        benchmark: str = "appworld",
        skill_type: str = "functional",
        tool_schemas: Optional[Dict[str, Any]] = None,
        max_group_size: int = 15,
        verbose: bool = True
    ):
        """
        Initialize skill merger.

        Args:
            llm: LLM instance
            benchmark: Benchmark name
            skill_type: Type of skills (functional or atomic)
            tool_schemas: Tool schemas for atomic merging
            max_group_size: Maximum skills to merge at once
            verbose: Whether to output verbose logs
        """
        self.llm = llm
        self.benchmark = benchmark
        self.skill_type = skill_type
        self.tool_schemas = tool_schemas or {}
        self.max_group_size = max_group_size
        self.verbose = verbose

    def _extract_skill(self, text: str) -> Optional[Dict]:
        """Extract merged skill from LLM response."""
        match = re.search(r"<skill>(.*?)</skill>", text, flags=re.S)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except json.JSONDecodeError:
                # Try eval for list format
                try:
                    result = eval(match.group(1).strip())
                    if isinstance(result, list) and result:
                        return result[0] if len(result) == 1 else result
                    return result
                except:
                    pass
        return None

    def get_prompt(self) -> str:
        """Get merge prompt based on skill type."""
        return PromptRegistry.get("skill_merge", self.skill_type)

    async def merge(
        self,
        skills: List[Dict],
        **kwargs
    ) -> Optional[Dict]:
        """
        Merge a group of similar skills.

        Args:
            skills: List of skill dictionaries to merge

        Returns:
            Merged skill dictionary
        """
        if len(skills) == 1:
            return skills[0]

        # Truncate if too many
        if len(skills) > self.max_group_size:
            import random
            skills = random.sample(skills, self.max_group_size)

        # Format skills for prompt
        skill_list = [
            json.dumps(s.get("skill", s), ensure_ascii=False, indent=2)
            for s in skills
        ]

        # Get tool schema if atomic
        tool_schema = None
        if self.skill_type == "atomic" and skills:
            tool_name = skills[0].get("skill", skills[0]).get("name")
            tool_schema = self.tool_schemas.get(tool_name)

        # Build message
        if tool_schema:
            content = (
                f"# Skill List:\n{skill_list}\n"
                f"# The Tool Schema:\n{json.dumps(tool_schema, indent=2)}"
            )
        else:
            content = f"# Skill List:\n{skill_list}"

        messages = [
            ("system", self.get_prompt()),
            ("human", content)
        ]

        if self.verbose:
            logger.info(f"Merging {len(skills)} skills...")

        try:
            response = await self.llm.ainvoke(
                messages=messages,
                regex_extractor=self._extract_skill,
                **kwargs
            )

            merged = self._extract_skill(response)

            if merged:
                if self.verbose:
                    logger.info("Merge successful")
                return {
                    "skill": merged,  # Use "skill" for consistency with pipeline expectations
                    "source": skills,
                    "merged_from_count": len(skills)
                }

        except Exception as e:
            logger.error(f"Error merging skills: {e}")

        return None

    async def merge_clusters(
        self,
        clusters: List[List[Dict]],
        **kwargs
    ) -> List[Dict]:
        """
        Merge all skill clusters.

        Args:
            clusters: List of skill clusters

        Returns:
            List of merged skills
        """
        import asyncio

        results = []
        tasks = [self.merge(cluster, **kwargs) for cluster in clusters]
        merge_results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in merge_results:
            if isinstance(result, Exception):
                logger.error(f"Merge error: {result}")
            elif result:
                results.append(result)

        logger.info(f"Merged {len(clusters)} clusters into {len(results)} skills")
        return results
