#!/usr/bin/env python3
"""
calculate-impact.py - Calculate project impact score from git statistics
Usage: python calculate-impact.py <repo-path> <author>
"""

import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

def run_git_command(repo_path, *args):
    """Execute git command and return output."""
    try:
        result = subprocess.run(
            ["git", "-C", repo_path] + list(args),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}", file=sys.stderr)
        return ""

def calculate_impact_score(repo_path, author):
    """Calculate weighted impact score."""
    # Get commit count
    commit_count_str = run_git_command(
        repo_path, "log", "--author=" + author, "--no-merges", "--oneline"
    )
    commit_count = len(commit_count_str.split('\n')) if commit_count_str else 0
    
    # Get lines changed
    numstat = run_git_command(
        repo_path, "log", "--author=" + author, "--no-merges", "--numstat", "--pretty=tformat:"
    )
    
    lines_added = 0
    lines_deleted = 0
    files_modified = set()
    
    for line in numstat.split('\n'):
        if line.strip():
            parts = line.split()
            if len(parts) >= 3:
                try:
                    lines_added += int(parts[0]) if parts[0] != '-' else 0
                    lines_deleted += int(parts[1]) if parts[1] != '-' else 0
                    files_modified.add(parts[2])
                except ValueError:
                    continue
    
    # Count feature commits (conventional commits)
    feature_commits = run_git_command(
        repo_path, "log", "--author=" + author, "--no-merges", 
        "--pretty=format:%s", "--grep=^feat:"
    )
    feature_count = len(feature_commits.split('\n')) if feature_commits else 0
    
    # Detect architectural changes (core/lib/common directories)
    arch_files = run_git_command(
        repo_path, "log", "--author=" + author, "--no-merges", 
        "--name-only", "--pretty=format:", 
        "--", "*/core/*", "*/lib/*", "*/common/*", "*/infrastructure/*"
    )
    arch_changes = len(set(f for f in arch_files.split('\n') if f.strip()))
    
    # Calculate impact score
    impact_score = (
        (commit_count * 0.2) +
        (lines_added / 1000 * 0.3) +
        (len(files_modified) * 0.15) +
        (feature_count * 0.25) +
        (arch_changes * 0.1)
    )
    
    return {
        "commit_count": commit_count,
        "lines_added": lines_added,
        "lines_deleted": lines_deleted,
        "files_modified": len(files_modified),
        "feature_count": feature_count,
        "architectural_changes": arch_changes,
        "impact_score": round(impact_score, 2)
    }

def main():
    if len(sys.argv) < 3:
        print("Usage: python calculate-impact.py <repo-path> <author>", file=sys.stderr)
        sys.exit(1)
    
    repo_path = sys.argv[1]
    author = sys.argv[2]
    
    if not Path(repo_path).is_dir():
        print(f"Error: Directory not found: {repo_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Calculating impact for author: {author}", file=sys.stderr)
    
    impact_data = calculate_impact_score(repo_path, author)
    
    # Output JSON
    output = {
        "metadata": {
            "repository": repo_path,
            "author": author,
            "analysis_date": datetime.now().strftime("%Y-%m-%d")
        },
        "impact_metrics": impact_data,
        "interpretation": {
            "level": (
                "Core developer" if impact_data["impact_score"] >= 100 else
                "Major contributor" if impact_data["impact_score"] >= 60 else
                "Significant contributor" if impact_data["impact_score"] >= 30 else
                "Regular contributor" if impact_data["impact_score"] >= 10 else
                "Minor contributor"
            ),
            "resume_prominence": (
                "high" if impact_data["impact_score"] >= 60 else
                "medium" if impact_data["impact_score"] >= 30 else
                "low"
            )
        }
    }
    
    print(json.dumps(output, indent=2))
    print(f"✓ Impact score: {impact_data['impact_score']}", file=sys.stderr)

if __name__ == "__main__":
    main()
