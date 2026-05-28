"""Configuration defaults for reflect_sessions."""

from __future__ import annotations

from pathlib import Path

CACHE_SCHEMA_VERSION = "2026-01-12-v1"
DEFAULT_MAX_REFLECTIONS = 10
DEFAULT_MAX_WORKERS = 4
DEFAULT_CODEX_TIMEOUT_SECONDS = 120
DEFAULT_SESSIONS_ROOT = Path.home() / ".codex" / "sessions"
DEFAULT_CACHE_DIR_NAME = "reflection_cache"
DEFAULT_PREFIX = "[SELF-REFLECTION] "
PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
DEFAULT_PROMPT_PRESET = "reflection"
DEFAULT_PROMPT_PATH = PROMPTS_DIR / "reflection.md"
DEFAULT_PROMPT_VERSION_PATH = PROMPTS_DIR / "reflection_version.json"
PROMPT_PRESET_SPECS = (
    (
        "reflection",
        "reflection.md",
        "Full reflection on repetition, friction, and skill ideas.",
    ),
    (
        "summary",
        "summary.md",
        "Concise summary of goals, actions, outputs, and decisions.",
    ),
    (
        "bloat",
        "bloat.md",
        "Identify bloat, dead ends, and cleanup opportunities.",
    ),
    (
        "incomplete",
        "incomplete.md",
        "List unfinished work, open loops, and missing follow-ups.",
    ),
    (
        "decisions",
        "decisions.md",
        "Capture key decisions, alternatives, and rationale.",
    ),
    (
        "next_steps",
        "next_steps.md",
        "Concrete follow-up actions, tests, and validations.",
    ),
)
AUTO_REFRESH_REASONS = {
    "conversation_updated_after_reflection",
    "cache_schema_mismatch",
}
