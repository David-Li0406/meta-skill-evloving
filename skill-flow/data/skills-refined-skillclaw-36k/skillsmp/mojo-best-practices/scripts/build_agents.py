#!/usr/bin/env python3
"""
Build script to auto-generate AGENTS.md from pattern files.

Usage:
    python scripts/build_agents.py

This follows the Supabase agent-skills pattern where AGENTS.md is
auto-generated and should never be manually edited.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown file."""
    if not content.startswith("---"):
        return {}

    end = content.find("---", 3)
    if end == -1:
        return {}

    frontmatter = content[3:end].strip()
    result = {}

    for line in frontmatter.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            # Handle arrays
            if value.startswith("[") and value.endswith("]"):
                value = [v.strip().strip('"').strip("'")
                        for v in value[1:-1].split(",")]

            result[key] = value

    return result


def get_first_paragraph(content: str) -> str:
    """Get the first paragraph after frontmatter."""
    # Skip frontmatter
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            content = content[end + 3:].strip()

    # Skip title
    lines = content.split("\n")
    start_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("#"):
            start_idx = i + 1
            break

    # Get first non-empty paragraph
    paragraph = []
    for line in lines[start_idx:]:
        line = line.strip()
        if not line:
            if paragraph:
                break
            continue
        if line.startswith("#") or line.startswith("|") or line.startswith("```"):
            if paragraph:
                break
            continue
        paragraph.append(line)

    return " ".join(paragraph)[:200]  # Truncate to 200 chars


def get_category_from_prefix(prefix: str) -> tuple:
    """Map pattern prefix to category name and priority."""
    categories = {
        "memory": ("Memory Safety & Ownership", "CRITICAL"),
        "type": ("Type System", "CRITICAL"),
        "gpu": ("GPU Programming", "CRITICAL"),
        "ffi": ("C Interoperability", "CRITICAL"),
        "struct": ("Struct Design", "HIGH"),
        "fn": ("Function Design", "HIGH"),
        "test": ("Testing", "HIGH"),
        "debug": ("Debugging", "HIGH"),
        "error": ("Error Handling", "MEDIUM-HIGH"),
        "perf": ("Performance Optimization", "MEDIUM"),
        "python": ("Python Interoperability", "MEDIUM"),
        "meta": ("Advanced Metaprogramming", "LOW"),
    }
    return categories.get(prefix, ("Other", "LOW"))


def sync_metadata(patterns_dir: Path, metadata_file: Path) -> None:
    """Count patterns by category prefix and update metadata.json.

    Note: Version-specific content is now consolidated within pattern files,
    not in separate stable/ and nightly/ directories.
    """
    # Prefixes to count
    prefixes = ["memory", "type", "gpu", "ffi", "struct", "fn", "test", "debug", "error", "perf", "python", "meta"]

    # Collect all pattern files (main directory only)
    pattern_files = list(patterns_dir.glob("*.md"))

    # Count patterns by prefix
    counts = {prefix: 0 for prefix in prefixes}
    total = 0

    for pattern_file in pattern_files:
        # Skip templates
        if pattern_file.name.startswith("_"):
            continue

        pattern_name = pattern_file.stem
        prefix = pattern_name.split("-")[0] if "-" in pattern_name else "other"

        if prefix in counts:
            counts[prefix] += 1
        total += 1

    # Read existing metadata
    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Update counts in metadata
    prefix_to_category = {
        "memory": "memory-safety",
        "type": "type-system",
        "gpu": "gpu-programming",
        "ffi": "c-interoperability",
        "struct": "struct-design",
        "fn": "function-design",
        "test": "testing",
        "debug": "debugging",
        "error": "error-handling",
        "perf": "performance",
        "python": "python-interop",
        "meta": "metaprogramming",
    }

    for prefix, category_key in prefix_to_category.items():
        if counts[prefix] > 0:
            if category_key in metadata["patterns"]["categories"]:
                metadata["patterns"]["categories"][category_key]["count"] = counts[prefix]
            else:
                # Create new category
                _, priority = get_category_from_prefix(prefix)
                metadata["patterns"]["categories"][category_key] = {
                    "prefix": f"{prefix}-",
                    "priority": priority,
                    "count": counts[prefix]
                }

    # Update total
    metadata["patterns"]["total"] = total

    # Update last_verified timestamp
    metadata["last_verified"] = "2026-01-26"

    # Write updated metadata
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        f.write("\n")

    print(f"Updated {metadata_file}")
    print(f"  Total patterns: {total}")
    for prefix, count in counts.items():
        if count > 0:
            print(f"  {prefix}: {count}")


