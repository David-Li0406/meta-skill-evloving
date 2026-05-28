"""Consensus checking logic with hash-based comparison."""

import hashlib
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConsensusResult:
    """Result of consensus checking."""

    status: str  # FULL_CONSENSUS | PARTIAL_CONSENSUS | NO_CONSENSUS
    agreed_items: list[dict[str, Any]] = field(default_factory=list)
    disputed_items: list[dict[str, Any]] = field(default_factory=list)
    consensus_percentage: float = 0.0
    next_action: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


class ConsensusChecker:
    """Check consensus across multiple AI analyses."""

    def __init__(self, threshold: float = 0.8):
        """Initialize consensus checker.

        Args:
            threshold: Minimum agreement ratio for FULL_CONSENSUS (default: 0.8)
        """
        self.threshold = threshold

    def check_consensus(self, analyses: list[dict[str, Any]]) -> ConsensusResult:
        """Check consensus by comparing conclusion hashes.

        Args:
            analyses: List of AI analyses with 'conclusion' field

        Returns:
            ConsensusResult with status and detailed breakdown
        """
        if len(analyses) < 2:
            return ConsensusResult(
                status="NO_CONSENSUS",
                next_action="NEED_MORE_ANALYSES",
                details={"reason": "Not enough analyses to compare"},
            )

        # Extract conclusions and compute hashes
        conclusion_hashes = []
        conclusion_map = {}

        for analysis in analyses:
            conclusion = self._normalize_conclusion(analysis.get("conclusion", ""))
            hash_value = self._compute_hash(conclusion)
            conclusion_hashes.append(hash_value)

            if hash_value not in conclusion_map:
                conclusion_map[hash_value] = {
                    "text": conclusion,
                    "count": 0,
                    "models": [],
                }
            conclusion_map[hash_value]["count"] += 1
            conclusion_map[hash_value]["models"].append(
                analysis.get("model", "unknown")
            )

        # Find most common conclusion
        sorted_conclusions = sorted(
            conclusion_map.items(), key=lambda x: x[1]["count"], reverse=True
        )
        most_common_hash, most_common_data = sorted_conclusions[0]

        # Calculate consensus percentage
        total_count = len(analyses)
        consensus_count = most_common_data["count"]
        consensus_percentage = consensus_count / total_count

        # Determine agreed and disputed items
        agreed_items = []
        disputed_items = []

        for hash_value, data in conclusion_map.items():
            item = {
                "conclusion": data["text"],
                "models": data["models"],
                "count": data["count"],
            }

            if hash_value == most_common_hash:
                agreed_items.append(item)
            else:
                disputed_items.append(item)

        # Determine status and next action
        if consensus_percentage >= self.threshold:
            status = "FULL_CONSENSUS"
            next_action = None
        elif consensus_percentage >= 0.5:
            status = "PARTIAL_CONSENSUS"
            next_action = "CROSS_REVIEW"
        else:
            status = "NO_CONSENSUS"
            next_action = "DEBATE"

        return ConsensusResult(
            status=status,
            agreed_items=agreed_items,
            disputed_items=disputed_items,
            consensus_percentage=consensus_percentage,
            next_action=next_action,
            details={
                "total_analyses": total_count,
                "unique_conclusions": len(conclusion_map),
                "most_common_count": consensus_count,
            },
        )

    def _normalize_conclusion(self, conclusion: str) -> str:
        """Normalize conclusion text for comparison.

        Args:
            conclusion: Raw conclusion text

        Returns:
            Normalized conclusion string
        """
        # Remove extra whitespace, convert to lowercase
        normalized = " ".join(conclusion.lower().strip().split())
        return normalized

    def _compute_hash(self, text: str) -> str:
        """Compute hash of text for comparison.

        Args:
            text: Text to hash

        Returns:
            SHA-256 hash string
        """
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def check_cross_review_consensus(
        self, reviews: list[dict[str, Any]]
    ) -> ConsensusResult:
        """Check consensus from cross-review feedback.

        Args:
            reviews: List of cross-review results

        Returns:
            ConsensusResult based on agreement/disagreement points
        """
        if not reviews:
            return ConsensusResult(
                status="NO_CONSENSUS",
                next_action="NEED_REVIEWS",
            )

        # Count agreement and disagreement points
        total_agreement_points = 0
        total_disagreement_points = 0

        for review in reviews:
            total_agreement_points += len(review.get("agreement_points", []))
            total_disagreement_points += len(review.get("disagreement_points", []))

        total_points = total_agreement_points + total_disagreement_points
        if total_points == 0:
            agreement_ratio = 0.0
        else:
            agreement_ratio = total_agreement_points / total_points

        # Determine status
        if agreement_ratio >= self.threshold:
            status = "FULL_CONSENSUS"
            next_action = None
        elif agreement_ratio >= 0.5:
            status = "PARTIAL_CONSENSUS"
            next_action = "DEBATE"
        else:
            status = "NO_CONSENSUS"
            next_action = "DEBATE"

        return ConsensusResult(
            status=status,
            consensus_percentage=agreement_ratio,
            next_action=next_action,
            details={
                "total_reviews": len(reviews),
                "agreement_points": total_agreement_points,
                "disagreement_points": total_disagreement_points,
            },
        )
