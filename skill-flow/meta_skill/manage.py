"""Management harness: run a meta-skill over a SkillPool, capture the trajectory.

Materializes the pool to a temp SKILL.md corpus, builds a BGE index, runs the
existing ``refine_library`` engine parameterized by the meta-skill, then
reconstructs a per-decision **decision log** (cluster / merge / filter) from the
refiner's own outputs (cluster_report.json + the refined _metadata/index.json,
which records ``merged_from``). Returns the refined pool + decision log.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from skill_flow.index.builder import build_index
from skill_flow.index.encoder import Encoder
from skill_flow.refiner.runner import refine_library

from meta_skill.data.schema import Skill, SkillPool
from meta_skill.metaskill import MetaSkill

_FM = re.compile(r"^---\s*\n(?P<fm>.*?)\n---\s*\n(?P<body>.*)$", re.DOTALL)


def _synth_description(skill: Skill) -> str:
    if skill.description.strip():
        return skill.description.strip().replace("\n", " ")[:300]
    # first non-empty, non-frontmatter line of the body
    body = skill.body
    m = _FM.match(body)
    text = m.group("body") if m else body
    for line in text.splitlines():
        s = line.strip().lstrip("#").strip()
        if s:
            return s[:300]
    return skill.name or skill.id


def _safe_path(key: str) -> str:
    return key.replace("..", "_")


def materialize_pool(pool: SkillPool, corpus_dir: Path) -> None:
    """Write the pool as a loader-compatible SKILL.md corpus."""
    corpus_dir.mkdir(parents=True, exist_ok=True)
    entries: dict[str, dict] = {}
    for s in pool.skills:
        desc = _synth_description(s)
        rel = _safe_path(s.id)
        d = corpus_dir / rel
        d.mkdir(parents=True, exist_ok=True)
        body = s.body
        if not _FM.match(body):  # ensure frontmatter so downstream parsers work
            body = f"---\nname: {s.name or s.id}\ndescription: {desc}\n---\n\n{body}"
        (d / "SKILL.md").write_text(body, encoding="utf-8")
        entries[s.id] = {
            "name": s.name or s.id,
            "description": desc,
            "source": s.source or "skillsmp",
            "local_path": rel,
        }
    meta = corpus_dir / "_metadata"
    meta.mkdir(parents=True, exist_ok=True)
    (meta / "index.json").write_text(
        json.dumps({"version": "1.0", "skills": entries}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _build_index(corpus_dir: Path, index_dir: Path) -> None:
    from skill_flow.corpus.loader import load_corpus

    records = load_corpus(corpus_dir)
    encoder = Encoder()  # auto device (CPU here)
    build_index(records, encoder, index_dir, batch_size=64, corpus_path=corpus_dir)


def _load_refined_pool(refined_dir: Path) -> SkillPool:
    from skill_flow.corpus.loader import load_content, load_corpus

    skills: list[Skill] = []
    for r in load_corpus(refined_dir):
        try:
            body = load_content(refined_dir, r)
        except OSError:
            body = ""
        src = "merged" if r.metadata.get("merged_from") else (r.source or "skillflow")
        skills.append(Skill(id=r.key, name=r.name, description=r.description,
                            body=body, source=src))
    return SkillPool(skills=skills)


def _decision_log(input_ids: list[str], refined_dir: Path, report_dir: Path) -> dict:
    idx = json.loads((refined_dir / "_metadata" / "index.json").read_text())["skills"]
    decisions: list[dict] = []

    # cluster decisions
    cr = report_dir / "cluster_report.json"
    if cr.is_file():
        for c in json.loads(cr.read_text()).get("clusters", []):
            members = c.get("keys") or c.get("members") or []
            if len(members) >= 2:
                decisions.append({"stage": "cluster", "member_ids": members})

    merged_inputs: set[str] = set()
    for key, entry in idx.items():
        mf = entry.get("merged_from")
        if mf:
            decisions.append({"stage": "merge", "inputs": list(mf), "output": key,
                              "name": entry.get("name", "")})
            merged_inputs.update(mf)

    kept = set(idx.keys())
    for sid in input_ids:
        if sid in kept:
            decisions.append({"stage": "keep", "skill_id": sid})
        elif sid in merged_inputs:
            pass  # accounted for by its merge decision
        else:
            decisions.append({"stage": "filter", "skill_id": sid, "decision": "drop"})

    return {"decisions": decisions,
            "summary": {"input": len(input_ids), "output": len(kept),
                        "merges": sum(1 for d in decisions if d["stage"] == "merge"),
                        "drops": sum(1 for d in decisions if d["stage"] == "filter")}}


def prepare_source(pool: SkillPool, cache_dir: Path) -> tuple[Path, Path]:
    """Materialize + index the (large) source pool ONCE; reuse across iterations.

    The source library is identical every iteration (only the meta-skill changes),
    so this avoids re-materializing/re-indexing ~30K skills 4x. Idempotent.
    """
    cache_dir = Path(cache_dir)
    corpus_dir = cache_dir / "corpus_in"
    index_dir = cache_dir / "index_in"
    done = cache_dir / ".source_ready"
    if done.is_file():
        return corpus_dir, index_dir
    corpus_dir.mkdir(parents=True, exist_ok=True)
    index_dir.mkdir(parents=True, exist_ok=True)
    materialize_pool(pool, corpus_dir)
    _build_index(corpus_dir, index_dir)
    done.write_text("ok", encoding="utf-8")
    return corpus_dir, index_dir


def _override_cache_dirs(cfg, cache_dir: Path) -> None:
    """Point all engine LLM caches at a shared dir (reused across iterations)."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    cfg.merger.cache_path = str(cache_dir / "merge_cache.json")
    cfg.quality_filter.cache_path = str(cache_dir / "filter_cache.json")
    cfg.autoskill.cache_path = str(cache_dir / "autoskill_judge_cache.json")
    cfg.skillclaw.evolve_cache_path = str(cache_dir / "skillclaw_evolve_cache.json")
    cfg.skillclaw.verify_cache_path = str(cache_dir / "skillclaw_verify_cache.json")
    cfg.agentskillos.label_cache_path = str(cache_dir / "agentskillos_labels.json")


