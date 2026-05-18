"""Plan rewriting for task adaptation.

Implements pseudo-plan rewriting as described in the SkillX paper (Section 4):
- Retrieve relevant plans from similar tasks
- Rewrite into a task-specific pseudo-plan
- The pseudo-plan serves as an intermediate query for skill retrieval
"""

import re
import logging
from typing import Optional, Dict, List, Any

try:
    from ..prompts.registry import PromptRegistry
except ImportError:
    from prompts.registry import PromptRegistry

logger = logging.getLogger(__name__)


class PlanRewriter:
    """
    Rewrite retrieved plans for specific tasks.

    Given a new task and retrieved reference plans, generates a task-specific
    pseudo-plan that adapts the reference plans to the current task context.

    This is used to improve retrieval relevance by creating an intermediate
    query that better aligns skill retrieval with the current execution setting.
    """

    def __init__(
        self,
        llm,
        benchmark: str = "appworld",
        max_retries: int = 3,
        verbose: bool = True
    ):
        """
        Initialize plan rewriter.

        Args:
            llm: LLM instance for plan rewriting
            benchmark: Benchmark name for prompt selection
            max_retries: Maximum retry attempts for LLM calls
            verbose: Whether to output verbose logs
        """
        self.llm = llm
        self.benchmark = benchmark
        self.max_retries = max_retries
        self.verbose = verbose

    def get_prompt(self) -> str:
        """Get plan rewrite prompt for current benchmark."""
        return PromptRegistry.get("plan_rewrite", self.benchmark)

    def _extract_plan_from_response(self, text: str) -> Optional[str]:
        """Extract plan from LLM response using <plan> tags."""
        match = re.search(r"<plan>(.*?)</plan>", text, flags=re.S)
        if match:
            return match.group(1).strip()
        if self.verbose:
            logger.warning("No <plan> block found in response")
        return None

    def _format_reference_tasks(self, retrieved_plans: List[Dict]) -> str:
        """
        Format retrieved plans into reference tasks text.

        Args:
            retrieved_plans: List of dicts with 'task'/'matched_query' and 'plan'/'plans' keys

        Returns:
            Formatted reference tasks string
        """
        reference_tasks = ""
        for idx, plan_info in enumerate(retrieved_plans):
            task = plan_info.get("task", plan_info.get("matched_query", f"Task-{idx+1}"))
            plan = plan_info.get("plan", plan_info.get("plans", ""))
            reference_tasks += f"Task-{idx+1} {task}:\nReference plan:\n{plan}\n\n"
        return reference_tasks

    async def rewrite(
        self,
        task: str,
        retrieved_plans: List[Dict],
        context: Optional[Dict] = None,
        **kwargs
    ) -> Optional[str]:
        """
        Rewrite retrieved plans for a specific task.

        Args:
            task: Target task description
            retrieved_plans: List of retrieved plan dictionaries
                Each dict should have:
                - 'task' or 'matched_query': The original task description
                - 'plan' or 'plans': The plan content
            context: Additional context (optional)

        Returns:
            Rewritten pseudo-plan, or None if rewriting failed
        """
        if not retrieved_plans:
            if self.verbose:
                logger.info("No retrieved plans provided, skipping rewrite")
            return None

        reference_tasks = self._format_reference_tasks(retrieved_plans)

        messages = [
            ("system", self.get_prompt()),
            ("human", f"#Reference Tasks:\n{reference_tasks}\n\n# New Task: {task}")
        ]

        if self.verbose:
            logger.info(f"Rewriting plan for task: {task[:50]}...")
            logger.info(f"Using {len(retrieved_plans)} reference plans")

        for retry in range(self.max_retries):
            try:
                response = await self.llm.ainvoke(
                    messages=messages,
                    regex_extractor=self._extract_plan_from_response,
                    **kwargs
                )

                plan = self._extract_plan_from_response(response)

                if plan:
                    if self.verbose:
                        logger.info("Plan rewrite successful")
                    return plan

            except Exception as e:
                logger.error(f"Error rewriting plan: {e}; retry {retry+1}/{self.max_retries}")

        logger.warning("Failed to rewrite plan after all retries")
        return None

    def rewrite_sync(
        self,
        task: str,
        retrieved_plans: List[Dict],
        context: Optional[Dict] = None,
        **kwargs
    ) -> Optional[str]:
        """
        Synchronous version of rewrite for non-async contexts.

        Args:
            task: Target task description
            retrieved_plans: List of retrieved plan dictionaries
            context: Additional context (optional)

        Returns:
            Rewritten pseudo-plan, or None if rewriting failed
        """
        if not retrieved_plans:
            if self.verbose:
                logger.info("No retrieved plans provided, skipping rewrite")
            return None

        reference_tasks = self._format_reference_tasks(retrieved_plans)

        messages = [
            {"role": "system", "content": self.get_prompt()},
            {"role": "user", "content": f"#Reference Tasks:\n{reference_tasks}\n\n# New Task: {task}"}
        ]

        if self.verbose:
            logger.info(f"Rewriting plan for task: {task[:50]}...")

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

                plan = self._extract_plan_from_response(response)

                if plan:
                    if self.verbose:
                        logger.info("Plan rewrite successful")
                    return plan

            except Exception as e:
                logger.error(f"Error rewriting plan: {e}; retry {retry+1}/{self.max_retries}")

        logger.warning("Failed to rewrite plan after all retries")
        return None


