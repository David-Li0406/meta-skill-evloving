#!/usr/bin/env python3
"""
Validates and auto-fixes source code references in documentation.
Detects line number drift between versions and updates references.

By default, fetches latest changes from remote repositories before validation.
Use --no-update to skip this step and use current local state.

Usage:
  python3 check-source-refs.py --docs docs/ --adk-python-repo ../adk-python
  python3 check-source-refs.py --docs docs/ --adk-python-repo ../adk-python --dry-run
  python3 check-source-refs.py --docs docs/ --adk-python-repo ../adk-python --no-update
"""

import argparse
import re
import subprocess
from dataclasses import dataclass
from difflib import SequenceMatcher
from enum import Enum
from pathlib import Path


class RefStatus(Enum):
    VALID = "valid"  # Code at same lines, unchanged
    DRIFTED = "drifted"  # Code found at different lines
    BROKEN = "broken"  # Code not found in file


@dataclass
class SourceRef:
    doc_file: Path
    doc_line: int
    url: str  # Full GitHub URL
    repo: str  # "adk-python" or "adk-samples"
    commit: str
    file_path: str
    line_start: int
    line_end: int | None  # None for single-line refs


@dataclass
class ValidationResult:
    ref: SourceRef
    status: RefStatus
    message: str
    new_commit: str | None = None
    new_line_start: int | None = None
    new_line_end: int | None = None


# GitHub URL pattern for adk-python and adk-samples
GITHUB_REF_PATTERN = re.compile(
    r"https://github\.com/google/(adk-python|adk-samples)/blob/"
    r"([a-f0-9]{40})/([^#\s\)]+)#L(\d+)(?:-L(\d+))?"
)


def extract_refs(docs_dir: Path) -> list[SourceRef]:
    """Extract all GitHub source references from markdown files."""
    refs = []
    for md_file in sorted(docs_dir.glob("part*.md")):
        content = md_file.read_text()
        for line_num, line in enumerate(content.split("\n"), 1):
            for match in GITHUB_REF_PATTERN.finditer(line):
                refs.append(
                    SourceRef(
                        doc_file=md_file,
                        doc_line=line_num,
                        url=match.group(0),
                        repo=match.group(1),
                        commit=match.group(2),
                        file_path=match.group(3),
                        line_start=int(match.group(4)),
                        line_end=int(match.group(5)) if match.group(5) else None,
                    )
                )
    return refs


