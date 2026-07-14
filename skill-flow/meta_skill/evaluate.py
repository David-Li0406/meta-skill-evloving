"""Evaluation harness: retrieval proxy (+ optional SkillsBench execution).

Retrieval proxy (cheap, every iteration): embed the refined pool + each task
instruction with BGE, cosine top-k. A ground-truth skill counts as *found* if
its surviving representative is retrieved — itself if kept, or the merged skill
that absorbed it (resolved from the decision log). Scored with SkillRouter's
metrics. Execution eval (optional) runs a small task sample on SkillsBench via
the local apptainer backend and records reward + trajectory.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from skill_flow.index.encoder import Encoder

from meta_skill.data.schema import SkillPool, Task

sys.path.insert(0, "/scratch/daweili5/SkillRouter")


def _survivor_map(decision_log: dict, refined_ids: set[str]) -> dict[str, str]:
    """Map each original skill id -> the id that represents it in the refined pool."""
    m: dict[str, str] = {}
    for d in decision_log.get("decisions", []):
        if d["stage"] == "merge":
            for inp in d["inputs"]:
                m[inp] = d["output"]
        elif d["stage"] == "keep":
            m[d["skill_id"]] = d["skill_id"]
    # any refined id maps to itself
    for rid in refined_ids:
        m.setdefault(rid, rid)
    return m


def retrieval_eval(
    refined: SkillPool, tasks: list[Task], decision_log: dict,
    top_k: int = 50, encoder: Encoder | None = None,
    emb_cache: dict | None = None,
) -> dict:
    from src.metrics import hit_at_k, ndcg_at_k, recall_at_k  # SkillRouter

    enc = encoder or Encoder()
    ids = refined.ids()
    # Reuse precomputed embeddings for unchanged skills; embed only the rest
    # (e.g. newly merged skills) — avoids re-embedding the whole ~30K library.
    if emb_cache:
        rows: list = [None] * len(ids)
        todo_idx, todo_txt = [], []
        for i, s in enumerate(refined.skills):
            v = emb_cache.get(s.id)
            if v is not None:
                rows[i] = v
            else:
                todo_idx.append(i)
                todo_txt.append(s.routing_text())
        if todo_txt:
            new = np.asarray(enc.encode_documents(todo_txt, batch_size=64), dtype=np.float32)
            for j, i in enumerate(todo_idx):
                rows[i] = new[j]
        pool_emb = np.vstack(rows).astype(np.float32)
    else:
        pool_texts = [s.routing_text() for s in refined.skills]
        pool_emb = np.asarray(enc.encode_documents(pool_texts, batch_size=64),
                              dtype=np.float32)
    survivor = _survivor_map(decision_log, set(ids))

    per_task: dict[str, dict] = {}
    hits1, rec10 = [], []
    for t in tasks:
        q = np.asarray(enc.encode_query(t.instruction[:2000]), dtype=np.float32).reshape(-1)
        scores = pool_emb @ q
        order = np.argsort(-scores)[:top_k]
        ranked = [ids[i] for i in order]
        ranked_set = set(ranked)
        # GT found if its survivor is retrieved
        gt_status = {}
        found = 0
        for g in t.gt_skill_ids:
            rep = survivor.get(g, g)
            ok = rep in ranked_set
            gt_status[g] = {"survivor": rep, "found": ok,
                            "rank": (ranked.index(rep) + 1) if ok else None}
            found += int(ok)
        relevant = {survivor.get(g, g) for g in t.gt_skill_ids}
        h1 = hit_at_k(ranked, relevant, 1)
        r10 = recall_at_k(ranked, relevant, 10)
        hits1.append(h1)
        rec10.append(r10)
        per_task[t.id] = {
            "gt_needed": t.gt_skill_ids,
            "gt_status": gt_status,
            "gt_found": found,
            "gt_total": len(t.gt_skill_ids),
            "hit@1": h1,
            "recall@10": r10,
            "top5": ranked[:5],
            "topk_keys": ranked[:8],  # for the injection selector_cache
        }
    return {
        "metrics": {"hit@1": float(np.mean(hits1)) if hits1 else 0.0,
                    "recall@10": float(np.mean(rec10)) if rec10 else 0.0,
                    "n_tasks": len(tasks)},
        "per_task": per_task,
    }


def evaluate(
    refined: SkillPool, tasks: list[Task], decision_log: dict,
    exec_sample: list[str] | None = None, workdir: Path | None = None,
    encoder: Encoder | None = None, emb_cache: dict | None = None,
) -> dict:
    """Full eval: retrieval proxy + optional execution on a task sample."""
    report = {"retrieval": retrieval_eval(refined, tasks, decision_log,
                                          encoder=encoder, emb_cache=emb_cache)}
    if exec_sample:
        from meta_skill.execute import run_execution_sample  # lazy (heavy)
        report["execution"] = run_execution_sample(
            refined, [t for t in tasks if t.id in set(exec_sample)],
            report["retrieval"]["per_task"], workdir,
        )
    return report
