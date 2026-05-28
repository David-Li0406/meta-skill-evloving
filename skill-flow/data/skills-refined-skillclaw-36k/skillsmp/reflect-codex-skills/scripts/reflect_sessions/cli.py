"""Command-line argument parsing for reflect_sessions."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import (
    DEFAULT_CODEX_TIMEOUT_SECONDS,
    DEFAULT_PREFIX,
    DEFAULT_PROMPT_PRESET,
    DEFAULT_SESSIONS_ROOT,
)
from .prompt import prompt_preset_choices, prompt_preset_help


def add_root_args(*, parser: argparse.ArgumentParser) -> None:
    """Add session root and cache arguments to the parser.

    Args:
        parser: ArgumentParser to update.
    """
    parser.add_argument(
        "--sessions-root",
        type=Path,
        default=DEFAULT_SESSIONS_ROOT,
        help="Root directory containing Codex session JSONL files.",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        help="Directory to store cached reflections (default: sessions_root/reflection_cache).",
    )


def add_output_args(*, parser: argparse.ArgumentParser) -> None:
    """Add output arguments to the parser.

    Args:
        parser: ArgumentParser to update.
    """
    parser.add_argument(
        "--output",
        type=str,
        default="-",
        help="Output JSON path, or '-' for stdout.",
    )
    parser.add_argument(
        "--output-style",
        type=str,
        default="json",
        choices=("human", "json", "json_extra_metadata"),
        help="Output style: human, json, or json_extra_metadata.",
    )


def add_listing_args(*, parser: argparse.ArgumentParser) -> None:
    """Add listing arguments to the parser.

    Args:
        parser: ArgumentParser to update.
    """
    parser.add_argument(
        "--list-projects",
        action="store_true",
        help="List available projects after filtering and exit.",
    )


def add_filter_args(*, parser: argparse.ArgumentParser) -> None:
    """Add session filtering arguments to the parser.

    Args:
        parser: ArgumentParser to update.
    """
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit to the most recent N sessions after filtering.",
    )
    parser.add_argument(
        "--project",
        type=str,
        help="Only include sessions matching this project label.",
    )
    parser.add_argument(
        "--since",
        type=str,
        help="Only include sessions on/after this ISO date or datetime.",
    )
    parser.add_argument(
        "--until",
        type=str,
        help="Only include sessions on/before this ISO date or datetime.",
    )
    parser.add_argument(
        "--session-id",
        action="append",
        help="Include a specific session id (repeatable).",
    )
    parser.add_argument(
        "--session-ids",
        type=str,
        help="Comma-separated session ids to include.",
    )
    parser.add_argument(
        "--include-most-recent",
        action="store_true",
        help="Include the most recent session (skipped by default).",
    )
    parser.add_argument(
        "--refresh-mode",
        type=str,
        default="never",
        choices=("never", "auto", "always"),
        help="Cache refresh mode: never, auto, or always.",
    )
    parser.add_argument(
        "--sequential",
        action="store_true",
        help="Run reflections sequentially instead of in parallel.",
    )


def add_prompt_args(*, parser: argparse.ArgumentParser) -> None:
    """Add prompt and reflection behavior arguments.

    Args:
        parser: ArgumentParser to update.
    """
    parser.add_argument(
        "--prefix",
        type=str,
        default=DEFAULT_PREFIX,
        help="Prefix for the duplicated session's first user message.",
    )
    parser.add_argument(
        "--prompt-preset",
        type=str,
        choices=prompt_preset_choices(),
        help=(
            f"Preset prompt to use (default: {DEFAULT_PROMPT_PRESET}). "
            f"{prompt_preset_help()}"
        ),
    )
    parser.add_argument(
        "--prompt-file",
        type=Path,
        help=(
            "Optional path to a custom prompt text file "
            "(mutually exclusive with --prompt-preset and --prompt-text)."
        ),
    )
    parser.add_argument(
        "--prompt-text",
        type=str,
        help=(
            "Inline prompt text "
            "(mutually exclusive with --prompt-preset and --prompt-file)."
        ),
    )


def add_codex_args(*, parser: argparse.ArgumentParser) -> None:
    """Add codex execution arguments to the parser.

    Args:
        parser: ArgumentParser to update.
    """
    parser.add_argument(
        "--codex-sandbox",
        type=str,
        default="read-only",
        help="Sandbox mode to pass to codex (default: read-only).",
    )
    parser.add_argument(
        "--codex-approval",
        type=str,
        default="never",
        help="Approval policy to pass to codex (default: never).",
    )
    parser.add_argument(
        "--codex-timeout-seconds",
        type=int,
        default=DEFAULT_CODEX_TIMEOUT_SECONDS,
        help="Timeout for a single codex exec call (default: 120).",
    )
    parser.add_argument(
        "--codex-path",
        type=str,
        help="Optional path to the codex binary (defaults to PATH lookup).",
    )


def add_debug_args(*, parser: argparse.ArgumentParser) -> None:
    """Add debugging arguments to the parser.

    Args:
        parser: ArgumentParser to update.
    """
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print debug information to stderr.",
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate reflections for Codex sessions and cache the results."
    )
    add_root_args(parser=parser)
    add_output_args(parser=parser)
    add_listing_args(parser=parser)
    add_filter_args(parser=parser)
    add_prompt_args(parser=parser)
    add_codex_args(parser=parser)
    add_debug_args(parser=parser)
    return parser.parse_args()
