"""Regenerate refined libraries + run SkillsBench execution for ALL meta-skills.

Crash/teardown-safe: a multi-day session gap both kills the process and reaps
/tmp, so EVERYTHING durable lives on /scratch and every phase is checkpointed:

  * source corpus+index, routing-text embeddings, AutoSkill judge/merge caches
    -> /scratch (shared across the 4 managements; the ~21K judge calls happen
    once and are reused, so a restart re-manages cheaply).
  * per-meta refined corpus + retrieval top-k -> /scratch, checkpointed after
    management so a restart skips straight to execution.
  * execution writes its job dir on /scratch; run_execution_sample's _collect_valid
    pre-scan makes it resume at PER-TASK granularity after an interruption.

    python -m meta_skill.regen_exec            # all 4 (seed + iter_1/2/3)
    python -m meta_skill.regen_exec 3          # only iter_3
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from skill_flow.index.encoder import Encoder

from meta_skill.data.schema import Skill, SkillPool
from meta_skill.evaluate import retrieval_eval
from meta_skill.execute import run_execution_sample
from meta_skill.loop import _load_dataset
from meta_skill.manage import manage, prepare_source
from meta_skill.metaskill import load_meta_skill

CFG_PATH = Path("meta_skill/config/evolve_autoskill_full.json")
OUT = Path("/scratch/daweili5/meta_skill_evolve/autoskill_full")
PERSIST = Path("/scratch/daweili5/meta_skill_evolve/regen_persist")
WORK = Path("/scratch/daweili5/meta_skill_evolve/regen_work")  # persistent (survives reaps)


def _emb_cache(pool, encoder: Encoder) -> dict:
    PERSIST.mkdir(parents=True, exist_ok=True)
    npz = PERSIST / "emb_cache.npz"
    if npz.is_file():
        z = np.load(npz, allow_pickle=True)
        return {k: v for k, v in zip(z["ids"], z["emb"])}
    texts = [s.routing_text() for s in pool.skills]
    mat = np.asarray(encoder.encode_documents(texts, batch_size=64), dtype=np.float32)
    np.savez(npz, ids=np.array(pool.ids(), dtype=object), emb=mat)
    return {sid: mat[i] for i, sid in enumerate(pool.ids())}


def _refined_ids_pool(corpus_refined: Path) -> SkillPool:
    """Lightweight pool of refined skill ids (execution only needs ids)."""
    idx = json.loads((corpus_refined / "_metadata" / "index.json").read_text())
    return SkillPool(skills=[Skill(id=k, name="", description="", body="", source="")
                             for k in idx["skills"]])


def run_iter(name: str, meta_path: str, ds, encoder, emb_cache, src, exec_sample) -> None:
    out_dir = OUT / name
    out_dir.mkdir(parents=True, exist_ok=True)
    regen = out_dir / "eval_report_regen.json"
    mwd = WORK / name
    mwd.mkdir(parents=True, exist_ok=True)
    cr_idx = mwd / "corpus_refined" / "_metadata" / "index.json"
    dl_path = mwd / "decision_log.json"

    rep = json.loads(regen.read_text()) if regen.is_file() else {}
    ex = rep.get("execution", {}).get("metrics", {})
    if ex.get("n_scored") is not None and ex.get("n_scored") == ex.get("n_tasks"):
        print(f"[regen] {name} already complete: {ex}", flush=True)
        return

    # Phase A: management + retrieval (checkpoint after).
    if cr_idx.is_file() and dl_path.is_file() and rep.get("retrieval"):
        decisions = json.loads(dl_path.read_text())
        print(f"[regen] {name}: reusing checkpointed refined library + retrieval", flush=True)
    else:
        print(f"[regen] {name}: managing (rebuild refined library; judge cache reused)...",
              flush=True)
        meta = load_meta_skill(meta_path)
        refined, decisions = manage(meta, ds.pool, mwd, source=src,
                                    cache_dir=PERSIST / "_caches")
        retrieval = retrieval_eval(refined, ds.scored_tasks(), decisions,
                                   encoder=encoder, emb_cache=emb_cache)
        rep = {"retrieval": retrieval}
        regen.write_text(json.dumps(rep, indent=2), encoding="utf-8")
        print(f"[regen] {name}: managed refined={len(refined)}; "
              f"retrieval {retrieval['metrics']}", flush=True)

    # Phase B: execution (resumable per-task via _collect_valid pre-scan).
    print(f"[regen] {name}: running 74-task execution (resumable)...", flush=True)
    refined_ids = _refined_ids_pool(mwd / "corpus_refined")
    tasks = [t for t in ds.scored_tasks() if t.id in set(exec_sample)]
    execution = run_execution_sample(refined_ids, tasks,
                                     rep["retrieval"]["per_task"], mwd)
    rep["execution"] = execution
    regen.write_text(json.dumps(rep, indent=2), encoding="utf-8")
    print(f"[regen] {name} DONE: execution {execution['metrics']}", flush=True)


def main() -> None:
    cfg = json.loads(CFG_PATH.read_text())
    metas = {
        "iter_0": cfg["seed_meta_skill"],
        "iter_1": str(OUT / "meta_iter_1.md"),
        "iter_2": str(OUT / "meta_iter_2.md"),
        "iter_3": str(OUT / "meta_iter_3.md"),
    }
    want = [f"iter_{i}" for i in sys.argv[1:]] or list(metas)

    ds = _load_dataset(cfg["train"])
    encoder = Encoder()
    print(f"[regen] dataset: {len(ds.pool)} skills, {len(ds.scored_tasks())} tasks", flush=True)
    src = prepare_source(ds.pool, PERSIST / "_source")
    emb_cache = _emb_cache(ds.pool, encoder)
    print(f"[regen] source + emb cache ready ({len(emb_cache)} embeddings)", flush=True)

    for name in want:
        run_iter(name, metas[name], ds, encoder, emb_cache, src, cfg["exec_sample"])

    print("[regen] ALL DONE", flush=True)
    Path("/scratch/daweili5/meta_skill_evolve/REGEN_DONE").write_text("ok")


if __name__ == "__main__":
    main()
