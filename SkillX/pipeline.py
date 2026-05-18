"""Main orchestration pipeline for SkillX."""

import asyncio
import json
import logging
from typing import List, Dict, Any, Optional
from collections import defaultdict
from pathlib import Path
from datetime import datetime

from .llm.client import LLM
from .core.skill import SkillLibrary, Skill, PlanSkill
from .core.trajectory import Trajectory, group_trajectories_by_task
from .extraction.plan_extractor import PlanExtractor, PlanCombiner
from .extraction.skill_extractor import (
    FunctionalSkillExtractor,
    AtomicSkillExtractor,
    HybridSkillExtractor,
    collect_skills_from_results,
    prepare_skills_for_clustering
)
from .extraction.tool_summary import ToolSummary
from .filtering.pipeline import TwoStageFilterPipeline
from .clustering.dbscan import DBSCANClusterer
from .clustering.merger import SkillMerger
from .data.loaders import TrajectoryLoader, SkillLibraryLoader
from .data.exporters import SkillLibraryExporter
from .expansion.base import BaseExpansionStrategy
from .expansion.task_manager import TaskSynthesisManager

logger = logging.getLogger(__name__)


class IterativeSkillPipeline:
    """
    Main pipeline supporting iterative skill extraction with optional expansion.

    Modes:
    - expansion_strategy=None: Pure extraction (no environment interaction)
    - expansion_strategy=ExpansionStrategy: With exploration and task synthesis

    Each epoch:
    1. Extract skills from current trajectory pool
    2. Filter extracted skills (two-stage)
    3. Cluster and merge similar skills
    4. Update skill library
    5. Save checkpoint
    6. Optional: Expand (explore → synthesize new tasks → add to pool)
    """

    def __init__(
        self,
        llm: LLM,
        benchmark: str = "appworld",
        skill_type: str = "functional",
        domain: str = "",
        plan_strategy: str = "shortest",
        atomic_mode: str = "omission",
        expansion_strategy: Optional[BaseExpansionStrategy] = None,
        task_manager: Optional[TaskSynthesisManager] = None,
        env_worker: Optional[Any] = None,
        tool_schemas: Optional[Dict[str, Any]] = None,
        existing_skills: Optional[Dict[str, Dict]] = None,
        output_dir: str = "./output",
        verbose: bool = True
    ):
        """
        Initialize iterative extraction pipeline.

        Args:
            llm: LLM instance
            benchmark: Benchmark name (appworld, bfcl, tau2bench)
            skill_type: Type of skills to extract (functional, atomic, or hybrid)
            domain: Domain name for tool-specific filtering (airline, retail, telecom, etc.)
            plan_strategy: Plan extraction strategy ("shortest" or "merge")
                - "shortest": Select shortest trajectory per task, extract one plan (default, faster)
                - "merge": Extract plans from all trajectories, then LLM merge (more comprehensive)
            atomic_mode: Mode for atomic skill extraction in hybrid mode:
                - "omission": Only extract atomic skills for tools not covered by functional skills (default)
                - "all": Extract atomic skills for all tools used in trajectory
            expansion_strategy: Optional expansion strategy (None = no expansion)
            task_manager: Optional TaskSynthesisManager for task synthesis (alternative to expansion_strategy)
            env_worker: Environment worker for expansion (required if expansion enabled)
            tool_schemas: Tool schemas for validation
            existing_skills: Existing skills for atomic extraction
            output_dir: Output directory
            verbose: Whether to output verbose logs
        """
        self.llm = llm
        self.benchmark = benchmark
        self.skill_type = skill_type
        self.domain = domain
        self.plan_strategy = plan_strategy
        self.atomic_mode = atomic_mode
        self.expansion = expansion_strategy
        self.task_manager = task_manager
        self.env_worker = env_worker
        self.existing_skills = existing_skills or {}
        self.output_dir = Path(output_dir)
        self.verbose = verbose

        # Auto-load tool_schemas based on benchmark if not provided
        if tool_schemas:
            self.tool_schemas = tool_schemas
        else:
            self.tool_schemas = self._load_default_schemas(benchmark, domain)

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self._init_components()

    def _init_components(self):
        """Initialize pipeline components."""
        self.plan_extractor = PlanExtractor(
            llm=self.llm,
            benchmark=self.benchmark,
            verbose=self.verbose
        )

        self.plan_combiner = PlanCombiner(
            llm=self.llm,
            benchmark=self.benchmark,
            verbose=self.verbose
        )

        self.tool_summary = ToolSummary(
            llm=self.llm,
            verbose=self.verbose
        )

        if self.skill_type == "functional":
            self.skill_extractor = FunctionalSkillExtractor(
                llm=self.llm,
                benchmark=self.benchmark,
                verbose=self.verbose
            )
        elif self.skill_type == "atomic":
            self.skill_extractor = AtomicSkillExtractor(
                llm=self.llm,
                benchmark=self.benchmark,
                existing_skills=self.existing_skills,
                verbose=self.verbose
            )
        elif self.skill_type == "hybrid":
            self.skill_extractor = HybridSkillExtractor(
                llm=self.llm,
                benchmark=self.benchmark,
                domain=self.domain,
                existing_skills=self.existing_skills,
                atomic_mode=self.atomic_mode,
                verbose=self.verbose
            )
        else:
            raise ValueError(f"Unknown skill_type: {self.skill_type}. Must be 'functional', 'atomic', or 'hybrid'")

        self.filter_pipeline = TwoStageFilterPipeline(
            llm=self.llm,
            benchmark=self.benchmark,
            domain=self.domain,
            tool_schemas=self.tool_schemas,
            verbose=self.verbose
        )

        self.clusterer = DBSCANClusterer(
            eps=0.10,  # 1 - 0.90 = 0.10 for cosine similarity threshold of 0.90
            min_samples=1,
            metric="cosine"
        )

        self.merger = SkillMerger(
            llm=self.llm,
            benchmark=self.benchmark,
            verbose=self.verbose
        )

    def _load_default_schemas(self, benchmark: str, domain: str) -> Dict[str, Any]:
        """
        Auto-load tool schemas based on benchmark and domain.

        Args:
            benchmark: Benchmark name (appworld, bfcl, tau2bench)
            domain: Domain name for tau2bench (airline, retail, telecom)

        Returns:
            Dictionary of tool schemas
        """
        try:
            from .config.tool_schemas import ToolSchemaRegistry

            if benchmark == "appworld":
                schemas = ToolSchemaRegistry.get_all("appworld")
                if schemas:
                    logger.info(f"Auto-loaded {len(schemas)} tool schemas for appworld")
                return schemas
            elif benchmark == "tau2bench" and domain:
                schemas = ToolSchemaRegistry.get_all(domain)
                if schemas:
                    logger.info(f"Auto-loaded {len(schemas)} tool schemas for tau2bench/{domain}")
                return schemas
            elif benchmark == "bfcl" and domain:
                schemas = ToolSchemaRegistry.get_all(f"bfcl_{domain}")
                if schemas:
                    logger.info(f"Auto-loaded {len(schemas)} tool schemas for bfcl/{domain}")
                return schemas

            return {}
        except ImportError as e:
            logger.warning(f"Could not load tool schemas: {e}")
            return {}

    async def run(
        self,
        trajectories: List[Dict],
        num_epochs: int = 1,
        filter_threshold: float = 0.999,
        batch_size: int = 10,
        max_concurrent: int = 5,
        skip_plan_extraction: bool = False,
        existing_plans: Optional[Dict[str, str]] = None,
        enable_clustering: bool = True,
        filter_timing: str = "pre_merge",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run the iterative extraction pipeline.

        Args:
            trajectories: Initial trajectory pool
            num_epochs: Number of iteration epochs
            filter_threshold: Minimum reward threshold
            batch_size: Batch size for processing
            max_concurrent: Maximum concurrent batches
            skip_plan_extraction: Whether to skip plan extraction
            existing_plans: Pre-existing plans to use
            enable_clustering: Whether to cluster and merge skills
            filter_timing: When to apply filtering:
                - "pre_merge": Filter before merge only (default)
                - "post_merge": Filter after merge only
                - "both": Filter before and after merge
                - "none": No filtering

        Returns:
            Dictionary with extraction results
        """
        results = {
            "skill_library": SkillLibrary(benchmark=self.benchmark),
            "epochs": [],
            "total_trajectories": len(trajectories),
            "final_skills_count": 0,
            "statistics": {}
        }

        skill_library = results["skill_library"]
        all_trajectories = list(trajectories)
        all_plans = existing_plans or {}

        for epoch in range(1, num_epochs + 1):
            logger.info(f"{'='*60}")
            logger.info(f"=== Epoch {epoch}/{num_epochs} ===")
            logger.info(f"{'='*60}")

            epoch_result = await self._run_epoch(
                trajectories=all_trajectories,
                skill_library=skill_library,
                plans=all_plans,
                epoch=epoch,
                filter_threshold=filter_threshold,
                batch_size=batch_size,
                max_concurrent=max_concurrent,
                skip_plan_extraction=skip_plan_extraction or (epoch > 1),
                enable_clustering=enable_clustering,
                filter_timing=filter_timing,
                **kwargs
            )

            results["epochs"].append(epoch_result)

            # Update plans if extracted
            if epoch_result.get("plans"):
                all_plans.update(epoch_result["plans"])

            # Save epoch checkpoint
            self._save_checkpoint(skill_library, epoch)

            # Run expansion if enabled and not last epoch
            if self.expansion is not None and epoch < num_epochs:
                logger.info(f"Running expansion after epoch {epoch}...")
                new_trajs = await self._expand(
                    skill_library=skill_library,
                    trajectories=all_trajectories,
                    epoch=epoch
                )
                if new_trajs:
                    all_trajectories.extend(new_trajs)
                    logger.info(f"Expansion added {len(new_trajs)} new trajectories")
                    results["total_trajectories"] = len(all_trajectories)

        # Final statistics
        results["final_skills_count"] = len(skill_library.get_all_skills())
        results["statistics"] = {
            "total_epochs": num_epochs,
            "total_trajectories": len(all_trajectories),
            "functional_skills": len(skill_library.functional),
            "atomic_skills": len(skill_library.atomic),
            "planning_skills": len(skill_library.planning),
            "expansion_enabled": self.expansion is not None
        }

        logger.info(f"Pipeline complete! Final statistics: {results['statistics']}")

        return results

    async def _run_epoch(
        self,
        trajectories: List[Dict],
        skill_library: SkillLibrary,
        plans: Dict[str, str],
        epoch: int,
        filter_threshold: float,
        batch_size: int,
        max_concurrent: int,
        skip_plan_extraction: bool,
        enable_clustering: bool,
        filter_timing: str = "pre_merge",
        **kwargs
    ) -> Dict[str, Any]:
        """Run a single extraction epoch."""
        epoch_result = {
            "epoch": epoch,
            "plans": {},
            "extracted_skills": [],
            "filtered_skills": [],
            "merged_skills": [],
            "statistics": {}
        }

        # Step 1: Filter successful trajectories
        logger.info(f"[Epoch {epoch}] Step 1: Filtering successful trajectories...")
        successful = TrajectoryLoader.filter_by_reward(trajectories, filter_threshold)
        epoch_result["statistics"]["input_trajectories"] = len(trajectories)
        epoch_result["statistics"]["successful_trajectories"] = len(successful)

        if not successful:
            logger.warning(f"[Epoch {epoch}] No successful trajectories found")
            return epoch_result

        # Step 1.5: Summarize long tool responses (前置，覆盖原始轨迹)
        logger.info(f"[Epoch {epoch}] Step 1.5: Summarizing tool responses...")
        successful = await self.tool_summary.summarize_multiple(
            successful,
            batch_size=batch_size,
            max_concurrent=max_concurrent
        )

        # Step 2: Extract plans (if not skipped)
        if not skip_plan_extraction:
            if self.plan_strategy == "shortest":
                # Strategy 1: Select shortest trajectory per task, extract one plan each
                shortest_per_task = self._select_shortest_per_task(successful)
                logger.info(
                    f"[Epoch {epoch}] Step 2: Extracting plans from {len(shortest_per_task)} "
                    f"shortest trajectories (strategy: shortest)..."
                )
                results = await self.plan_extractor.extract_batch(
                    shortest_per_task,
                    batch_size=batch_size,
                    max_concurrent=max_concurrent
                )
                new_plans = {
                    r["user_task"]: r["plan"]
                    for r in results
                    if r and "plan" in r and "user_task" in r
                }
            else:
                # Strategy 2: Extract from all trajectories, then merge
                logger.info(
                    f"[Epoch {epoch}] Step 2: Extracting plans from all {len(successful)} "
                    f"trajectories (strategy: merge)..."
                )
                grouped_plans = await self.plan_extractor.extract_and_group(
                    successful,
                    filter_threshold=filter_threshold,
                    batch_size=batch_size,
                    max_concurrent=max_concurrent
                )
                # Combine plans for each task
                logger.info(f"[Epoch {epoch}] Combining plans...")
                new_plans = await self.plan_combiner.combine_grouped_plans(grouped_plans)

            plans.update(new_plans)
            epoch_result["plans"] = new_plans
            logger.info(f"[Epoch {epoch}] Extracted {len(new_plans)} plans")

            # Add plans to skill library
            for task, plan in new_plans.items():
                skill_library.add_plan(task, PlanSkill(task=task, plan=plan))
            logger.info(f"[Epoch {epoch}] Added {len(new_plans)} plans to skill library")
        else:
            logger.info(f"[Epoch {epoch}] Step 2: Skipping plan extraction...")

        # Step 3: Prepare trajectories for skill extraction
        logger.info(f"[Epoch {epoch}] Step 3: Preparing trajectories...")
        prepared = self._prepare_for_skill_extraction(
            successful, plans, skill_library, epoch
        )

        # Step 4: Extract skills (轨迹已在 Step 1.5 总结)
        logger.info(f"[Epoch {epoch}] Step 4: Extracting skills...")
        extraction_results = await self.skill_extractor.extract_batch(
            prepared,
            batch_size=batch_size,
            max_concurrent=max_concurrent
        )

        all_skills = collect_skills_from_results(extraction_results, self.skill_type)
        epoch_result["extracted_skills"] = all_skills
        epoch_result["statistics"]["extracted_skills"] = len(all_skills)

        if not all_skills:
            logger.warning(f"[Epoch {epoch}] No skills extracted")
            return epoch_result

        # Step 5: Pre-merge filtering (if enabled)
        if filter_timing in ("pre_merge", "both"):
            logger.info(f"[Epoch {epoch}] Step 5: Filtering skills (pre-merge)...")
            filtered = await self.filter_pipeline.filter(
                all_skills,
                batch_size=batch_size,
                max_concurrent=max_concurrent
            )
            epoch_result["filtered_skills"] = filtered
            epoch_result["statistics"]["filtered_skills"] = len(filtered)

            if not filtered:
                logger.warning(f"[Epoch {epoch}] No skills passed pre-merge filtering")
                return epoch_result
        else:
            logger.info(f"[Epoch {epoch}] Step 5: Skipping pre-merge filtering (filter_timing={filter_timing})")
            filtered = all_skills
            epoch_result["filtered_skills"] = filtered
            epoch_result["statistics"]["filtered_skills"] = len(filtered)

        # Step 6: Cluster and merge (optional)
        if enable_clustering and len(filtered) > 1:
            logger.info(f"[Epoch {epoch}] Step 6: Clustering and merging skills...")
            merged = await self._cluster_and_merge(filtered)
            epoch_result["merged_skills"] = merged
            epoch_result["statistics"]["merged_skills"] = len(merged)
        else:
            merged = filtered
            epoch_result["merged_skills"] = merged
            epoch_result["statistics"]["merged_skills"] = len(merged)

        # Step 6.5: Post-merge filtering (if enabled)
        if filter_timing in ("post_merge", "both"):
            logger.info(f"[Epoch {epoch}] Step 6.5: Filtering skills (post-merge)...")
            merged = await self.filter_pipeline.filter(
                merged,
                batch_size=batch_size,
                max_concurrent=max_concurrent
            )
            # Keep only skills that passed filter
            merged = [s for s in merged if s.get("filter_result", True)]
            epoch_result["merged_skills"] = merged
            epoch_result["statistics"]["post_merge_filtered"] = len(merged)

            if not merged:
                logger.warning(f"[Epoch {epoch}] No skills passed post-merge filtering")
                return epoch_result

        # Step 7: Update skill library
        logger.info(f"[Epoch {epoch}] Step 7: Updating skill library...")
        skill_objects = []

        def _validate_and_complete_skill(skill_data: Dict, parent_skill_type: str = None, source_item: Dict = None) -> Optional[Dict]:
            """Validate and complete a skill dict with required fields. Returns None if invalid."""
            if not isinstance(skill_data, dict) or "name" not in skill_data:
                return None
            # Ensure all required fields exist with defaults
            skill_data.setdefault("document", "")
            skill_data.setdefault("content", "")
            skill_data.setdefault("tools", [])
            # Ensure metadata
            if "metadata" not in skill_data or not isinstance(skill_data.get("metadata"), dict):
                skill_data["metadata"] = {}
            # Set skill_type
            skill_type = None
            if source_item:
                skill_type = source_item.get("skill_type")
            skill_type = skill_type or parent_skill_type
            if skill_type and "skill_type" not in skill_data["metadata"]:
                skill_data["metadata"]["skill_type"] = skill_type
            return skill_data

        def process_skill_item(item: Dict, parent_skill_type: str = None) -> None:
            """Process a single skill item and add to skill_objects."""
            skill_data = item.get("skill", item)

            # Handle case where skill_data is a list (from merge prompt returning multiple skills)
            if isinstance(skill_data, list):
                for sub_skill in skill_data:
                    completed = _validate_and_complete_skill(sub_skill, parent_skill_type, item)
                    if completed is None:
                        logger.warning(f"Skipping invalid sub_skill: {type(sub_skill)} keys={list(sub_skill.keys())[:5] if isinstance(sub_skill, dict) else 'N/A'}")
                        continue
                    try:
                        skill_objects.append(Skill.from_dict(completed))
                    except Exception as e:
                        logger.warning(f"Failed to create Skill from sub_skill: {e}")
                return

            if isinstance(skill_data, dict) and "name" in skill_data:
                completed = _validate_and_complete_skill(skill_data, parent_skill_type, item)
                if completed is None:
                    logger.warning(f"Skipping invalid skill_data: keys={list(skill_data.keys())[:5]}")
                    return
                try:
                    skill_objects.append(Skill.from_dict(completed))
                except Exception as e:
                    logger.warning(f"Failed to create Skill: {e}")
            elif "name" in item:
                completed = _validate_and_complete_skill(item, parent_skill_type)
                if completed is None:
                    return
                try:
                    skill_objects.append(Skill.from_dict(completed))
                except Exception as e:
                    logger.warning(f"Failed to create Skill from item: {e}")
            else:
                logger.warning(f"Skipping invalid skill structure: {list(item.keys())[:5]}")

        for s in merged:
            if isinstance(s, dict):
                process_skill_item(s)
            elif isinstance(s, Skill):
                skill_objects.append(s)

        skill_library.merge(skill_objects, epoch=epoch)

        logger.info(f"[Epoch {epoch}] Complete! Skills in library: {len(skill_library.get_all_skills())}")

        return epoch_result

    def _group_by_task(self, trajectories: List[Dict]) -> Dict[str, List[Dict]]:
        """Group trajectories by user_task."""
        grouped = defaultdict(list)
        for traj in trajectories:
            task = traj.get("user_task", traj.get("task_id", ""))
            grouped[task].append(traj)
        return dict(grouped)

    def _select_shortest_per_task(self, trajectories: List[Dict]) -> List[Dict]:
        """Select the shortest trajectory for each task."""
        grouped = self._group_by_task(trajectories)
        shortest_list = []
        for task, trajs in grouped.items():
            # Sort by trajectory length and pick shortest
            trajs.sort(key=lambda x: len(x.get("task_history", x.get("trajectory", []))))
            shortest_list.append(trajs[0])
        return shortest_list

    def _prepare_for_skill_extraction(
        self,
        trajectories: List[Dict],
        plans: Dict[str, str],
        skill_library: SkillLibrary,
        epoch: int
    ) -> List[Dict]:
        """Prepare trajectories for skill extraction."""
        prepared = []

        # Group by task
        grouped = defaultdict(list)
        for traj in trajectories:
            task = traj.get("user_task", traj.get("task_id", ""))
            grouped[task].append(traj)

        for task, trajs in grouped.items():
            # Get shortest successful trajectory
            trajs.sort(key=lambda x: len(x.get("task_history", x.get("trajectory", []))))
            shortest = trajs[0]

            item = {
                "user_task": task,
                "successful_trajectory": shortest.get("task_history", shortest.get("trajectory", [])),
                "plan": plans.get(task, ""),
                "exp_metadata": shortest.get("exp_metadata", {}),
                "epoch": epoch
            }

            # Add existing skill library for atomic extraction
            if self.skill_type == "atomic":
                item["skill_library"] = [s.to_dict() for s in skill_library.atomic]

            # Add failed trajectory if available (for atomic skills)
            all_trajs = [t for ts in grouped.values() for t in ts]
            for t in all_trajs:
                if t.get("user_task") == task and t.get("reward", 1) < 0.5:
                    item["failed_trajectory"] = t.get("task_history", t.get("trajectory", []))
                    break

            prepared.append(item)

        return prepared

    async def _cluster_and_merge(self, skills: List[Dict]) -> List[Dict]:
        """Cluster similar skills and merge them."""
        if len(skills) <= 1:
            return skills

        # Prepare for clustering
        skill_texts = prepare_skills_for_clustering(skills)

        # Cluster
        clusters = await self.clusterer.cluster_async(skill_texts)

        # Merge each cluster
        merged = []
        for cluster_id, skill_indices in clusters.items():
            cluster_skills = [skills[i] for i in skill_indices]

            # Get skill_type from the first skill in cluster (they should all be the same type)
            cluster_skill_type = cluster_skills[0].get("skill_type")

            if len(cluster_skills) == 1:
                merged.append(cluster_skills[0])
            else:
                # Merge cluster
                merged_skill = await self.merger.merge(cluster_skills)
                if merged_skill:
                    # Preserve skill_type from original cluster
                    if cluster_skill_type:
                        merged_skill["skill_type"] = cluster_skill_type
                    merged.append(merged_skill)
                else:
                    # If merge fails, keep the first skill
                    merged.append(cluster_skills[0])

        return merged

    async def _expand(
        self,
        skill_library: SkillLibrary,
        trajectories: List[Dict],
        epoch: int
    ) -> List[Dict]:
        """
        Run expansion to generate new trajectories.

        Supports two modes:
        1. expansion_strategy: Uses ExperienceGuidedExplorer for exploration + summarization
        2. task_manager: Uses TaskSynthesisManager for direct task synthesis from seeds
        """
        # Mode 1: Use TaskSynthesisManager if available (abstracted from AgentEvolver)
        if self.task_manager is not None:
            successful = [t for t in trajectories if t.get("reward", 0) >= 0.999]
            if not successful:
                logger.info("No successful trajectories for task synthesis")
                return []

            # Prepare seed tasks from successful trajectories
            seed_tasks = [
                {
                    "task_id": t.get("task_id", f"seed_{i}"),
                    "user_task": t.get("user_task", "")
                }
                for i, t in enumerate(successful)
            ]

            logger.info(f"Synthesizing tasks from {len(seed_tasks)} seed tasks")
            new_tasks = await self.task_manager.generate_tasks(seed_tasks)

            # Convert to trajectory format using TaskSynthesisManager's method
            return self.task_manager.tasks_to_trajectories(new_tasks, epoch)

        # Mode 2: Use expansion_strategy (ExperienceGuidedExplorer)
        if self.expansion is None:
            return []

        # Analyze experience
        successful = [t for t in trajectories if t.get("reward", 0) >= 0.999]
        failed = [t for t in trajectories if t.get("reward", 0) < 0.999]

        logger.info(f"Analyzing experience: {len(successful)} successful, {len(failed)} failed")
        experience = await self.expansion.analyze_experience(successful, failed)

        # Explore environment
        if self.env_worker is not None:
            logger.info("Exploring environment...")
            exploration_trajs = await self.expansion.explore(
                skill_library=skill_library,
                env_worker=self.env_worker,
                experience=experience
            )
        else:
            logger.warning("No env_worker provided, skipping exploration")
            exploration_trajs = []

        if not exploration_trajs:
            logger.info("No exploration trajectories generated")
            return []

        # Synthesize new tasks from exploration
        logger.info("Synthesizing new tasks...")
        new_tasks = await self.expansion.summarize(exploration_trajs)

        # Convert synthesized tasks to trajectory format
        new_trajectories = self._tasks_to_trajectories(new_tasks, epoch)

        return new_trajectories

    def _tasks_to_trajectories(
        self,
        tasks: List[Dict],
        epoch: int
    ) -> List[Dict]:
        """Convert synthesized tasks to trajectory format."""
        import uuid

        trajectories = []
        for task in tasks:
            trajectory = {
                "trajectory_id": f"synthetic_{uuid.uuid4().hex[:8]}",
                "benchmark": self.benchmark,
                "task_id": task.get("task_id", f"synthetic_{uuid.uuid4().hex[:8]}"),
                "user_task": task.get("query", task.get("user_task", "")),
                "task_history": [],  # To be filled by agent execution
                "reward": None,  # Not yet executed
                "metadata": {
                    "source": "expansion",
                    "epoch": epoch,
                    "confidence": task.get("confidence", 0.5),
                    "action_sequence": task.get("action_sequence", ""),
                    "synthesized_at": datetime.now().isoformat()
                }
            }
            trajectories.append(trajectory)

        return trajectories

    def _save_checkpoint(self, skill_library: SkillLibrary, epoch: int) -> str:
        """Save checkpoint after each epoch."""
        checkpoint_dir = self.output_dir / "checkpoints"
        checkpoint_dir.mkdir(parents=True, exist_ok=True)

        checkpoint_path = checkpoint_dir / f"skill_library_epoch_{epoch}.json"
        skill_library.save(str(checkpoint_path))

        logger.info(f"Saved checkpoint to {checkpoint_path}")
        return str(checkpoint_path)

    def save_results(
        self,
        results: Dict[str, Any],
        prefix: str = "extraction"
    ) -> Dict[str, str]:
        """
        Save extraction results to files.

        Args:
            results: Results dictionary from run()
            prefix: File prefix

        Returns:
            Dictionary mapping result type to file path
        """
        saved_paths = {}
        skill_library = results.get("skill_library")

        if skill_library is None:
            logger.warning("No skill library in results")
            return saved_paths

        # Save final skill library
        library_path = self.output_dir / f"{prefix}_skill_library.json"
        skill_library.save(str(library_path))
        saved_paths["skill_library"] = str(library_path)

        # Save epoch summaries
        epochs_path = self.output_dir / f"{prefix}_epochs.json"
        epoch_summaries = []
        for epoch_result in results.get("epochs", []):
            summary = {
                "epoch": epoch_result.get("epoch"),
                "statistics": epoch_result.get("statistics", {})
            }
            epoch_summaries.append(summary)

        with open(epochs_path, "w") as f:
            json.dump(epoch_summaries, f, indent=2)
        saved_paths["epochs"] = str(epochs_path)

        # Save statistics
        stats_path = self.output_dir / f"{prefix}_statistics.json"
        with open(stats_path, "w") as f:
            json.dump(results.get("statistics", {}), f, indent=2)
        saved_paths["statistics"] = str(stats_path)

        logger.info(f"Saved results to: {saved_paths}")
        return saved_paths


# Backward compatibility alias
SkillExtractionPipeline = IterativeSkillPipeline


async def run_pipeline(
    trajectories_path: str,
    output_dir: str,
    model: str = "gpt-4.1-2025-04-14",
    benchmark: str = "appworld",
    skill_type: str = "functional",
    domain: str = "",
    plan_strategy: str = "shortest",
    num_epochs: int = 1,
    filter_threshold: float = 0.999,
    batch_size: int = 10,
    max_concurrent: int = 5,
    filter_timing: str = "pre_merge",
    enable_expansion: bool = False,
    env_url: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Convenience function to run the full pipeline.

    Args:
        trajectories_path: Path to trajectories file
        output_dir: Output directory
        model: LLM model name
        benchmark: Benchmark name
        skill_type: Type of skills (functional, atomic, or hybrid)
        domain: Domain name for tool-specific filtering (airline, retail, telecom, etc.)
        plan_strategy: Plan extraction strategy ("shortest" or "merge")
        num_epochs: Number of extraction epochs
        filter_threshold: Minimum reward threshold
        batch_size: Batch size
        max_concurrent: Max concurrent batches
        filter_timing: When to filter ("pre_merge", "post_merge", "both", "none")
        enable_expansion: Whether to enable skill expansion
        env_url: Environment URL (required if enable_expansion=True)

    Returns:
        Extraction results
    """
    # Load trajectories
    trajectories = TrajectoryLoader.load(trajectories_path)

    # Initialize LLM
    llm = LLM(model=model)

    # Initialize expansion strategy if enabled
    expansion_strategy = None
    env_worker = None
    if enable_expansion:
        from .expansion import ExperienceGuidedExplorer
        expansion_strategy = ExperienceGuidedExplorer(
            llm=llm,
            verbose=True
        )
        # Note: env_worker needs to be provided separately for actual exploration
        if env_url:
            logger.info(f"Expansion enabled with env_url: {env_url}")
            # env_worker would be created from env_url here

    # Create and run pipeline
    pipeline = IterativeSkillPipeline(
        llm=llm,
        benchmark=benchmark,
        skill_type=skill_type,
        domain=domain,
        plan_strategy=plan_strategy,
        expansion_strategy=expansion_strategy,
        env_worker=env_worker,
        output_dir=output_dir,
        verbose=True
    )

    results = await pipeline.run(
        trajectories,
        num_epochs=num_epochs,
        filter_threshold=filter_threshold,
        batch_size=batch_size,
        max_concurrent=max_concurrent,
        filter_timing=filter_timing,
        **kwargs
    )

    # Save results
    pipeline.save_results(results)

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SkillX Extraction Pipeline")
    parser.add_argument("--input", type=str, required=True, help="Input trajectories file")
    parser.add_argument("--output", type=str, required=True, help="Output directory")
    parser.add_argument("--model", type=str, default="gpt-4.1-2025-04-14", help="LLM model")
    parser.add_argument("--benchmark", type=str, default="appworld",
                        choices=["appworld", "bfcl", "tau2bench"], help="Benchmark name")
    parser.add_argument("--skill-type", type=str, default="functional",
                        choices=["functional", "atomic", "hybrid"], help="Skill type")
    parser.add_argument("--domain", type=str, default="",
                        help="Domain name for tool-specific filtering (airline, retail, telecom, etc.)")
    parser.add_argument("--epochs", type=int, default=1, help="Number of extraction epochs")
    parser.add_argument("--threshold", type=float, default=0.999, help="Reward threshold")
    parser.add_argument("--batch-size", type=int, default=10, help="Batch size")
    parser.add_argument("--max-concurrent", type=int, default=5, help="Max concurrent")
    parser.add_argument("--plan-strategy", type=str, default="shortest",
                        choices=["shortest", "merge"],
                        help="Plan extraction strategy: 'shortest' (default, faster) or 'merge' (comprehensive)")
    parser.add_argument("--filter-timing", type=str, default="pre_merge",
                        choices=["pre_merge", "post_merge", "both", "none"],
                        help="When to apply filtering: 'pre_merge' (default), 'post_merge', 'both', or 'none'")
    parser.add_argument("--enable-expansion", action="store_true", help="Enable skill expansion")
    parser.add_argument("--env-url", type=str, default=None, help="Environment URL for expansion")

    args = parser.parse_args()

    asyncio.run(run_pipeline(
        trajectories_path=args.input,
        output_dir=args.output,
        model=args.model,
        benchmark=args.benchmark,
        skill_type=args.skill_type,
        domain=args.domain,
        plan_strategy=args.plan_strategy,
        num_epochs=args.epochs,
        filter_threshold=args.threshold,
        batch_size=args.batch_size,
        max_concurrent=args.max_concurrent,
        filter_timing=args.filter_timing,
        enable_expansion=args.enable_expansion,
        env_url=args.env_url
    ))
