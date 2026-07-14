"""Meta-skill evolving loop: manage -> evaluate -> attribute -> refine -> repeat.

Each iteration runs the current meta-skill over the training pool, evaluates the
refined library (retrieval proxy + optional execution), attributes outcomes to
pipeline decisions, then asks Claude Code to rewrite the meta-skill. Tracks a
metric history + best-so-far, then compares best vs seed on a held-out set.
"""

from __future__ import annotations

import json
from pathlib import Path

from skill_flow.index.encoder import Encoder

from meta_skill.attribute import attribute
from meta_skill.data.schema import Dataset
from meta_skill.evaluate import evaluate, retrieval_eval
from meta_skill.manage import manage
from meta_skill.metaskill import MetaSkill, load_meta_skill
from meta_skill.refine import refine


def _load_dataset(spec: dict) -> Dataset:
    src = spec["source"]
    if src == "skillflow":
        from meta_skill.data.skillflow import load_skillflow
        from meta_skill.data.subset import subset_dataset
        ds = load_skillflow(corpus_dir=spec.get("corpus_dir", "data/skills-refined-36k"),
                            task_names=spec.get("tasks"),
                            corpus_limit=spec.get("corpus_limit", 2000),
                            index_dir=spec.get("index_dir"))
        if spec.get("subset_size"):
            ds = subset_dataset(ds, target_size=spec["subset_size"])
        return ds
    if src == "skillrouter":
        from meta_skill.data.skillrouter import load_skillrouter
        return load_skillrouter(tier=spec.get("tier", "easy"),
                                include_pool=spec.get("include_pool", True))
    raise ValueError(f"unknown dataset source: {src}")


def _score(eval_report: dict) -> float:
    m = eval_report.get("retrieval", {}).get("metrics", {})
    score = float(m.get("recall@10", 0.0)) + 0.5 * float(m.get("hit@1", 0.0))
    ex = eval_report.get("execution", {}).get("metrics", {})
    if ex.get("mean_reward") is not None:  # weight real task success heavily
        score += 2.0 * float(ex["mean_reward"])
    return score


