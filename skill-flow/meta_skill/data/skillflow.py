"""Adapter: SkillFlow SKILL.md corpus + SkillsBench tasks -> unified Dataset.

The managed pool is the SKILL.md corpus (skillsmp/*). Each task's ground-truth
skills are its SkillsBench *oracle* skills (environment/skills/<name>/SKILL.md),
injected into the pool with task-scoped ids ``skillsbench/<task>/<name>`` so the
retrieval eval can measure whether GT survives management — mirroring how the
existing retriever eval injects GT into the index.
"""

from __future__ import annotations

import json
from pathlib import Path

from skill_flow.corpus.loader import load_content, load_corpus

from meta_skill.data.schema import Dataset, GoldStandard, Skill, SkillPool, Task

SKILLFLOW_ROOT = Path("/home/daweili5/meta-skill-evolving/skill-flow")
TASKS_DIR = SKILLFLOW_ROOT / "integration/skillsbench/tasks"


def _corpus_skills(corpus_dir: Path, limit: int | None = None,
                   index_dir: Path | None = None) -> list[Skill]:
    # Fast path: read bodies/descriptions from the prebuilt index artifacts
    # (3 JSON files) instead of 30K individual SKILL.md reads on beegfs.
    if index_dir is not None and (Path(index_dir) / "skill_contents.json").is_file():
        idx = Path(index_dir)
        ids = json.loads((idx / "skill_ids.json").read_text())
        desc = json.loads((idx / "skill_descriptions.json").read_text())
        cont = json.loads((idx / "skill_contents.json").read_text())
        if limit:
            ids = ids[:limit]
        return [Skill(id=k, name=k.split("/")[-1], description=desc.get(k, ""),
                      body=cont.get(k, ""), source="skillflow") for k in ids]

    records = load_corpus(corpus_dir)
    if limit:
        records = records[:limit]
    out: list[Skill] = []
    for r in records:
        try:
            body = load_content(corpus_dir, r)
        except OSError:
            continue  # skip records whose SKILL.md is missing/unreadable
        out.append(
            Skill(id=r.key, name=r.name, description=r.description, body=body,
                  source="skillflow")
        )
    return out


def _oracle_skills_for(task: str) -> list[Skill]:
    sk_dir = TASKS_DIR / task / "environment" / "skills"
    out: list[Skill] = []
    if not sk_dir.is_dir():
        return out
    for sd in sorted(sk_dir.iterdir()):
        md = sd / "SKILL.md"
        if md.is_file():
            body = md.read_text(encoding="utf-8", errors="replace")
            out.append(
                Skill(id=f"skillsbench/{task}/{sd.name}", name=sd.name,
                      description="", body=body, source="gt")
            )
    return out


def load_skillflow(
    corpus_dir: str | Path = "data/skills-refined-36k",
    task_names: list[str] | None = None,
    corpus_limit: int | None = None,
    index_dir: str | Path | None = None,
) -> Dataset:
    """Build a unified Dataset: corpus pool + GT-injected oracle skills.

    ``task_names`` selects which SkillsBench tasks to include (default: all that
    have oracle skills). ``corpus_limit`` caps the corpus pool for cheap runs.
    ``index_dir`` (with skill_contents.json) enables fast loading of large
    corpora from prebuilt artifacts instead of per-file reads.
    """
    corpus_dir = Path(corpus_dir)
    if task_names is None:
        task_names = sorted(
            d.name for d in TASKS_DIR.iterdir()
            if (d / "environment" / "skills").is_dir()
            and any((d / "environment" / "skills").iterdir())
        )

    pool = _corpus_skills(corpus_dir, limit=corpus_limit,
                          index_dir=Path(index_dir) if index_dir else None)
    tasks: list[Task] = []
    by_task: dict[str, Task] = {}
    for t in task_names:
        oracle = _oracle_skills_for(t)
        if not oracle:
            continue
        pool.extend(oracle)
        instr_path = TASKS_DIR / t / "instruction.md"
        instr = instr_path.read_text(encoding="utf-8") if instr_path.is_file() else ""
        gt_ids = [s.id for s in oracle]
        task = Task(id=t, instruction=instr, gt_skill_ids=gt_ids,
                    relevance={sid: 3.0 for sid in gt_ids})
        tasks.append(task)
        by_task[t] = task

    # dedupe pool by id (corpus + oracle)
    seen: dict[str, Skill] = {}
    for s in pool:
        seen.setdefault(s.id, s)
    return Dataset(
        name="skillflow",
        pool=SkillPool(skills=list(seen.values())),
        tasks=tasks,
        gold=GoldStandard(by_task=by_task),
    )
