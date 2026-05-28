#!/usr/bin/env python3
"""
Detect the VCS for a given path.

Uses `jj root` when available, then falls back to walking parent directories
for `.jj` and `.git` markers.

Usage:
    python detect_vcs.py
    python detect_vcs.py --path /path/to/check
    python detect_vcs.py --format json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class VcsKind(str, Enum):
    JJ = "jj"
    GIT = "git"
    COLOCATED = "colocated"
    NONE = "none"


@dataclass(frozen=True)
class DetectionResult:
    kind: VcsKind
    path: Path
    root: Optional[Path]
    jj_root: Optional[Path]
    git_root: Optional[Path]
    jj_root_source: Optional[str]
    git_root_source: Optional[str]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict:
        return {
            "vcs": self.kind.value,
            "path": str(self.path),
            "root": str(self.root) if self.root else None,
            "jj_root": str(self.jj_root) if self.jj_root else None,
            "git_root": str(self.git_root) if self.git_root else None,
            "jj_root_source": self.jj_root_source,
            "git_root_source": self.git_root_source,
            "warnings": list(self.warnings),
        }

    def to_text(self) -> str:
        lines = [
            f"vcs: {self.kind.value}",
            f"root: {self.root if self.root else 'none'}",
            f"jj_root: {self.jj_root if self.jj_root else 'none'}",
            f"git_root: {self.git_root if self.git_root else 'none'}",
            f"path: {self.path}",
        ]
        if self.jj_root_source:
            lines.append(f"jj_root_source: {self.jj_root_source}")
        if self.git_root_source:
            lines.append(f"git_root_source: {self.git_root_source}")
        if self.warnings:
            lines.append("warnings:")
            lines.extend([f"- {warning}" for warning in self.warnings])
        return "\n".join(lines)


@dataclass(frozen=True)
class JjRootResult:
    root: Optional[Path]
    error: Optional[str]
    command_available: bool


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


def normalize_path(path_str: str) -> Path:
    path = Path(path_str).expanduser()
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    if path.is_dir():
        return path.resolve()
    return path.parent.resolve()


def try_jj_root(base_dir: Path) -> JjRootResult:
    try:
        result = subprocess.run(
            ["jj", "root"],
            cwd=base_dir,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        return JjRootResult(None, str(exc), False)

    if result.returncode != 0:
        error = (result.stderr or result.stdout or "").strip()
        return JjRootResult(None, error or "jj root failed", True)

    output = result.stdout.strip()
    if not output:
        return JjRootResult(None, "jj root returned empty output", True)

    root_path = Path(output)
    if not root_path.is_absolute():
        root_path = (base_dir / root_path).resolve()
    return JjRootResult(root_path, None, True)


def find_marker(start_dir: Path, marker: str) -> Optional[Path]:
    current = start_dir
    for candidate in [current, *current.parents]:
        if (candidate / marker).exists():
            return candidate
    return None


def detect_vcs(base_dir: Path) -> DetectionResult:
    warnings: list[str] = []

    jj_result = try_jj_root(base_dir)
    jj_root = None
    jj_root_source = None
    if jj_result.root:
        jj_root = jj_result.root
        jj_root_source = "jj root"
    else:
        if not jj_result.command_available:
            warnings.append("jj not found on PATH; skipped jj root")
        elif jj_result.error:
            lowered = jj_result.error.lower()
            if "no jj repo" not in lowered and "not a jj repo" not in lowered:
                warnings.append(f"jj root unavailable: {jj_result.error}")
        jj_root = find_marker(base_dir, ".jj")
        if jj_root:
            jj_root_source = "walk"

    git_root = find_marker(base_dir, ".git")
    git_root_source = "walk" if git_root else None

    if jj_root and git_root and jj_root == git_root:
        kind = VcsKind.COLOCATED
        root = jj_root
    elif jj_root:
        kind = VcsKind.JJ
        root = jj_root
    elif git_root:
        kind = VcsKind.GIT
        root = git_root
    else:
        kind = VcsKind.NONE
        root = None

    return DetectionResult(
        kind=kind,
        path=base_dir,
        root=root,
        jj_root=jj_root,
        git_root=git_root,
        jj_root_source=jj_root_source,
        git_root_source=git_root_source,
        warnings=tuple(warnings),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect VCS for a path.")
    parser.add_argument(
        "--path",
        default=".",
        help="Path to inspect (default: current directory)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (text or json)",
    )

    args = parser.parse_args()

    try:
        base_dir = normalize_path(args.path)
    except FileNotFoundError as exc:
        emit_error(
            format_name=args.format,
            what_failed="path does not exist",
            why_failed=str(exc),
            required="Provide an existing file or directory path",
            discovered=f"path={args.path}",
        )
        return

    result = detect_vcs(base_dir)

    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(result.to_text())


if __name__ == "__main__":
    main()
