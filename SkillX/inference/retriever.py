"""Enhanced skill retrieval with embedding-based search."""

import re
import logging
from typing import List, Dict, Optional, Any
import numpy as np

from .base import BaseSkillRetriever
from .embedding_service import EmbeddingService

try:
    from ..core.skill import Skill, SkillLibrary, PlanSkill
    from ..prompts.registry import PromptRegistry
except ImportError:
    from core.skill import Skill, SkillLibrary, PlanSkill
    from prompts.registry import PromptRegistry

logger = logging.getLogger(__name__)


class SkillRetriever(BaseSkillRetriever):
    """
    Skill retrieval service with embedding-based search.

    Supports:
    - Plan retrieval by task similarity
    - Skill retrieval by query similarity
    - Tool-based skill filtering
    """

    def __init__(
        self,
        skill_library: Optional[SkillLibrary] = None,
        embedding_service: Optional[EmbeddingService] = None,
        similarity_threshold: float = 0.45
    ):
        """
        Initialize retriever.

        Args:
            skill_library: SkillLibrary instance
            embedding_service: EmbeddingService for similarity search
            similarity_threshold: Minimum similarity threshold
        """
        self.skill_library = skill_library
        self.embedding_service = embedding_service or EmbeddingService()
        self.similarity_threshold = similarity_threshold

        self._plan_embeddings: Optional[np.ndarray] = None
        self._plan_texts: List[str] = []
        self._plan_tasks: List[str] = []

        self._skill_embeddings: Optional[np.ndarray] = None
        self._skill_texts: List[str] = []
        self._skills: List[Skill] = []

        if skill_library:
            self._build_indices()

    def load_library(self, library: SkillLibrary) -> None:
        """Load skill library and build indices."""
        self.skill_library = library
        self._build_indices()
        logger.info(f"Loaded library: {len(self._plan_tasks)} plans, {len(self._skills)} skills")

    def _build_indices(self) -> None:
        """Build embedding indices for plans and skills."""
        if not self.skill_library:
            return

        self._plan_texts = []
        self._plan_tasks = []
        for task, plan_skill in self.skill_library.planning.items():
            self._plan_tasks.append(task)
            self._plan_texts.append(f"{task}\n{plan_skill.plan}")

        if self._plan_texts:
            self._plan_embeddings = self.embedding_service.encode(self._plan_texts)
            logger.info(f"Built plan index: {len(self._plan_texts)} plans")

        self._skills = self.skill_library.functional + self.skill_library.atomic
        self._skill_texts = [skill.get_embedding_text() for skill in self._skills]

        if self._skill_texts:
            self._skill_embeddings = self.embedding_service.encode(self._skill_texts)
            logger.info(f"Built skill index: {len(self._skill_texts)} skills")

    async def retrieve_plan(
        self,
        task: str,
        top_k: int = 3
    ) -> List[Dict]:
        """
        Retrieve relevant plans for a task.

        Args:
            task: Task description
            top_k: Number of plans to retrieve

        Returns:
            List of plan dicts with task, plan, and similarity
        """
        if not self._plan_texts:
            return []

        results = self.embedding_service.top_k(
            query=task,
            corpus=self._plan_texts,
            corpus_embeddings=self._plan_embeddings,
            k=top_k,
            threshold=self.similarity_threshold
        )

        plans = []
        for r in results:
            idx = r["index"]
            task_id = self._plan_tasks[idx]
            plan_skill = self.skill_library.planning[task_id]
            plans.append({
                "task": task_id,
                "plan": plan_skill.plan,
                "similarity": r["similarity"],
                "matched_query": task_id
            })

        return plans

    async def retrieve_skills(
        self,
        query: str,
        skill_type: str = "all",
        top_k: int = 5,
        tool_filter: Optional[set] = None
    ) -> List[Dict]:
        """
        Retrieve relevant skills.

        Args:
            query: Query text (task or plan step)
            skill_type: Type filter ("functional", "atomic", "all")
            top_k: Number of skills to retrieve
            tool_filter: Set of allowed tool names (optional)

        Returns:
            List of skill dicts with skill and similarity
        """
        if not self._skill_texts:
            return []

        filtered_indices = []
        filtered_texts = []
        filtered_skills = []

        for i, skill in enumerate(self._skills):
            if skill_type != "all" and skill.skill_type != skill_type:
                continue
            if tool_filter and not all(t in tool_filter for t in skill.tools):
                continue

            filtered_indices.append(i)
            filtered_texts.append(self._skill_texts[i])
            filtered_skills.append(skill)

        if not filtered_texts:
            return []

        filtered_embeddings = self._skill_embeddings[filtered_indices]

        results = self.embedding_service.top_k(
            query=query,
            corpus=filtered_texts,
            corpus_embeddings=filtered_embeddings,
            k=top_k,
            threshold=self.similarity_threshold
        )

        skills = []
        for r in results:
            idx = r["index"]
            skill = filtered_skills[idx]
            skills.append({
                "name": skill.name,
                "document": skill.document,
                "content": skill.content,
                "tools": skill.tools,
                "skill_type": skill.skill_type,
                "similarity": r["similarity"]
            })

        return skills

    async def retrieve_skills_for_plan(
        self,
        plan: str,
        skills_per_step: int = 4,
        tool_filter: Optional[set] = None
    ) -> List[Dict]:
        """
        Retrieve skills for each step in a plan.

        Args:
            plan: Plan text with step markers
            skills_per_step: Number of skills per step
            tool_filter: Set of allowed tool names

        Returns:
            Deduplicated list of skills relevant to the plan
        """
        steps = []
        for line in plan.split("\n"):
            line = line.strip()
            if line.startswith("#") or line.startswith("step"):
                steps.append(line)
            elif len(line) > 10:
                steps.append(line)

        if not steps:
            steps = [plan]

        seen_names = set()
        all_skills = []

        for step in steps:
            if len(step) < 5:
                continue

            skills = await self.retrieve_skills(
                query=step,
                skill_type="all",
                top_k=skills_per_step,
                tool_filter=tool_filter
            )

            for skill in skills:
                if skill["name"] not in seen_names:
                    seen_names.add(skill["name"])
                    all_skills.append(skill)

        return all_skills