def manage(meta: MetaSkill, pool: SkillPool, workdir: Path,
           source: tuple[Path, Path] | None = None,
           cache_dir: Path | None = None) -> tuple[SkillPool, dict]:
    """Run the meta-skill over the pool; return (refined_pool, decision_log).

    ``source`` = (corpus_dir, index_dir) of a prebuilt source (from
    ``prepare_source``); when given, skip the per-iteration materialize+index.
    ``cache_dir`` shares the engine LLM caches across iterations (fast).
    """
    workdir = Path(workdir)
    refined_dir = workdir / "corpus_refined"
    report_dir = workdir / "refiner_report"
    for d in (refined_dir, report_dir):
        d.mkdir(parents=True, exist_ok=True)

    if source is not None:
        corpus_dir, index_dir = source
    else:
        corpus_dir = workdir / "corpus_in"
        index_dir = workdir / "index_in"
        corpus_dir.mkdir(parents=True, exist_ok=True)
        index_dir.mkdir(parents=True, exist_ok=True)
        materialize_pool(pool, corpus_dir)
        _build_index(corpus_dir, index_dir)

    cfg = meta.to_refiner_config(
        tmp_dir=workdir / "prompts",
        source_corpus_dir=str(corpus_dir),
        source_index_dir=str(index_dir),
        output_corpus_dir=str(refined_dir),
        report_dir=str(report_dir),
    )
    if cache_dir is not None:
        _override_cache_dirs(cfg, Path(cache_dir))
    refine_library(cfg)

    refined_pool = _load_refined_pool(refined_dir)
    decisions = _decision_log(pool.ids(), refined_dir, report_dir)
    (workdir / "decision_log.json").write_text(
        json.dumps(decisions, indent=2, ensure_ascii=False), encoding="utf-8")
    return refined_pool, decisions
