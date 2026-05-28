#!/usr/bin/env python3
"""
SLOC Tracker Tool

Tracks Source Lines of Code (SLOC) changes per file.
Captures baseline, tracks changes, and calculates deltas.

Usage:
    python sloc_tracker.py /path/to/project --baseline [files...]
    python sloc_tracker.py /path/to/project --update [files...]
    python sloc_tracker.py /path/to/project --final

Returns JSON with SLOC data.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
import re


class SLOCTracker:
    """Tracks source lines of code changes."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.baseline_file = project_path / "planning/phase-structure/.sloc-baseline.json"

    def create_baseline(self, files: List[str]) -> Dict:
        """Create baseline SLOC measurement for files."""
        baseline = {}

        for file_path in files:
            full_path = self.project_path / file_path

            if full_path.exists():
                sloc = self._count_sloc(full_path)
                baseline[file_path] = {
                    "baseline": sloc,
                    "current": sloc,
                    "delta": 0
                }

        # Save baseline
        self._save_baseline(baseline)

        return {
            "action": "baseline_created",
            "files_tracked": len(baseline),
            "total_baseline_sloc": sum(f["baseline"] for f in baseline.values()),
            "baseline": baseline
        }

    def update_current(self, files: List[str] = None) -> Dict:
        """Update current SLOC measurements."""
        # Load baseline
        baseline = self._load_baseline()

        if not baseline:
            return {
                "error": "No baseline found. Create baseline first with --baseline"
            }

        # If no files specified, use all files from baseline
        if files is None:
            files = list(baseline.keys())

        # Update current SLOC
        for file_path in files:
            full_path = self.project_path / file_path

            if full_path.exists():
                current_sloc = self._count_sloc(full_path)

                if file_path in baseline:
                    baseline[file_path]["current"] = current_sloc
                    baseline[file_path]["delta"] = current_sloc - baseline[file_path]["baseline"]
                else:
                    # New file not in baseline
                    baseline[file_path] = {
                        "baseline": 0,
                        "current": current_sloc,
                        "delta": current_sloc
                    }
            elif file_path in baseline:
                # File was deleted
                baseline[file_path]["current"] = 0
                baseline[file_path]["delta"] = -baseline[file_path]["baseline"]

        # Save updated baseline
        self._save_baseline(baseline)

        # Calculate summary
        total_delta = sum(f["delta"] for f in baseline.values())
        files_increased = sum(1 for f in baseline.values() if f["delta"] > 0)
        files_decreased = sum(1 for f in baseline.values() if f["delta"] < 0)
        files_unchanged = sum(1 for f in baseline.values() if f["delta"] == 0)

        return {
            "action": "sloc_updated",
            "files_tracked": len(baseline),
            "total_baseline_sloc": sum(f["baseline"] for f in baseline.values()),
            "total_current_sloc": sum(f["current"] for f in baseline.values()),
            "total_delta": total_delta,
            "files_increased": files_increased,
            "files_decreased": files_decreased,
            "files_unchanged": files_unchanged,
            "details": baseline
        }

    def generate_final_report(self) -> Dict:
        """Generate final SLOC report."""
        baseline = self._load_baseline()

        if not baseline:
            return {
                "error": "No baseline found. Create baseline first with --baseline"
            }

        # Update all files one last time
        result = self.update_current()

        # Generate markdown table
        markdown_table = self._generate_markdown_table(baseline)

        # Calculate code distribution
        distribution = self._calculate_distribution(baseline)

        return {
            "action": "final_report",
            "summary": {
                "total_files": len(baseline),
                "total_baseline_sloc": sum(f["baseline"] for f in baseline.values()),
                "total_current_sloc": sum(f["current"] for f in baseline.values()),
                "total_delta": sum(f["delta"] for f in baseline.values()),
                "files_created": sum(1 for f in baseline.values() if f["baseline"] == 0 and f["current"] > 0),
                "files_modified": sum(1 for f in baseline.values() if f["baseline"] > 0 and f["delta"] != 0),
                "files_deleted": sum(1 for f in baseline.values() if f["current"] == 0 and f["baseline"] > 0)
            },
            "distribution": distribution,
            "markdown_table": markdown_table,
            "details": baseline
        }

    def _count_sloc(self, file_path: Path) -> int:
        """Count source lines of code (non-blank, non-comment)."""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.splitlines()

            sloc = 0
            in_multiline_comment = False

            for line in lines:
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # Handle multi-line comments
                if file_path.suffix in ['.js', '.ts', '.tsx', '.jsx']:
                    if '/*' in line:
                        in_multiline_comment = True
                    if '*/' in line:
                        in_multiline_comment = False
                        continue
                    if in_multiline_comment:
                        continue

                # Skip single-line comments
                if line.startswith('//') or line.startswith('#') or line.startswith('*'):
                    continue

                # Count as SLOC
                sloc += 1

            return sloc

        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
            return 0

    def _save_baseline(self, baseline: Dict):
        """Save baseline to JSON file."""
        self.baseline_file.parent.mkdir(parents=True, exist_ok=True)
        self.baseline_file.write_text(json.dumps(baseline, indent=2), encoding='utf-8')

    def _load_baseline(self) -> Dict:
        """Load baseline from JSON file."""
        if not self.baseline_file.exists():
            return {}

        try:
            return json.loads(self.baseline_file.read_text(encoding='utf-8'))
        except Exception as e:
            print(f"Warning: Could not load baseline: {e}", file=sys.stderr)
            return {}

    def _generate_markdown_table(self, baseline: Dict) -> str:
        """Generate markdown table for SLOC changes."""
        table = "| File | Baseline SLOC | Current SLOC | Delta | Change % |\n"
        table += "|------|---------------|--------------|-------|----------|\n"

        # Sort by absolute delta (largest changes first)
        sorted_files = sorted(baseline.items(), key=lambda x: abs(x[1]["delta"]), reverse=True)

        for file_path, data in sorted_files:
            baseline_sloc = data["baseline"]
            current_sloc = data["current"]
            delta = data["delta"]

            # Calculate change percentage
            if baseline_sloc > 0:
                change_pct = round((delta / baseline_sloc) * 100, 1)
            elif current_sloc > 0:
                change_pct = 100.0  # New file
            else:
                change_pct = 0.0

            # Format delta with + or -
            delta_str = f"+{delta}" if delta > 0 else str(delta)

            # Indicate new/deleted files
            if baseline_sloc == 0 and current_sloc > 0:
                baseline_str = "0 (new)"
            elif current_sloc == 0 and baseline_sloc > 0:
                current_str = "0 (deleted)"
            else:
                baseline_str = str(baseline_sloc)
                current_str = str(current_sloc)

            baseline_str = baseline_str if baseline_sloc != 0 or current_sloc == 0 else "0 (new)"
            current_str = str(current_sloc) if current_sloc != 0 or baseline_sloc == 0 else "0 (deleted)"

            table += f"| {file_path} | {baseline_str} | {current_str} | {delta_str} | {change_pct:+.1f}% |\n"

        return table

    def _calculate_distribution(self, baseline: Dict) -> Dict:
        """Calculate code distribution by file type."""
        distribution = {
            "source": 0,
            "tests": 0,
            "docs": 0,
            "other": 0
        }

        for file_path, data in baseline.items():
            sloc = data["current"]

            if sloc == 0:
                continue

            # Categorize by file path
            file_path_lower = file_path.lower()

            if any(test_dir in file_path_lower for test_dir in ['test/', 'tests/', '__tests__/', 'spec/']):
                distribution["tests"] += sloc
            elif any(doc_ext in file_path_lower for doc_ext in ['.md', '.txt', '.rst']):
                distribution["docs"] += sloc
            elif any(src_ext in file_path_lower for src_ext in ['.ts', '.tsx', '.js', '.jsx', '.py', '.java', '.go']):
                distribution["source"] += sloc
            else:
                distribution["other"] += sloc

        # Calculate percentages
        total = sum(distribution.values())

        if total > 0:
            distribution_pct = {
                category: round((count / total) * 100, 1)
                for category, count in distribution.items()
            }
        else:
            distribution_pct = {category: 0.0 for category in distribution.keys()}

        return {
            "counts": distribution,
            "percentages": distribution_pct,
            "total": total
        }


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: python sloc_tracker.py /path/to/project --baseline [files...] | --update [files...] | --final"
        }, indent=2))
        sys.exit(1)

    project_path = Path(sys.argv[1])
    action = sys.argv[2]
    files = sys.argv[3:] if len(sys.argv) > 3 else None

    if not project_path.exists():
        print(json.dumps({
            "error": f"Project path not found: {project_path}"
        }, indent=2))
        sys.exit(1)

    tracker = SLOCTracker(project_path)

    if action == "--baseline":
        if not files:
            print(json.dumps({
                "error": "No files specified for baseline. Provide file paths after --baseline"
            }, indent=2))
            sys.exit(1)
        result = tracker.create_baseline(files)

    elif action == "--update":
        result = tracker.update_current(files)

    elif action == "--final":
        result = tracker.generate_final_report()

    else:
        print(json.dumps({
            "error": f"Unknown action: {action}. Use --baseline, --update, or --final"
        }, indent=2))
        sys.exit(1)

    # Output JSON
    print(json.dumps(result, indent=2))

    # Exit with error if there was an error
    sys.exit(0 if "error" not in result else 1)


if __name__ == "__main__":
    main()
