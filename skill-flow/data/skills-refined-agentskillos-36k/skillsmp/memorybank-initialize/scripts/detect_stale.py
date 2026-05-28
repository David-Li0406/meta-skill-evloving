#!/usr/bin/env python3
"""
Memory Bank Staleness Detector

Detects outdated information in Memory Bank files by comparing file modification
times with recent git activity.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import subprocess
import json


MEMORY_BANK_FILES = [
    "projectbrief.md",
    "productContext.md",
    "techContext.md",
    "systemPatterns.md",
    "activeContext.md",
    "progress.md",
]

# Files that should be updated frequently
ACTIVE_FILES = ["activeContext.md", "progress.md"]

# Staleness thresholds (in days)
STALE_THRESHOLD = 7  # Files not updated in 7 days
VERY_STALE_THRESHOLD = 30  # Files not updated in 30 days


def find_memory_bank(project_path: Path) -> Path:
    """Find the memory-bank directory in the project."""
    memory_bank_path = project_path / "memory-bank"

    if not memory_bank_path.exists():
        print(f"❌ Memory Bank not found at {memory_bank_path}")
        sys.exit(1)

    return memory_bank_path


def get_file_age(file_path: Path) -> int:
    """Get the age of a file in days since last modification."""
    if not file_path.exists():
        return -1

    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
    age = datetime.now() - mtime
    return age.days


def get_recent_commits(project_path: Path, days: int = 7) -> List[Dict]:
    """Get recent git commits."""
    try:
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        result = subprocess.run(
            ["git", "log", f"--since={since_date}", "--pretty=format:%H|%s|%ad", "--date=short"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return []

        commits = []
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split("|", 2)
                if len(parts) == 3:
                    commits.append({
                        "hash": parts[0][:7],
                        "message": parts[1],
                        "date": parts[2]
                    })

        return commits

    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        return []


def check_git_activity(project_path: Path, exclude_paths: List[str] = None) -> Dict:
    """Check recent git activity excluding memory-bank changes."""
    exclude_paths = exclude_paths or ["memory-bank/"]

    try:
        # Get commits in last 7 days
        recent_commits = get_recent_commits(project_path, days=7)

        # Count commits that don't only touch memory-bank
        code_commits = []
        for commit in recent_commits:
            result = subprocess.run(
                ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit["hash"]],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                files = result.stdout.strip().split("\n")
                # Check if commit touches files outside memory-bank
                has_code_changes = any(
                    not any(exclude in f for exclude in exclude_paths)
                    for f in files if f
                )

                if has_code_changes:
                    code_commits.append(commit)

        return {
            "total_commits": len(recent_commits),
            "code_commits": len(code_commits),
            "recent_activity": len(code_commits) > 0,
            "commits": code_commits[:5]  # Return up to 5 most recent
        }

    except Exception:
        return {
            "total_commits": 0,
            "code_commits": 0,
            "recent_activity": False,
            "commits": []
        }


def analyze_staleness(memory_bank: Path, project_path: Path, stale_threshold: int = STALE_THRESHOLD) -> Dict:
    """Analyze staleness of Memory Bank files."""
    results = {
        "timestamp": datetime.now().isoformat(),
        "files": {},
        "warnings": [],
        "recommendations": [],
    }

    # Check each file
    for filename in MEMORY_BANK_FILES:
        file_path = memory_bank / filename
        age = get_file_age(file_path)

        is_active_file = filename in ACTIVE_FILES

        status = "fresh"
        if age < 0:
            status = "missing"
        elif is_active_file and age > stale_threshold:
            status = "stale"
        elif age > VERY_STALE_THRESHOLD:
            status = "very_stale"
        elif age > stale_threshold:
            status = "stale"

        results["files"][filename] = {
            "age_days": age,
            "status": status,
            "is_active_file": is_active_file
        }

        # Generate warnings
        if status == "missing":
            results["warnings"].append(f"❌ {filename} is missing")
        elif status == "very_stale":
            results["warnings"].append(f"⚠️  {filename} not updated in {age} days (very stale)")
        elif status == "stale":
            if is_active_file:
                results["warnings"].append(f"⚠️  {filename} not updated in {age} days (should be updated frequently)")

    # Check git activity
    git_activity = check_git_activity(project_path)
    results["git_activity"] = git_activity

    # Generate recommendations
    if git_activity["recent_activity"]:
        stale_files = [f for f, data in results["files"].items() if data["status"] in ["stale", "very_stale"]]
        if stale_files:
            results["recommendations"].append(
                f"📝 Recent code changes detected ({git_activity['code_commits']} commits). "
                f"Consider updating: {', '.join(stale_files)}"
            )

    # Check if active files need updates
    for filename in ACTIVE_FILES:
        file_data = results["files"].get(filename, {})
        if file_data.get("age_days", 0) > stale_threshold:
            results["recommendations"].append(
                f"📝 {filename} should be updated more frequently (currently {file_data['age_days']} days old)"
            )

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Detect stale information in Memory Bank",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s .
  %(prog)s /path/to/project
  %(prog)s . --json
  %(prog)s . --threshold 14
        """
    )

    parser.add_argument(
        "project_path",
        type=Path,
        help="Path to project root containing memory-bank directory"
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=STALE_THRESHOLD,
        help=f"Staleness threshold in days (default: {STALE_THRESHOLD})"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    # Validate project path
    if not args.project_path.exists():
        print(f"❌ Project path does not exist: {args.project_path}")
        sys.exit(1)

    # Find memory bank
    memory_bank = find_memory_bank(args.project_path)

    # Analyze staleness
    results = analyze_staleness(memory_bank, args.project_path, stale_threshold=args.threshold)

    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"Memory Bank Staleness Check: {memory_bank}")
        print(f"{'='*60}\n")

        # Show file status
        print("File Status:")
        for filename, data in results["files"].items():
            age = data["age_days"]
            status = data["status"]

            if status == "missing":
                print(f"  ❌ {filename}: MISSING")
            elif status == "very_stale":
                print(f"  🔴 {filename}: {age} days old (very stale)")
            elif status == "stale":
                print(f"  🟡 {filename}: {age} days old (stale)")
            else:
                print(f"  ✅ {filename}: {age} days old (fresh)")

        # Show git activity
        if results["git_activity"]["recent_activity"]:
            print(f"\nRecent Git Activity:")
            print(f"  {results['git_activity']['code_commits']} code commits in last 7 days")
            for commit in results["git_activity"]["commits"][:3]:
                print(f"  • {commit['hash']}: {commit['message']} ({commit['date']})")

        # Show warnings
        if results["warnings"]:
            print(f"\nWarnings:")
            for warning in results["warnings"]:
                print(f"  {warning}")

        # Show recommendations
        if results["recommendations"]:
            print(f"\nRecommendations:")
            for rec in results["recommendations"]:
                print(f"  {rec}")

        print(f"\n{'='*60}\n")

    # Exit with warning code if there are staleness issues
    has_issues = len(results["warnings"]) > 0 or len(results["recommendations"]) > 0
    sys.exit(1 if has_issues else 0)


if __name__ == "__main__":
    main()
