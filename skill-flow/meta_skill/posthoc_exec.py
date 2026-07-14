"""Post-hoc SkillsBench execution for iterations the loop ran retrieval-only.

The evolving loop only executes the seed + final meta-skill (``exec_iters``).
To get a reward/pass@1 number for *every* meta-skill in the comparison table,
this re-runs the exact same execution path for the in-between iterations using
each iteration's already-saved refined library (``corpus_refined``) and its
retrieval top-k (from ``eval_report.json``). Results are written back into the
iteration's ``eval_report.json`` under ``execution`` so the table builder sees a
uniform schema across all iterations.

    python -m meta_skill.posthoc_exec 1 2        # run iters 1 and 2
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from meta_skill.data.schema import Skill, SkillPool, Task
from meta_skill.execute import run_execution_sample

OUT = Path("/scratch/daweili5/meta_skill_evolve/autoskill_full")
WORK = Path("/tmp/metaskill-autoskill-full")


def _refined_ids_pool(corpus_refined: Path) -> SkillPool:
    """Lightweight pool of just the refined skill ids.

    ``run_execution_sample`` only consults ``refined.ids()`` (to keep selector
    keys that survived management); the SKILL.md bodies are read straight from
    the on-disk ``corpus_refined`` during injection, so loading ~30K bodies here
    is unnecessary. Read the ids from the cheap metadata index instead.
    """
    idx = json.loads((corpus_refined / "_metadata" / "index.json").read_text())
    return SkillPool(skills=[Skill(id=k, name="", description="", body="",
                                   source="merged")
                             for k in idx["skills"]])


def run_iter(it: int, exec_sample: list[str]) -> dict:
    mwd = WORK / f"iter_{it}"
    refined = _refined_ids_pool(mwd / "corpus_refined")
    er_path = OUT / f"iter_{it}" / "eval_report.json"
    rep = json.loads(er_path.read_text())
    per_task = rep["retrieval"]["per_task"]
    # run_execution_sample only needs each task's id (instruction/GT come from
    # the SkillsBench task dir inside the sandbox); keep these lightweight.
    tasks = [Task(id=t, instruction="", gt_skill_ids=[])
             for t in exec_sample if t in per_task]
    result = run_execution_sample(refined, tasks, per_task, mwd)
    rep["execution"] = result
    er_path.write_text(json.dumps(rep, indent=2), encoding="utf-8")
    return result["metrics"]


if __name__ == "__main__":
    cfg = json.loads(Path("meta_skill/config/evolve_autoskill_full.json").read_text())
    exec_sample = cfg["exec_sample"]
    for it in (int(x) for x in sys.argv[1:]):
        m = run_iter(it, exec_sample)
        print(f"iter_{it} execution: {m}", flush=True)