def main():
    script_dir = Path(__file__).parent
    patterns_dir = script_dir.parent / "patterns"
    output_file = script_dir.parent / "AGENTS.md"

    # Collect all patterns
    patterns_by_category = defaultdict(list)

    # Scan main patterns directory only (version-specific content is now inline)
    pattern_files = list(patterns_dir.glob("*.md"))

    for pattern_file in sorted(pattern_files):
        # Skip templates
        if pattern_file.name.startswith("_"):
            continue

        content = pattern_file.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(content)

        # Get pattern name (filename without .md)
        pattern_name = pattern_file.stem

        # Determine category from prefix
        prefix = pattern_name.split("-")[0] if "-" in pattern_name else "other"
        category_name, priority = get_category_from_prefix(prefix)

        # Get title from frontmatter or generate from filename
        title = frontmatter.get("title", pattern_name.replace("-", " ").title())

        # Get impact from frontmatter
        impact = frontmatter.get("impact", priority)

        # Get description
        description = frontmatter.get("description", get_first_paragraph(content))

        # Get consolidated rules list
        consolidates = frontmatter.get("consolidates", [])

        # Determine file path relative to skill root
        relative_path = pattern_file.relative_to(patterns_dir.parent)

        patterns_by_category[category_name].append({
            "name": pattern_name,
            "title": title,
            "impact": impact,
            "description": description,
            "priority": priority,
            "file": str(relative_path),
            "version": frontmatter.get("version", ""),
            "consolidates": consolidates,
        })

    # Generate AGENTS.md
    output = []
    output.append("# Mojo Best Practices Patterns")
    output.append("")
    output.append("> **Auto-generated.** Do not edit manually. Run `python scripts/build_agents.py` to regenerate.")
    output.append("")

    # Priority order for categories
    priority_order = ["CRITICAL", "HIGH", "MEDIUM-HIGH", "MEDIUM", "LOW"]

    # Sort categories by priority
    sorted_categories = sorted(
        patterns_by_category.items(),
        key=lambda x: priority_order.index(x[1][0]["priority"]) if x[1] else 999
    )

    # Table of contents
    output.append("## Table of Contents")
    output.append("")
    total_patterns = sum(len(patterns) for patterns in patterns_by_category.values())
    output.append(f"**{total_patterns} patterns** across **{len(patterns_by_category)} categories**")
    output.append("")

    for category_name, patterns in sorted_categories:
        anchor = category_name.lower().replace(" ", "-").replace("&", "").replace("/", "")
        output.append(f"- [{category_name}](#{anchor}) ({len(patterns)} patterns)")
    output.append("")
    output.append("---")
    output.append("")

    # Generate each category section
    for category_name, patterns in sorted_categories:
        priority = patterns[0]["priority"] if patterns else "MEDIUM"
        output.append(f"## {category_name}")
        output.append("")
        output.append(f"**Priority:** {priority} | **Patterns:** {len(patterns)}")
        output.append("")

        for pattern in sorted(patterns, key=lambda x: x["name"]):
            output.append(f"### {pattern['title']}")
            output.append("")
            output.append(f"**Pattern:** `{pattern['name']}` | **Impact:** {pattern['impact']}")
            output.append("")
            if pattern["description"]:
                output.append(pattern["description"])
                output.append("")
            if pattern["consolidates"]:
                output.append(f"**Consolidates:** {', '.join(pattern['consolidates'])}")
                output.append("")
            output.append(f"See: [{pattern['file']}]({pattern['file']})")
            output.append("")

        output.append("---")
        output.append("")

    # Write output
    output_file.write_text("\n".join(output), encoding="utf-8")
    print(f"Generated {output_file}")
    print(f"  Total patterns: {total_patterns}")
    print(f"  Categories: {len(patterns_by_category)}")

    # Sync metadata.json with accurate counts
    metadata_file = script_dir.parent / "metadata.json"
    sync_metadata(patterns_dir, metadata_file)


if __name__ == "__main__":
    main()
