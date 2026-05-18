"""LLM general-filter that decides keep / drop per SKILL.md.

Adapts SkillX/filtering/general_filter.py — same keep/drop verdict pattern,
adjusted rubric for SKILL.md (no `apis.*` checks; checks frontmatter,
reusability, non-triviality).
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import threading
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Template
from openai import OpenAI

from skill_flow.refiner.models import QualityFilterConfig

logger = logging.getLogger(__name__)


_ANSWER_RE = re.compile(
    r"<answer>\s*(?P<verdict>keep|drop|good|bad)\s*</answer>",
    re.IGNORECASE | re.DOTALL,
)


class SkillMdQualityFilter:
    """Keep-or-drop verdict for a single SKILL.md, with JSON caching.

    Cache key = sha256(skill_key + content). Re-running on the same
    content reuses the cached verdict.
    """

    def __init__(self, config: QualityFilterConfig) -> None:
        self._config = config
        load_dotenv()
        self._client = OpenAI()
        self._template = Template(
            Path(config.instruction_path).read_text(encoding="utf-8"),
        )
        self._cache_path = Path(config.cache_path)
        self._cache: dict[str, dict[str, str]] = self._load_cache()
        self._lock = threading.RLock()
        self._save_every = 200
        self._writes_since_save = 0

    def _load_cache(self) -> dict[str, dict[str, str]]:
        if self._cache_path.exists():
            data: dict[str, dict[str, str]] = json.loads(
                self._cache_path.read_text(encoding="utf-8"),
            )
            logger.info("Loaded %d filter cache entries", len(data))
            return data
        return {}

    def _save_cache(self) -> None:
        self._cache_path.parent.mkdir(parents=True, exist_ok=True)
        self._cache_path.write_text(
            json.dumps(self._cache, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @staticmethod
    def _cache_key(skill_key: str, content: str) -> str:
        h = hashlib.sha256()
        h.update(skill_key.encode("utf-8"))
        h.update(b"\x00")
        h.update(content.encode("utf-8"))
        return h.hexdigest()[:16]

    def judge(self, skill_key: str, content: str) -> bool:
        """Return True to keep, False to drop. Defaults to keep on failure."""
        ckey = self._cache_key(skill_key, content)
        with self._lock:
            if ckey in self._cache:
                return self._cache[ckey].get("verdict") == "keep"

        system_msg = self._template.render()
        user_msg = f"=== SKILL: {skill_key} ===\n{content}"
        try:
            response = self._call_llm(system_msg, user_msg)
            verdict, reason = self._parse_verdict(response)
        except Exception as exc:  # noqa: BLE001 — log and fall back
            logger.warning(
                "Quality filter failed for %s: %s — defaulting to KEEP",
                skill_key,
                exc,
            )
            verdict, reason = "keep", "filter-error-default-keep"

        with self._lock:
            self._cache[ckey] = {"verdict": verdict, "reason": reason}
            self._writes_since_save += 1
            if self._writes_since_save >= self._save_every:
                self._save_cache()
                self._writes_since_save = 0
        return verdict == "keep"

    def flush(self) -> None:
        """Force a cache write — call once after parallel judging."""
        with self._lock:
            if self._writes_since_save:
                self._save_cache()
                self._writes_since_save = 0

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
    def _parse_verdict(response: str) -> tuple[str, str]:
        m = _ANSWER_RE.search(response)
        if m is None:
            # Fallback heuristic: any clear keep/good signal anywhere?
            text = response.lower()
            verdict = "keep" if "keep" in text or "good" in text else "drop"
            return verdict, "no-answer-tag"
        raw = m.group("verdict").lower()
        verdict = "keep" if raw in {"keep", "good"} else "drop"
        reason_m = re.search(
            r"<reason>\s*(.*?)\s*</reason>",
            response,
            re.IGNORECASE | re.DOTALL,
        )
        reason = reason_m.group(1).strip() if reason_m else ""
        return verdict, reason[:160]
