#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


# Exclude worker-local and machine-local state files.
# `.auth_current_name` can pin Codex to a different auth file than `auth.json`,
# which breaks skills that intentionally inject a specific `auth.json`.
EXCLUDE_ROOT = {"sessions", "log", "history.jsonl", ".auth_current_name"}


def _is_same_filetype(src: Path, dst: Path) -> bool:
    try:
        # Treat symlinks distinctly: Path.is_file()/is_dir() follow links.
        if src.is_symlink() or dst.is_symlink():
            return src.is_symlink() and dst.is_symlink()
        if src.is_dir() and dst.is_dir():
            return True
        if src.is_file() and dst.is_file():
            return True
    except OSError:
        return False
    return False


def _safe_unlink(path: Path) -> None:
    try:
        if path.is_symlink() or path.is_file():
            path.unlink()
        else:
            shutil.rmtree(path)
    except FileNotFoundError:
        return


def _sync_entry(src: Path, dst: Path) -> None:
    if dst.exists() and not _is_same_filetype(src, dst):
        _safe_unlink(dst)

    if src.is_symlink():
        target = os.readlink(src)
        if dst.exists():
            _safe_unlink(dst)
        dst.symlink_to(target)
        return

    if src.is_dir():
        _sync_dir(src, dst)
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _sync_dir(src_dir: Path, dst_dir: Path) -> None:
    dst_dir.mkdir(parents=True, exist_ok=True)
    try:
        src_children = {p.name: p for p in src_dir.iterdir()}
    except OSError:
        return

    # Copy/update
    for name, src_child in src_children.items():
        _sync_entry(src_child, dst_dir / name)

    # Delete extras
    try:
        for dst_child in dst_dir.iterdir():
            if dst_child.name not in src_children:
                _safe_unlink(dst_child)
    except OSError:
        return


def sync_codex_home(src_root: Path, dst_root: Path) -> None:
    src_root = src_root.expanduser()
    dst_root = dst_root.expanduser()
    if not src_root.exists():
        raise FileNotFoundError(f"source CODEX_HOME not found: {src_root}")

    dst_root.mkdir(parents=True, exist_ok=True)

    try:
        src_entries = {p.name: p for p in src_root.iterdir() if p.name not in EXCLUDE_ROOT}
    except OSError as exc:
        raise RuntimeError(f"failed to list source CODEX_HOME: {exc}") from exc

    # Copy/update included entries
    for name, src_entry in src_entries.items():
        _sync_entry(src_entry, dst_root / name)

    # Delete extras in dst, but preserve excluded root items (worker-local)
    try:
        for dst_entry in dst_root.iterdir():
            if dst_entry.name in EXCLUDE_ROOT:
                continue
            if dst_entry.name not in src_entries:
                _safe_unlink(dst_entry)
    except OSError:
        pass

    # Ensure worker-local dirs exist
    (dst_root / "sessions").mkdir(parents=True, exist_ok=True)
    (dst_root / "log").mkdir(parents=True, exist_ok=True)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Sync ~/.codex into a per-worker CODEX_HOME, excluding sessions/log/history.jsonl."
    )
    parser.add_argument("--src", default=str(Path.home() / ".codex"), help="Source CODEX_HOME (default: ~/.codex)")
    parser.add_argument("--dst", required=True, help="Destination CODEX_HOME (per-worker).")
    args = parser.parse_args(argv[1:])

    try:
        sync_codex_home(Path(args.src), Path(args.dst))
        return 0
    except Exception as exc:
        print(f"❌ sync_codex_home failed: {exc}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(os.sys.argv))
