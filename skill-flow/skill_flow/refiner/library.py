"""Write the refined corpus directory layout.

Produces a corpus structure compatible with skill_flow.corpus.loader:

    <output_corpus_dir>/
        _metadata/index.json
        skillsmp/<key>/SKILL.md      # singleton skills passed through
        skillsmp/merged-<hash>/SKILL.md   # synthesized merge results
"""

from __future__ import annotations

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from skill_flow.models import SkillRecord
    from skill_flow.refiner.models import MergedSkill

logger = logging.getLogger(__name__)


def write_refined_corpus(
    source_corpus_dir: Path,
    output_corpus_dir: Path,
    kept_singletons: list[SkillRecord],
    kept_merged: list[MergedSkill],
) -> None:
    """Materialize the refined corpus on disk."""
    output_corpus_dir.mkdir(parents=True, exist_ok=True)
    meta_dir = output_corpus_dir / "_metadata"
    meta_dir.mkdir(parents=True, exist_ok=True)

    skills_entries: dict[str, dict[str, object]] = {}

    for record in kept_singletons:
        _copy_singleton(source_corpus_dir, output_corpus_dir, record)
        skills_entries[record.key] = _singleton_index_entry(record)

    for merged in kept_merged:
        _write_merged(output_corpus_dir, merged)
        skills_entries[merged.key] = _merged_index_entry(merged)

    index = {
        "version": "1.0-refined",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "skills": skills_entries,
    }
    (meta_dir / "index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    logger.info(
        "Wrote refined corpus to %s: %d singletons + %d merged = %d skills",
        output_corpus_dir,
        len(kept_singletons),
        len(kept_merged),
        len(skills_entries),
    )


def _copy_singleton(
    src_corpus_dir: Path,
    dest_corpus_dir: Path,
    record: SkillRecord,
) -> None:
    src_dir = src_corpus_dir / record.local_path
    dest_dir = dest_corpus_dir / record.local_path
    if not src_dir.exists():
        # Some metadata entries point at directories that lack SKILL.md;
        # synthesize a minimal one from the metadata so the loader is happy.
        dest_dir.mkdir(parents=True, exist_ok=True)
        skill_md = dest_dir / "SKILL.md"
        skill_md.write_text(
            f"---\nname: {record.name}\ndescription: {record.description}\n---\n",
            encoding="utf-8",
        )
        return
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    shutil.copytree(src_dir, dest_dir, symlinks=False)


def _write_merged(dest_corpus_dir: Path, merged: MergedSkill) -> None:
    folder = dest_corpus_dir / merged.key
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "SKILL.md").write_text(merged.content, encoding="utf-8")


def _singleton_index_entry(record: SkillRecord) -> dict[str, object]:
    entry: dict[str, object] = {
        "name": record.name,
        "description": record.description,
        "source": record.source,
        "local_path": record.local_path,
    }
    metadata = getattr(record, "metadata", None) or {}
    for k, v in metadata.items():
        if k not in entry:
            entry[k] = v
    return entry


def _merged_index_entry(merged: MergedSkill) -> dict[str, object]:
    return {
        "name": merged.name,
        "description": merged.description,
        "source": "skillsmp",
        "local_path": merged.key,
        "merged_from": merged.source_keys,
    }