def run_loop(config: dict) -> dict:
    out_root = Path(config["output_dir"])
    out_root.mkdir(parents=True, exist_ok=True)
    train = _load_dataset(config["train"])
    encoder = Encoder()

    seed = load_meta_skill(config["seed_meta_skill"])
    meta = seed
    history: list[dict] = []
    best = {"score": -1.0, "iter": -1, "meta_path": config["seed_meta_skill"]}
    n_iter = int(config.get("iterations", 2))
    exec_sample = config.get("exec_sample")
    # which iterations actually run execution (default: seed + final).
    exec_iters = config.get("exec_iters")
    if exec_iters is None:
        exec_iters = [0, n_iter - 1]
    exec_iters = {(i if i >= 0 else n_iter + i) for i in exec_iters}
    method = config.get("engine", seed.engine)

    # Heavy per-iteration I/O (corpus/index materialization) goes on a fast
    # local disk; small persisted artifacts stay under out_root (beegfs).
    work_root = Path(config.get("work_root", "/tmp/metaskill-work"))
    work_root.mkdir(parents=True, exist_ok=True)

    # Build the (large) source corpus+index once; reuse every iteration.
    from meta_skill.manage import prepare_source
    src = None
    if config.get("cache_source", True):
        src = prepare_source(train.pool, work_root / "_source")

    # Embed the full source pool ONCE with routing-text; reuse for unchanged
    # skills across iterations (only newly merged skills get re-embedded).
    emb_cache: dict | None = None
    if config.get("reuse_embeddings", True) and len(train.pool) > 2000:
        import numpy as np
        cache_npz = work_root / "emb_cache.npz"
        if cache_npz.is_file():
            z = np.load(cache_npz, allow_pickle=True)
            emb_cache = {k: v for k, v in zip(z["ids"], z["emb"])}
        else:
            texts = [s.routing_text() for s in train.pool.skills]
            mat = np.asarray(encoder.encode_documents(texts, batch_size=64),
                             dtype=np.float32)
            ids_arr = np.array(train.pool.ids(), dtype=object)
            np.savez(cache_npz, ids=ids_arr, emb=mat)
            emb_cache = {sid: mat[i] for i, sid in enumerate(train.pool.ids())}

    for it in range(n_iter):
        wd = out_root / f"iter_{it}"           # small persisted artifacts
        mwd = work_root / f"iter_{it}"         # heavy corpus/index/exec I/O
        wd.mkdir(parents=True, exist_ok=True)
        mwd.mkdir(parents=True, exist_ok=True)
        # resume: skip iterations already completed
        if (wd / "eval_report.json").is_file():
            report = json.loads((wd / "eval_report.json").read_text())
            decisions = json.loads((wd / "decision_log.json").read_text())
            meta_next = out_root / f"meta_iter_{it + 1}.md"
            if it < n_iter - 1 and meta_next.is_file():
                meta = load_meta_skill(meta_next)
            attrib = attribute(train.gold, train.scored_tasks(), decisions, report)
            score = _score(report)
            history.append({"iter": it, "score": round(score, 4),
                            **report["retrieval"]["metrics"],
                            "execution": report.get("execution", {}).get("metrics", {}),
                            "blame": attrib["stage_blame"]})
            if score > best["score"]:
                best = {"score": score, "iter": it,
                        "meta_path": str(config["seed_meta_skill"] if it == 0
                                         else out_root / f"meta_iter_{it}.md")}
            continue
        refined, decisions = manage(meta, train.pool, mwd, source=src,
                                    cache_dir=work_root / '_caches')
        report = evaluate(refined, train.scored_tasks(), decisions,
                          exec_sample=(exec_sample if it in exec_iters else None),
                          workdir=mwd, encoder=encoder, emb_cache=emb_cache)
        attrib = attribute(train.gold, train.scored_tasks(), decisions, report)
        score = _score(report)
        hist_entry = {"iter": it, "score": round(score, 4),
                      **report["retrieval"]["metrics"],
                      "execution": report.get("execution", {}).get("metrics", {}),
                      "blame": attrib["stage_blame"]}
        history.append(hist_entry)
        (wd / "decision_log.json").write_text(json.dumps(decisions, indent=2))
        (wd / "eval_report.json").write_text(json.dumps(report, indent=2))
        (wd / "attribution.json").write_text(json.dumps(attrib, indent=2))
        if score > best["score"]:
            best = {"score": score, "iter": it,
                    "meta_path": str(config["seed_meta_skill"] if it == 0
                                     else out_root / f"meta_iter_{it}.md")}
        # refine -> next meta-skill (skip on the last iteration)
        if it < n_iter - 1:
            next_path = out_root / f"meta_iter_{it + 1}.md"
            try:
                meta = refine(meta, decisions, report, attrib, history, next_path,
                              model=config.get("refiner_model", "opus"))
            except Exception as exc:  # noqa: BLE001
                (wd / "refine_error.txt").write_text(str(exc))
                break

    (out_root / "history.json").write_text(json.dumps(history, indent=2))
    result = {"history": history, "best": best, "method": method}

    # final compare: best vs seed on held-out
    if config.get("held_out"):
        result["compare"] = compare(config, best, seed, encoder)
    (out_root / "result.json").write_text(json.dumps(result, indent=2))
    return result


def compare(config: dict, best: dict, seed: MetaSkill, encoder: Encoder) -> dict:
    held = _load_dataset(config["held_out"])
    if len(held.pool) == 0:
        return {"skipped": "held-out pool empty (download SkillRouter shards)"}
    out_root = Path(config["output_dir"]) / "compare"
    out_root.mkdir(parents=True, exist_ok=True)
    best_meta = load_meta_skill(best["meta_path"])
    res = {}
    for label, meta in [("seed", seed), ("evolved", best_meta)]:
        refined, decisions = manage(meta, held.pool, out_root / label)
        er = retrieval_eval(refined, held.scored_tasks(), decisions, encoder=encoder)
        res[label] = er["metrics"]
    res["delta"] = {k: res["evolved"].get(k, 0) - res["seed"].get(k, 0)
                    for k in res["seed"] if isinstance(res["seed"][k], (int, float))}
    return res
