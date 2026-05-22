"""Pydantic models for the refiner module."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class MergerConfig(BaseModel):
    """LLM merger configuration."""

    enabled: bool = True
    model: str = "gpt-4o-mini"
    max_tokens: int = 4096
    temperature: float = 0.0
    max_group_size: int = 15  # mirrors SkillX merger.py:89
    max_workers: int = 8
    skip_cluster_size_above: int = 0  # 0 = never skip; otherwise drop clusters larger than this
    instruction_path: str = "skill_flow/refiner/instructions/merge_v1.j2"
    cache_path: str = "outputs/refiner/merge_cache.json"


class QualityFilterConfig(BaseModel):
    """LLM general-filter configuration."""

    enabled: bool = True
    model: str = "gpt-4o-mini"
    max_tokens: int = 512
    temperature: float = 0.0
    max_workers: int = 8
    instruction_path: str = "skill_flow/refiner/instructions/filter_v1.j2"
    cache_path: str = "outputs/refiner/filter_cache.json"


class AutoSkillConfig(BaseModel):
    """AutoSkill-style dedupe: vector-similarity pairs + LLM merge-judge.

    Mirrors AutoSkill/autoskill/management/maintenance.py online dedup flow,
    adapted to a batch pass over the static corpus.
    """

    enabled: bool = True
    model: str = "gpt-4o-mini"
    max_tokens: int = 256
    temperature: float = 0.0
    top_k: int = 10  # neighbors per skill in vector search
    similarity_threshold: float = 0.85  # cosine >= τ → candidate pair
    max_workers: int = 32
    instruction_path: str = (
        "skill_flow/refiner/instructions/autoskill_merge_judge_v1.j2"
    )
    cache_path: str = "outputs/refiner/autoskill_judge_cache.json"


class SkillClawConfig(BaseModel):
    """SkillClaw-style evolution: improve / create / merge / skip per cluster.

    Mirrors SkillClaw/evolve_server/pipeline/execution.py::evolve_skill_from_sessions
    + skill_verifier.py, adapted to treat each DBSCAN cluster as
    one batch of "session evidence" of the same intent.
    """

    enabled: bool = True
    model: str = "gpt-4o-mini"
    max_tokens: int = 4096
    temperature: float = 0.0
    max_workers: int = 16
    max_group_size: int = 5
    verify_enabled: bool = True
    verify_model: str = "gpt-4o-mini"
    verify_min_score: float = 0.5
    verify_max_tokens: int = 256
    evolve_instruction_path: str = (
        "skill_flow/refiner/instructions/skillclaw_evolve_v1.j2"
    )
    verify_instruction_path: str = (
        "skill_flow/refiner/instructions/skillclaw_verify_v1.j2"
    )
    evolve_cache_path: str = "outputs/refiner/skillclaw_evolve_cache.json"
    verify_cache_path: str = "outputs/refiner/skillclaw_verify_cache.json"


class AgentSkillOSConfig(BaseModel):
    """AgentSkillOS-style: 2-phase capability tree + active/dormant prune.

    Phase 1: discover top-level categories (KMeans on BGE for determinism +
    LLM-named category labels).
    Phase 2: classify each skill into a leaf node.
    Active/dormant: per leaf, keep top-N by composite score; the rest are
    dropped from the refined corpus (recorded in dormant_index.json).

    Mirrors AgentSkillOS/src/manager/tree/{builder,layer_processor}.py.
    """

    enabled: bool = True
    model: str = "gpt-4o-mini"
    max_tokens: int = 512
    temperature: float = 0.0
    max_workers: int = 32
    n_categories: int = 32  # KMeans clusters for the top-level tree
    active_per_leaf: int = 0  # 0 = keep all; >0 = prune dormant
    label_instruction_path: str = (
        "skill_flow/refiner/instructions/agentskillos_label_category_v1.j2"
    )
    label_cache_path: str = "outputs/refiner/agentskillos_labels.json"


class RefinerConfig(BaseModel):
    """Top-level refiner config (added under ``Config.refiner``).

    `engine` selects the management strategy. Default "skillx" preserves
    the original cluster→merge→filter pipeline. Each engine ignores config
    fields it doesn't use (e.g. AgentSkillOS ignores `merger`).
    """

    engine: Literal[
        "skillx", "autoskill", "skillclaw", "agentskillos",
    ] = "skillx"
    source_index_dir: str = "outputs/indices/bge-base/"
    source_corpus_dir: str = "data/skills/"
    output_corpus_dir: str = "data/skills-refined/"
    report_dir: str = "outputs/refiner/"
    eps: float = 0.10
    merger: MergerConfig = MergerConfig()
    quality_filter: QualityFilterConfig = QualityFilterConfig()
    autoskill: AutoSkillConfig = AutoSkillConfig()
    skillclaw: SkillClawConfig = SkillClawConfig()
    agentskillos: AgentSkillOSConfig = AgentSkillOSConfig()


class MergedSkill(BaseModel):
    """A skill synthesized from a cluster of >=2 source skills."""

    key: str  # synthesized key, e.g. ``skillsmp/merged-<hash>``
    name: str
    description: str
    content: str  # full SKILL.md text (frontmatter + body)
    source_keys: list[str]


class RefineReport(BaseModel):
    """Summary of a refine run, written to ``report_dir/summary.json``."""

    engine: str = "skillx"
    before_count: int
    after_count: int
    clusters_total: int = 0
    clusters_merged: int = 0
    merge_failures: int = 0
    dropped_by_filter: int = 0
    kept_singletons: int = 0
    kept_merged: int = 0
    elapsed_sec: float = 0.0
    # engine-specific extras
    extra: dict[str, object] = {}
