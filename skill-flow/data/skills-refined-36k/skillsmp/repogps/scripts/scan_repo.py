#!/usr/bin/env python3
"""
RepoGPS scanner (standalone).

Usage:
  python scan_repo.py https://github.com/xai-org/x-algorithm
  python scan_repo.py https://github.com/owner/repo --branch main --out .repogps_cache
"""

from __future__ import annotations

import argparse
import pathlib
from typing import List

from _github import (
    RepoRef,
    parse_github_url,
    get_default_branch,
    get_repo_tree,
    fetch_files_parallel,
    safe_write_json,
    slugify_path,
    pick_key_files,
)


def main():
    ap = argparse.ArgumentParser(description="RepoGPS - Scan repository")
    ap.add_argument("repo_url", help="GitHub repo URL")
    ap.add_argument(
        "--branch", default=None, help="Branch name (default: repo default branch)"
    )
    ap.add_argument("--out", default=".repogps_cache", help="Output base directory")
    ap.add_argument(
        "--max-chars", type=int, default=120_000, help="Max chars per fetched file"
    )
    ap.add_argument(
        "--parallel", "-p", type=int, default=8, help="Parallel downloads (default: 8)"
    )
    args = ap.parse_args()

    ref: RepoRef = parse_github_url(args.repo_url)
    branch = args.branch or get_default_branch(ref)

    out_base = pathlib.Path(args.out)
    repo_dir = out_base / f"{ref.owner}__{ref.repo}__{branch}"
    repo_dir.mkdir(parents=True, exist_ok=True)

    print(f"[RepoGPS] Scanning: {args.repo_url} (branch={branch})")

    paths, truncated = get_repo_tree(ref, branch)
    if truncated:
        print("  ⚠ Repository has >100k files. Tree is truncated.")

    safe_write_json(
        repo_dir / "repo_tree.json",
        {
            "repo_url": args.repo_url,
            "branch": branch,
            "paths": paths,
            "truncated": truncated,
        },
    )

    groups = pick_key_files(paths)
    safe_write_json(repo_dir / "key_files.json", groups)

    key_files_flat: List[str] = []
    for v in groups.values():
        key_files_flat.extend(v)
    key_files_flat = sorted(set(key_files_flat))

    print(f"  Found {len(paths)} files, selected {len(key_files_flat)} key files")

    dl_dir = repo_dir / "downloaded"
    dl_dir.mkdir(parents=True, exist_ok=True)

    results = fetch_files_parallel(
        ref,
        branch,
        key_files_flat,
        dl_dir,
        max_chars=args.max_chars,
        max_workers=args.parallel,
    )

    downloaded_index = [
        {"path": r.path, "saved_as": r.saved_as} for r in results if r.success
    ]
    safe_write_json(repo_dir / "downloaded_index.json", downloaded_index)

    success = sum(1 for r in results if r.success)
    failed = sum(1 for r in results if not r.success)

    print(
        f"\n[RepoGPS] Done. Downloaded {success} files"
        + (f" ({failed} failed)" if failed else "")
    )
    print(f"  Output folder: {repo_dir}")


if __name__ == "__main__":
    main()