class PlanRewriteService:
    """
    High-level service for plan retrieval and rewriting.

    Combines plan retrieval with plan rewriting to generate
    task-specific pseudo-plans for skill retrieval.
    """

    def __init__(
        self,
        llm,
        retriever,
        benchmark: str = "appworld",
        enable_rewrite: bool = True,
        top_k_plans: int = 3,
        verbose: bool = True
    ):
        """
        Initialize plan rewrite service.

        Args:
            llm: LLM instance
            retriever: SkillRetriever instance for plan retrieval
            benchmark: Benchmark name
            enable_rewrite: Whether to enable plan rewriting (can be disabled)
            top_k_plans: Number of plans to retrieve
            verbose: Whether to output verbose logs
        """
        self.llm = llm
        self.retriever = retriever
        self.benchmark = benchmark
        self.enable_rewrite = enable_rewrite
        self.top_k_plans = top_k_plans
        self.verbose = verbose

        self.rewriter = PlanRewriter(
            llm=llm,
            benchmark=benchmark,
            verbose=verbose
        )

    async def get_pseudo_plan(
        self,
        task: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get pseudo-plan for a task.

        Flow:
        1. Retrieve similar plans
        2. Rewrite into task-specific pseudo-plan (if enabled)
        3. Return pseudo-plan with metadata

        Args:
            task: Task description

        Returns:
            Dict with:
            - 'pseudo_plan': The rewritten plan (or None)
            - 'retrieved_plans': List of retrieved plans
            - 'rewrite_enabled': Whether rewriting was attempted
        """
        result = {
            "pseudo_plan": None,
            "retrieved_plans": [],
            "rewrite_enabled": self.enable_rewrite
        }

        retrieved_plans = await self.retriever.retrieve_plan(
            task=task,
            top_k=self.top_k_plans
        )

        result["retrieved_plans"] = retrieved_plans

        if not retrieved_plans:
            if self.verbose:
                logger.info("No plans retrieved, cannot generate pseudo-plan")
            return result

        if self.enable_rewrite:
            pseudo_plan = await self.rewriter.rewrite(
                task=task,
                retrieved_plans=retrieved_plans,
                **kwargs
            )
            result["pseudo_plan"] = pseudo_plan
        else:
            if retrieved_plans:
                result["pseudo_plan"] = retrieved_plans[0].get("plan", "")

        return result
