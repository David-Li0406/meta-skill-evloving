#!/usr/bin/env python3
"""
Extract checkable requirements from ADR (Architectural Decision Record) documents.

Usage:
    python extract_adr_requirements.py --adr path/to/ADR-018-singleton-pattern.md
    python extract_adr_requirements.py --adr-dir path/to/decisions/ --output requirements.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any


def extract_requirements_from_adr(adr_path: Path) -> Dict[str, Any]:
    """
    Extract checkable requirements from an ADR document.

    Returns:
        Dictionary with ADR metadata and list of requirements
    """
    try:
        with open(adr_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {adr_path}: {e}", file=sys.stderr)
        return {}

    # Extract ADR number and title
    adr_match = re.search(r'#\s+ADR[-_]?(\d+):\s*(.+)', content, re.IGNORECASE)
    if adr_match:
        adr_number = adr_match.group(1)
        adr_title = adr_match.group(2).strip()
    else:
        adr_number = adr_path.stem
        adr_title = "Unknown"

    # Extract status
    status_match = re.search(r'\*\*Status\*\*:\s*(\w+)', content, re.IGNORECASE)
    status = status_match.group(1) if status_match else "Unknown"

    # Extract decision section
    decision_match = re.search(
        r'##\s+Decision\s*\n(.*?)(?=##|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    decision_text = decision_match.group(1) if decision_match else ""

    # Extract requirements (imperative statements)
    requirements = []

    # Look for bullet points with imperative verbs
    imperative_verbs = [
        'must', 'shall', 'will', 'should', 'require', 'need',
        'use', 'implement', 'follow', 'ensure', 'avoid', 'prevent'
    ]

    for line in decision_text.split('\n'):
        line = line.strip()
        if line.startswith('-') or line.startswith('*'):
            req_text = line.lstrip('-*').strip()
            # Check if line contains imperative verb
            if any(verb in req_text.lower() for verb in imperative_verbs):
                requirements.append({
                    "text": req_text,
                    "checkable": True,
                    "type": classify_requirement(req_text)
                })

    # Look for "Requirements" section if exists
    req_section_match = re.search(
        r'##\s+Requirements?\s*\n(.*?)(?=##|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    if req_section_match:
        req_section = req_section_match.group(1)
        for line in req_section.split('\n'):
            line = line.strip()
            if line.startswith('-') or line.startswith('*'):
                req_text = line.lstrip('-*').strip()
                if req_text and req_text not in [r["text"] for r in requirements]:
                    requirements.append({
                        "text": req_text,
                        "checkable": True,
                        "type": classify_requirement(req_text)
                    })

    # Extract consequences (positive and negative)
    consequences = []
    cons_match = re.search(
        r'##\s+Consequences?\s*\n(.*?)(?=##|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )
    if cons_match:
        cons_text = cons_match.group(1)
        for line in cons_text.split('\n'):
            line = line.strip()
            if line.startswith('-') or line.startswith('*'):
                cons_text = line.lstrip('-*').strip()
                if cons_text:
                    consequences.append(cons_text)

    return {
        "adr_number": adr_number,
        "adr_title": adr_title,
        "status": status,
        "file_path": str(adr_path),
        "requirements": requirements,
        "consequences": consequences,
        "total_requirements": len(requirements)
    }


def classify_requirement(req_text: str) -> str:
    """Classify requirement type based on content."""
    req_lower = req_text.lower()

    if any(word in req_lower for word in ['security', 'encrypt', 'auth', 'secure', 'password']):
        return "security"
    elif any(word in req_lower for word in ['performance', 'cache', 'optimize', 'fast', 'latency']):
        return "performance"
    elif any(word in req_lower for word in ['test', 'coverage', 'unit test', 'integration test']):
        return "testing"
    elif any(word in req_lower for word in ['pattern', 'singleton', 'factory', 'observer', 'strategy']):
        return "design_pattern"
    elif any(word in req_lower for word in ['api', 'endpoint', 'rest', 'graphql', 'http']):
        return "api_contract"
    elif any(word in req_lower for word in ['database', 'sql', 'query', 'data', 'schema']):
        return "data_storage"
    elif any(word in req_lower for word in ['log', 'monitor', 'trace', 'observability']):
        return "observability"
    elif any(word in req_lower for word in ['error', 'exception', 'handle', 'retry']):
        return "error_handling"
    elif any(word in req_lower for word in ['compliance', 'hipaa', 'pci', 'gdpr', 'sox']):
        return "compliance"
    elif any(word in req_lower for word in ['framework', 'library', 'dependency', 'technology']):
        return "technology"
    else:
        return "general"


def extract_from_directory(adr_dir: Path) -> List[Dict[str, Any]]:
    """Extract requirements from all ADRs in a directory."""
    adr_files = list(adr_dir.glob("ADR-*.md")) + list(adr_dir.glob("adr-*.md"))

    results = []
    for adr_file in sorted(adr_files):
        print(f"Processing {adr_file.name}...", file=sys.stderr)
        adr_data = extract_requirements_from_adr(adr_file)
        if adr_data:
            results.append(adr_data)

    return results


def generate_checklist(adr_data: Dict[str, Any]) -> str:
    """Generate markdown checklist from ADR requirements."""
    lines = []
    lines.append(f"# {adr_data['adr_title']} - Requirements Checklist")
    lines.append("")
    lines.append(f"**ADR Number**: ADR-{adr_data['adr_number']}")
    lines.append(f"**Status**: {adr_data['status']}")
    lines.append("")
    lines.append("## Requirements")
    lines.append("")

    for req in adr_data['requirements']:
        lines.append(f"- [ ] {req['text']} _(Type: {req['type']})_")

    if adr_data['consequences']:
        lines.append("")
        lines.append("## Expected Consequences")
        lines.append("")
        for cons in adr_data['consequences']:
            lines.append(f"- {cons}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Extract checkable requirements from ADR documents"
    )

    parser.add_argument("--adr", type=str,
                       help="Path to single ADR file")
    parser.add_argument("--adr-dir", type=str,
                       help="Path to directory containing ADR files")
    parser.add_argument("--output", type=str,
                       help="Output file path (JSON or markdown)")
    parser.add_argument("--format", type=str, default="json",
                       choices=["json", "markdown"],
                       help="Output format")

    args = parser.parse_args()

    if not args.adr and not args.adr_dir:
        print("Error: Must specify either --adr or --adr-dir", file=sys.stderr)
        sys.exit(1)

    # Extract requirements
    if args.adr:
        adr_path = Path(args.adr)
        if not adr_path.exists():
            print(f"Error: ADR file not found: {adr_path}", file=sys.stderr)
            sys.exit(1)
        results = [extract_requirements_from_adr(adr_path)]
    else:
        adr_dir = Path(args.adr_dir)
        if not adr_dir.is_dir():
            print(f"Error: Directory not found: {adr_dir}", file=sys.stderr)
            sys.exit(1)
        results = extract_from_directory(adr_dir)

    # Generate output
    if args.format == "json":
        output = json.dumps(results, indent=2)
    else:  # markdown
        if len(results) == 1:
            output = generate_checklist(results[0])
        else:
            output = "\n\n---\n\n".join(generate_checklist(adr) for adr in results)

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
    total_reqs = sum(adr['total_requirements'] for adr in results)
    print(f"\nProcessed {len(results)} ADR(s)", file=sys.stderr)
    print(f"Total requirements extracted: {total_reqs}", file=sys.stderr)


if __name__ == "__main__":
    main()
