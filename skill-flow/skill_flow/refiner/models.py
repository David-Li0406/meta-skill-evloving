"""Pydantic models for the refiner module."""

from __future__ import annotations

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


class RefinerConfig(BaseModel):
    """Top-level refiner config (added under ``Config.refiner``)."""

    source_index_dir: str = "outputs/indices/bge-base/"
    source_corpus_dir: str = "data/skills/"
    output_corpus_dir: str = "data/skills-refined/"
    report_dir: str = "outputs/refiner/"
    eps: float = 0.10
    merger: MergerConfig = MergerConfig()
    quality_filter: QualityFilterConfig = QualityFilterConfig()


class MergedSkill(BaseModel):
    """A skill synthesized from a cluster of >=2 source skills."""

    key: str  # synthesized key, e.g. ``skillsmp/merged-<hash>``
    name: str
    description: str
    content: str  # full SKILL.md text (frontmatter + body)
    source_keys: list[str]


class RefineReport(BaseModel):
    """Summary of a refine run, written to ``report_dir/summary.json``."""

    before_count: int
    after_count: int
    clusters_total: int
    clusters_merged: int  # clusters of size >=2 that produced a merged skill
    merge_failures: int
    dropped_by_filter: int
    kept_singletons: int
    kept_merged: int
    elapsed_sec: float
