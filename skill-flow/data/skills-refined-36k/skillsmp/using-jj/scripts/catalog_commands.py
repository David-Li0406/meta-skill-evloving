#!/usr/bin/env python3
"""
Build a catalog of jj commands.

Preferred source: `jj util markdown-help`.
Fallback source: `jj util completion bash` (command names only).

Usage:
    python catalog_commands.py
    python catalog_commands.py --format json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class SourceKind(str, Enum):
    MARKDOWN_HELP = "markdown-help"
    COMPLETION_BASH = "completion:bash"


@dataclass
class CommandEntry:
    name: str
    summary: Optional[str] = None
    usage: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "summary": self.summary,
            "usage": self.usage,
        }


@dataclass
class CatalogResult:
    source: SourceKind
    commands: list[CommandEntry]

    def to_dict(self) -> dict:
        return {
            "source": self.source.value,
            "generated_at": datetime.now(timezone.utc)
            .isoformat()
            .replace("+00:00", "Z"),
            "command_count": len(self.commands),
            "commands": [entry.to_dict() for entry in self.commands],
        }

    def to_text(self) -> str:
        lines = [
            f"source: {self.source.value}",
            f"count: {len(self.commands)}",
        ]
        for entry in self.commands:
            summary = entry.summary or "(no summary available)"
            lines.append(f"{entry.name} - {summary}")
        return "\n".join(lines)


def emit_error(
    *,
    format_name: str,
    what_failed: str,
    why_failed: str,
    required: str,
    discovered: Optional[str] = None,
) -> None:
    payload = {
        "what_failed": what_failed,
        "why_failed": why_failed,
        "required": required,
        "discovered": discovered,
    }
    if format_name == "json":
        print(json.dumps({"error": payload}, indent=2))
    else:
        lines = [
            f"Error: {what_failed}",
            f"Why: {why_failed}",
            f"Required: {required}",
        ]
        if discovered:
            lines.append(f"Discovered: {discovered}")
        print("\n".join(lines), file=sys.stderr)
    sys.exit(1)


def run_jj(argv: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            argv,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise FileNotFoundError("jj executable not found") from exc


def load_markdown_help() -> str:
    result = run_jj(["jj", "util", "markdown-help"])
    if result.returncode != 0:
        error = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(error or "jj util markdown-help failed")
    output = result.stdout
    if not output.strip():
        raise RuntimeError("jj util markdown-help returned empty output")
    return output


def strip_inline_markdown(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text


def parse_usage(line: str) -> Optional[str]:
    if not line.startswith("**Usage:**"):
        return None
    content = line.split("**Usage:**", 1)[1].strip()
    if content.startswith("`") and content.endswith("`"):
        return content.strip("`")
    match = re.match(r"`([^`]+)`", content)
    if match:
        return match.group(1)
    return content or None


def parse_markdown_help(text: str) -> list[CommandEntry]:
    commands: list[CommandEntry] = []
    current: Optional[CommandEntry] = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        heading = re.match(r"^## `([^`]+)`\s*$", line)
        if heading:
            if current:
                commands.append(current)
            current = CommandEntry(name=heading.group(1).strip())
            continue

        if not current:
            continue

        stripped = line.strip()
        if not stripped:
            continue

        usage = parse_usage(stripped)
        if usage and current.usage is None:
            current.usage = usage
            continue

        if current.summary is None:
            if stripped.startswith("######"):
                continue
            current.summary = strip_inline_markdown(stripped)

    if current:
        commands.append(current)

    return commands


def load_completion_commands() -> list[CommandEntry]:
    result = run_jj(["jj", "util", "completion", "bash"])
    if result.returncode != 0:
        error = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(error or "jj util completion bash failed")
    output = result.stdout
    if not output.strip():
        raise RuntimeError("jj util completion bash returned empty output")

    commands = sorted(parse_bash_completion(output))
    return [CommandEntry(name=command) for command in commands]


def decode_bash_state(state: str) -> Optional[list[str]]:
    if state == "jj":
        return ["jj"]
    if state.startswith("jj__"):
        rest = state[len("jj__") :]
        parts = ["jj"] + [part for part in rest.split("__") if part]
        return parts
    return None


def parse_bash_completion(text: str) -> set[str]:
    commands: set[str] = {"jj"}
    pattern = re.compile(r"^\s*([A-Za-z0-9_]+),([A-Za-z0-9_-]+)\)")

    for line in text.splitlines():
        match = pattern.match(line)
        if not match:
            continue
        state, token = match.groups()
        parts = decode_bash_state(state)
        if not parts:
            continue
        command = " ".join(parts + [token])
        commands.add(command)

    return commands


def build_catalog() -> CatalogResult:
    markdown_error: Optional[str] = None
    try:
        markdown = load_markdown_help()
        commands = parse_markdown_help(markdown)
        if commands:
            return CatalogResult(source=SourceKind.MARKDOWN_HELP, commands=commands)
        markdown_error = "jj util markdown-help produced no commands"
    except FileNotFoundError as exc:
        raise exc
    except RuntimeError as exc:
        markdown_error = str(exc)

    completion_error: Optional[str] = None
    try:
        completion_commands = load_completion_commands()
        if completion_commands:
            return CatalogResult(
                source=SourceKind.COMPLETION_BASH, commands=completion_commands
            )
        completion_error = "jj util completion produced no commands"
    except RuntimeError as exc:
        completion_error = str(exc)

    details = " ; ".join(
        part
        for part in [
            f"markdown-help: {markdown_error}" if markdown_error else None,
            f"completion: {completion_error}" if completion_error else None,
        ]
        if part
    )
    raise RuntimeError(details or "No command metadata available")


def main() -> None:
    parser = argparse.ArgumentParser(description="Catalog jj commands.")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (text or json)",
    )

    args = parser.parse_args()

    try:
        catalog = build_catalog()
    except FileNotFoundError:
        emit_error(
            format_name=args.format,
            what_failed="jj executable not found",
            why_failed="jj is not installed or not on PATH",
            required="Install jj or ensure it is on PATH",
            discovered="command=jj util markdown-help",
        )
        return
    except RuntimeError as exc:
        emit_error(
            format_name=args.format,
            what_failed="command metadata unavailable",
            why_failed=str(exc),
            required="A working jj executable with metadata commands",
            discovered="tried: jj util markdown-help; fallback: jj util completion bash",
        )
        return

    if args.format == "json":
        print(json.dumps(catalog.to_dict(), indent=2))
    else:
        print(catalog.to_text())


if __name__ == "__main__":
    main()
