"""Build a small GT-preserving skill subset for cheap smoke runs.

Keeps every ground-truth skill referenced by the chosen tasks, then adds
lexical nearest-neighbor distractors from the corpus so the management engines
(cluster/merge/filter) have near-duplicate structure to act on. Management
re-embeds the subset, so cheap lexical selection here is sufficient.
"""

from __future__ import annotations

import re

from meta_skill.data.schema import Dataset, GoldStandard, Skill, SkillPool

_TOKEN = re.compile(r"[a-z0-9]+")


def _tokens(s: Skill) -> set[str]:
    text = f"{s.name} {s.description}".lower()
    return set(_TOKEN.findall(text))


def subset_dataset(ds: Dataset, target_size: int = 200, nn_per_gt: int = 6) -> Dataset:
    """Return a new Dataset whose pool is ~target_size skills incl. all GT."""
    by_id = ds.pool.index()
    gt_ids: set[str] = set()
    for t in ds.scored_tasks():
        gt_ids.update(t.gt_skill_ids)
    gt_skills = [by_id[i] for i in gt_ids if i in by_id]

    corpus = [s for s in ds.pool.skills if s.id not in gt_ids]
    gt_tok = [(_tokens(g)) for g in gt_skills]

    # rank corpus skills by max token-overlap with any GT skill (desc)
    scored: list[tuple[float, Skill]] = []
    for c in corpus:
        ct = _tokens(c)
        best = max((len(ct & gt) / (len(ct | gt) or 1) for gt in gt_tok), default=0.0)
        scored.append((best, c))
    scored.sort(key=lambda x: x[0], reverse=True)

    keep: list[Skill] = list(gt_skills)
    # take top NN distractors first (clusterable), then fill with the rest
    for _, c in scored:
        if len(keep) >= target_size:
            break
        keep.append(c)

    seen: dict[str, Skill] = {}
    for s in keep:
        seen.setdefault(s.id, s)
    return Dataset(
        name=f"{ds.name}-subset{len(seen)}",
        pool=SkillPool(skills=list(seen.values())),
        tasks=ds.tasks,
        gold=GoldStandard(by_task=ds.gold.by_task),
    )
