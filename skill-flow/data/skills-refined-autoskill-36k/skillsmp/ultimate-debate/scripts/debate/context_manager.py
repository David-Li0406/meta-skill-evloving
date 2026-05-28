"""Debate context management with MD file persistence."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class DebateContextManager:
    """Manage debate context using markdown files for context efficiency."""

    def __init__(self, task_id: str):
        """Initialize context manager.

        Args:
            task_id: Unique identifier for this debate task
        """
        self.task_id = task_id
        self.base_path = Path(".claude/debates") / task_id
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save_task(self, task: str, metadata: dict[str, Any] | None = None) -> str:
        """Save initial task description.

        Args:
            task: Task description
            metadata: Optional metadata (created_at, etc.)

        Returns:
            Path to saved file
        """
        file_path = self.base_path / "TASK.md"

        content = f"""# Task: {self.task_id}

## Description
{task}

## Metadata
- Created: {metadata.get('created_at', datetime.now().isoformat()) if metadata else datetime.now().isoformat()}
- Status: {metadata.get('status', 'RUNNING') if metadata else 'RUNNING'}
- Max Rounds: {metadata.get('max_rounds', 5) if metadata else 5}
"""

        file_path.write_text(content, encoding="utf-8")
        return str(file_path)

    def save_round(self, round_num: int, model: str, content: dict[str, Any]) -> str:
        """Save analysis round result.

        Args:
            round_num: Round number (0-based)
            model: Model name (claude/gpt/gemini)
            content: Analysis content (analysis, conclusion, confidence)

        Returns:
            Path to saved file
        """
        round_dir = self.base_path / f"round_{round_num:02d}"
        round_dir.mkdir(exist_ok=True)

        file_path = round_dir / f"{model}.md"

        analysis = content.get("analysis", "")
        conclusion = content.get("conclusion", "")
        confidence = content.get("confidence", 0.0)

        content_md = f"""# Round {round_num} - {model}

## Analysis
{analysis}

## Conclusion
{conclusion}

## Confidence
{confidence}

## Timestamp
{datetime.now().isoformat()}
"""

        file_path.write_text(content_md, encoding="utf-8")
        return str(file_path)

    def save_cross_review(
        self, round_num: int, reviewer: str, reviewed: str, content: dict[str, Any]
    ) -> str:
        """Save cross-review result.

        Args:
            round_num: Round number
            reviewer: Model doing the review
            reviewed: Model being reviewed
            content: Review content (feedback, agreement_points, disagreement_points)

        Returns:
            Path to saved file
        """
        review_dir = self.base_path / f"round_{round_num:02d}" / "reviews"
        review_dir.mkdir(exist_ok=True)

        file_path = review_dir / f"{reviewer}_reviews_{reviewed}.md"

        feedback = content.get("feedback", "")
        agreement_points = content.get("agreement_points", [])
        disagreement_points = content.get("disagreement_points", [])

        content_md = f"""# Cross Review: {reviewer} → {reviewed}

## Feedback
{feedback}

## Agreement Points
{self._format_list(agreement_points)}

## Disagreement Points
{self._format_list(disagreement_points)}

## Timestamp
{datetime.now().isoformat()}
"""

        file_path.write_text(content_md, encoding="utf-8")
        return str(file_path)

    def save_consensus_result(self, round_num: int, result: dict[str, Any]) -> str:
        """Save consensus checking result.

        Args:
            round_num: Round number
            result: Consensus result data

        Returns:
            Path to saved file
        """
        file_path = self.base_path / f"round_{round_num:02d}" / "CONSENSUS.md"

        status = result.get("status", "UNKNOWN")
        agreed_items = result.get("agreed_items", [])
        disputed_items = result.get("disputed_items", [])
        consensus_percentage = result.get("consensus_percentage", 0.0)
        next_action = result.get("next_action")

        content = f"""# Consensus Check - Round {round_num}

## Status
**{status}** ({consensus_percentage * 100:.1f}% consensus)

## Agreed Items
{self._format_items(agreed_items)}

## Disputed Items
{self._format_items(disputed_items)}

## Next Action
{next_action or "None - Consensus reached"}

