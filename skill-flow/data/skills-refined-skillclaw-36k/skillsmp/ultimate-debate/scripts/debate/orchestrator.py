"""Ultimate debate orchestrator with 5-phase workflow."""

import asyncio
import uuid
from datetime import datetime
from typing import Any

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.base_client import BaseAIClient
from debate.consensus_checker import ConsensusChecker, ConsensusResult
from debate.context_manager import DebateContextManager


class UltimateDebate:
    """Orchestrate multi-AI debate with consensus checking."""

    def __init__(
        self,
        task: str,
        task_id: str | None = None,
        max_rounds: int = 5,
        consensus_threshold: float = 0.8,
    ):
        """Initialize debate orchestrator.

        Args:
            task: Task description to debate
            task_id: Optional task ID (generated if not provided)
            max_rounds: Maximum debate rounds before forced conclusion
            consensus_threshold: Minimum agreement ratio for full consensus
        """
        self.task = task
        self.task_id = task_id or self._generate_task_id()
        self.round = 0
        self.max_rounds = max_rounds
        self.consensus_threshold = consensus_threshold

        # Initialize components
        self.context_manager = DebateContextManager(self.task_id)
        self.consensus_checker = ConsensusChecker(threshold=consensus_threshold)

        # AI clients (placeholder - to be injected)
        self.ai_clients: dict[str, BaseAIClient] = {}

        # Debate state
        self.current_analyses: dict[str, dict[str, Any]] = {}
        self.consensus_result: ConsensusResult | None = None

    def _generate_task_id(self) -> str:
        """Generate unique task ID.

        Returns:
            UUID-based task ID
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        short_uuid = str(uuid.uuid4())[:8]
        return f"debate_{timestamp}_{short_uuid}"

    def register_ai_client(self, model_name: str, client: BaseAIClient) -> None:
        """Register an AI client for debate.

        Args:
            model_name: Model identifier (claude/gpt/gemini)
            client: AI client instance
        """
        self.ai_clients[model_name] = client

    async def run(self) -> dict[str, Any]:
        """Run complete debate workflow.

        Returns:
            Final debate result with consensus and strategy
        """
        # Save initial task
        self.context_manager.save_task(
            self.task,
            {
                "created_at": datetime.now().isoformat(),
                "max_rounds": self.max_rounds,
                "status": "RUNNING",
            },
        )

        while self.round < self.max_rounds:
            print(f"\n=== Round {self.round} ===")

            # Phase 1: Parallel analysis
            print("Phase 1: Parallel Analysis")
            analyses = await self.run_parallel_analysis()

            # Phase 2: Consensus check (initial)
            print("Phase 2: Initial Consensus Check")
            self.consensus_result = self.consensus_checker.check_consensus(
                list(analyses.values())
            )

            # Save consensus result
            self.context_manager.save_consensus_result(
                self.round,
                {
                    "status": self.consensus_result.status,
                    "agreed_items": self.consensus_result.agreed_items,
                    "disputed_items": self.consensus_result.disputed_items,
                    "consensus_percentage": self.consensus_result.consensus_percentage,
                    "next_action": self.consensus_result.next_action,
                },
            )

            # Check if consensus reached
            if self.is_consensus_reached():
                print(
                    f"Consensus reached! ({self.consensus_result.consensus_percentage * 100:.1f}%)"
                )
                break

            # Phase 3: Cross review
            if self.consensus_result.next_action == "CROSS_REVIEW":
                print("Phase 3: Cross Review")
                reviews = await self.run_cross_review()

                # Re-check consensus after review
                review_consensus = self.consensus_checker.check_cross_review_consensus(
                    list(reviews.values())
                )

                if review_consensus.status == "FULL_CONSENSUS":
                    self.consensus_result = review_consensus
                    break

            # Phase 4: Debate round
            if self.consensus_result.next_action == "DEBATE":
                print("Phase 4: Debate Round")
                debate_results = await self.run_debate_round()

                # Update analyses with debate results
                for model, result in debate_results.items():
                    self.current_analyses[model]["conclusion"] = result.get(
                        "updated_position", ""
                    )

            self.round += 1

        # Phase 5: Final strategy
        print("Phase 5: Final Strategy")
        final_result = self.get_final_strategy()

        # Generate FINAL.md
        self.context_manager.generate_final_md(final_result)

        return final_result

    async def run_parallel_analysis(self) -> dict[str, dict[str, Any]]:
        """Phase 1: Run parallel analysis from all AI models.

        Returns:
            Dict mapping model name to analysis result
        """
        if not self.ai_clients:
            # Placeholder: mock responses when no real clients
            return self._mock_parallel_analysis()

        tasks = []
        model_names = []

        for model_name, client in self.ai_clients.items():
            tasks.append(client.analyze(self.task))
            model_names.append(model_name)

        results = await asyncio.gather(*tasks)

        analyses = {}
        for model_name, result in zip(model_names, results):
            result["model"] = model_name
            analyses[model_name] = result

            # Save to context
            self.context_manager.save_round(self.round, model_name, result)

        self.current_analyses = analyses
        return analyses

    async def run_cross_review(self) -> dict[str, dict[str, Any]]:
        """Phase 2: Run cross-review between models.

        Returns:
            Dict mapping reviewer-reviewed pair to review result
        """
        if not self.ai_clients:
            # Placeholder: mock reviews
            return self._mock_cross_review()

        reviews = {}
        tasks = []
        review_keys = []

        for reviewer_name, reviewer_client in self.ai_clients.items():
            for reviewed_name, reviewed_analysis in self.current_analyses.items():
                if reviewer_name == reviewed_name:
                    continue

                own_analysis = self.current_analyses[reviewer_name]

                tasks.append(
                    reviewer_client.review(self.task, reviewed_analysis, own_analysis)
                )
                review_keys.append((reviewer_name, reviewed_name))

        results = await asyncio.gather(*tasks)

        for (reviewer_name, reviewed_name), result in zip(review_keys, results):
            key = f"{reviewer_name}_reviews_{reviewed_name}"
            reviews[key] = result

            # Save to context
            self.context_manager.save_cross_review(
                self.round, reviewer_name, reviewed_name, result
            )

        return reviews

    def is_consensus_reached(self) -> bool:
        """Phase 3: Check if consensus is reached.

        Returns:
            True if full consensus reached
        """
        if not self.consensus_result:
            return False

        return self.consensus_result.status == "FULL_CONSENSUS"

    async def run_debate_round(self) -> dict[str, dict[str, Any]]:
        """Phase 4: Run debate round for disputed items.

        Returns:
            Dict mapping model name to updated position
        """
        if not self.ai_clients:
            # Placeholder: mock debate
            return self._mock_debate_round()

        debates = {}
        tasks = []
        model_names = []

        for model_name, client in self.ai_clients.items():
            own_position = self.current_analyses[model_name]
            opposing_views = [
                analysis
                for name, analysis in self.current_analyses.items()
                if name != model_name
            ]

            tasks.append(client.debate(self.task, own_position, opposing_views))
            model_names.append(model_name)

        results = await asyncio.gather(*tasks)

        for model_name, result in zip(model_names, results):
            debates[model_name] = result

            # Save to context
            self.context_manager.save_debate_round(self.round, model_name, result)

        return debates

    def get_final_strategy(self) -> dict[str, Any]:
        """Phase 5: Generate final strategy from consensus.

        Returns:
            Final result dict with strategy and metadata
        """
        if not self.consensus_result:
            return {
                "status": "FAILED",
                "final_strategy": {},
                "total_rounds": self.round,
                "consensus_percentage": 0.0,
                "task_id": self.task_id,
            }

        # Extract final strategy from agreed items
        final_strategy = {}
        if self.consensus_result.agreed_items:
            most_agreed = self.consensus_result.agreed_items[0]
            final_strategy = {
                "conclusion": most_agreed.get("conclusion", ""),
                "supporting_models": most_agreed.get("models", []),
                "confidence": self.consensus_result.consensus_percentage,
            }

        return {
            "status": self.consensus_result.status,
            "final_strategy": final_strategy,
            "total_rounds": self.round,
            "consensus_percentage": self.consensus_result.consensus_percentage,
            "task_id": self.task_id,
            "agreed_items": self.consensus_result.agreed_items,
            "disputed_items": self.consensus_result.disputed_items,
        }

    def get_status(self) -> dict[str, Any]:
        """Get current debate status.

        Returns:
            Status dict
        """
        context_status = self.context_manager.get_status()

        return {
            "task_id": self.task_id,
            "current_round": self.round,
            "max_rounds": self.max_rounds,
            "consensus_status": (
                self.consensus_result.status if self.consensus_result else "PENDING"
            ),
            "consensus_percentage": (
                self.consensus_result.consensus_percentage
                if self.consensus_result
                else 0.0
            ),
            "registered_models": list(self.ai_clients.keys()),
            "context": context_status,
        }

    # Placeholder methods for testing without real AI clients
    def _mock_parallel_analysis(self) -> dict[str, dict[str, Any]]:
        """Generate mock parallel analysis results."""
        models = ["claude", "gpt", "gemini"]
        analyses = {}

        for model in models:
            analysis = {
                "model": model,
                "analysis": f"Mock analysis from {model}",
                "conclusion": f"Mock conclusion from {model}",
                "confidence": 0.85,
            }
            analyses[model] = analysis
            self.context_manager.save_round(self.round, model, analysis)

        self.current_analyses = analyses
        return analyses

    def _mock_cross_review(self) -> dict[str, dict[str, Any]]:
        """Generate mock cross-review results."""
        models = ["claude", "gpt", "gemini"]
        reviews = {}

        for reviewer in models:
            for reviewed in models:
                if reviewer == reviewed:
                    continue

                review = {
                    "feedback": f"{reviewer} reviews {reviewed}",
                    "agreement_points": ["Point 1", "Point 2"],
                    "disagreement_points": ["Point 3"],
                }
                key = f"{reviewer}_reviews_{reviewed}"
                reviews[key] = review

                self.context_manager.save_cross_review(
                    self.round, reviewer, reviewed, review
                )

        return reviews

    def _mock_debate_round(self) -> dict[str, dict[str, Any]]:
        """Generate mock debate round results."""
        models = ["claude", "gpt", "gemini"]
        debates = {}

        for model in models:
            debate = {
                "updated_position": f"Updated position from {model}",
                "rebuttals": ["Rebuttal 1", "Rebuttal 2"],
                "concessions": ["Concession 1"],
            }
            debates[model] = debate

            self.context_manager.save_debate_round(self.round, model, debate)

        return debates
