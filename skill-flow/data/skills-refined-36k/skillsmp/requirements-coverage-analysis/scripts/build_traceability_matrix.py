#!/usr/bin/env python3
"""
Build traceability matrix from requirements to implementation artifacts.

Usage:
    python build_traceability_matrix.py \
      --requirements Docs/architecture/_main/03-Business-Requirements.md \
      --features "Docs/implementation/_main/feature-*.md" \
      --output traceability-matrix.json
"""

import argparse
import glob
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any


def extract_requirements_from_doc(doc_path: Path) -> List[Dict]:
    """Extract requirements from requirements document."""
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {doc_path}: {e}", file=sys.stderr)
        return []

    requirements = []
    req_pattern = r'([A-Z]+-\d+):?\s+(.+?)(?:\n|$)'

    for match in re.finditer(req_pattern, content, re.MULTILINE):
        req_id = match.group(1)
        req_desc = match.group(2).strip()

        requirements.append({
            "id": req_id,
            "description": req_desc,
            "features": [],
            "waves": [],
            "status": "uncovered"
        })

    return requirements


def extract_requirement_refs_from_feature(feature_path: Path) -> Dict:
    """Extract requirement references from feature plan."""
    try:
        with open(feature_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {feature_path}: {e}", file=sys.stderr)
        return {}

    # Extract feature number from filename (e.g., feature-5.1-name.md)
    feature_match = re.search(r'feature-(\d+\.\d+)', feature_path.name)
    feature_id = feature_match.group(1) if feature_match else feature_path.stem

    # Find requirement references
    req_refs = set()
    for match in re.finditer(r'([A-Z]+-\d+)', content):
        req_refs.add(match.group(1))

    # Check coverage level
    coverage_level = "partial"
    if re.search(r'fully (implements?|covers?|addresses?)', content, re.IGNORECASE):
        coverage_level = "full"

    return {
        "feature_id": feature_id,
        "feature_file": str(feature_path),
        "requirement_refs": list(req_refs),
        "coverage_level": coverage_level
    }


def extract_requirement_refs_from_waves(waves_pattern: str) -> List[Dict]:
    """Extract requirement references from wave plans."""
    wave_files = glob.glob(waves_pattern)
    wave_data = []

    for wave_file in wave_files:
        wave_path = Path(wave_file)

        try:
            with open(wave_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {wave_path}: {e}", file=sys.stderr)
            continue

        # Extract wave number from filename (e.g., wave-5.1.1-name.md)
        wave_match = re.search(r'wave-(\d+\.\d+\.\d+)', wave_path.name)
        wave_id = wave_match.group(1) if wave_match else wave_path.stem

        # Find requirement references
        req_refs = set()
        for match in re.finditer(r'([A-Z]+-\d+)', content):
            req_refs.add(match.group(1))

        wave_data.append({
            "wave_id": wave_id,
            "wave_file": str(wave_path),
            "requirement_refs": list(req_refs)
        })

    return wave_data


def build_matrix(requirements: List[Dict], features: List[Dict], waves: List[Dict]) -> List[Dict]:
    """Build traceability matrix linking requirements to features and waves."""
    # Map requirement IDs to features
    for feature in features:
        for req_id in feature["requirement_refs"]:
            for req in requirements:
                if req["id"] == req_id:
                    req["features"].append({
                        "feature_id": feature["feature_id"],
                        "feature_file": feature["feature_file"],
                        "coverage_level": feature["coverage_level"]
                    })
                    # Update status
                    if feature["coverage_level"] == "full":
                        req["status"] = "covered"
                    elif req["status"] == "uncovered":
                        req["status"] = "partial"

    # Map requirement IDs to waves
    for wave in waves:
        for req_id in wave["requirement_refs"]:
            for req in requirements:
                if req["id"] == req_id:
                    req["waves"].append({
                        "wave_id": wave["wave_id"],
                        "wave_file": wave["wave_file"]
                    })

    return requirements


def calculate_coverage_stats(matrix: List[Dict]) -> Dict:
    """Calculate coverage statistics."""
    total = len(matrix)
    covered = sum(1 for req in matrix if req["status"] == "covered")
    partial = sum(1 for req in matrix if req["status"] == "partial")
    uncovered = sum(1 for req in matrix if req["status"] == "uncovered")

    coverage_pct = ((covered + (partial * 0.5)) / total * 100) if total > 0 else 0

    return {
        "total": total,
        "covered": covered,
        "partial": partial,
        "uncovered": uncovered,
        "coverage_percentage": round(coverage_pct, 2)
    }


def generate_markdown_matrix(matrix: List[Dict], stats: Dict) -> str:
    """Generate markdown traceability matrix."""
    lines = ["# Requirements Traceability Matrix\n"]
    lines.append(f"**Total Requirements**: {stats['total']}")
    lines.append(f"**Coverage**: {stats['coverage_percentage']}%\n")

    lines.append("| Requirement ID | Description | Features | Waves | Status |")
    lines.append("|----------------|-------------|----------|-------|--------|")

    for req in matrix:
        req_id = req["id"]
        desc = req["description"][:50] + "..." if len(req["description"]) > 50 else req["description"]
        features = ", ".join([f["feature_id"] for f in req["features"]]) or "-"
        waves = ", ".join([w["wave_id"] for w in req["waves"]]) or "-"

        status_emoji = {
            "covered": "✅",
            "partial": "⚠️",
            "uncovered": "❌"
        }
        status = f"{status_emoji.get(req['status'], '❓')} {req['status'].title()}"

        lines.append(f"| {req_id} | {desc} | {features} | {waves} | {status} |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Build requirements traceability matrix"
    )

    parser.add_argument("--requirements", type=str, required=True,
                       help="Path to requirements document")
    parser.add_argument("--features", type=str, required=True,
                       help="Glob pattern for feature plans (e.g., 'Docs/implementation/_main/feature-*.md')")
    parser.add_argument("--waves", type=str,
                       help="Glob pattern for wave plans (optional)")
    parser.add_argument("--output", type=str,
                       help="Output file path (JSON or markdown)")
    parser.add_argument("--format", type=str, default="json",
                       choices=["json", "markdown"],
                       help="Output format")

    args = parser.parse_args()

    # Load requirements
    req_path = Path(args.requirements)
    if not req_path.exists():
        print(f"Error: Requirements document not found: {req_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Extracting requirements from {req_path}...", file=sys.stderr)
    requirements = extract_requirements_from_doc(req_path)
    print(f"Found {len(requirements)} requirement(s)", file=sys.stderr)

    # Load features
    feature_files = glob.glob(args.features)
    if not feature_files:
        print(f"Warning: No feature files found matching: {args.features}", file=sys.stderr)

    print(f"Analyzing {len(feature_files)} feature(s)...", file=sys.stderr)
    features = []
    for feature_file in feature_files:
        feature_data = extract_requirement_refs_from_feature(Path(feature_file))
        if feature_data:
            features.append(feature_data)

    # Load waves (optional)
    waves = []
    if args.waves:
        print(f"Analyzing waves matching: {args.waves}...", file=sys.stderr)
        waves = extract_requirement_refs_from_waves(args.waves)
        print(f"Found {len(waves)} wave(s)", file=sys.stderr)

    # Build matrix
    print("Building traceability matrix...", file=sys.stderr)
    matrix = build_matrix(requirements, features, waves)

    # Calculate statistics
    stats = calculate_coverage_stats(matrix)

    # Generate output
    if args.format == "json":
        result = {
            "statistics": stats,
            "matrix": matrix
        }
        output = json.dumps(result, indent=2)
    else:  # markdown
        output = generate_markdown_matrix(matrix, stats)

    # Write output
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Output written to {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)

    # Print summary
    print(f"\n=== Coverage Summary ===", file=sys.stderr)
    print(f"Total Requirements: {stats['total']}", file=sys.stderr)
    print(f"Fully Covered:      {stats['covered']} ({stats['covered']/stats['total']*100:.1f}%)", file=sys.stderr)
    print(f"Partially Covered:  {stats['partial']} ({stats['partial']/stats['total']*100:.1f}%)", file=sys.stderr)
    print(f"Uncovered:          {stats['uncovered']} ({stats['uncovered']/stats['total']*100:.1f}%)", file=sys.stderr)
    print(f"Coverage Score:     {stats['coverage_percentage']}%", file=sys.stderr)


if __name__ == "__main__":
    main()
