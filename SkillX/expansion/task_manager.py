"""Task synthesis manager for skill expansion.

Abstracted from AgentEvolver's TaskManager to provide:
1. Exploration: Generate trajectories from seed tasks
2. Summarization: Convert trajectories to new tasks
3. Filtering: Quality control for synthetic tasks
4. Deduplication: Avoid generating duplicate tasks
"""

import json
import uuid
import asyncio
import hashlib
import logging
from typing import List, Dict, Any, Optional, Set
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

from .strategies.base import ExplorationStrategy, TaskObjective

logger = logging.getLogger(__name__)


class TaskPostFilter:
    """Base class for post-generation task filters."""

    def filter(self, tasks: List[Dict]) -> List[Dict]:
        """
        Filter a list of tasks.

        Args:
            tasks: List of task dictionaries

        Returns:
            Filtered list of tasks
        """
        return tasks


class DuplicateFilter(TaskPostFilter):
    """Filter to remove duplicate tasks based on query similarity."""

    def __init__(self, existing_queries: Optional[Set[str]] = None):
        self.existing_queries = existing_queries or set()

    def add_query(self, query: str) -> None:
        """Add a query to the existing set."""
        self.existing_queries.add(self._normalize_query(query))

    def filter(self, tasks: List[Dict]) -> List[Dict]:
        """Remove tasks with duplicate queries."""
        filtered = []
        for task in tasks:
            query = task.get("query", "")
            normalized = self._normalize_query(query)
            if normalized and normalized not in self.existing_queries:
                filtered.append(task)
                self.existing_queries.add(normalized)
        return filtered

    def _normalize_query(self, query: str) -> str:
        """Normalize query for comparison."""
        return query.lower().strip()


class ConfidenceFilter(TaskPostFilter):
    """Filter tasks below a confidence threshold."""

    def __init__(self, min_confidence: float = 0.5):
        self.min_confidence = min_confidence

    def filter(self, tasks: List[Dict]) -> List[Dict]:
        return [
            t for t in tasks
            if t.get("confidence", 0) >= self.min_confidence
        ]


