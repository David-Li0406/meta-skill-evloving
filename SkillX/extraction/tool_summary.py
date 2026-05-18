"""Tool response summarization for long feedback compression."""

import re
import asyncio
import logging
from typing import Dict, Optional, List
from copy import deepcopy
from tqdm import tqdm

try:
    from ..prompts.registry import PromptRegistry
except ImportError:
    from prompts.registry import PromptRegistry

logger = logging.getLogger(__name__)


class ToolSummary:
    """
    Summarize long tool/environment feedback in trajectories.

    Compresses verbose API responses while preserving key information
    relevant to the agent's intent.
    """

    def __init__(
        self,
        llm,
        max_len: int = 1500,
        verbose: bool = True
    ):
        """
        Initialize ToolSummary.

        Args:
            llm: LLM instance for summarization
            max_len: Maximum content length before summarization
            verbose: Whether to output verbose logs
        """
        self.llm = llm
        self.max_len = max_len
        self.verbose = verbose

    def _extract_feedback(self, text: str) -> Optional[str]:
        """Extract feedback from LLM response."""
        match = re.search(r"<feedback>(.*?)</feedback>", text, flags=re.S)
        if match:
            return match.group(1).strip()
        if self.verbose:
            logger.warning("No <feedback> block found in response")
        return None

    async def summarize_step(
        self,
        assistant_content: str,
        environment_feedback: str,
        **kwargs
    ) -> str:
        """
        Summarize a single tool response.

        Args:
            assistant_content: The assistant's action/reasoning
            environment_feedback: The environment's response

        Returns:
            Summarized feedback
        """
        prompt = PromptRegistry.get("tool_summary", "default")
        messages = [
            ("system", prompt),
            ("human", (
                f"# The AI Assistant Action: {assistant_content}\n\n"
                f"# The environment feedback: {environment_feedback}"
            ))
        ]

        response = await self.llm.ainvoke(
            messages=messages,
            regex_extractor=self._extract_feedback,
            **kwargs
        )

        feedback = self._extract_feedback(response)
        return feedback if feedback else environment_feedback

    async def summarize_trajectory(
        self,
        trajectory_item: Dict,
        **kwargs
    ) -> Dict:
        """
        Summarize all long tool responses in a trajectory.

        Args:
            trajectory_item: Dictionary with 'trajectory' key

        Returns:
            Item with summarized trajectory
        """
        result = deepcopy(trajectory_item)
        trajectory = result.get("trajectory", result.get("task_history", []))

        for idx, step in enumerate(trajectory):
            # Check if this is a user/tool response that's too long
            if step.get("role") in ["user", "tool"] and len(step.get("content", "")) > self.max_len:
                # Get preceding assistant action
                if idx > 0:
                    assistant_content = trajectory[idx - 1].get("content", "")
                else:
                    assistant_content = ""

                # Summarize
                summarized = await self.summarize_step(
                    assistant_content=assistant_content,
                    environment_feedback=step["content"],
                    **kwargs
                )

                # Update trajectory
                if "trajectory" in result:
                    result["trajectory"][idx]["content"] = summarized
                else:
                    result["task_history"][idx]["content"] = summarized

        if self.verbose:
            logger.info("Trajectory summarization complete")

        return result

    async def _process_batch(
        self,
        batch: List[Dict],
        pbar: Optional[tqdm],
        **kwargs
    ) -> List[Dict]:
        """Process a batch of trajectories."""
        tasks = [
            self.summarize_trajectory(item, **kwargs)
            for item in batch
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error summarizing trajectory: {result}")
                processed.append(batch[i])  # Keep original on error
            else:
                processed.append(result)

            if pbar:
                pbar.update(1)

        return processed

    async def summarize_multiple(
        self,
        items: List[Dict],
        batch_size: int = 10,
        max_concurrent: int = 5,
        show_progress: bool = True,
        **kwargs
    ) -> List[Dict]:
        """
        Summarize multiple trajectories.

        Args:
            items: List of trajectory items
            batch_size: Batch size for processing
            max_concurrent: Maximum concurrent batches
            show_progress: Whether to show progress bar

        Returns:
            List of items with summarized trajectories
        """
        logger.info(f"Summarizing {len(items)} trajectories")

        # Create batches
        batches = []
        for i in range(0, len(items), batch_size):
            batches.append(items[i:i + batch_size])

        logger.info(
            f"Processing in {len(batches)} batches "
            f"(batch_size: {batch_size}, max_concurrent: {max_concurrent})"
        )

        # Progress bar
        pbar = None
        if show_progress:
            pbar = tqdm(
                total=len(items),
                desc="Summarizing trajectories",
                unit="item",
                ncols=100
            )

        final_results = []

        try:
            semaphore = asyncio.Semaphore(max_concurrent)

            async def process_with_semaphore(batch):
                async with semaphore:
                    return await self._process_batch(batch, pbar, **kwargs)

            batch_tasks = [
                process_with_semaphore(batch)
                for batch in batches
            ]

            all_results = await asyncio.gather(*batch_tasks)

            for batch_results in all_results:
                final_results.extend(batch_results)

        finally:
            if pbar:
                pbar.close()

        success_count = sum(1 for r in final_results if r is not None)
        logger.info(
            f"Summarization complete: {success_count}/{len(items)} successful"
        )

        return final_results
