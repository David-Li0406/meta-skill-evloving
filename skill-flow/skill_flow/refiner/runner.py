"""Orchestrates the refiner pipeline; dispatches on RefinerConfig.engine.

Supported engines:
- "skillx" (default): DBSCAN cluster → LLM merge → LLM quality-filter
- "autoskill": vector-similarity pairs → LLM merge-judge → SkillX merger
- "skillclaw": DBSCAN cluster → LLM evolve (improve/create/merge/skip) + verify
- "agentskillos": KMeans top-level categories + LLM labels + active/dormant split
"""

from __future__ import annotations

import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

from skill_flow.corpus.loader import load_corpus
from skill_flow.refiner.cluster import cluster_skills
from skill_flow.refiner.engines import (
    refine_agentskillos,
    refine_autoskill,
    refine_skillclaw,
)
from skill_flow.refiner.library import write_refined_corpus
from skill_flow.refiner.merger import SkillMdMerger
from skill_flow.refiner.models import (
    MergedSkill,
    RefineReport,
    RefinerConfig,
)
from skill_flow.refiner.quality_filter import SkillMdQualityFilter

if TYPE_CHECKING:
    from skill_flow.models import SkillRecord

logger = logging.getLogger(__name__)


def refine_library(config: RefinerConfig) -> RefineReport:
    """Run the configured engine end-to-end."""
    started = time.time()

    source_corpus = Path(config.source_corpus_dir)
    index_dir = Path(config.source_index_dir)
    output_corpus = Path(config.output_corpus_dir)
    report_dir = Path(config.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)

    records = load_corpus(source_corpus)
    logger.info("Loaded %d skill records from %s", len(records), source_corpus)

    skill_ids: list[str] = json.loads(
        (index_dir / "skill_ids.json").read_text(encoding="utf-8"),
    )
    contents: dict[str, str] = json.loads(
        (index_dir / "skill_contents.json").read_text(encoding="utf-8"),
    )
    embeddings: np.ndarray = np.load(index_dir / "embeddings.npy")

    by_key = {r.key: r for r in records}
    indexed_records: list[SkillRecord] = []
    rows: list[int] = []
    for i, key in enumerate(skill_ids):
        rec = by_key.get(key)
        if rec is not None:
            indexed_records.append(rec)
            rows.append(i)
    if len(indexed_records) != len(skill_ids):
        logger.warning(
            "Index has %d ids but metadata has %d records — using %d intersection",
            len(skill_ids), len(records), len(indexed_records),
        )
    emb_subset = embeddings[rows] if rows else embeddings

    engine = config.engine
    logger.info("Refiner engine: %s", engine)

    if engine == "skillx":
        kept_singletons, kept_merged, dropped, extra = _run_skillx(
            indexed_records, emb_subset, contents, config, report_dir,
        )
    elif engine == "autoskill":
        singletons, merged_skills, merge_failures, ex = refine_autoskill(
            indexed_records, emb_subset, contents, config, report_dir,
        )
        # Apply shared SkillX-style quality filter after merge
        kept_singletons, kept_merged, dropped = _apply_quality_filter(
            config, singletons, merged_skills, contents,
        )
        extra = {**ex, "merge_failures": merge_failures}
    elif engine == "skillclaw":
        clusters = cluster_skills(emb_subset, eps=config.eps)
        _write_cluster_report(clusters, indexed_records, report_dir)
        singletons, merged_skills, merge_failures, ex = refine_skillclaw(
            indexed_records, clusters, contents, config, report_dir,
        )
        # SkillClaw has its own verifier; skip the shared quality_filter.
        kept_singletons, kept_merged, dropped = singletons, merged_skills, 0
        extra = {**ex, "merge_failures": merge_failures}
    elif engine == "agentskillos":
        singletons, merged_skills, merge_failures, ex = refine_agentskillos(
            indexed_records, emb_subset, contents, config, report_dir,
        )
        kept_singletons, kept_merged, dropped = singletons, merged_skills, 0
        extra = {**ex, "merge_failures": merge_failures}
    else:
        msg = f"Unknown engine: {engine!r}"
        raise ValueError(msg)

    write_refined_corpus(
        source_corpus, output_corpus, kept_singletons, kept_merged,
    )

    report = RefineReport(
        engine=engine,
        before_count=len(records),
        after_count=len(kept_singletons) + len(kept_merged),
        clusters_total=int(extra.get("clusters_total", 0)),
        clusters_merged=len(kept_merged),
        merge_failures=int(extra.get("merge_failures", 0)),
        dropped_by_filter=dropped,
        kept_singletons=len(kept_singletons),
        kept_merged=len(kept_merged),
        elapsed_sec=round(time.time() - started, 2),
        extra=extra,
    )
    (report_dir / "summary.json").write_text(
        report.model_dump_json(indent=2), encoding="utf-8",
    )
    logger.info("Refine complete (%s): %s", engine, report.model_dump())
    return report