## Timestamp
{datetime.now().isoformat()}
"""

        file_path.write_text(content, encoding="utf-8")
        return str(file_path)

    def save_debate_round(
        self, round_num: int, model: str, content: dict[str, Any]
    ) -> str:
        """Save debate round result.

        Args:
            round_num: Round number
            model: Model name
            content: Debate content (updated_position, rebuttals, concessions)

        Returns:
            Path to saved file
        """
        debate_dir = self.base_path / f"round_{round_num:02d}" / "debates"
        debate_dir.mkdir(exist_ok=True)

        file_path = debate_dir / f"{model}.md"

        updated_position = content.get("updated_position", "")
        rebuttals = content.get("rebuttals", [])
        concessions = content.get("concessions", [])

        content_md = f"""# Debate Round {round_num} - {model}

## Updated Position
{updated_position}

## Rebuttals
{self._format_list(rebuttals)}

## Concessions
{self._format_list(concessions)}

## Timestamp
{datetime.now().isoformat()}
"""

        file_path.write_text(content_md, encoding="utf-8")
        return str(file_path)

    def generate_final_md(self, result: dict[str, Any]) -> str:
        """Generate final summary markdown.

        Args:
            result: Final consensus result

        Returns:
            Path to FINAL.md
        """
        file_path = self.base_path / "FINAL.md"

        status = result.get("status", "UNKNOWN")
        final_strategy = result.get("final_strategy", {})
        total_rounds = result.get("total_rounds", 0)
        consensus_percentage = result.get("consensus_percentage", 0.0)

        content = f"""# Final Result - {self.task_id}

## Status
**{status}** ({consensus_percentage * 100:.1f}% consensus)

## Final Strategy
{json.dumps(final_strategy, indent=2, ensure_ascii=False)}

## Summary
- Total Rounds: {total_rounds}
- Consensus Reached: {status == 'FULL_CONSENSUS'}

## Timestamp
{datetime.now().isoformat()}

---
Generated by Ultimate Debate Skill
"""

        file_path.write_text(content, encoding="utf-8")
        return str(file_path)

    def load_round(self, round_num: int, model: str) -> dict[str, Any]:
        """Load analysis round result.

        Args:
            round_num: Round number
            model: Model name

        Returns:
            Analysis content dict
        """
        file_path = self.base_path / f"round_{round_num:02d}" / f"{model}.md"

        if not file_path.exists():
            return {}

        content = file_path.read_text(encoding="utf-8")

        # Simple parsing (could be enhanced with frontmatter parser)
        result = {
            "raw_content": content,
            "file_path": str(file_path),
        }

        return result

    def load_consensus_result(self, round_num: int) -> dict[str, Any]:
        """Load consensus result.

        Args:
            round_num: Round number

        Returns:
            Consensus result dict
        """
        file_path = self.base_path / f"round_{round_num:02d}" / "CONSENSUS.md"

        if not file_path.exists():
            return {}

        content = file_path.read_text(encoding="utf-8")

        return {
            "raw_content": content,
            "file_path": str(file_path),
        }

    def get_status(self) -> dict[str, Any]:
        """Get current debate status.

        Returns:
            Status dict with rounds, files, etc.
        """
        rounds = sorted(self.base_path.glob("round_*"))

        return {
            "task_id": self.task_id,
            "base_path": str(self.base_path),
            "total_rounds": len(rounds),
            "rounds": [r.name for r in rounds],
            "has_final": (self.base_path / "FINAL.md").exists(),
        }

    def _format_list(self, items: list[str]) -> str:
        """Format list as markdown bullets.

        Args:
            items: List of strings

        Returns:
            Markdown formatted list
        """
        if not items:
            return "- (None)"

        return "\n".join(f"- {item}" for item in items)

    def _format_items(self, items: list[dict[str, Any]]) -> str:
        """Format items with models and counts.

        Args:
            items: List of item dicts

        Returns:
            Markdown formatted items
        """
        if not items:
            return "- (None)"

        result = []
        for item in items:
            conclusion = item.get("conclusion", "")
            models = item.get("models", [])
            count = item.get("count", 0)
            result.append(
                f"- **{conclusion}** (Models: {', '.join(models)}, Count: {count})"
            )

        return "\n".join(result)
