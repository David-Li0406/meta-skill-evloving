"""Unified data schema bridging SkillRouter and SkillFlow.

Both benchmarks derive ground truth from SkillsBench, so their tasks overlap;
only the skill pools differ. These models normalize a skill, a task, and the
gold standard so either benchmark can serve as the train or held-out set.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Skill(BaseModel):
    """A single skill in a pool. ``body`` is the full SKILL.md / skill text."""

    id: str
    name: str = ""
    description: str = ""
    body: str = ""
    source: str = ""  # "skillrouter" | "skillflow" | "gt" | "merged" | ...

    def routing_text(self, desc_max: int = 500, body_max: int = 8000) -> str:
        """Concatenated text used for embedding/retrieval (name|desc|body)."""
        return f"{self.name} | {self.description[:desc_max]} | {self.body[:body_max]}"


class Task(BaseModel):
    """A routing/execution task with its ground-truth skills."""

    id: str
    instruction: str = ""
    gt_skill_ids: list[str] = Field(default_factory=list)
    # graded relevance: skill_id -> grade (3.0 GT, 1.0 degraded, ...)
    relevance: dict[str, float] = Field(default_factory=dict)
    excluded: bool = False
    metadata: dict[str, object] = Field(default_factory=dict)


class SkillPool(BaseModel):
    """A collection of skills with an id index."""

    skills: list[Skill] = Field(default_factory=list)

    def index(self) -> dict[str, Skill]:
        return {s.id: s for s in self.skills}

    def ids(self) -> list[str]:
        return [s.id for s in self.skills]

    def __len__(self) -> int:
        return len(self.skills)


class GoldStandard(BaseModel):
    """task_id -> {gt_skill_ids, graded relevance}. Convenience accessors."""

    by_task: dict[str, Task] = Field(default_factory=dict)

    def gt_for(self, task_id: str) -> set[str]:
        t = self.by_task.get(task_id)
        return set(t.gt_skill_ids) if t else set()

    def relevance_for(self, task_id: str) -> dict[str, float]:
        t = self.by_task.get(task_id)
        return dict(t.relevance) if t else {}


class Dataset(BaseModel):
    """A unified benchmark: a skill pool + scored tasks + gold standard."""

    name: str
    pool: SkillPool
    tasks: list[Task] = Field(default_factory=list)
    gold: GoldStandard = Field(default_factory=GoldStandard)

    def scored_tasks(self) -> list[Task]:
        return [t for t in self.tasks if not t.excluded]
