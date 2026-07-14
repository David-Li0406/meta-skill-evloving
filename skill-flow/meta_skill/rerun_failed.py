"""Re-run reward-0/None tasks for every meta-skill under working-network conditions.

A transient outage to the Ubuntu apt mirror during iter_3's execution window broke
~17 sandbox builds (missing python3/poppler/tesseract -> agent ran in a broken env
-> scored 0), dragging iter_3's reward to an artifact 0.263. To make the 4-way
comparison fair, re-run EVERY task that scored 0 or None in any iteration now that
the mirror is reachable: genuinely-hard tasks fail again, network-broken tasks
recover. Reuses each iteration's already-rebuilt refined library + retrieval top-k
(no re-management). Resumable: cleared-then-rerun is idempotent because a recovered
task no longer matches the reward-0/None filter.

    python -m meta_skill.rerun_failed            # all 4 iters
    python -m meta_skill.rerun_failed 3          # only iter_3
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from meta_skill.data.schema import Skill, SkillPool, Task
from meta_skill.execute import run_execution_sample

OUT = Path("/scratch/daweili5/meta_skill_evolve/autoskill_full")
RW = Path("/scratch/daweili5/meta_skill_evolve/regen_work")


def _refined_ids_pool(corpus_refined: Path) -> SkillPool:
    idx = json.loads((corpus_refined / "_metadata" / "index.json").read_text())
    return SkillPool(skills=[Skill(id=k, name="", description="", body="", source="")
                             for k in idx["skills"]])


def _metrics(per_task: dict) -> dict:
    rewards = [v["reward"] for v in per_task.values() if v.get("reward") is not None]
    return {"mean_reward": sum(rewards) / len(rewards) if rewards else None,
            "n_scored": len(rewards), "n_tasks": len(per_task)}


def rerun_iter(name: str) -> None:
    regen = OUT / name / "eval_report_regen.json"
    rep = json.loads(regen.read_text())
    per_task = rep["execution"]["per_task"]
    failed = [t for t, v in per_task.items() if v.get("reward") in (0.0, None)]
    if not failed:
        print(f"[rerun] {name}: nothing to re-run", flush=True)
        return
    mwd = RW / name
    jobs = mwd / "evaluation"
    # clear the failed tasks' stale (broken-build) trial dirs so they run fresh
    cleared = 0
    for t in failed:
        for trial in jobs.glob(f"*/{t}__*"):
            shutil.rmtree(trial, ignore_errors=True)
            cleared += 1
    print(f"[rerun] {name}: re-running {len(failed)} reward-0/None tasks "
          f"(cleared {cleared} stale trials)...", flush=True)

    refined = _refined_ids_pool(mwd / "corpus_refined")
    tasks = [Task(id=t, instruction="", gt_skill_ids=[]) for t in failed]
    res = run_execution_sample(refined, tasks, rep["retrieval"]["per_task"], mwd)

    # merge recovered rewards back in
    recovered = 0
    for t in failed:
        new = res["per_task"].get(t, {}).get("reward")
        if new is not None:
            if per_task[t].get("reward") in (0.0, None) and new > 0:
                recovered += 1
            per_task[t]["reward"] = new
    rep["execution"]["metrics"] = _metrics(per_task)
    regen.write_text(json.dumps(rep, indent=2), encoding="utf-8")
    print(f"[rerun] {name} DONE: recovered {recovered} tasks; "
          f"now {rep['execution']['metrics']}", flush=True)


def main() -> None:
    want = [f"iter_{i}" for i in sys.argv[1:]] or ["iter_0", "iter_1", "iter_2", "iter_3"]
    for name in want:
        rerun_iter(name)
    print("[rerun] ALL DONE", flush=True)
    Path("/scratch/daweili5/meta_skill_evolve/RERUN_DONE").write_text("ok")


if __name__ == "__main__":
    main()
