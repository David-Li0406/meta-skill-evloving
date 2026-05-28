#!/usr/bin/env python3
"""
Summarize THOR log files for quick triage.
Extracts key findings, counts by severity, and identifies top targets.
"""

import sys
import os
import re
from collections import defaultdict

def parse_thor_log(filepath):
    """Parse THOR text log and extract findings."""
    findings = {
        'alerts': [],
        'warnings': [],
        'notices': [],
        'errors': []
    }

    modules = defaultdict(int)
    targets = defaultdict(list)
    signatures = defaultdict(int)

    level_pattern = re.compile(r'\b(Alert|Warning|Notice|Error)\b', re.IGNORECASE)
    score_pattern = re.compile(r'SCORE:\s*(\d+)')
    target_pattern = re.compile(r'TARGET:\s*(.+?)(?:\s+[A-Z_]+:|$)')
    module_pattern = re.compile(r'MODULE:\s*(\w+)')
    name_pattern = re.compile(r'NAME:\s*(.+?)(?:\s+[A-Z_]+:|$)')

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            level_match = level_pattern.search(line)
            if not level_match:
                continue

            level = level_match.group(1).lower()
            if level not in findings:
                continue

            score = None
            score_match = score_pattern.search(line)
            if score_match:
                score = int(score_match.group(1))

            target = None
            target_match = target_pattern.search(line)
            if target_match:
                target = target_match.group(1).strip()

            module = None
            module_match = module_pattern.search(line)
            if module_match:
                module = module_match.group(1)
                modules[module] += 1

            name = None
            name_match = name_pattern.search(line)
            if name_match:
                name = name_match.group(1).strip()
                signatures[name] += 1

            finding = {
                'level': level,
                'score': score,
                'target': target,
                'module': module,
                'name': name,
                'line': line.strip()[:200]
            }

            findings[level + 's'].append(finding)

            if target:
                targets[target].append(finding)

    return findings, modules, targets, signatures

def print_summary(findings, modules, targets, signatures, filepath):
    """Print formatted summary."""
    total = sum(len(v) for v in findings.values())

    print(f"=== THOR Log Summary: {os.path.basename(filepath)} ===\n")

    # Counts by severity
    print("Findings by Severity:")
    print(f"  Alerts:   {len(findings['alerts']):5d}")
    print(f"  Warnings: {len(findings['warnings']):5d}")
    print(f"  Notices:  {len(findings['notices']):5d}")
    print(f"  Errors:   {len(findings['errors']):5d}")
    print(f"  Total:    {total:5d}\n")

    # Top modules
    if modules:
        print("Top Modules:")
        for mod, count in sorted(modules.items(), key=lambda x: -x[1])[:5]:
            print(f"  {mod}: {count}")
        print()

    # Top signatures
    if signatures:
        print("Top Signatures:")
        for sig, count in sorted(signatures.items(), key=lambda x: -x[1])[:10]:
            print(f"  {sig}: {count}")
        print()

    # High-priority findings (Alerts)
    if findings['alerts']:
        print("=== ALERTS (Review First) ===")
        for f in findings['alerts'][:10]:
            score_str = f"[{f['score']}]" if f['score'] else ""
            target_str = f['target'][:60] if f['target'] else "N/A"
            name_str = f['name'] or "Unknown"
            print(f"  {score_str:6s} {name_str[:40]:40s} -> {target_str}")
        if len(findings['alerts']) > 10:
            print(f"  ... and {len(findings['alerts']) - 10} more alerts")
        print()

    # Warnings sample
    if findings['warnings']:
        print("=== WARNINGS (Sample) ===")
        for f in findings['warnings'][:5]:
            score_str = f"[{f['score']}]" if f['score'] else ""
            target_str = f['target'][:60] if f['target'] else "N/A"
            name_str = f['name'] or "Unknown"
            print(f"  {score_str:6s} {name_str[:40]:40s} -> {target_str}")
        if len(findings['warnings']) > 5:
            print(f"  ... and {len(findings['warnings']) - 5} more warnings")
        print()

    # Targets with most findings
    if targets:
        print("Targets with Most Findings:")
        multi_hit_targets = [(t, fs) for t, fs in targets.items() if len(fs) > 1]
        for target, fs in sorted(multi_hit_targets, key=lambda x: -len(x[1]))[:5]:
            max_score = max((f['score'] or 0) for f in fs)
            print(f"  [{max_score:3d}] {target[:70]} ({len(fs)} findings)")
        print()

    print("=== End Summary ===")

def main():
    if len(sys.argv) < 2:
        print("Usage: summarize_thor_log.py <logfile>", file=sys.stderr)
        print("  Parses THOR text log and outputs triage summary.", file=sys.stderr)
        sys.exit(2)

    logfile = sys.argv[1]
    if not os.path.exists(logfile):
        print(f"Error: file not found: {logfile}", file=sys.stderr)
        sys.exit(2)

    try:
        findings, modules, targets, signatures = parse_thor_log(logfile)
        print_summary(findings, modules, targets, signatures, logfile)
    except Exception as e:
        print(f"Error parsing log: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
