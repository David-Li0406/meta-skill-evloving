#!/usr/bin/env python3
"""Analyze task DAG and compute max parallel width for ship recommendations."""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_tasks(tasks_dir: Path) -> dict[str, Any]:
    """Load all task JSON files from directory."""
    tasks: dict[str, Any] = {}
    for f in sorted(tasks_dir.glob("*.json")):
        task = json.loads(f.read_text())
        tasks[task["id"]] = task
    return tasks


def compute_levels(tasks: dict[str, Any]) -> dict[str, int]:
    """Assign each task to a level based on dependencies (0 = no deps)."""
    levels: dict[str, int] = {}

    def get_level(tid: str) -> int:
        if tid in levels:
            return levels[tid]
        blocked_by = tasks[tid].get("blockedBy", [])
        if not blocked_by:
            levels[tid] = 0
        else:
            # Level is 1 + max level of all blockers
            levels[tid] = 1 + max(get_level(b) for b in blocked_by if b in tasks)
        return levels[tid]

    for tid in tasks:
        get_level(tid)
    return levels


def max_parallel_width(levels: dict[str, int]) -> int:
    """Count max tasks at any single level (max parallelism)."""
    if not levels:
        return 0
    counts = Counter(levels.values())
    return max(counts.values())


def validate_ship_assignments(tasks: dict[str, Any], levels: dict[str, int]) -> list[str]:
    """Validate that tasks at the same level are assigned to different ships.

    Returns a list of validation errors (empty if valid).
    """
    errors: list[str] = []

    # Group tasks by level
    tasks_by_level: dict[int, list[str]] = defaultdict(list)
    for tid, level in levels.items():
        tasks_by_level[level].append(tid)

    # Check each level for ship conflicts
    for level, task_ids in sorted(tasks_by_level.items()):
        ships_at_level: dict[str, list[str]] = defaultdict(list)

        for tid in task_ids:
            task = tasks[tid]
            ship = task.get("metadata", {}).get("ship")
            if ship is None:
                errors.append(f"Task {tid} has no ship assignment")
                continue
            ships_at_level[ship].append(tid)

        # Check for conflicts (multiple tasks on same ship at same level)
        for ship, tids in ships_at_level.items():
            if len(tids) > 1:
                errors.append(f"Level {level}: {ship} has multiple tasks: {', '.join(tids)}")

    return errors


def main(tasks_dir: Path) -> dict[str, Any]:
    """Analyze tasks and return ship recommendation."""
    tasks = load_tasks(tasks_dir)
    if not tasks:
        return {
            "total_tasks": 0,
            "max_parallel_width": 0,
            "recommended_ships": 1,
            "levels": {},
            "validation_errors": [],
        }

    levels = compute_levels(tasks)
    width = max_parallel_width(levels)
    errors = validate_ship_assignments(tasks, levels)

    return {
        "total_tasks": len(tasks),
        "max_parallel_width": width,
        "recommended_ships": max(1, width),  # At least 1 ship
        "levels": dict(sorted(levels.items(), key=lambda x: (x[1], x[0]))),
        "validation_errors": errors,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <tasks-directory>", file=sys.stderr)
        sys.exit(1)

    tasks_dir = Path(sys.argv[1])
    if not tasks_dir.is_dir():
        print(f"Error: {tasks_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    result = main(tasks_dir)
    print(json.dumps(result, indent=2))
