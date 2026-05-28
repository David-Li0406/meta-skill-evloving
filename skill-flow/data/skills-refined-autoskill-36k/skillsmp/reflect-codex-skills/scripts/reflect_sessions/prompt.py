"""Prompt handling for reflect_sessions."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .config import (
    DEFAULT_PROMPT_PATH,
    DEFAULT_PROMPT_PRESET,
    DEFAULT_PROMPT_VERSION_PATH,
    PROMPT_PRESET_SPECS,
    PROMPTS_DIR,
)
from .models import PromptVersionState
from .time import now_iso, utc_date_str


@dataclass(slots=True, frozen=True)
class PromptPreset:
    """Metadata describing a prompt preset.

    Attributes:
        name: CLI-facing preset name.
        path: Path to the preset prompt file.
        description: Short description of the preset.

    Example:
        preset = PromptPreset(
            name="summary",
            path=Path("prompts/summary.md"),
            description="Concise summary output.",
        )
    """

    name: str
    path: Path
    description: str

    def cli_label(self) -> str:
        """Return a one-line label for CLI help output."""
        return f"{self.name}: {self.description}"


@dataclass(slots=True)
class PromptSelection:
    """Resolved prompt selection from CLI arguments.

    Attributes:
        prompt_text: Prompt text to send to Codex.
        prompt_path: Optional prompt file path (None for inline prompts).
        source: Source label (preset, file, or inline).
        preset: Preset name when source is preset.

    Example:
        selection = PromptSelection(
            prompt_text="Summarize.",
            prompt_path=None,
            source="inline",
            preset=None,
        )
    """

    prompt_text: str
    prompt_path: Path | None
    source: str
    preset: str | None

    def label(self, *, prompt_hash: str) -> str:
        """Return the canonical label for prompt output metadata.

        Args:
            prompt_hash: SHA-256 hash for the prompt text.

        Returns:
            Label string to record for the prompt source.
        """
        if self.prompt_path:
            return str(self.prompt_path)
        return f"inline:{prompt_hash[:8]}"

    def version_state_path(self, *, prompt_hash: str, cache_dir: Path) -> Path:
        """Return the version state path for this prompt selection.

        Args:
            prompt_hash: SHA-256 hash for the prompt text.
            cache_dir: Cache directory for inline prompt state.

        Returns:
            Path to the prompt version state file.
        """
        if self.prompt_path:
            return prompt_version_path_for_prompt(prompt_path=self.prompt_path)
        return inline_prompt_version_path(prompt_hash=prompt_hash, cache_dir=cache_dir)


def prompt_presets() -> list[PromptPreset]:
    """Return the available prompt presets.

    Returns:
        List of prompt preset metadata.
    """
    return [
        PromptPreset(name=name, path=PROMPTS_DIR / filename, description=description)
        for name, filename, description in PROMPT_PRESET_SPECS
    ]


def prompt_preset_choices() -> tuple[str, ...]:
    """Return preset names for argparse choices.

    Returns:
        Tuple of preset names.
    """
    return tuple(preset.name for preset in prompt_presets())


def prompt_preset_help() -> str:
    """Return a compact help string describing prompt presets.

    Returns:
        Help string suitable for argparse descriptions.
    """
    labels = "; ".join(preset.cli_label() for preset in prompt_presets())
    return f"Available presets: {labels}"


def prompt_cache_key(*, prompt_label: str) -> str:
    """Return a stable cache key for a prompt label.

    Args:
        prompt_label: Label describing the prompt source.

    Returns:
        Short cache key string derived from the label.

    Example:
        key = prompt_cache_key(prompt_label="/path/to/reflection.md")
    """
    digest = hashlib.sha256(prompt_label.encode("utf-8")).hexdigest()
    return digest[:12]


def is_default_prompt_path(*, prompt_path: Path | None) -> bool:
    """Return True when the prompt path matches the default prompt.

    Args:
        prompt_path: Prompt file path, if any.

    Returns:
        True when the resolved prompt path matches the default prompt.
    """
    if prompt_path is None:
        return False
    return prompt_path.resolve() == DEFAULT_PROMPT_PATH.resolve()


def resolve_prompt_preset(*, name: str) -> PromptPreset:
    """Resolve a prompt preset by name.

    Args:
        name: Preset name from the CLI.

    Returns:
        PromptPreset metadata.

    Example:
        preset = resolve_prompt_preset(name="summary")
    """
    presets = {preset.name: preset for preset in prompt_presets()}
    assert name in presets, f"Unknown prompt preset: {name}"
    preset = presets[name]
    assert preset.path.exists(), f"Prompt preset file not found: {preset.path}"
    return preset


def resolve_prompt_selection(
    *,
    prompt_file: Path | None,
    prompt_preset: str | None,
    prompt_text: str | None,
) -> PromptSelection:
    """Resolve the prompt selection from CLI arguments.

    Args:
        prompt_file: Optional file path to a prompt.
        prompt_preset: Optional preset name.
        prompt_text: Optional inline prompt text.

    Returns:
        PromptSelection describing the resolved prompt source.

    Example:
        selection = resolve_prompt_selection(
            prompt_file=None,
            prompt_preset="summary",
            prompt_text=None,
        )
    """
    selected = [
        prompt_file is not None,
        prompt_preset is not None,
        prompt_text is not None,
    ]
    assert sum(selected) <= 1, (
        "Use only one of --prompt-file, --prompt-preset, or --prompt-text."
    )
    if prompt_text is not None:
        cleaned = prompt_text.strip()
        assert cleaned, "Prompt text is empty."
        return PromptSelection(
            prompt_text=cleaned,
            prompt_path=None,
            source="inline",
            preset=None,
        )
    if prompt_preset is None and prompt_file is None:
        prompt_preset = DEFAULT_PROMPT_PRESET
    if prompt_preset is not None:
        preset = resolve_prompt_preset(name=prompt_preset)
        prompt_text = load_prompt_text(prompt_path=preset.path)
        return PromptSelection(
            prompt_text=prompt_text,
            prompt_path=preset.path,
            source="preset",
            preset=preset.name,
        )
    assert prompt_file is not None
    resolved = resolve_prompt_path(prompt_file=prompt_file)
    prompt_text = load_prompt_text(prompt_path=resolved)
    return PromptSelection(
        prompt_text=prompt_text,
        prompt_path=resolved,
        source="file",
        preset=None,
    )


def next_prompt_version(*, previous_version: str | None, date_str: str) -> str:
    """Build the next prompt version for the given date.

    Args:
        previous_version: Last prompt version string.
        date_str: Date string in YYYY-MM-DD format.

    Returns:
        New prompt version string.
    """
    if previous_version and previous_version.startswith(f"{date_str}-v"):
        suffix = previous_version.split("-v", maxsplit=1)[-1]
        if suffix.isdigit():
            return f"{date_str}-v{int(suffix) + 1}"
    return f"{date_str}-v1"


def prompt_version_path_for_prompt(*, prompt_path: Path) -> Path:
    """Return the prompt version state path for a prompt file.

    Args:
        prompt_path: Path to the prompt file.

    Returns:
        Path to the corresponding prompt version state file.

    Example:
        state_path = prompt_version_path_for_prompt(
            prompt_path=Path("prompts/reflection.md"),
        )
    """
    if prompt_path == DEFAULT_PROMPT_PATH:
        return DEFAULT_PROMPT_VERSION_PATH
    return prompt_path.with_name(f"{prompt_path.stem}_version.json")


def inline_prompt_version_path(*, prompt_hash: str, cache_dir: Path) -> Path:
    """Return the version state path for an inline prompt.

    Args:
        prompt_hash: SHA-256 hash for the prompt text.
        cache_dir: Cache directory for storing prompt state.

    Returns:
        Path to the inline prompt version state file.

    Example:
        path = inline_prompt_version_path(
            prompt_hash="hash",
            cache_dir=Path("/tmp/cache"),
        )
    """
    prompt_dir = cache_dir / "prompt_versions"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    return prompt_dir / f"inline_{prompt_hash}.json"


def load_prompt_version_state(*, path: Path) -> PromptVersionState:
    """Load prompt version state from disk.

    Args:
        path: Path to the prompt version state file.

    Returns:
        PromptVersionState instance.
    """
    if not path.exists():
        return PromptVersionState(prompt_version="", prompt_hash="", updated_at="")
    data = json.loads(path.read_text())
    assert isinstance(data, dict), "Prompt version state is not a dict"
    return PromptVersionState.from_dict(data=data)


def write_prompt_version_state(*, path: Path, state: PromptVersionState) -> None:
    """Write prompt version state to disk.

    Args:
        path: Path to the prompt version state file.
        state: Prompt version state to write.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(state.to_dict(), indent=2, ensure_ascii=True)
    path.write_text(payload + "\n")