class SkillSelfFilter:
    """
    LLM-based skill self-filtering.

    Given a task, plan, and candidate skills, uses LLM to select
    the most relevant skills for the specific task context.

    This implements the "LLM self-filter" described in the SkillX paper
    for reducing noise in retrieved skills at inference time.
    """

    def __init__(
        self,
        llm,
        benchmark: str = "appworld",
        max_retries: int = 3,
        verbose: bool = True
    ):
        """
        Initialize skill self-filter.

        Args:
            llm: LLM instance for filtering
            benchmark: Benchmark name for prompt selection
            max_retries: Maximum retry attempts
            verbose: Whether to output verbose logs
        """
        self.llm = llm
        self.benchmark = benchmark
        self.max_retries = max_retries
        self.verbose = verbose

    def get_prompt(self) -> str:
        """Get skill selection prompt for current benchmark."""
        return PromptRegistry.get("skill_select", self.benchmark)

    def _extract_skill_names(self, text: str) -> Optional[List[str]]:
        """Extract skill names list from LLM response."""
        match = re.search(r"```python\s*(.*?)\s*```", text, flags=re.S)
        if match:
            try:
                names = eval(match.group(1).strip())
                if isinstance(names, list):
                    return names
            except Exception:
                pass

        if self.verbose:
            logger.warning("No valid skill list found in response")
        return None

    def _format_skill_library(self, skills: List[Dict]) -> List[Dict]:
        """Format skills for prompt input."""
        return [
            {"skill_name": s.get("name", ""), "skill_description": s.get("document", "")}
            for s in skills
        ]

    async def filter(
        self,
        task: str,
        plan: str,
        skills: List[Dict],
        **kwargs
    ) -> List[Dict]:
        """
        Filter skills based on task and plan relevance.

        Args:
            task: User task description
            plan: Plan text
            skills: List of candidate skill dicts

        Returns:
            Filtered list of skills
        """
        if not skills:
            return []

        formatted_library = self._format_skill_library(skills)
        prompt = self.get_prompt().format(
            user_task=task,
            plan=plan,
            skill_library=formatted_library
        )

        messages = [{"role": "user", "content": prompt}]

        if self.verbose:
            logger.info(f"Filtering {len(skills)} skills for task: {task[:50]}...")

        for retry in range(self.max_retries):
            try:
                response = await self.llm.ainvoke(messages=messages, **kwargs)

                if isinstance(response, dict):
                    response = response.get("content", "")

                selected_names = self._extract_skill_names(response)

                if selected_names is not None:
                    selected_skills = [
                        s for s in skills if s.get("name") in selected_names
                    ]
                    if self.verbose:
                        logger.info(f"Selected {len(selected_skills)} out of {len(skills)} skills")
                    return selected_skills

            except Exception as e:
                logger.error(f"Error filtering skills: {e}; retry {retry+1}/{self.max_retries}")

        logger.warning("Failed to filter skills, returning all candidates")
        return skills

    def filter_sync(
        self,
        task: str,
        plan: str,
        skills: List[Dict],
        **kwargs
    ) -> List[Dict]:
        """
        Synchronous version of filter.

        Args:
            task: User task description
            plan: Plan text
            skills: List of candidate skill dicts

        Returns:
            Filtered list of skills
        """
        if not skills:
            return []

        formatted_library = self._format_skill_library(skills)
        prompt = self.get_prompt().format(
            user_task=task,
            plan=plan,
            skill_library=formatted_library
        )

        messages = [{"role": "user", "content": prompt}]

        if self.verbose:
            logger.info(f"Filtering {len(skills)} skills for task: {task[:50]}...")

        for retry in range(self.max_retries):
            try:
                if hasattr(self.llm, 'chat'):
                    response = self.llm.chat(messages=messages, **kwargs)
                    if isinstance(response, dict):
                        response = response.get("content", "")
                elif hasattr(self.llm, 'invoke'):
                    response = self.llm.invoke(messages=messages, **kwargs)
                else:
                    raise ValueError("LLM must have 'chat' or 'invoke' method")

                selected_names = self._extract_skill_names(response)

                if selected_names is not None:
                    selected_skills = [
                        s for s in skills if s.get("name") in selected_names
                    ]
                    if self.verbose:
                        logger.info(f"Selected {len(selected_skills)} out of {len(skills)} skills")
                    return selected_skills

            except Exception as e:
                logger.error(f"Error filtering skills: {e}; retry {retry+1}/{self.max_retries}")

        logger.warning("Failed to filter skills, returning all candidates")
        return skills