def _run_skillx(
    indexed_records: list[SkillRecord],
    embeddings: np.ndarray,
    contents: dict[str, str],
    config: RefinerConfig,
    report_dir: Path,
) -> tuple[list[SkillRecord], list[MergedSkill], int, dict[str, object]]:
    """Original SkillX pipeline (DBSCAN → merge → filter)."""
    clusters = cluster_skills(embeddings, eps=config.eps)
    _write_cluster_report(clusters, indexed_records, report_dir)

    merged_skills: list[MergedSkill] = []
    merge_failures = 0
    skip_above = config.merger.skip_cluster_size_above
    multi = [
        c for c in clusters
        if len(c) >= 2 and (skip_above <= 0 or len(c) <= skip_above)
    ]
    skipped_big = sum(
        1 for c in clusters
        if len(c) >= 2 and skip_above > 0 and len(c) > skip_above
    )
    if skipped_big:
        logger.info(
            "Skipping %d clusters with size > %d (their members become singletons)",
            skipped_big, skip_above,
        )
    if config.merger.enabled and multi:
        merger = SkillMdMerger(config.merger)
        cluster_records_list = [
            [indexed_records[i] for i in cluster] for cluster in multi
        ]
        with ThreadPoolExecutor(max_workers=config.merger.max_workers) as pool:
            futures = [
                pool.submit(merger.merge, recs, contents)
                for recs in cluster_records_list
            ]
            for i, fut in enumerate(futures, 1):
                try:
                    merged = fut.result()
                except Exception as exc:  # noqa: BLE001
                    logger.warning("merge error on cluster %d: %s", i, exc)
                    merged = None
                if merged is None:
                    merge_failures += 1
                else:
                    merged_skills.append(merged)
                if i % 100 == 0:
                    logger.info("merged %d/%d clusters", i, len(multi))
        merger.flush()

    surviving_singletons: list[SkillRecord] = []
    merged_source_keys: set[str] = {
        k for m in merged_skills for k in m.source_keys
    }
    for cluster in clusters:
        if len(cluster) == 1:
            surviving_singletons.append(indexed_records[cluster[0]])
            continue
        for i in cluster:
            rec = indexed_records[i]
            if rec.key not in merged_source_keys:
                surviving_singletons.append(rec)

    kept_singletons, kept_merged, dropped = _apply_quality_filter(
        config, surviving_singletons, merged_skills, contents,
    )
    extra = {
        "engine": "skillx",
        "clusters_total": len(clusters),
        "merge_failures": merge_failures,
    }
    return kept_singletons, kept_merged, dropped, extra


def _write_cluster_report(
    clusters: list[list[int]],
    indexed_records: list[SkillRecord],
    report_dir: Path,
) -> None:
    (report_dir / "cluster_report.json").write_text(
        json.dumps(
            {
                "n_clusters": len(clusters),
                "sizes": [len(c) for c in clusters],
                "size_ge_2_count": sum(1 for c in clusters if len(c) >= 2),
                "members": [
                    [indexed_records[i].key for i in c]
                    for c in clusters if len(c) >= 2
                ],
            },
            indent=2, ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def _apply_quality_filter(
    config: RefinerConfig,
    singletons: list[SkillRecord],
    merged: list[MergedSkill],
    contents: dict[str, str],
) -> tuple[list[SkillRecord], list[MergedSkill], int]:
    qf = (
        SkillMdQualityFilter(config.quality_filter)
        if config.quality_filter.enabled else None
    )
    if qf is None:
        return singletons, merged, 0

    decisions: dict[str, bool] = {}
    work: list[tuple[str, str]] = []
    for rec in singletons:
        body = contents.get(rec.key, "")
        if not body:
            body = f"---\nname: {rec.name}\ndescription: {rec.description}\n---\n"
        work.append((rec.key, body))
    for m in merged:
        work.append((m.key, m.content))

    with ThreadPoolExecutor(max_workers=qf._config.max_workers) as pool:  # noqa: SLF001
        futures = {pool.submit(qf.judge, k, b): k for k, b in work}
        done = 0
        for fut in as_completed(futures):
            key = futures[fut]
            try:
                decisions[key] = fut.result()
            except Exception as exc:  # noqa: BLE001
                logger.warning("filter error for %s: %s", key, exc)
                decisions[key] = True
            done += 1
            if done % 1000 == 0:
                logger.info("filtered %d/%d skills", done, len(work))
    qf.flush()

    kept_singletons = [r for r in singletons if decisions.get(r.key, True)]
    kept_merged = [m for m in merged if decisions.get(m.key, True)]
    dropped = (len(singletons) - len(kept_singletons)) + (
        len(merged) - len(kept_merged)
    )
    logger.info(
        "Quality filter: kept %d/%d singletons + %d/%d merged (%d dropped)",
        len(kept_singletons), len(singletons),
        len(kept_merged), len(merged), dropped,
    )
    return kept_singletons, kept_merged, dropped