class TaskSynthesisManager:
    """
    Manager for synthetic task generation.

    This class abstracts AgentEvolver's TaskManager, providing:
    1. Exploration strategy: Generate trajectories from seed tasks
    2. Summarization: Convert trajectories to task objectives
    3. Post-filtering: Quality control for generated tasks
    4. Deduplication: Track existing tasks to avoid duplicates
    5. Checkpoint support: Resume interrupted generation

    Usage:
        manager = TaskSynthesisManager(
            llm=llm,
            exploration_strategy=RandomExplorationStrategy(llm),
            n_rollouts=3
        )

        seed_tasks = [{"task_id": "1", "user_task": "Book a flight"}]
        new_tasks = await manager.generate_tasks(seed_tasks)
    """

    def __init__(
        self,
        llm,
        exploration_strategy: ExplorationStrategy,
        env_client: Optional[Any] = None,
        n_rollouts: int = 1,
        num_threads: int = 10,
        post_filters: Optional[List[TaskPostFilter]] = None,
        verbose: bool = True
    ):
        """
        Initialize task synthesis manager.

        Args:
            llm: LLM instance
            exploration_strategy: Strategy for exploration and summarization
            env_client: Optional environment client
            n_rollouts: Number of exploration rollouts per seed task
            num_threads: Maximum concurrent exploration threads
            post_filters: List of post-generation filters
            verbose: Whether to output verbose logs
        """
        self.llm = llm
        self.exploration_strategy = exploration_strategy
        self.env_client = env_client
        self.n_rollouts = n_rollouts
        self.num_threads = num_threads
        self.verbose = verbose

        # Set up exploration strategy dependencies
        self.exploration_strategy.inject_dependencies(llm=llm, env_client=env_client)

        # Initialize filters
        self.duplicate_filter = DuplicateFilter()
        self.post_filters = post_filters or [
            self.duplicate_filter,
            ConfidenceFilter(min_confidence=0.3)
        ]

        # Track generated tasks
        self.generated_tasks: List[Dict] = []
        self.seed_tasks: List[Dict] = []

    def load_seed_tasks(self, tasks: List[Dict]) -> None:
        """
        Load seed tasks for generation.

        Args:
            tasks: List of seed task dictionaries
        """
        self.seed_tasks = tasks
        logger.info(f"Loaded {len(tasks)} seed tasks")

    def add_existing_queries(self, queries: List[str]) -> None:
        """
        Add existing queries to avoid duplicates.

        Args:
            queries: List of existing task queries
        """
        for query in queries:
            self.duplicate_filter.add_query(query)

    async def generate_tasks(
        self,
        seed_tasks: Optional[List[Dict]] = None,
        show_progress: bool = True,
        checkpoint_file: Optional[str] = None
    ) -> List[Dict]:
        """
        Generate synthetic tasks from seed tasks.

        Args:
            seed_tasks: Seed tasks (uses loaded tasks if not provided)
            show_progress: Whether to show progress bar
            checkpoint_file: Optional file for checkpointing

        Returns:
            List of generated task dictionaries
        """
        if seed_tasks is not None:
            self.seed_tasks = seed_tasks

        if not self.seed_tasks:
            logger.warning("No seed tasks provided")
            return []

        # Prepare task queue (n_rollouts per seed task)
        task_queue = self.seed_tasks * self.n_rollouts
        logger.info(f"Generating tasks from {len(self.seed_tasks)} seeds "
                   f"with {self.n_rollouts} rollouts ({len(task_queue)} total)")

        # Load checkpoint if exists
        processed_indices = set()
        results = []
        if checkpoint_file:
            results, processed_indices = self._load_checkpoint(
                checkpoint_file,
                self.seed_tasks
            )

        # Process in batches
        parallel_num = min(self.num_threads, len(self.seed_tasks))

        if show_progress:
            pbar = tqdm(total=len(task_queue), desc="Generating tasks", unit="task")
            pbar.update(len(processed_indices) * parallel_num)
        else:
            pbar = None

        try:
            batch_indices = list(range(0, len(task_queue), parallel_num))

            for idx, i in enumerate(batch_indices):
                if idx in processed_indices:
                    continue

                batch = task_queue[i:i + parallel_num]
                batch_results = await self._process_batch(batch)

                results.extend(batch_results)

                # Apply filters
                results = self._apply_filters(results)

                # Update duplicate tracker
                for task in batch_results:
                    query = task.get("query", "")
                    if query:
                        self.duplicate_filter.add_query(query)

                processed_indices.add(idx)

                if pbar:
                    pbar.update(len(batch))

                # Save checkpoint
                if checkpoint_file:
                    self._save_checkpoint(checkpoint_file, results, processed_indices, self.seed_tasks)

        finally:
            if pbar:
                pbar.close()

        # Final filtering
        results = self._apply_filters(results)

        self.generated_tasks = results
        logger.info(f"Generated {len(results)} unique tasks")

        return results

    async def _process_batch(self, batch: List[Dict]) -> List[Dict]:
        """Process a batch of seed tasks."""
        tasks = [
            self._explore_and_summarize(task)
            for task in batch
        ]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)

        results = []
        for result in batch_results:
            if isinstance(result, Exception):
                logger.error(f"Error in batch processing: {result}")
            elif result:
                results.extend(result)

        return results

    async def _explore_and_summarize(self, seed_task: Dict) -> List[Dict]:
        """
        Explore from seed task and summarize to new tasks.

        Args:
            seed_task: Seed task dictionary

        Returns:
            List of generated task objectives
        """
        try:
            # Step 1: Explore
            trajectories = await self.exploration_strategy.explore(seed_task)

            if not trajectories:
                logger.debug(f"No trajectories from seed: {seed_task.get('task_id', 'unknown')}")
                return []

            # Step 2: Summarize each trajectory
            all_objectives = []
            for trajectory in trajectories:
                objectives = await self.exploration_strategy.summarize(seed_task, trajectory)
                all_objectives.extend(objectives)

            # Add metadata
            for obj in all_objectives:
                obj["source_seed_task"] = seed_task.get("task_id", "unknown")
                obj["generated_at"] = datetime.now().isoformat()

            return all_objectives

        except Exception as e:
            logger.error(f"Error in explore_and_summarize: {e}")
            return []

    def _apply_filters(self, tasks: List[Dict]) -> List[Dict]:
        """Apply all post-filters to tasks."""
        result = tasks
        for filter_obj in self.post_filters:
            result = filter_obj.filter(result)
        return result

    def _compute_tasks_hash(self, tasks: List[Dict]) -> str:
        """Compute hash of seed tasks for checkpoint validation."""
        task_strs = [f"{t.get('task_id', '')}:{t.get('user_task', '')}" for t in tasks]
        combined = "|".join(task_strs)
        return hashlib.md5(combined.encode()).hexdigest()

    def _save_checkpoint(
        self,
        filepath: str,
        results: List[Dict],
        processed_indices: Set[int],
        seed_tasks: List[Dict]
    ) -> None:
        """Save checkpoint to file."""
        try:
            checkpoint = {
                "results": results,
                "processed_indices": list(processed_indices),
                "tasks_hash": self._compute_tasks_hash(seed_tasks),
                "timestamp": datetime.now().isoformat()
            }
            with open(filepath, "w") as f:
                json.dump(checkpoint, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save checkpoint: {e}")

    def _load_checkpoint(
        self,
        filepath: str,
        seed_tasks: List[Dict]
    ) -> tuple:
        """Load checkpoint from file."""
        import os

        results = []
        processed_indices = set()

        if not os.path.exists(filepath):
            return results, processed_indices

        try:
            with open(filepath, "r") as f:
                checkpoint = json.load(f)

            # Validate hash
            current_hash = self._compute_tasks_hash(seed_tasks)
            if checkpoint.get("tasks_hash") != current_hash:
                logger.warning("Checkpoint hash mismatch, starting fresh")
                os.remove(filepath)
                return results, processed_indices

            results = checkpoint.get("results", [])
            processed_indices = set(checkpoint.get("processed_indices", []))
            logger.info(f"Loaded checkpoint: {len(results)} results, "
                       f"{len(processed_indices)} batches processed")

        except Exception as e:
            logger.warning(f"Failed to load checkpoint: {e}")

        return results, processed_indices

    def tasks_to_trajectories(
        self,
        tasks: Optional[List[Dict]] = None,
        epoch: int = 1
    ) -> List[Dict]:
        """
        Convert generated tasks to trajectory format for skill extraction.

        Args:
            tasks: Tasks to convert (uses generated_tasks if not provided)
            epoch: Current epoch number

        Returns:
            List of trajectory-formatted dictionaries
        """
        if tasks is None:
            tasks = self.generated_tasks

        trajectories = []
        for task in tasks:
            trajectory = {
                "trajectory_id": f"synthetic_{uuid.uuid4().hex[:8]}",
                "benchmark": "synthetic",
                "task_id": task.get("task_id", f"synthetic_{uuid.uuid4().hex[:8]}"),
                "user_task": task.get("query", task.get("user_task", "")),
                "task_history": [],  # To be filled by agent execution
                "reward": None,  # Not yet evaluated
                "metadata": {
                    "source": "task_synthesis",
                    "epoch": epoch,
                    "confidence": task.get("confidence", 0.5),
                    "action_sequence": task.get("action_sequence", ""),
                    "source_seed_task": task.get("source_seed_task", ""),
                    "generated_at": task.get("generated_at", datetime.now().isoformat())
                }
            }
            trajectories.append(trajectory)

        return trajectories

    def get_statistics(self) -> Dict[str, Any]:
        """Get generation statistics."""
        return {
            "seed_tasks": len(self.seed_tasks),
            "n_rollouts": self.n_rollouts,
            "generated_tasks": len(self.generated_tasks),
            "unique_queries": len(self.duplicate_filter.existing_queries),
            "num_filters": len(self.post_filters)
        }
