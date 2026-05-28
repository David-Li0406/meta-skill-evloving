#!/usr/bin/env python3
"""
RepoGPS - Main orchestrator for scanning and analyzing repositories.

Supports both GitHub repositories and local directories.

This script chains together:
1. Scan repo - Fetches repo tree and downloads/copies key files
2. Find entrypoints - Identifies likely code entrypoints
3. Extract runbook - Extracts run/test commands

Usage:
  # GitHub URL
  python repogps.py https://github.com/xai-org/x-algorithm
  python repogps.py https://github.com/owner/repo --branch main --out .repogps_cache

  # Local directory
  python repogps.py /path/to/local/repo
  python repogps.py ./my-project --out .repogps_cache
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import re
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any, Union

from _github import (
    RepoRef,
    LocalRef,
    parse_github_url,
    is_local_path,
    parse_local_path,
    get_default_branch,
    get_repo_tree,
    get_local_tree,
    fetch_text_file,
    fetch_files_parallel,
    copy_local_files,
    safe_write_json,
    safe_write_text,
    slugify_path,
    pick_key_files,
    setup_logging,
    logger,
    ProgressReporter,
    DownloadResult,
    score_entrypoint_path,
    score_entrypoint_content,
    extract_ci_commands,
    ENTRYPOINT_PATTERNS,
    CONTENT_HINTS,
    # Shared command extraction utilities
    load_downloaded_text,
    load_key_files,
    dedupe,
    extract_commands_from_readme,
    extract_from_package_json,
    extract_from_makefile,
    detect_languages,
)


@dataclass
class AnalysisResult:
    """Result of a complete repository analysis."""

    success: bool
    cache_dir: Optional[pathlib.Path] = None
    error: Optional[str] = None
    stages_completed: List[str] = None

    def __post_init__(self):
        if self.stages_completed is None:
            self.stages_completed = []


# =============================================================================
# STAGE 1: SCAN REPOSITORY (GitHub or Local)
# =============================================================================


def scan_github(
    repo_url: str,
    branch: Optional[str],
    out_base: pathlib.Path,
    max_chars: int,
    parallel_downloads: int = 8,
    verbose: bool = False,
) -> pathlib.Path:
    """
    Stage 1 for GitHub: Fetch repo tree and download key files.
    Returns the output directory path.
    """
    ref: RepoRef = parse_github_url(repo_url)
    branch = branch or get_default_branch(ref)

    repo_dir = out_base / f"{ref.owner}__{ref.repo}__{branch}"
    repo_dir.mkdir(parents=True, exist_ok=True)

    print(f"[RepoGPS] Stage 1: Scanning {repo_url} (branch={branch})")

    # Get file tree
    paths, truncated = get_repo_tree(ref, branch)
    if truncated:
        print(f"  ⚠ Repository has >100k files. Analysis may be incomplete.")

    safe_write_json(
        repo_dir / "repo_tree.json",
        {
            "repo_url": repo_url,
            "branch": branch,
            "paths": paths,
            "truncated": truncated,
            "total_files": len(paths),
            "source": "github",
        },
    )

    # Select key files
    groups = pick_key_files(paths)
    safe_write_json(repo_dir / "key_files.json", groups)

    key_files_flat: List[str] = []
    for v in groups.values():
        key_files_flat.extend(v)
    key_files_flat = sorted(set(key_files_flat))

    print(f"  Found {len(paths)} files, selected {len(key_files_flat)} key files")

    # Download files
    dl_dir = repo_dir / "downloaded"
    dl_dir.mkdir(parents=True, exist_ok=True)

    if parallel_downloads > 1:
        # Parallel download
        results = fetch_files_parallel(
            ref,
            branch,
            key_files_flat,
            dl_dir,
            max_chars=max_chars,
            max_workers=parallel_downloads,
            show_progress=True,
        )
        downloaded_index = [
            {"path": r.path, "saved_as": r.saved_as} for r in results if r.success
        ]
        success_count = sum(1 for r in results if r.success)
        fail_count = sum(1 for r in results if not r.success)
    else:
        # Sequential download (legacy)
        downloaded_index = []
        success_count = 0
        fail_count = 0
        for path in key_files_flat:
            try:
                text = fetch_text_file(ref, branch, path, max_chars=max_chars)
                out_path = dl_dir / f"{slugify_path(path)}.txt"
                safe_write_text(out_path, text)
                downloaded_index.append(
                    {"path": path, "saved_as": str(out_path.relative_to(repo_dir))}
                )
                print(f"  ✓ {path}")
                success_count += 1
            except Exception as e:
                print(f"  ✗ {path} ({e})")
                fail_count += 1

    safe_write_json(repo_dir / "downloaded_index.json", downloaded_index)
    print(
        f"  Downloaded {success_count} files"
        + (f" ({fail_count} failed)" if fail_count else "")
    )

    return repo_dir


def scan_local(
    local_path: str,
    out_base: pathlib.Path,
    max_chars: int,
    verbose: bool = False,
) -> pathlib.Path:
    """
    Stage 1 for local directories: Scan tree and copy key files.
    Returns the output directory path.
    """
    ref: LocalRef = parse_local_path(local_path)

    # Create cache directory name from local path
    safe_name = re.sub(r"[^\w\-.]", "_", ref.name)
    repo_dir = out_base / f"local__{safe_name}"
    repo_dir.mkdir(parents=True, exist_ok=True)

    print(f"[RepoGPS] Stage 1: Scanning local directory {ref.path}")

    # Get file tree
    paths, truncated = get_local_tree(ref)
    if truncated:
        print(f"  ⚠ Directory has >100k files. Analysis may be incomplete.")

    safe_write_json(
        repo_dir / "repo_tree.json",
        {
            "repo_url": str(ref.path),
            "branch": "local",
            "paths": paths,
            "truncated": truncated,
            "total_files": len(paths),
            "source": "local",
        },
    )

    # Select key files
    groups = pick_key_files(paths)
    safe_write_json(repo_dir / "key_files.json", groups)

    key_files_flat: List[str] = []
    for v in groups.values():
        key_files_flat.extend(v)
    key_files_flat = sorted(set(key_files_flat))

    print(f"  Found {len(paths)} files, selected {len(key_files_flat)} key files")

    # Copy files to cache
    dl_dir = repo_dir / "downloaded"
    dl_dir.mkdir(parents=True, exist_ok=True)

    results = copy_local_files(
        ref,
        key_files_flat,
        dl_dir,
        max_chars=max_chars,
        show_progress=True,
    )

    downloaded_index = [
        {"path": r.path, "saved_as": r.saved_as} for r in results if r.success
    ]
    success_count = sum(1 for r in results if r.success)
    fail_count = sum(1 for r in results if not r.success)

    safe_write_json(repo_dir / "downloaded_index.json", downloaded_index)
    print(
        f"  Copied {success_count} files"
        + (f" ({fail_count} failed)" if fail_count else "")
    )

    return repo_dir


def scan_repo(
    repo_input: str,
    branch: Optional[str],
    out_base: pathlib.Path,
    max_chars: int,
    parallel_downloads: int = 8,
    verbose: bool = False,
) -> pathlib.Path:
    """
    Stage 1: Unified scanner for GitHub URLs or local directories.
    Auto-detects input type and dispatches to appropriate scanner.
    Returns the output directory path.
    """
    if is_local_path(repo_input):
        return scan_local(repo_input, out_base, max_chars, verbose)
    else:
        return scan_github(
            repo_input, branch, out_base, max_chars, parallel_downloads, verbose
        )


# =============================================================================
# STAGE 2: FIND ENTRYPOINTS
# =============================================================================

# find_downloaded_text is now load_downloaded_text from _github.py


def find_entrypoints(cache_dir: pathlib.Path, verbose: bool = False) -> None:
    """Stage 2: Identify likely code entrypoints."""
    print("[RepoGPS] Stage 2: Finding entrypoints")

    tree = json.loads((cache_dir / "repo_tree.json").read_text(encoding="utf-8"))
    paths: List[str] = tree["paths"]

    candidates: List[Tuple[str, float, List[str]]] = []

    for p in paths:
        base = score_entrypoint_path(p)
        if base <= 0:
            continue

        evidence = [f"path_match(base={base:.2f})"]
        content = load_downloaded_text(cache_dir, p)
        score = base

        if content:
            b = score_entrypoint_content(content)
            if b > 0:
                evidence.append(f"content_hints(+{b:.2f})")
            score += b
        else:
            evidence.append("content_unavailable")

        score = min(score, 1.0)
        candidates.append((p, score, evidence))

    candidates.sort(key=lambda x: x[1], reverse=True)

    out = {
        "top_entrypoints": [
            {"path": p, "confidence": round(s, 3), "evidence": ev}
            for (p, s, ev) in candidates[:15]
        ],
        "note": "Confidence is heuristic. Open these files to confirm wiring/entrypoint.",
    }

    (cache_dir / "entrypoints.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )

    for item in out["top_entrypoints"][:5]:
        print(f"  - {item['path']}  (conf={item['confidence']})")


# =============================================================================
# STAGE 3: EXTRACT RUNBOOK
# =============================================================================

# Note: The following functions are now imported from _github.py:
# - load_downloaded_text (formerly load_text_if_exists)
# - load_key_files
# - extract_commands_from_readme
# - extract_from_package_json
# - extract_from_makefile
# - dedupe
# - detect_languages


def extract_runbook(cache_dir: pathlib.Path, verbose: bool = False) -> None:
    """Stage 3: Extract run/test commands from docs and manifests."""
    print("[RepoGPS] Stage 3: Extracting runbook")

    key_files = load_key_files(cache_dir)

    confirmed_run: List[str] = []
    confirmed_test: List[str] = []

    # README
    for rp in key_files.get("docs", []):
        text = load_downloaded_text(cache_dir, rp)
        if text:
            r, t = extract_commands_from_readme(text)
            confirmed_run += r
            confirmed_test += t

    # Manifests
    for mp in key_files.get("manifests", []):
        text = load_downloaded_text(cache_dir, mp)
        if not text:
            continue

        if mp.endswith("package.json"):
            r, t = extract_from_package_json(text)
            confirmed_run += r
            confirmed_test += t
        elif mp.endswith("Makefile"):
            r, t = extract_from_makefile(text)
            confirmed_run += r
            confirmed_test += t

    # CI workflows (with multi-platform support)
    for wf in key_files.get("ci", []):
        text = load_downloaded_text(cache_dir, wf)
        if text:
            r, t = extract_ci_commands(text, wf)
            confirmed_run += r
            confirmed_test += t

    confirmed_run = dedupe(confirmed_run)
    confirmed_test = dedupe(confirmed_test)

    # Inference based on detected languages
    inferred_run: List[str] = []
    inferred_test: List[str] = []
    missing: List[str] = []

    manifests = set(key_files.get("manifests", []))
    entrypoints = set(key_files.get("entrypoints", []))

    # Detect languages
    langs = detect_languages(manifests, entrypoints)

    if "python" in langs:
        if not confirmed_test:
            inferred_test.append("pytest -q")
        if not confirmed_run:
            inferred_run.append("python -m <module>  # replace with actual module")

    if "javascript" in langs or "typescript" in langs:
        if not confirmed_test:
            inferred_test.append("npm test")
        if not confirmed_run:
            inferred_run.append("npm run dev")

    if "rust" in langs:
        if not confirmed_test:
            inferred_test.append("cargo test")
        if not confirmed_run:
            inferred_run.append("cargo run")

    if "go" in langs:
        if not confirmed_test:
            inferred_test.append("go test ./...")
        if not confirmed_run:
            inferred_run.append("go run .")

    if "java" in langs:
        if not confirmed_test:
            inferred_test.append("mvn test  # or: gradle test")
        if not confirmed_run:
            inferred_run.append("mvn spring-boot:run  # or: gradle bootRun")

    if "csharp" in langs:
        if not confirmed_test:
            inferred_test.append("dotnet test")
        if not confirmed_run:
            inferred_run.append("dotnet run")

    if "ruby" in langs:
        if not confirmed_test:
            inferred_test.append("bundle exec rspec")
        if not confirmed_run:
            inferred_run.append("bundle exec rails server")

    if "php" in langs:
        if not confirmed_test:
            inferred_test.append("./vendor/bin/phpunit")
        if not confirmed_run:
            inferred_run.append("php artisan serve")

    # Missing info hints
    if not confirmed_run and not inferred_run:
        missing.append("No run command found. Check README or Makefile.")
    if not confirmed_test and not inferred_test:
        missing.append("No test command found. Check CI workflows.")

    out = {
        "run": {
            "confirmed": confirmed_run,
            "inferred": inferred_run,
        },
        "test": {
            "confirmed": confirmed_test,
            "inferred": inferred_test,
        },
        "languages_detected": sorted(langs),
        "missing_info": missing,
        "note": "Confirmed commands from docs/manifests/CI. Inferred are best guesses.",
    }

    (cache_dir / "runbook.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    if out["run"]["confirmed"]:
        print(f"  Confirmed run: {out['run']['confirmed'][0]}")
    elif out["run"]["inferred"]:
        print(f"  Inferred run: {out['run']['inferred'][0]}")

    if out["test"]["confirmed"]:
        print(f"  Confirmed test: {out['test']['confirmed'][0]}")
    elif out["test"]["inferred"]:
        print(f"  Inferred test: {out['test']['inferred'][0]}")

    if out["languages_detected"]:
        print(f"  Languages: {', '.join(out['languages_detected'])}")


# detect_languages is now imported from _github.py

# =============================================================================
# SUMMARY GENERATION
# =============================================================================


def detect_repo_type(
    key_files: Dict[str, List[str]], languages: List[str]
) -> Dict[str, Any]:
    """Detect repository type and characteristics."""
    repo_type = {
        "is_monorepo": False,
        "has_tests": False,
        "has_ci": False,
        "has_docs": False,
        "frameworks": [],
        "warnings": [],
    }

    manifests = key_files.get("manifests", [])
    tests = key_files.get("tests_sample", [])
    ci = key_files.get("ci", [])
    docs = key_files.get("docs", [])

    # Check for monorepo (multiple manifests at different paths)
    manifest_dirs = set()
    for m in manifests:
        parts = m.split("/")
        if len(parts) > 1:
            manifest_dirs.add(parts[0])
    if len(manifest_dirs) >= 2:
        repo_type["is_monorepo"] = True
        repo_type["sub_projects"] = list(manifest_dirs)

    repo_type["has_tests"] = len(tests) > 0
    repo_type["has_ci"] = len(ci) > 0
    repo_type["has_docs"] = len(docs) > 0

    # Detect frameworks from manifests
    for m in manifests:
        if "package.json" in m:
            repo_type["frameworks"].append("node")
        if "Cargo.toml" in m:
            repo_type["frameworks"].append("rust")
        if "go.mod" in m:
            repo_type["frameworks"].append("go")
        if "pyproject.toml" in m or "requirements.txt" in m:
            repo_type["frameworks"].append("python")

    # Add warnings for missing elements
    if not repo_type["has_tests"]:
        repo_type["warnings"].append("No tests detected")
    if not repo_type["has_ci"]:
        repo_type["warnings"].append("No CI configuration found")
    if not repo_type["has_docs"]:
        repo_type["warnings"].append("No README or documentation found")

    return repo_type


def generate_summary(cache_dir: pathlib.Path) -> Dict[str, Any]:
    """Generate a consolidated summary of all analysis results."""
    import datetime

    summary: Dict[str, Any] = {
        "generated_at": datetime.datetime.now().isoformat(),
        "cache_dir": str(cache_dir),
        "repo_info": {},
        "repo_type": {},
        "key_files": {},
        "entrypoints": [],
        "runbook": {},
        "languages": [],
        "quick_summary": "",  # Human-readable summary for Claude
    }

    # Load repo info
    repo_tree_path = cache_dir / "repo_tree.json"
    if repo_tree_path.exists():
        data = json.loads(repo_tree_path.read_text(encoding="utf-8"))
        summary["repo_info"] = {
            "url": data.get("repo_url", ""),
            "branch": data.get("branch", ""),
            "total_files": data.get("total_files", len(data.get("paths", []))),
            "truncated": data.get("truncated", False),
        }

    # Load key files
    key_files_path = cache_dir / "key_files.json"
    if key_files_path.exists():
        summary["key_files"] = json.loads(key_files_path.read_text(encoding="utf-8"))

    # Load entrypoints
    entrypoints_path = cache_dir / "entrypoints.json"
    if entrypoints_path.exists():
        data = json.loads(entrypoints_path.read_text(encoding="utf-8"))
        summary["entrypoints"] = data.get("top_entrypoints", [])[:5]

    # Load runbook
    runbook_path = cache_dir / "runbook.json"
    if runbook_path.exists():
        data = json.loads(runbook_path.read_text(encoding="utf-8"))
        summary["runbook"] = data
        summary["languages"] = data.get("languages_detected", [])

    # Detect repo type and characteristics
    summary["repo_type"] = detect_repo_type(summary["key_files"], summary["languages"])

    # Generate quick summary for Claude
    quick_parts = []

    # Basic info
    if summary["repo_info"]:
        url = summary["repo_info"].get("url", "Unknown")
        total = summary["repo_info"].get("total_files", 0)
        quick_parts.append(f"Repository: {url} ({total} files)")

    # Languages
    if summary["languages"]:
        quick_parts.append(f"Languages: {', '.join(summary['languages'])}")

    # Repo type
    rt = summary["repo_type"]
    if rt.get("is_monorepo"):
        quick_parts.append(
            f"Type: Monorepo with sub-projects: {', '.join(rt.get('sub_projects', []))}"
        )

    # Top entrypoint
    if summary["entrypoints"]:
        top = summary["entrypoints"][0]
        quick_parts.append(
            f"Main entrypoint: {top['path']} (confidence: {top['confidence']})"
        )

    # Run/test commands
    runbook = summary.get("runbook", {})
    run_cmds = runbook.get("run", {})
    test_cmds = runbook.get("test", {})

    if run_cmds.get("confirmed"):
        quick_parts.append(f"Run command: {run_cmds['confirmed'][0]}")
    elif run_cmds.get("inferred"):
        quick_parts.append(f"Run command (inferred): {run_cmds['inferred'][0]}")

    if test_cmds.get("confirmed"):
        quick_parts.append(f"Test command: {test_cmds['confirmed'][0]}")
    elif test_cmds.get("inferred"):
        quick_parts.append(f"Test command (inferred): {test_cmds['inferred'][0]}")

    # Warnings
    if rt.get("warnings"):
        quick_parts.append(f"Warnings: {'; '.join(rt['warnings'])}")

    if summary["repo_info"].get("truncated"):
        quick_parts.append("WARNING: Repo has >100k files, analysis may be incomplete")

    summary["quick_summary"] = "\n".join(quick_parts)

    return summary


# =============================================================================
# MAIN ORCHESTRATOR
# =============================================================================


def run_analysis(
    repo_url: str,
    branch: Optional[str] = None,
    out_base: pathlib.Path = None,
    max_chars: int = 120_000,
    parallel_downloads: int = 8,
    verbose: bool = False,
    output_json: bool = False,
) -> AnalysisResult:
    """
    Run complete repository analysis with error handling.
    """
    if out_base is None:
        out_base = pathlib.Path(".repogps_cache")

    result = AnalysisResult(success=False)
    start_time = time.time()

    print("=" * 60)
    print("  RepoGPS - Repository Analysis Tool")
    print("=" * 60)
    print()

    # Stage 1: Scan
    try:
        cache_dir = scan_repo(
            repo_url,
            branch,
            out_base,
            max_chars,
            parallel_downloads=parallel_downloads,
            verbose=verbose,
        )
        result.cache_dir = cache_dir
        result.stages_completed.append("scan")
        print()
    except Exception as e:
        result.error = f"Stage 1 (scan) failed: {e}"
        print(f"\n[ERROR] {result.error}")
        return result

    # Stage 2: Find entrypoints
    try:
        find_entrypoints(cache_dir, verbose=verbose)
        result.stages_completed.append("entrypoints")
        print()
    except Exception as e:
        result.error = f"Stage 2 (entrypoints) failed: {e}"
        print(f"\n[WARNING] {result.error}")
        # Continue anyway - this stage is not critical

    # Stage 3: Extract runbook
    try:
        extract_runbook(cache_dir, verbose=verbose)
        result.stages_completed.append("runbook")
        print()
    except Exception as e:
        result.error = f"Stage 3 (runbook) failed: {e}"
        print(f"\n[WARNING] {result.error}")
        # Continue anyway - this stage is not critical

    # Generate summary
    try:
        summary = generate_summary(cache_dir)
        summary_path = cache_dir / "summary.json"
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        result.stages_completed.append("summary")
    except Exception as e:
        print(f"\n[WARNING] Failed to generate summary: {e}")

    elapsed = time.time() - start_time
    result.success = True

    print("=" * 60)
    print("[RepoGPS] Analysis Complete!")
    print(f"  Output directory: {cache_dir}")
    print(f"  Total files in repo: {summary['repo_info'].get('total_files', 'N/A')}")
    print(f"  Time elapsed: {elapsed:.1f}s")
    print()
    print("Generated files:")
    print("  - repo_tree.json      (full file tree)")
    print("  - key_files.json      (categorized important files)")
    print("  - entrypoints.json    (likely code entry points)")
    print("  - runbook.json        (run/test commands)")
    print("  - summary.json        (consolidated summary)")
    print("  - downloaded/         (downloaded file contents)")
    print("=" * 60)

    if output_json:
        print()
        print(json.dumps(summary, indent=2))

    return result


def main():
    ap = argparse.ArgumentParser(
        description="RepoGPS - Scan and analyze GitHub repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python repogps.py https://github.com/xai-org/x-algorithm
  python repogps.py https://github.com/owner/repo --branch main
  python repogps.py https://github.com/owner/repo --verbose --parallel 8
  python repogps.py https://github.com/owner/repo --json
        """,
    )
    ap.add_argument("repo_url", help="GitHub repository URL")
    ap.add_argument(
        "--branch",
        "-b",
        default=None,
        help="Branch name (default: repo's default branch)",
    )
    ap.add_argument(
        "--out",
        "-o",
        default=".repogps_cache",
        help="Output base directory (default: .repogps_cache)",
    )
    ap.add_argument(
        "--max-chars",
        type=int,
        default=120_000,
        help="Max chars per fetched file (default: 120000)",
    )
    ap.add_argument(
        "--parallel",
        "-p",
        type=int,
        default=8,
        help="Number of parallel downloads (default: 8, use 1 for sequential)",
    )
    ap.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    ap.add_argument(
        "--json", action="store_true", help="Output summary as JSON at the end"
    )

    args = ap.parse_args()

    # Setup logging
    setup_logging(verbose=args.verbose)

    result = run_analysis(
        repo_url=args.repo_url,
        branch=args.branch,
        out_base=pathlib.Path(args.out),
        max_chars=args.max_chars,
        parallel_downloads=args.parallel,
        verbose=args.verbose,
        output_json=args.json,
    )

    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
