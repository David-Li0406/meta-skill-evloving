"""Credit assignment: attribute task outcomes to management-pipeline decisions.

Joins ground truth (skills a task needs) × the management decision log × the
evaluation outcomes into per-task blame/credit records. The refiner agent uses
these to learn which decisions hurt (dropped/merged-away a needed skill) and
which helped (kept the right skills findable).
"""

from __future__ import annotations

from meta_skill.data.schema import GoldStandard, Task


def _decision_index(decision_log: dict) -> dict[str, dict]:
    """skill_id -> the decision that determined its fate."""
    out: dict[str, dict] = {}
    for d in decision_log.get("decisions", []):
        if d["stage"] == "merge":
            for inp in d["inputs"]:
                out[inp] = d
        elif d["stage"] in ("keep", "filter"):
            out[d["skill_id"]] = d
    return out


def attribute(
    gold: GoldStandard, tasks: list[Task], decision_log: dict, eval_report: dict,
) -> dict:
    """Produce per-task attribution records + aggregate stage blame counts."""
    didx = _decision_index(decision_log)
    retr = eval_report.get("retrieval", {}).get("per_task", {})
    execu = eval_report.get("execution", {}).get("per_task", {})

    records: list[dict] = []
    stage_blame: dict[str, int] = {"filter": 0, "merge": 0, "cluster": 0, "retrieval": 0}
    stage_credit: dict[str, int] = {"keep": 0, "merge": 0}

    for t in tasks:
        rt = retr.get(t.id, {})
        gt_status = rt.get("gt_status", {})
        reward = execu.get(t.id, {}).get("reward")
        per_gt = []
        task_failed = (rt.get("gt_found", 0) < rt.get("gt_total", 0)) or (
            reward is not None and reward < 0.999
        )
        for g in t.gt_skill_ids:
            dec = didx.get(g, {"stage": "keep", "skill_id": g})
            found = gt_status.get(g, {}).get("found", False)
            if not found:
                # blame the decision that determined this GT skill's fate
                if dec["stage"] == "filter":
                    reason = "dropped by quality filter"
                    blame = "filter"
                elif dec["stage"] == "merge":
                    reason = f"merged into '{dec.get('name') or dec.get('output')}' and no longer retrieved"
                    blame = "merge"
                else:
                    reason = "kept but not retrieved by the embedder"
                    blame = "retrieval"
                stage_blame[blame] = stage_blame.get(blame, 0) + 1
                per_gt.append({"gt": g, "found": False, "blamed_stage": blame,
                               "decision": dec, "explanation": reason})
            else:
                if dec["stage"] in stage_credit:
                    stage_credit[dec["stage"]] += 1
                per_gt.append({"gt": g, "found": True, "helped_stage": dec["stage"],
                               "decision": dec})
        records.append({
            "task": t.id,
            "reward": reward,
            "retrieval_recall": rt.get("recall@10"),
            "task_failed": task_failed,
            "gt_attribution": per_gt,
        })

    return {
        "records": records,
        "stage_blame": stage_blame,
        "stage_credit": stage_credit,
        "summary": {
            "n_tasks": len(tasks),
            "n_failed": sum(1 for r in records if r["task_failed"]),
            "top_blamed_stage": max(stage_blame, key=stage_blame.get) if any(stage_blame.values()) else None,
        },
    }
