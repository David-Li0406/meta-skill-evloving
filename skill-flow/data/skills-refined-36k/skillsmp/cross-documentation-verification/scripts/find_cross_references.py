#!/usr/bin/env python3
"""
Find all cross-references between documentation files.

Usage:
    python find_cross_references.py --doc feature-5.1-global-services.md
    python find_cross_references.py --dir Docs/ --output cross-refs.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set


def find_references_in_content(content: str, source_file: Path) -> List[Dict]:
    """
    Find all references to other documents in content.

    Looks for:
    - Markdown links: [text](path/to/file.md)
    - Document references: feature-X.Y, wave-X.Y.Z, ADR-XXX, epic-X
    - Relative paths: ../path/to/file.md
    """
    references = []

    # Pattern 1: Markdown links
    md_link_pattern = r'\[([^\]]+)\]\(([^\)]+\.md)\)'
    for match in re.finditer(md_link_pattern, content):
        link_text = match.group(1)
        link_path = match.group(2)
        references.append({
            "type": "markdown_link",
            "text": link_text,
            "target": link_path,
            "source": str(source_file)
        })

    # Pattern 2: Epic references (epic-X, epic-X-name)
    epic_pattern = r'\bepic-(\d+)(?:-[\w-]+)?\.md\b'
    for match in re.finditer(epic_pattern, content):
        references.append({
            "type": "epic_reference",
            "text": match.group(0),
            "target": match.group(0),
            "epic_number": match.group(1),
            "source": str(source_file)
        })

    # Pattern 3: Feature references (feature-X.Y, feature-X.Y-name)
    feature_pattern = r'\bfeature-(\d+)\.(\d+)(?:-[\w-]+)?\.md\b'
    for match in re.finditer(feature_pattern, content):
        references.append({
            "type": "feature_reference",
            "text": match.group(0),
            "target": match.group(0),
            "epic_number": match.group(1),
            "feature_number": match.group(2),
            "source": str(source_file)
        })

    # Pattern 4: Wave references (wave-X.Y.Z, wave-X.Y.Z-name)
    wave_pattern = r'\bwave-(\d+)\.(\d+)\.(\d+)(?:-[\w-]+)?\.md\b'
    for match in re.finditer(wave_pattern, content):
        references.append({
            "type": "wave_reference",
            "text": match.group(0),
            "target": match.group(0),
            "epic_number": match.group(1),
            "feature_number": match.group(2),
            "wave_number": match.group(3),
            "source": str(source_file)
        })

    # Pattern 5: ADR references (ADR-XXX, adr-xxx)
    adr_pattern = r'\b[Aa][Dd][Rr]-(\d+)\b'
    for match in re.finditer(adr_pattern, content):
        references.append({
            "type": "adr_reference",
            "text": match.group(0),
            "target": f"ADR-{match.group(1)}.md",
            "adr_number": match.group(1),
            "source": str(source_file)
        })

    # Pattern 6: Architecture doc references
    arch_pattern = r'\b(\d+-[\w-]+\.md)\b'
    for match in re.finditer(arch_pattern, content):
        filename = match.group(1)
        # Skip if already captured by other patterns
        if not any(filename.startswith(prefix) for prefix in ['epic-', 'feature-', 'wave-', 'ADR-', 'adr-']):
            references.append({
                "type": "architecture_reference",
                "text": filename,
                "target": filename,
                "source": str(source_file)
            })

    return references


def analyze_document(doc_path: Path) -> Dict:
    """Analyze a single document for cross-references."""
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {doc_path}: {e}", file=sys.stderr)
        return {}

    references = find_references_in_content(content, doc_path)

    return {
        "file": str(doc_path),
        "references": references,
        "reference_count": len(references),
        "referenced_documents": list(set(ref["target"] for ref in references))
    }


def analyze_directory(dir_path: Path, pattern: str = "*.md") -> List[Dict]:
    """Analyze all markdown files in directory."""
    results = []

    for doc_file in dir_path.rglob(pattern):
        # Skip non-documentation files
        if any(skip in str(doc_file) for skip in ['node_modules', '.git', 'archive']):
            continue

        print(f"Analyzing {doc_file.name}...", file=sys.stderr)
        analysis = analyze_document(doc_file)
        if analysis:
            results.append(analysis)

    return results


def build_dependency_graph(analyses: List[Dict]) -> Dict:
    """Build a dependency graph showing which docs reference which."""
    graph = {}

    for analysis in analyses:
        source = analysis["file"]
        targets = analysis["referenced_documents"]

        graph[source] = {
            "references": targets,
            "referenced_by": []
        }

    # Build reverse references (referenced_by)
    for source, data in graph.items():
        for target in data["references"]:
            # Find matching file
            for other_source in graph.keys():
                if target in other_source or other_source.endswith(target):
                    graph[other_source]["referenced_by"].append(source)
                    break

    return graph


def find_missing_references(analyses: List[Dict], base_dir: Path) -> List[Dict]:
    """Find broken references (documents that don't exist)."""
    missing = []

    all_files = set()
    for analysis in analyses:
        all_files.add(Path(analysis["file"]).name)

    for analysis in analyses:
        for ref in analysis["references"]:
            target = ref["target"]
            # Check if target exists
            if target not in all_files:
                # Try to find it in directory
                found = False
                for doc_file in base_dir.rglob("*.md"):
                    if target in str(doc_file) or doc_file.name == target:
                        found = True
                        break
                if not found:
                    missing.append({
                        "source": analysis["file"],
                        "target": target,
                        "reference_type": ref["type"],
                        "reference_text": ref["text"]
                    })

    return missing


def main():
    parser = argparse.ArgumentParser(
        description="Find cross-references between documentation files"
    )

    parser.add_argument("--doc", type=str,
                       help="Path to single document file")
    parser.add_argument("--dir", type=str,
                       help="Path to directory containing documents")
    parser.add_argument("--output", type=str,
                       help="Output file path (JSON)")
    parser.add_argument("--check-missing", action="store_true",
                       help="Check for missing/broken references")
    parser.add_argument("--build-graph", action="store_true",
                       help="Build dependency graph")

    args = parser.parse_args()

    if not args.doc and not args.dir:
        print("Error: Must specify either --doc or --dir", file=sys.stderr)
        sys.exit(1)

    # Analyze documents
    if args.doc:
        doc_path = Path(args.doc)
        if not doc_path.exists():
            print(f"Error: Document not found: {doc_path}", file=sys.stderr)
            sys.exit(1)
        results = [analyze_document(doc_path)]
        base_dir = doc_path.parent
    else:
        dir_path = Path(args.dir)
        if not dir_path.is_dir():
            print(f"Error: Directory not found: {dir_path}", file=sys.stderr)
            sys.exit(1)
        results = analyze_directory(dir_path)
        base_dir = dir_path

    # Build outputs
    output = {
        "analyses": results,
        "total_documents": len(results),
        "total_references": sum(r["reference_count"] for r in results)
    }

    if args.build_graph:
        output["dependency_graph"] = build_dependency_graph(results)

    if args.check_missing:
        missing = find_missing_references(results, base_dir)
        output["missing_references"] = missing
        output["missing_count"] = len(missing)

    # Write output
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2)
            print(f"Output written to {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(json.dumps(output, indent=2))

    # Print summary
    print(f"\nProcessed {len(results)} document(s)", file=sys.stderr)
    print(f"Total references found: {output['total_references']}", file=sys.stderr)
    if args.check_missing:
        print(f"Missing references: {output['missing_count']}", file=sys.stderr)


if __name__ == "__main__":
    main()
