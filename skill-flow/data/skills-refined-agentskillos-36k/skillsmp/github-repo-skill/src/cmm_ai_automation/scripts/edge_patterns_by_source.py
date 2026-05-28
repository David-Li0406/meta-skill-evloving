#!/usr/bin/env python3
"""
Extract edge patterns from transformed data with per-source subdirectories.

For directory structure like kg-microbe/data/transformed/<source>/nodes.tsv, edges.tsv.
Source breakdown IS preserved - each pattern is labeled by its source directory name.

Output format:
    source | subject_category | subject_prefix | predicate | object_category | object_prefix | count
"""

import csv
import re
import sys
from collections import Counter
from pathlib import Path

CURIE_PATTERN = re.compile(r"^([^:]+):(.+)$")

# Type alias for edge patterns
EdgePattern = tuple[str, str, str, str, str, str]


def extract_prefix(curie: str | None) -> str:
    """Extract prefix from CURIE."""
    if not curie:
        return "(empty)"
    match = CURIE_PATTERN.match(curie.strip())
    if match:
        return match.group(1)
    return "(invalid)"


def analyze_edges(edges_file: Path, nodes_file: Path, source: str) -> Counter[EdgePattern]:
    """Analyze edges and return patterns."""
    # Build node category lookup
    node_categories: dict[str, str] = {}
    with nodes_file.open() as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            node_id = row.get("id", "").strip()
            category = row.get("category", "").strip()
            if node_id:
                node_categories[node_id] = category if category else "(empty)"

    # Extract patterns from edges
    patterns: Counter[EdgePattern] = Counter()
    with edges_file.open() as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            subj = row.get("subject", "").strip()
            pred = row.get("predicate", "").strip()
            obj = row.get("object", "").strip()

            subj_cat = node_categories.get(subj, "(unknown)")
            obj_cat = node_categories.get(obj, "(unknown)")

            subj_prefix = extract_prefix(subj)
            obj_prefix = extract_prefix(obj)

            pattern = (source, subj_cat, subj_prefix, pred, obj_cat, obj_prefix)
            patterns[pattern] += 1

    return patterns


def main() -> None:
    """Main function to analyze all sources."""
    if len(sys.argv) < 2:
        print("Usage: python edge_patterns_by_source.py <transformed_dir>", file=sys.stderr)
        sys.exit(1)

    transformed_dir = Path(sys.argv[1])
    all_patterns: Counter[EdgePattern] = Counter()

    # Find all source directories
    for source_dir in transformed_dir.iterdir():
        if not source_dir.is_dir():
            continue

        edges_file = source_dir / "edges.tsv"
        nodes_file = source_dir / "nodes.tsv"

        if not edges_file.exists() or not nodes_file.exists():
            continue

        source = source_dir.name
        patterns = analyze_edges(edges_file, nodes_file, source)
        all_patterns.update(patterns)

    # Output as TSV
    writer = csv.writer(sys.stdout, delimiter="\t")
    writer.writerow(
        ["source", "subject_category", "subject_prefix", "predicate", "object_category", "object_prefix", "count"]
    )

    # Sort by count descending
    for pattern, count in sorted(all_patterns.items(), key=lambda x: -x[1]):
        writer.writerow([*pattern, count])


if __name__ == "__main__":
    main()