def ensure_prompt_version_state(
    *, state_path: Path, prompt_hash: str, now: datetime
) -> PromptVersionState:
    """Ensure the prompt version state matches the current prompt hash.

    Args:
        state_path: Path to the prompt version state file.
        prompt_hash: SHA-256 hash of the prompt text.
        now: Current timestamp in UTC.

    Returns:
        PromptVersionState reflecting the latest prompt hash.

    Example:
        state = ensure_prompt_version_state(
            state_path=Path("prompts/reflection_version.json"),
            prompt_hash="hash",
            now=datetime(2026, 1, 12, tzinfo=timezone.utc),
        )
    """
    state = load_prompt_version_state(path=state_path)
    date_str = utc_date_str(timestamp=now)
    if not state.prompt_version or state.prompt_hash != prompt_hash:
        prompt_version = next_prompt_version(
            previous_version=state.prompt_version or None,
            date_str=date_str,
        )
        state = PromptVersionState(
            prompt_version=prompt_version,
            prompt_hash=prompt_hash,
            updated_at=now_iso(),
        )
        write_prompt_version_state(path=state_path, state=state)
    return state


def resolve_prompt_path(*, prompt_file: Path | None) -> Path:
    """Resolve the prompt file path.

    Args:
        prompt_file: Optional file path containing the prompt.

    Returns:
        Path to the prompt file.

    Example:
        prompt_path = resolve_prompt_path(prompt_file=None)
    """
    resolved = (prompt_file or DEFAULT_PROMPT_PATH).expanduser()
    assert resolved.exists(), f"Prompt file not found: {resolved}"
    return resolved


def load_prompt_text(*, prompt_path: Path) -> str:
    """Load the reflection prompt text.

    Args:
        prompt_path: Path containing the prompt.

    Returns:
        Prompt string.

    Example:
        prompt = load_prompt_text(prompt_path=Path("prompts/reflection.md"))
    """
    text = prompt_path.read_text().strip()
    assert text, f"Prompt file is empty: {prompt_path}"
    return text


def compute_prompt_hash(*, prompt_text: str) -> str:
    """Compute a SHA-256 hash for the prompt text.

    Args:
        prompt_text: Prompt text to hash.

    Returns:
        Hex digest for the prompt text.

    Example:
        digest = compute_prompt_hash(prompt_text="Hello")
    """
    return hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()
