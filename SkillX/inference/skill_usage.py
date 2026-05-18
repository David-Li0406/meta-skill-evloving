"""Main skill usage service for inference."""

import logging
from typing import List, Dict, Optional, Any, Set

from .retriever import SkillRetriever
from .skill_selector import SkillSelector
from .plan_rewriter import PlanRewriter
from .prompt_formatters import get_formatter, BasePromptFormatter
from .embedding_service import EmbeddingService

try:
    from ..core.skill import SkillLibrary
except ImportError:
    from core.skill import SkillLibrary

logger = logging.getLogger(__name__)


class SkillUsageService:
    """
    Main service for skill usage during inference.

    Provides a unified interface for:
    - Plan retrieval and rewriting
    - Skill retrieval and selection
    - Prompt formatting for different benchmarks

    Usage modes:
    - vanilla: No skills or plans
    - plan_only: Only retrieve and use plans
    - skill_only: Only retrieve and use skills
    - plan_with_skill: Both plans and skills (default)
    """

    def __init__(
        self,
        skill_library: Optional[SkillLibrary] = None,
        embedding_service: Optional[EmbeddingService] = None,
        llm=None,
        benchmark: str = "appworld",
        mode: str = "plan_with_skill"
    ):
        """
        Initialize skill usage service.

        Args:
            skill_library: SkillLibrary instance
            embedding_service: Embedding service for retrieval
            llm: LLM instance for skill selection and plan rewriting
            benchmark: Benchmark name (appworld, bfcl, tau2bench)
            mode: Usage mode (vanilla, plan_only, skill_only, plan_with_skill)
        """
        self.benchmark = benchmark
        self.mode = mode
        self.llm = llm

        self.embedding_service = embedding_service or EmbeddingService()

        self.retriever = SkillRetriever(
            skill_library=skill_library,
            embedding_service=self.embedding_service
        )

        self.selector = SkillSelector(llm) if llm else None
        self.rewriter = PlanRewriter(llm) if llm else None

        self.formatter = get_formatter(benchmark)

        self._available_tools: Optional[Set[str]] = None

    def set_available_tools(self, tools: Set[str]) -> None:
        """Set available tools for filtering skills."""
        self._available_tools = tools
        logger.info(f"Set {len(tools)} available tools for filtering")

    def load_library(self, library: SkillLibrary) -> None:
        """Load skill library."""
        self.retriever.load_library(library)

    async def prepare_prompt(
        self,
        task: str,
        base_prompt: str = "",
        max_skills: int = 10,
        rewrite_plan: bool = True
    ) -> Dict[str, Any]:
        """
        Prepare system prompt with skills and plans.

        Args:
            task: Task description
            base_prompt: Base system prompt (e.g., domain policy)
            max_skills: Maximum number of skills to include
            rewrite_plan: Whether to rewrite retrieved plans

        Returns:
            Dict with system_prompt and metadata
        """
        metadata = {
            "mode": self.mode,
            "benchmark": self.benchmark,
            "retrieved_plans": [],
            "selected_skills": [],
            "raw_retrieved_skills": [],
        }

        if self.mode == "vanilla":
            return {
                "system_prompt": base_prompt,
                "metadata": metadata
            }

        plan = None
        skill_library_str = ""

        if self.mode in ("plan_only", "plan_with_skill"):
            plans = await self.retriever.retrieve_plan(task, top_k=3)
            metadata["retrieved_plans"] = plans

            if plans:
                plan = plans[0]["plan"]

                if rewrite_plan and self.rewriter:
                    plan = await self.rewriter.rewrite(
                        task=task,
                        retrieved_plan=plan
                    )
                    metadata["rewritten_plan"] = plan

        if self.mode in ("skill_only", "plan_with_skill"):
            if plan:
                raw_skills = await self.retriever.retrieve_skills_for_plan(
                    plan=plan,
                    skills_per_step=4,
                    tool_filter=self._available_tools
                )
            else:
                raw_skills = await self.retriever.retrieve_skills(
                    query=task,
                    skill_type="all",
                    top_k=max_skills * 2,
                    tool_filter=self._available_tools
                )

            metadata["raw_retrieved_skills"] = [s["name"] for s in raw_skills]

            if self.selector and len(raw_skills) > max_skills:
                selected_skills = await self.selector.select(
                    user_task=task,
                    plan=plan or task,
                    skill_library=raw_skills,
                    max_skills=max_skills
                )
            else:
                selected_skills = raw_skills[:max_skills]

            metadata["selected_skills"] = selected_skills
            skill_library_str = self.formatter.format_skill_library(selected_skills)

        system_prompt = self.formatter.format_system_prompt(
            base_prompt=base_prompt,
            skill_library=skill_library_str,
            plan=plan if self.mode in ("plan_only", "plan_with_skill") else None
        )

        return {
            "system_prompt": system_prompt,
            "metadata": metadata
        }

    async def get_skills_for_step(
        self,
        step: str,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Get relevant skills for a specific step.

        Useful for dynamic skill retrieval during execution.

        Args:
            step: Step description
            top_k: Number of skills to retrieve

        Returns:
            List of skill dicts
        """
        return await self.retriever.retrieve_skills(
            query=step,
            skill_type="all",
            top_k=top_k,
            tool_filter=self._available_tools
        )


async def create_skill_service(
    library_path: str,
    embedding_url: str = "http://127.0.0.1:7000",
    llm=None,
    benchmark: str = "appworld",
    mode: str = "plan_with_skill"
) -> SkillUsageService:
    """
    Factory function to create a configured skill service.

    Args:
        library_path: Path to skill library JSON file
        embedding_url: Embedding service URL
        llm: LLM instance
        benchmark: Benchmark name
        mode: Usage mode

    Returns:
        Configured SkillUsageService instance
    """
    library = SkillLibrary.load(library_path)
    embedding_service = EmbeddingService(base_url=embedding_url)

    service = SkillUsageService(
        skill_library=library,
        embedding_service=embedding_service,
        llm=llm,
        benchmark=benchmark,
        mode=mode
    )

    return service
