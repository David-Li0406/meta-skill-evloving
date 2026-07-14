"""Adapter: SkillRouter eval_core -> unified Dataset.

SkillRouter ships lightweight metadata (tasks.jsonl, relevance.json) in-repo and
the large skill-pool shards (easy/hard/*.jsonl.gz) on Hugging Face. This adapter
always loads tasks + relevance; the skill pool is loaded from shards only if a
tier directory exists locally (run ``scripts/download_eval_data.sh`` first).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from meta_skill.data.schema import Dataset, GoldStandard, Skill, SkillPool, Task

SKILLROUTER_ROOT = Path("/scratch/daweili5/SkillRouter")


def _load_shards(pool_dir: Path) -> list[Skill]:
    """Load skills from a tier dir of jsonl/jsonl.gz shards via SkillRouter's IO."""
    sys.path.insert(0, str(SKILLROUTER_ROOT))
    from src.data_io import iter_jsonl_paths, stream_jsonl  # type: ignore

    skills: list[Skill] = []
    for shard in iter_jsonl_paths(pool_dir):
        for row in stream_jsonl(shard):
            sid = row.get("skill_id") or row.get("id") or ""
            if not sid:
                continue
            skills.append(
                Skill(
                    id=sid,
                    name=row.get("name", ""),
                    description=row.get("description", row.get("desc", "")),
                    body=row.get("body", ""),
                    source="skillrouter",
                )
            )
    return skills


def load_skillrouter(
    data_root: str | Path = SKILLROUTER_ROOT / "data/eval_core",
    tier: str | None = "easy",
    include_pool: bool = True,
) -> Dataset:
    """Build a unified Dataset from SkillRouter eval_core.

    ``tier`` selects which skill-pool shard dir to load (easy|hard|None).
    ``include_pool`` False skips shard loading (tasks+gold only).
    """
    data_root = Path(data_root)
    relevance = json.loads((data_root / "relevance.json").read_text(encoding="utf-8"))

    tasks: list[Task] = []
    by_task: dict[str, Task] = {}
    with (data_root / "tasks.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            tid = row["task_id"]
            rel = relevance.get(tid, {})
            # default scoring: skip generic_only tasks
            excluded = bool(row.get("excluded")) or rel.get("task_type") == "generic_only"
            task = Task(
                id=tid,
                instruction=row.get("instruction_text", ""),
                gt_skill_ids=list(rel.get("gt_skill_ids", [])),
                relevance={k: float(v) for k, v in rel.get("relevance", {}).items()},
                excluded=excluded,
                metadata={
                    "domain": row.get("domain"),
                    "difficulty": row.get("difficulty"),
                    "task_type": rel.get("task_type"),
                },
            )
            tasks.append(task)
            by_task[tid] = task

    skills: list[Skill] = []
    if include_pool and tier:
        pool_dir = data_root / tier
        if pool_dir.is_dir():
            skills = _load_shards(pool_dir)

    return Dataset(
        name=f"skillrouter-{tier or 'meta'}",
        pool=SkillPool(skills=skills),
        tasks=tasks,
        gold=GoldStandard(by_task=by_task),
    )
