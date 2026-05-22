"""Alternative refinement engines: AutoSkill, SkillClaw, AgentSkillOS.

All engines share the same I/O contract:
    refine_X(records, indexed_records, embeddings, contents, config, report_dir)
        -> (kept_singletons, kept_merged, dropped, extra_stats)

Outputs feed into ``library.write_refined_corpus`` and the shared
``RefineReport`` so downstream pipelines (build-index, selector, harbor
benchmark) are unchanged.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from dotenv import load_dotenv
from jinja2 import Template
from openai import OpenAI

from skill_flow.refiner.merger import SkillMdMerger
from skill_flow.refiner.models import (
    AgentSkillOSConfig,
    AutoSkillConfig,
    MergedSkill,
    SkillClawConfig,
)

if TYPE_CHECKING:
    from skill_flow.models import SkillRecord
    from skill_flow.refiner.models import RefinerConfig

logger = logging.getLogger(__name__)


_FRONTMATTER_RE = re.compile(
    r"^---\s*\n(?P<fm>.*?)\n---\s*\n(?P<body>.*)$",
    re.DOTALL,
)
_NAME_RE = re.compile(r"^name\s*:\s*(.+?)\s*$", re.MULTILINE)
_DESC_RE = re.compile(r"^description\s*:\s*(.+?)\s*$", re.MULTILINE)
_SKILL_TAG_RE = re.compile(r"<skill>\s*(?P<body>.*?)\s*</skill>", re.DOTALL | re.IGNORECASE)
_VERDICT_RE = re.compile(r"<verdict>\s*(?P<v>merge|keep|skip|same|distinct)\s*</verdict>", re.IGNORECASE)
_ACTION_RE = re.compile(r"<action>\s*(?P<a>improve|create|merge|skip|optimize_description)\s*</action>", re.IGNORECASE)
_SCORE_RE = re.compile(r"<score>\s*(?P<s>[01]?\.?\d+)\s*</score>")
_LABEL_RE = re.compile(r"<label>\s*(?P<l>.+?)\s*</label>", re.DOTALL)


# ---------------------------------------------------------------------------
# AutoSkill engine
# ---------------------------------------------------------------------------


class AutoSkillJudge:
    """LLM merge-judge with disk cache: MERGE | KEEP-SEPARATE per pair."""

    def __init__(self, cfg: AutoSkillConfig) -> None:
        self._cfg = cfg
        load_dotenv()
        self._client = OpenAI()
        self._tmpl = Template(Path(cfg.instruction_path).read_text(encoding="utf-8"))
        self._cache_path = Path(cfg.cache_path)
        self._cache: dict[str, str] = self._load()
        self._lock = threading.RLock()
        self._save_every = 100
        self._writes = 0

    def _load(self) -> dict[str, str]:
        if self._cache_path.exists():
            data = json.loads(self._cache_path.read_text(encoding="utf-8"))
            logger.info("Loaded %d autoskill judge cache entries", len(data))
            return data
        return {}

    def _save(self) -> None:
        self._cache_path.parent.mkdir(parents=True, exist_ok=True)
        self._cache_path.write_text(
            json.dumps(self._cache, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @staticmethod
    def _ckey(a: str, b: str) -> str:
        joined = "|".join(sorted([a, b]))
        return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:16]

    def judge(
        self,
        a_key: str, a_md: str,
        b_key: str, b_md: str,
    ) -> bool:
        """Return True if the two skills should be MERGED."""
        ck = self._ckey(a_key, b_key)
        with self._lock:
            if ck in self._cache:
                return self._cache[ck] == "merge"
        system = self._tmpl.render()
        user = (
            f"=== SKILL A: {a_key} ===\n{a_md[:2000]}\n\n"
            f"=== SKILL B: {b_key} ===\n{b_md[:2000]}"
        )
        try:
            resp = self._client.chat.completions.create(
                model=self._cfg.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_completion_tokens=self._cfg.max_tokens,
                **({} if self._cfg.model.startswith("gpt-5") else {"temperature": self._cfg.temperature}),
            )
            text = resp.choices[0].message.content or ""
        except Exception as exc:  # noqa: BLE001
            logger.warning("autoskill judge failed for %s/%s: %s", a_key, b_key, exc)
            verdict = "keep"
        else:
            m = _VERDICT_RE.search(text)
            raw = m.group("v").lower() if m else ("merge" if "merge" in text.lower() else "keep")
            verdict = "merge" if raw in {"merge", "same"} else "keep"
        with self._lock:
            self._cache[ck] = verdict
            self._writes += 1
            if self._writes >= self._save_every:
                self._save()
                self._writes = 0
        return verdict == "merge"

    def flush(self) -> None:
        with self._lock:
            if self._writes:
                self._save()
                self._writes = 0


class _UnionFind:
    def __init__(self, n: int) -> None:
        self.p = list(range(n))

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def refine_autoskill(
    indexed_records: list,
    embeddings: np.ndarray,
    contents: dict[str, str],
    config: RefinerConfig,
    report_dir: Path,
) -> tuple[list, list[MergedSkill], int, dict[str, object]]:
    """AutoSkill engine: similarity-pair judge → union-find → reuse SkillX merger."""
    cfg = config.autoskill
    n = len(indexed_records)
    if n == 0:
        return [], [], 0, {"engine": "autoskill"}

    # 1. Find candidate pairs via FAISS-style similarity (normalized embeddings → IP)
    emb = embeddings.astype(np.float32, copy=False)
    norms = np.linalg.norm(emb, axis=1, keepdims=True) + 1e-12
    emb = emb / norms
    # Batched cosine: chunk rows to keep memory bounded
    chunk = 2048
    candidate_pairs: list[tuple[int, int]] = []
    seen_pairs: set[tuple[int, int]] = set()
    k = cfg.top_k
    tau = cfg.similarity_threshold
    logger.info("autoskill: scanning %d skills for similarity pairs (k=%d, τ=%.2f)", n, k, tau)
    for start in range(0, n, chunk):
        end = min(start + chunk, n)
        sims = emb[start:end] @ emb.T  # (chunk, n)
        # exclude self
        for local_i, row in enumerate(sims):
            i = start + local_i
            row[i] = -1.0
            top = np.argpartition(-row, min(k, n - 1))[:k]
            for j in top:
                j = int(j)
                if j == i:
                    continue
                if row[j] < tau:
                    continue
                a, b = (i, j) if i < j else (j, i)
                if (a, b) in seen_pairs:
                    continue
                seen_pairs.add((a, b))
                candidate_pairs.append((a, b))
        if start % (chunk * 10) == 0:
            logger.info("autoskill: scanned %d/%d", end, n)
    logger.info("autoskill: %d candidate pairs above threshold", len(candidate_pairs))

    # 2. LLM judge each pair (parallel)
    judge = AutoSkillJudge(cfg)
    merges: list[tuple[int, int]] = []

    def _body_of(idx: int) -> str:
        rec = indexed_records[idx]
        body = contents.get(rec.key, "")
        if not body:
            body = f"---\nname: {rec.name}\ndescription: {rec.description}\n---\n"
        return body

    if candidate_pairs:
        with ThreadPoolExecutor(max_workers=cfg.max_workers) as pool:
            futures = {
                pool.submit(
                    judge.judge,
                    indexed_records[a].key, _body_of(a),
                    indexed_records[b].key, _body_of(b),
                ): (a, b)
                for a, b in candidate_pairs
            }
            for i, fut in enumerate(as_completed(futures), 1):
                a, b = futures[fut]
                try:
                    if fut.result():
                        merges.append((a, b))
                except Exception as exc:  # noqa: BLE001
                    logger.warning("autoskill judge error on pair (%d,%d): %s", a, b, exc)
                if i % 500 == 0:
                    logger.info("autoskill: judged %d/%d pairs", i, len(candidate_pairs))
        judge.flush()
    logger.info("autoskill: %d pairs judged MERGE", len(merges))

    # 3. Union-find → clusters
    uf = _UnionFind(n)
    for a, b in merges:
        uf.union(a, b)
    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        groups[uf.find(i)].append(i)
    clusters = list(groups.values())
    multi = [c for c in clusters if len(c) >= 2]
    logger.info("autoskill: %d clusters total, %d multi-member", len(clusters), len(multi))

    # 4. Reuse SkillX merger (same merge_v1.j2 prompt) on multi-member clusters
    merged_skills: list[MergedSkill] = []
    merge_failures = 0
    if multi and config.merger.enabled:
        merger = SkillMdMerger(config.merger)
        cluster_records = [[indexed_records[i] for i in c] for c in multi]
        with ThreadPoolExecutor(max_workers=config.merger.max_workers) as pool:
            futures = [pool.submit(merger.merge, recs, contents) for recs in cluster_records]
            for i, fut in enumerate(futures, 1):
                try:
                    merged = fut.result()
                except Exception as exc:  # noqa: BLE001
                    logger.warning("autoskill merge error on cluster %d: %s", i, exc)
                    merged = None
                if merged is None:
                    merge_failures += 1
                else:
                    merged_skills.append(merged)
                if i % 100 == 0:
                    logger.info("autoskill: merged %d/%d clusters", i, len(multi))
        merger.flush()

    merged_keys = {k for m in merged_skills for k in m.source_keys}
    singletons = []
    for cluster in clusters:
        if len(cluster) == 1:
            singletons.append(indexed_records[cluster[0]])
        else:
            for i in cluster:
                rec = indexed_records[i]
                if rec.key not in merged_keys:
                    singletons.append(rec)

    extra = {
        "engine": "autoskill",
        "candidate_pairs": len(candidate_pairs),
        "merged_pairs": len(merges),
        "clusters_total": len(clusters),
    }
    (report_dir / "autoskill_pairs.json").write_text(
        json.dumps(
            {
                "candidate_pairs": len(candidate_pairs),
                "merged_pairs": len(merges),
                "merge_examples": [
                    [indexed_records[a].key, indexed_records[b].key]
                    for a, b in merges[:50]
                ],
            },
            indent=2, ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return singletons, merged_skills, merge_failures, extra


# ---------------------------------------------------------------------------
# SkillClaw engine
# ---------------------------------------------------------------------------


class SkillClawEvolver:
    """LLM evolve: improve / create / merge / skip per cluster, with cache."""

    def __init__(self, cfg: SkillClawConfig) -> None:
        self._cfg = cfg
        load_dotenv()
        self._client = OpenAI()
        self._tmpl = Template(Path(cfg.evolve_instruction_path).read_text(encoding="utf-8"))
        self._cache_path = Path(cfg.evolve_cache_path)
        self._cache: dict[str, dict[str, object]] = self._load()
        self._lock = threading.RLock()
        self._save_every = 25
        self._writes = 0

    def _load(self) -> dict[str, dict[str, object]]:
        if self._cache_path.exists():
            data = json.loads(self._cache_path.read_text(encoding="utf-8"))
            logger.info("Loaded %d skillclaw evolve cache entries", len(data))
            return data
        return {}

    def _save(self) -> None:
        self._cache_path.parent.mkdir(parents=True, exist_ok=True)
        self._cache_path.write_text(
            json.dumps(self._cache, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @staticmethod
    def _ckey(source_keys: list[str]) -> str:
        joined = "|".join(sorted(source_keys))
        return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:16]

    def evolve(
        self,
        records: list,
        contents: dict[str, str],
    ) -> tuple[str, MergedSkill | None]:
        """Returns (action, merged_skill_or_None).

        action ∈ {improve, create, merge, skip}.
        For skip, returns (None) — callers fall back to passthrough.
        """
        capped = records[: self._cfg.max_group_size]
        source_keys = [r.key for r in capped]
        ck = self._ckey(source_keys)
        with self._lock:
            if ck in self._cache:
                cached = self._cache[ck]
                action = str(cached.get("action", "skip"))
                if cached.get("merged"):
                    return action, MergedSkill(**cached["merged"])  # type: ignore[arg-type]
                return action, None

        system = self._tmpl.render(n=len(capped))
        parts: list[str] = []
        for i, r in enumerate(capped, 1):
            body = contents.get(r.key, "")
            if not body:
                body = f"---\nname: {r.name}\ndescription: {r.description}\n---\n"
            parts.append(f"=== EVIDENCE {i}: {r.key} ===\n{body[:2500]}")
        user = "\n\n".join(parts)

        try:
            resp = self._client.chat.completions.create(
                model=self._cfg.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_completion_tokens=self._cfg.max_tokens,
                **({} if self._cfg.model.startswith("gpt-5") else {"temperature": self._cfg.temperature}),
            )
            text = resp.choices[0].message.content or ""
        except Exception as exc:  # noqa: BLE001
            logger.warning("skillclaw evolve failed for %s: %s", source_keys[:3], exc)
            with self._lock:
                self._cache[ck] = {"action": "skip"}
                self._writes += 1
            return "skip", None

        m = _ACTION_RE.search(text)
        action = m.group("a").lower() if m else "skip"
        if action == "optimize_description":
            action = "improve"
        merged: MergedSkill | None = None
        if action in {"improve", "create", "merge"}:
            md = self._extract(text)
            if md:
                name, desc = self._parse_fm(md)
                if name:
                    slug = re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")[:32] or "skill"
                    merged = MergedSkill(
                        key=f"skillsmp/skillclaw-{ck}-{slug}"[:120],
                        name=name,
                        description=desc,
                        content=md,
                        source_keys=source_keys,
                    )
        with self._lock:
            self._cache[ck] = {"action": action, "merged": merged.model_dump() if merged else None}
            self._writes += 1
            if self._writes >= self._save_every:
                self._save()
                self._writes = 0
        return action, merged

    def flush(self) -> None:
        with self._lock:
            if self._writes:
                self._save()
                self._writes = 0

    @staticmethod
    def _extract(text: str) -> str | None:
        m = _SKILL_TAG_RE.search(text)
        if m:
            body = m.group("body").strip()
            return body if body.startswith("---") and "\n---" in body else None
        return None

    @staticmethod
    def _parse_fm(md: str) -> tuple[str, str]:
        m = _FRONTMATTER_RE.match(md.strip())
        if not m:
            return "", ""
        fm = m.group("fm")
        name_m = _NAME_RE.search(fm)
        desc_m = _DESC_RE.search(fm)
        return (
            name_m.group(1).strip().strip('"\'') if name_m else "",
            desc_m.group(1).strip().strip('"\'') if desc_m else "",
        )


class SkillClawVerifier:
    """Optional 0-1 LLM quality score gate."""

    def __init__(self, cfg: SkillClawConfig) -> None:
        self._cfg = cfg
        load_dotenv()
        self._client = OpenAI()
        self._tmpl = Template(Path(cfg.verify_instruction_path).read_text(encoding="utf-8"))
        self._cache_path = Path(cfg.verify_cache_path)
        self._cache: dict[str, dict[str, object]] = self._load()
        self._lock = threading.RLock()
        self._save_every = 200
        self._writes = 0

    def _load(self) -> dict[str, dict[str, object]]:
        if self._cache_path.exists():
            data = json.loads(self._cache_path.read_text(encoding="utf-8"))
            logger.info("Loaded %d skillclaw verify cache entries", len(data))
            return data
        return {}

    def _save(self) -> None:
        self._cache_path.parent.mkdir(parents=True, exist_ok=True)
        self._cache_path.write_text(
            json.dumps(self._cache, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def score(self, skill_key: str, content: str) -> float:
        h = hashlib.sha256()
        h.update(skill_key.encode("utf-8"))
        h.update(b"\x00")
        h.update(content.encode("utf-8"))
        ck = h.hexdigest()[:16]
        with self._lock:
            if ck in self._cache:
                return float(self._cache[ck].get("score", 1.0))
        try:
            resp = self._client.chat.completions.create(
                model=self._cfg.verify_model,
                messages=[
                    {"role": "system", "content": self._tmpl.render()},
                    {"role": "user", "content": f"=== SKILL: {skill_key} ===\n{content[:3000]}"},
                ],
                max_completion_tokens=self._cfg.verify_max_tokens,
                **({} if self._cfg.verify_model.startswith("gpt-5") else {"temperature": self._cfg.temperature}),
            )
            text = resp.choices[0].message.content or ""
        except Exception as exc:  # noqa: BLE001
            logger.warning("skillclaw verify failed for %s: %s", skill_key, exc)
            score = 1.0
        else:
            m = _SCORE_RE.search(text)
            try:
                score = float(m.group("s")) if m else 1.0
            except ValueError:
                score = 1.0
            score = max(0.0, min(1.0, score))
        with self._lock:
            self._cache[ck] = {"score": score}
            self._writes += 1
            if self._writes >= self._save_every:
                self._save()
                self._writes = 0
        return score

    def flush(self) -> None:
        with self._lock:
            if self._writes:
                self._save()
                self._writes = 0


def refine_skillclaw(
    indexed_records: list,
    clusters: list[list[int]],
    contents: dict[str, str],
    config: RefinerConfig,
    report_dir: Path,
) -> tuple[list, list[MergedSkill], int, dict[str, object]]:
    """SkillClaw engine: cluster → evolve → optional verify."""
    cfg = config.skillclaw
    multi = [c for c in clusters if len(c) >= 2]
    logger.info("skillclaw: %d clusters total, %d multi-member", len(clusters), len(multi))

    evolver = SkillClawEvolver(cfg)
    actions = {"improve": 0, "create": 0, "merge": 0, "skip": 0}
    merged_skills: list[MergedSkill] = []
    failed = 0

    cluster_records_list = [[indexed_records[i] for i in c] for c in multi]
    if multi:
        with ThreadPoolExecutor(max_workers=cfg.max_workers) as pool:
            futures = [pool.submit(evolver.evolve, recs, contents) for recs in cluster_records_list]
            for i, fut in enumerate(futures, 1):
                try:
                    action, merged = fut.result()
                except Exception as exc:  # noqa: BLE001
                    logger.warning("skillclaw evolve error on cluster %d: %s", i, exc)
                    action, merged = "skip", None
                    failed += 1
                actions[action if action in actions else "skip"] += 1
                if merged is not None:
                    merged_skills.append(merged)
                if i % 100 == 0:
                    logger.info("skillclaw: evolved %d/%d clusters", i, len(multi))
        evolver.flush()
    logger.info("skillclaw actions: %s", actions)

    # Verifier (optional)
    if cfg.verify_enabled and merged_skills:
        verifier = SkillClawVerifier(cfg)
        kept_merged: list[MergedSkill] = []
        dropped_verify = 0
        with ThreadPoolExecutor(max_workers=cfg.max_workers) as pool:
            futures = {
                pool.submit(verifier.score, m.key, m.content): m for m in merged_skills
            }
            for fut in as_completed(futures):
                m = futures[fut]
                try:
                    s = fut.result()
                except Exception as exc:  # noqa: BLE001
                    logger.warning("skillclaw verify error for %s: %s", m.key, exc)
                    s = 1.0
                if s >= cfg.verify_min_score:
                    kept_merged.append(m)
                else:
                    dropped_verify += 1
        verifier.flush()
        merged_skills = kept_merged
        logger.info("skillclaw verifier dropped %d merged skills", dropped_verify)

    # Survivors: skills not in any merged cluster, plus skip-action members
    merged_source_keys: set[str] = {k for m in merged_skills for k in m.source_keys}
    singletons = []
    for cluster in clusters:
        if len(cluster) == 1:
            singletons.append(indexed_records[cluster[0]])
            continue
        for i in cluster:
            rec = indexed_records[i]
            if rec.key not in merged_source_keys:
                singletons.append(rec)

    extra = {
        "engine": "skillclaw",
        "clusters_total": len(clusters),
        "actions": actions,
        "failed": failed,
        "kept_merged": len(merged_skills),
    }
    (report_dir / "skillclaw_actions.json").write_text(
        json.dumps(extra, indent=2, ensure_ascii=False), encoding="utf-8",
    )
    return singletons, merged_skills, failed, extra


# ---------------------------------------------------------------------------
# AgentSkillOS engine
# ---------------------------------------------------------------------------


class AgentSkillOSLabeler:
    """LLM-labels each KMeans cluster centroid with a category name."""

    def __init__(self, cfg: AgentSkillOSConfig) -> None:
        self._cfg = cfg
        load_dotenv()
        self._client = OpenAI()
        self._tmpl = Template(Path(cfg.label_instruction_path).read_text(encoding="utf-8"))
        self._cache_path = Path(cfg.label_cache_path)
        self._cache: dict[str, str] = self._load()
        self._lock = threading.RLock()

    def _load(self) -> dict[str, str]:
        if self._cache_path.exists():
            return json.loads(self._cache_path.read_text(encoding="utf-8"))
        return {}

    def label(self, cluster_id: int, sample_descriptions: list[str]) -> str:
        joined = "|".join(sample_descriptions[:8])
        ck = hashlib.sha256(joined.encode("utf-8")).hexdigest()[:16]
        with self._lock:
            if ck in self._cache:
                return self._cache[ck]
        system = self._tmpl.render()
        user = "Skill descriptions:\n" + "\n".join(
            f"- {d}" for d in sample_descriptions[:8]
        )
        try:
            resp = self._client.chat.completions.create(
                model=self._cfg.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_completion_tokens=self._cfg.max_tokens,
                **({} if self._cfg.model.startswith("gpt-5") else {"temperature": self._cfg.temperature}),
            )
            text = resp.choices[0].message.content or ""
        except Exception as exc:  # noqa: BLE001
            logger.warning("agentskillos label failed for cluster %d: %s", cluster_id, exc)
            text = ""
        m = _LABEL_RE.search(text)
        label = (m.group("l") if m else text.strip().split("\n")[0]) or f"category-{cluster_id}"
        label = label.strip().strip('"').strip("'")[:80]
        with self._lock:
            self._cache[ck] = label
            self._cache_path.parent.mkdir(parents=True, exist_ok=True)
            self._cache_path.write_text(
                json.dumps(self._cache, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        return label


def refine_agentskillos(
    indexed_records: list,
    embeddings: np.ndarray,
    contents: dict[str, str],
    config: RefinerConfig,
    report_dir: Path,
) -> tuple[list, list[MergedSkill], int, dict[str, object]]:
    """AgentSkillOS engine: KMeans top-level categories → LLM labels → optional prune to top-N per category."""
    cfg = config.agentskillos
    from sklearn.cluster import MiniBatchKMeans  # local import to avoid hard dep elsewhere

    n = len(indexed_records)
    if n == 0:
        return [], [], 0, {"engine": "agentskillos"}

    emb = embeddings.astype(np.float32, copy=False)
    norms = np.linalg.norm(emb, axis=1, keepdims=True) + 1e-12
    emb = emb / norms

    k = min(cfg.n_categories, n)
    logger.info("agentskillos: KMeans n_clusters=%d over %d skills", k, n)
    km = MiniBatchKMeans(n_clusters=k, batch_size=4096, n_init=3, random_state=0)
    labels = km.fit_predict(emb)
    centers = km.cluster_centers_
    centers /= np.linalg.norm(centers, axis=1, keepdims=True) + 1e-12

    # Per-cluster sample descriptions for LLM labeling
    by_cluster: dict[int, list[int]] = defaultdict(list)
    for i, c in enumerate(labels):
        by_cluster[int(c)].append(i)

    labeler = AgentSkillOSLabeler(cfg)
    category_labels: dict[int, str] = {}

    def _label_one(cid: int, members: list[int]) -> tuple[int, str]:
        # sample 8 members closest to the centroid
        if len(members) > 8:
            sub = np.array(members)
            sims = (emb[sub] @ centers[cid])
            top = sub[np.argsort(-sims)[:8]]
        else:
            top = members
        descs = [indexed_records[i].description[:200] for i in top]
        return cid, labeler.label(cid, descs)

    with ThreadPoolExecutor(max_workers=min(cfg.max_workers, k)) as pool:
        futures = [pool.submit(_label_one, cid, members) for cid, members in by_cluster.items()]
        for fut in as_completed(futures):
            cid, label = fut.result()
            category_labels[cid] = label
    logger.info("agentskillos: labeled %d categories", len(category_labels))

    # Active/dormant split: per category, rank by cosine to centroid + description length
    survivors: list[int] = []
    dormant: list[int] = []
    per_cluster_keep: list[int] = []
    for cid, members in by_cluster.items():
        if cfg.active_per_leaf <= 0 or len(members) <= cfg.active_per_leaf:
            survivors.extend(members)
            per_cluster_keep.append(len(members))
            continue
        # score: centroid similarity + length bonus
        sub = np.array(members)
        sims = emb[sub] @ centers[cid]
        lengths = np.array([
            min(2000, len(contents.get(indexed_records[i].key, "")))
            for i in members
        ])
        composite = sims + 0.0002 * lengths
        order = np.argsort(-composite)
        keep_idx = sub[order[: cfg.active_per_leaf]]
        drop_idx = sub[order[cfg.active_per_leaf :]]
        survivors.extend(keep_idx.tolist())
        dormant.extend(drop_idx.tolist())
        per_cluster_keep.append(cfg.active_per_leaf)

    singletons = [indexed_records[i] for i in survivors]
    logger.info(
        "agentskillos: kept %d active, dropped %d dormant from %d skills",
        len(singletons), len(dormant), n,
    )

    # Write report artifacts
    (report_dir / "agentskillos_tree.json").write_text(
        json.dumps(
            {
                "n_categories": len(by_cluster),
                "category_labels": {str(cid): lbl for cid, lbl in category_labels.items()},
                "category_sizes": {str(cid): len(m) for cid, m in by_cluster.items()},
            },
            indent=2, ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (report_dir / "agentskillos_dormant_index.json").write_text(
        json.dumps(
            [
                {
                    "key": indexed_records[i].key,
                    "category": category_labels.get(int(labels[i]), ""),
                }
                for i in dormant
            ],
            indent=2, ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    extra = {
        "engine": "agentskillos",
        "n_categories": len(by_cluster),
        "n_active": len(survivors),
        "n_dormant": len(dormant),
    }
    return singletons, [], 0, extra
