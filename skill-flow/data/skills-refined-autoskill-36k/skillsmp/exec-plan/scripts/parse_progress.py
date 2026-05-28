#!/usr/bin/env python3
"""
Parse and summarize the Progress section of an ExecPlan.

Usage:
    python parse_progress.py <plan.md>
    python parse_progress.py <plan.md> --json

Outputs a summary of completed, in-progress, and remaining items.
Useful for status checks and resuming work.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_progress(filepath: str) -> dict:
    """
    Parse the Progress section from an ExecPlan.
    
    Returns dict with:
        - completed: list of (timestamp, description) tuples
        - remaining: list of descriptions
        - partial: list of (done_part, remaining_part) tuples
        - total: total item count
        - completion_pct: percentage complete
    """
    path = Path(filepath)
    if not path.exists():
        return {"error": f"File not found: {filepath}"}
    
    content = path.read_text()
    lines = content.split('\n')
    
    in_progress = False
    completed = []
    remaining = []
    partial = []
    
    for line in lines:
        # Detect Progress section
        if re.match(r'^#+\s*Progress', line, re.IGNORECASE):
            in_progress = True
            continue
        
        # Detect end of Progress section
        if in_progress and line.startswith('#') and not re.match(r'^#+\s*Progress', line, re.IGNORECASE):
            in_progress = False
            continue
        
        if not in_progress:
            continue
        
        # Parse completed items: - [x] (timestamp) description
        match = re.match(r'^-\s*\[x\]\s*(?:\(([^)]+)\))?\s*(.+)', line, re.IGNORECASE)
        if match:
            timestamp = match.group(1) or "no timestamp"
            description = match.group(2).strip()
            completed.append((timestamp, description))
            continue
        
        # Parse incomplete items: - [ ] description
        match = re.match(r'^-\s*\[\s*\]\s*(.+)', line)
        if match:
            description = match.group(1).strip()
            
            # Check for partial completion pattern
            partial_match = re.search(r'\(completed:\s*([^;]+);\s*remaining:\s*([^)]+)\)', description)
            if partial_match:
                done_part = partial_match.group(1).strip()
                remain_part = partial_match.group(2).strip()
                partial.append((done_part, remain_part))
            else:
                remaining.append(description)
    
    total = len(completed) + len(remaining) + len(partial)
    if total == 0:
        completion_pct = 0
    else:
        # Partial items count as 0.5
        completed_count = len(completed) + (len(partial) * 0.5)
        completion_pct = round((completed_count / total) * 100)
    
    return {
        "completed": completed,
        "remaining": remaining,
        "partial": partial,
        "total": total,
        "completion_pct": completion_pct,
    }


def format_summary(result: dict) -> str:
    """Format the parse result as a human-readable summary."""
    if "error" in result:
        return f"Error: {result['error']}"
    
    lines = []
    lines.append(f"Progress: {result['completion_pct']}% complete ({len(result['completed'])}/{result['total']} items)")
    lines.append("")
    
    if result['completed']:
        lines.append("COMPLETED:")
        for timestamp, desc in result['completed']:
            lines.append(f"  ✓ [{timestamp}] {desc}")
        lines.append("")
    
    if result['partial']:
        lines.append("IN PROGRESS:")
        for done, remain in result['partial']:
            lines.append(f"  ◐ Done: {done}")
            lines.append(f"    Remaining: {remain}")
        lines.append("")
    
    if result['remaining']:
        lines.append("REMAINING:")
        for desc in result['remaining']:
            lines.append(f"  ○ {desc}")
        lines.append("")
    
    # Show what to work on next
    if result['partial']:
        lines.append(f"NEXT: Continue '{result['partial'][0][1]}'")
    elif result['remaining']:
        lines.append(f"NEXT: Start '{result['remaining'][0]}'")
    else:
        lines.append("NEXT: All items complete - write Outcomes & Retrospective")
    
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_progress.py <plan.md> [--json]")
        print()
        print("Parses the Progress section and shows status summary.")
        sys.exit(1)
    
    filepath = sys.argv[1]
    as_json = '--json' in sys.argv
    
    result = parse_progress(filepath)
    
    if as_json:
        # Convert tuples to lists for JSON serialization
        output = {
            "completed": [{"timestamp": t, "description": d} for t, d in result.get("completed", [])],
            "remaining": result.get("remaining", []),
            "partial": [{"done": d, "remaining": r} for d, r in result.get("partial", [])],
            "total": result.get("total", 0),
            "completion_pct": result.get("completion_pct", 0),
        }
        if "error" in result:
            output["error"] = result["error"]
        print(json.dumps(output, indent=2))
    else:
        print(format_summary(result))
    
    sys.exit(0 if "error" not in result else 1)


if __name__ == "__main__":
    main()
