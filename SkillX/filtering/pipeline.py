"""Two-stage filtering pipeline."""

import json
import logging
from typing import List, Dict, Optional, Any

from .base import GeneralFilter, ToolSchemaFilter

logger = logging.getLogger(__name__)


class TwoStageFilterPipeline:
    """
    Two-stage filtering pipeline for skill quality control.

    Stage 1 (General Filter): Checks general skill quality
    - Domain specificity
    - No over-encapsulation
    - No Python imports
    - Parameter reusability
    - No functional style

    Stage 2 (Tool Filter): Validates tool usage
    - Parameter validation against schema
    - Call dependency checks
    - Comment-function alignment
    """

    def __init__(
        self,
        llm,
        benchmark: str = "appworld",
        domain: str = "",
        tool_schemas: Optional[Dict[str, Any]] = None,
        skip_stage1: bool = False,
        skip_stage2: bool = False,
        verbose: bool = True
    ):
        """
        Initialize two-stage filter pipeline.

        Args:
            llm: LLM instance for filtering
            benchmark: Benchmark name
            domain: Domain name for tool schema registry (airline, retail, telecom, etc.)
            tool_schemas: Dictionary of tool schemas for Stage 2 (overrides registry)
            skip_stage1: Whether to skip general filter
            skip_stage2: Whether to skip tool schema filter
            verbose: Whether to output verbose logs
        """
        self.llm = llm
        self.benchmark = benchmark
        self.domain = domain
        self.verbose = verbose
        self.skip_stage1 = skip_stage1
        self.skip_stage2 = skip_stage2

        # Initialize filters
        self.general_filter = GeneralFilter(
            llm=llm,
            benchmark=benchmark,
            verbose=verbose
        )

        self.tool_filter = ToolSchemaFilter(
            llm=llm,
            benchmark=benchmark,
            domain=domain,
            tool_schemas=tool_schemas,
            verbose=verbose
        )

        # Log schema info
        if domain and verbose:
            schema_count = len(self.tool_filter.tool_schemas)
            logger.info(f"Loaded {schema_count} tool schemas for domain '{domain}'")

    def load_tool_schemas(self, schemas: Dict[str, Any]) -> None:
        """Load tool schemas for Stage 2 validation."""
        self.tool_filter.load_schemas(schemas)

    def _validate_skill_structure(self, skill: Dict) -> bool:
        """Validate that skill has required structure."""
        skill_data = skill.get("skill", skill)

        # Check for tools field
        if "tools" not in skill_data:
            return False

        tools = skill_data.get("tools", [])
        if not tools or len(tools) == 0:
            return False

        return True

    def _prepare_skill_for_tool_filter(
        self,
        skill: Dict,
        tool_schemas: Dict[str, Any]
    ) -> Optional[Dict]:
        """
        Prepare skill for tool filter by adding tool documentation.

        Args:
            skill: Skill dictionary
            tool_schemas: Available tool schemas

        Returns:
            Skill with tool_doc added, or None if no schemas found at all
        """
        skill_data = skill.get("skill", skill)
        tools = skill_data.get("tools", [])

        if not tools:
            return None

        # Get schemas for available tools, warn about missing ones
        tool_docs = []
        missing_tools = []
        for tool_name in tools:
            if tool_name in tool_schemas:
                tool_docs.append(tool_schemas[tool_name])
            else:
                missing_tools.append(tool_name)

        if missing_tools:
            logger.debug(f"Missing schemas for tools: {missing_tools}")

        # Only skip if ALL tools are missing schemas
        if not tool_docs:
            logger.debug(f"No schemas found for any tools in skill, skipping")
            return None

        # Add tool documentation to skill
        skill_copy = skill.copy()
        skill_copy["tool_doc"] = json.dumps(tool_docs, ensure_ascii=False, indent=2)

        return skill_copy

    async def filter(
        self,
        skills: List[Dict],
        batch_size: int = 10,
        max_concurrent: int = 5,
        show_progress: bool = True,
        **kwargs
    ) -> List[Dict]:
        """
        Run two-stage filtering on skills.

        Args:
            skills: List of skill dictionaries
            batch_size: Batch size for processing
            max_concurrent: Maximum concurrent batches
            show_progress: Whether to show progress bar

        Returns:
            List of skills that passed both stages
        """
        logger.info(f"Starting two-stage filtering on {len(skills)} skills")

        # Split by skill_type so atomic skills bypass Stage 1.
        def _get_skill_type(s: Dict) -> str:
            t = s.get("skill_type")
            if not t:
                inner = s.get("skill")
                if isinstance(inner, dict):
                    t = inner.get("skill_type")
                    if not t and isinstance(inner.get("metadata"), dict):
                        t = inner["metadata"].get("skill_type")
            return t or "functional"

        functional_skills = [s for s in skills if _get_skill_type(s) != "atomic"]
        atomic_skills = [s for s in skills if _get_skill_type(s) == "atomic"]

        # Stage 1: General Filter (functional only)
        if not self.skip_stage1 and functional_skills:
            logger.info("Stage 1: Running general quality filter...")
            stage1_results = await self.general_filter.filter_batch(
                functional_skills,
                batch_size=batch_size,
                max_concurrent=max_concurrent,
                show_progress=show_progress,
                **kwargs
            )
            passed_functional = [
                s for s in stage1_results
                if s.get("filter_result", False)
            ]
        else:
            if self.skip_stage1:
                logger.info("Stage 1: Skipped (skip_stage1=True)")
            passed_functional = functional_skills

        current_skills = passed_functional + atomic_skills
        logger.info(
            f"Stage 1 complete: {len(passed_functional)}/{len(functional_skills)} "
            f"functional passed; {len(atomic_skills)} atomic skills bypassed Stage 1"
        )

        if not current_skills:
            logger.warning("No skills passed Stage 1")
            return []

        # Validate structure and prepare for Stage 2
        if not self.skip_stage2:
            valid_skills = []
            for skill in current_skills:
                if self._validate_skill_structure(skill):
                    prepared = self._prepare_skill_for_tool_filter(
                        skill,
                        self.tool_filter.tool_schemas
                    )
                    if prepared:
                        valid_skills.append(prepared)

            if not valid_skills:
                logger.warning("No skills have valid tool schemas for Stage 2")
                return current_skills  # Return Stage 1 results

            # Stage 2: Tool Schema Filter
            logger.info("Stage 2: Running tool schema validation...")
            stage2_results = await self.tool_filter.filter_batch(
                valid_skills,
                batch_size=batch_size,
                max_concurrent=max_concurrent,
                show_progress=show_progress,
                **kwargs
            )

            # Keep only passed skills
            final_skills = [
                s for s in stage2_results
                if s.get("filter_result", False)
            ]
            logger.info(
                f"Stage 2 complete: {len(final_skills)}/{len(valid_skills)} passed"
            )
        else:
            logger.info("Stage 2: Skipped")
            final_skills = current_skills

        logger.info(
            f"Two-stage filtering complete: {len(final_skills)}/{len(skills)} "
            f"skills passed ({len(final_skills)/len(skills)*100:.1f}%)"
        )

        return final_skills


async def two_stage_filter(
    llm,
    skills: List[Dict],
    benchmark: str = "appworld",
    domain: str = "",
    tool_schemas: Optional[Dict[str, Any]] = None,
    **kwargs
) -> List[Dict]:
    """
    Convenience function for two-stage filtering.

    Args:
        llm: LLM instance
        skills: List of skill dictionaries
        benchmark: Benchmark name
        domain: Domain name for tool schema registry (airline, retail, telecom, etc.)
        tool_schemas: Tool schemas for validation (overrides registry)
        **kwargs: Additional arguments

    Returns:
        List of filtered skills
    """
    pipeline = TwoStageFilterPipeline(
        llm=llm,
        benchmark=benchmark,
        domain=domain,
        tool_schemas=tool_schemas,
        verbose=True
    )

    return await pipeline.filter(skills, **kwargs)
