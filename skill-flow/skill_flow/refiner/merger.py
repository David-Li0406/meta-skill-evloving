"""LLM-driven merger that synthesizes one SKILL.md from a cluster."""

from __future__ import annotations

import hashlib
import json
import logging
import re
import threading
from pathlib import Path
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from jinja2 import Template
from openai import OpenAI

from skill_flow.refiner.models import MergedSkill, MergerConfig

if TYPE_CHECKING:
    from skill_flow.models import SkillRecord

logger = logging.getLogger(__name__)


_FRONTMATTER_RE = re.compile(
    r"^---\s*\n(?P<fm>.*?)\n---\s*\n(?P<body>.*)$",
    re.DOTALL,
)
_NAME_RE = re.compile(r"^name\s*:\s*(.+?)\s*$", re.MULTILINE)
_DESC_RE = re.compile(r"^description\s*:\s*(.+?)\s*$", re.MULTILINE)
_SKILL_TAG_RE = re.compile(
    r"<skill>\s*(?P<body>.*?)\s*</skill>",
    re.DOTALL | re.IGNORECASE,
)
_SKILL_OPEN_RE = re.compile(r"<skill>\s*(?P<body>.*)$", re.DOTALL | re.IGNORECASE)


class SkillMdMerger:
    """Synthesize one SKILL.md from a cluster of source skills.

    Cached by the sorted tuple of source skill keys: if the same cluster
    appears twice (e.g. when re-running), the cached merged skill is reused.
    """

    def __init__(self, config: MergerConfig) -> None:
        self._config = config
        load_dotenv()
        self._client = OpenAI()
        self._template = Template(
            Path(config.instruction_path).read_text(encoding="utf-8"),
        )
        self._cache_path = Path(config.cache_path)
        self._cache: dict[str, dict[str, object]] = self._load_cache()
        self._lock = threading.RLock()
        self._save_every = 25  # batch disk writes to keep workers unblocked
        self._writes_since_save = 0

    def _load_cache(self) -> dict[str, dict[str, object]]:
        if self._cache_path.exists():
            data: dict[str, dict[str, object]] = json.loads(
                self._cache_path.read_text(encoding="utf-8"),
            )
            logger.info("Loaded %d merge cache entries", len(data))
            return data
        return {}

    def _save_cache(self) -> None:
        self._cache_path.parent.mkdir(parents=True, exist_ok=True)
        self._cache_path.write_text(
            json.dumps(self._cache, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @staticmethod
    def _cache_key(source_keys: list[str]) -> str:
        joined = "|".join(sorted(source_keys))
        return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:16]

    def merge(
        self,
        cluster: list[SkillRecord],
        contents: dict[str, str],
    ) -> MergedSkill | None:
        """Merge a cluster of >=2 skills into one MergedSkill.

        Returns ``None`` on LLM/parse failure.
        """
        if len(cluster) < 2:
            msg = "merge() requires a cluster of at least 2 skills"
            raise ValueError(msg)

        # Cap input size like SkillX merger.py:89
        capped = cluster[: self._config.max_group_size]
        source_keys = [s.key for s in capped]
        ckey = self._cache_key(source_keys)

        with self._lock:
            if ckey in self._cache:
                cached = self._cache[ckey]
                logger.debug("Merge cache hit for cluster of %d", len(capped))
                return MergedSkill(**cached)  # type: ignore[arg-type]

        user_msg = self._build_user_message(capped, contents)
        system_msg = self._template.render(skills=capped)
        content = self._call_llm(system_msg, user_msg)
        merged_md = self._extract_skill_block(content)
        if merged_md is None:
            logger.warning(
                "Merge failed (no <skill> block) for cluster %s; "
                "response head: %s",
                source_keys,
                content[:200],
            )
            return None

        name, desc = self._parse_frontmatter(merged_md)
        if not name:
            logger.warning(
                "Merge produced skill with no `name` for cluster %s",
                source_keys,
            )
            return None

        slug = self._slug(name)
        merged_key = f"skillsmp/merged-{ckey}-{slug}"[:120]
        merged = MergedSkill(
            key=merged_key,
            name=name,
            description=desc,
            content=merged_md,
            source_keys=source_keys,
        )

        with self._lock:
            self._cache[ckey] = merged.model_dump()
            self._writes_since_save += 1
            if self._writes_since_save >= self._save_every:
                self._save_cache()
                self._writes_since_save = 0
        return merged

    def flush(self) -> None:
        """Force a cache write — call this once after parallel merging."""
        with self._lock:
            if self._writes_since_save:
                self._save_cache()
                self._writes_since_save = 0

    @staticmethod
    def _build_user_message(
        cluster: list[SkillRecord],
        contents: dict[str, str],
    ) -> str:
        parts: list[str] = []
        for i, s in enumerate(cluster, 1):
            body = contents.get(s.key, "").strip()
            if not body:
                body = (
                    f"---\nname: {s.name}\ndescription: {s.description}\n---\n"
                    "(no content available)"
                )
            parts.append(f"=== SKILL {i}: {s.key} ===\n{body}")
        return "\n\n".join(parts)

    def _call_llm(self, system_msg: str, user_msg: str) -> str:
        kwargs: dict[str, object] = {
            "model": self._config.model,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            "max_completion_tokens": self._config.max_tokens,
        }
        if not self._config.model.startswith("gpt-5"):
            kwargs["temperature"] = self._config.temperature
        resp = self._client.chat.completions.create(**kwargs)  # type: ignore[call-overload]
        return resp.choices[0].message.content or ""

    @staticmethod
    def _extract_skill_block(content: str) -> str | None:
        match = _SKILL_TAG_RE.search(content)
        if match is not None:
            body = match.group("body").strip()
            return body or None
        # Tolerant fallback: response truncated before </skill>. Take
        # everything after the opening <skill> tag if it looks like SKILL.md.
        open_match = _SKILL_OPEN_RE.search(content)
        if open_match is None:
            return None
        body = open_match.group("body").strip()
        if body.startswith("---") and "\n---" in body:
            return body
        return None

    @staticmethod
    def _parse_frontmatter(md: str) -> tuple[str, str]:
        m = _FRONTMATTER_RE.match(md.strip())
        if m is None:
            return "", ""
        fm = m.group("fm")
        name_m = _NAME_RE.search(fm)
        desc_m = _DESC_RE.search(fm)
        name = name_m.group(1).strip().strip('"\'') if name_m else ""
        desc = desc_m.group(1).strip().strip('"\'') if desc_m else ""
        return name, desc

    @staticmethod
    def _slug(name: str) -> str:
        cleaned = re.sub(r"[^a-zA-Z0-9-]+", "-", name.lower())
        return cleaned.strip("-")[:32] or "skill"