def get_code_at_commit(
    repo_path: Path, commit: str, file_path: str, start: int, end: int
) -> str | None:
    """Extract code lines from repo at specific commit."""
    try:
        result = subprocess.run(
            ["git", "show", f"{commit}:{file_path}"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        lines = result.stdout.split("\n")
        return "\n".join(lines[start - 1 : end])
    except subprocess.CalledProcessError:
        return None


def find_code_in_file(
    repo_path: Path, version: str, file_path: str, code_block: str
) -> tuple[int, int] | None:
    """Search for code block in file at version, return new line numbers."""
    try:
        result = subprocess.run(
            ["git", "show", f"{version}:{file_path}"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        file_lines = result.stdout.split("\n")
        code_lines = code_block.split("\n")
        code_len = len(code_lines)

        # Search for exact or fuzzy match
        best_match = None
        best_ratio = 0.8  # Minimum similarity threshold

        for i in range(len(file_lines) - code_len + 1):
            candidate = "\n".join(file_lines[i : i + code_len])
            ratio = SequenceMatcher(None, code_block, candidate).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = (i + 1, i + code_len)

        return best_match
    except subprocess.CalledProcessError:
        return None


def get_head_commit(repo_path: Path, version: str = "HEAD") -> str:
    """Get the commit hash for a version/tag/HEAD."""
    result = subprocess.run(
        ["git", "rev-parse", version],
        cwd=repo_path,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def update_repo(repo_path: Path, repo_name: str) -> bool:
    """Fetch latest changes and tags from remote. Returns True if successful."""
    print(f"Updating {repo_name} repository...")
    try:
        # Fetch all branches and tags
        subprocess.run(
            ["git", "fetch", "--all", "--tags"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        # Pull latest changes for current branch
        subprocess.run(
            ["git", "pull", "--ff-only"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"  Updated {repo_name} successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Warning: Could not update {repo_name}: {e.stderr.strip()}")
        print(f"  Continuing with current local state...")
        return False


def validate_ref(
    ref: SourceRef, repos: dict[str, Path], new_version: str
) -> ValidationResult:
    """Validate a single reference against new version."""
    repo_path = repos.get(ref.repo)
    if not repo_path or not repo_path.exists():
        return ValidationResult(
            ref, RefStatus.BROKEN, f"Repository {ref.repo} not found"
        )

    end = ref.line_end or ref.line_start
    old_code = get_code_at_commit(repo_path, ref.commit, ref.file_path, ref.line_start, end)
    if old_code is None:
        return ValidationResult(
            ref, RefStatus.BROKEN, "Cannot read code at pinned commit"
        )

    try:
        new_commit = get_head_commit(repo_path, new_version)
    except subprocess.CalledProcessError:
        return ValidationResult(
            ref, RefStatus.BROKEN, f"Cannot resolve version {new_version}"
        )

    # Check if code is at same location
    new_code = get_code_at_commit(repo_path, new_version, ref.file_path, ref.line_start, end)
    if new_code == old_code:
        return ValidationResult(ref, RefStatus.VALID, "Code unchanged", new_commit=new_commit)

    # Search for code elsewhere in file
    new_location = find_code_in_file(repo_path, new_version, ref.file_path, old_code)
    if new_location:
        return ValidationResult(
            ref,
            RefStatus.DRIFTED,
            f"Code moved from L{ref.line_start} to L{new_location[0]}",
            new_commit=new_commit,
            new_line_start=new_location[0],
            new_line_end=new_location[1] if ref.line_end else None,
        )

    return ValidationResult(
        ref, RefStatus.BROKEN, f"Code not found at L{ref.line_start} or nearby"
    )


def apply_fix(result: ValidationResult, dry_run: bool = False) -> bool:
    """Update the markdown file with new reference. Returns True if fixed."""
    if result.status != RefStatus.DRIFTED or not result.new_commit:
        return False

    doc_file = result.ref.doc_file
    content = doc_file.read_text()

    # Build old and new URLs
    old_url = result.ref.url
    new_url = old_url.replace(result.ref.commit, result.new_commit)

    # Update line numbers
    if result.new_line_end:
        new_line_suffix = f"#L{result.new_line_start}-L{result.new_line_end}"
    else:
        new_line_suffix = f"#L{result.new_line_start}"

    new_url = re.sub(r"#L\d+(-L\d+)?$", new_line_suffix, new_url)

    if dry_run:
        print(f"  Would fix: {old_url}")
        print(f"         -> {new_url}")
        return True

    new_content = content.replace(old_url, new_url)
    if new_content != content:
        doc_file.write_text(new_content)
        return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Validate and auto-fix source code references in docs"
    )
    parser.add_argument(
        "--docs", required=True, type=Path, help="Documentation directory"
    )
    parser.add_argument(
        "--adk-python-repo", type=Path, help="Path to adk-python repository"
    )
    parser.add_argument(
        "--adk-samples-repo", type=Path, help="Path to adk-samples repository"
    )
    parser.add_argument(
        "--new-version",
        default="HEAD",
        help="Version to validate against (tag or HEAD)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Report issues without fixing"
    )
    parser.add_argument(
        "--no-update",
        action="store_true",
        help="Skip updating repositories (use current local state)",
    )
    args = parser.parse_args()

    repos = {}
    if args.adk_python_repo:
        repos["adk-python"] = args.adk_python_repo
    if args.adk_samples_repo:
        repos["adk-samples"] = args.adk_samples_repo

    if not repos:
        print("Error: At least one repository path must be provided")
        return 1

    # Update repositories to latest versions unless --no-update is specified
    if not args.no_update:
        print("Fetching latest changes from remote repositories...")
        for repo_name, repo_path in repos.items():
            if repo_path.exists():
                update_repo(repo_path, repo_name)
        print()

    refs = extract_refs(args.docs)
    print(f"Found {len(refs)} source code references")

    # Filter refs to only those for available repos
    refs = [r for r in refs if r.repo in repos]
    print(f"Validating {len(refs)} references for available repos: {list(repos.keys())}")

    results: dict[str, list[ValidationResult]] = {"valid": [], "drifted": [], "broken": []}
    fixed_count = 0

    for ref in refs:
        result = validate_ref(ref, repos, args.new_version)
        results[result.status.value].append(result)

        if result.status == RefStatus.DRIFTED:
            if apply_fix(result, args.dry_run):
                fixed_count += 1

    # Print summary
    print("\n## Source Code Reference Validation")
    print("\n### Summary")
    print(f"- Total references: {len(refs)}")
    print(f"- Valid: {len(results['valid'])}")
    print(f"- Drifted: {len(results['drifted'])} ({fixed_count} {'would be ' if args.dry_run else ''}fixed)")
    print(f"- Broken: {len(results['broken'])}")

    if results["drifted"]:
        action = "Would auto-fix" if args.dry_run else "Auto-fixed"
        print(f"\n### Drifted References ({action})")
        for i, r in enumerate(results["drifted"], 1):
            print(f"\n#### D{i}: {r.ref.file_path}:{r.ref.line_start}")
            print(f"- **Doc**: {r.ref.doc_file.name}:{r.ref.doc_line}")
            print(f"- **Status**: {r.message}")

    if results["broken"]:
        print("\n### Broken References (require manual fix)")
        for i, r in enumerate(results["broken"], 1):
            print(f"\n#### B{i}: {r.ref.file_path}:{r.ref.line_start}")
            print(f"- **Doc**: {r.ref.doc_file.name}:{r.ref.doc_line}")
            print(f"- **Status**: {r.message}")
            print("- **Action**: Locate new code location or remove reference")

    return 1 if results["broken"] else 0


if __name__ == "__main__":
    exit(main())
