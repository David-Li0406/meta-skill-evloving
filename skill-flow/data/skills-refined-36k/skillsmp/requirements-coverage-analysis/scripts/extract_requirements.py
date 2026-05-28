#!/usr/bin/env python3
"""
Extract structured requirements from markdown documents.

Usage:
    python extract_requirements.py --doc Docs/architecture/_main/03-Business-Requirements.md
    python extract_requirements.py --doc feature-5.1.md --format json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any


def extract_requirements(content: str, doc_path: Path) -> List[Dict[str, Any]]:
    """
    Extract requirements from markdown content.

    Looks for patterns like:
    - REQ-001: Description
    - **REQ-002**: Description
    - ## REQ-003: Title
    """
    requirements = []

    # Pattern 1: REQ-XXX: Description (standalone or in headers)
    req_pattern = r'(?:^|\s|[#*]+)\s*([A-Z]+-\d+):?\s+(.+?)(?:\n|$)'

    for match in re.finditer(req_pattern, content, re.MULTILINE):
        req_id = match.group(1)
        req_desc = match.group(2).strip()

        # Try to extract additional information
        priority = extract_priority_near(content, match.start())
        req_type = classify_requirement(req_desc)
        acceptance_criteria = extract_acceptance_criteria_for(content, req_id)

        requirements.append({
            "id": req_id,
            "description": req_desc,
            "priority": priority,
            "type": req_type,
            "acceptance_criteria": acceptance_criteria,
            "source": str(doc_path)
        })

    return requirements


def extract_priority_near(content: str, position: int, window: int = 200) -> str:
    """Extract priority level near a requirement."""
    # Look within window characters of the requirement
    start = max(0, position - window)
    end = min(len(content), position + window)
    snippet = content[start:end].lower()

    if 'critical' in snippet or 'high priority' in snippet:
        return "Critical"
    elif 'high' in snippet:
        return "High"
    elif 'medium' in snippet:
        return "Medium"
    elif 'low' in snippet:
        return "Low"
    else:
        return "Unknown"


def classify_requirement(description: str) -> str:
    """Classify requirement type based on description."""
    desc_lower = description.lower()

    if any(word in desc_lower for word in ['must', 'shall', 'will', 'required']):
        return "Functional"
    elif any(word in desc_lower for word in ['performance', 'latency', 'throughput', 'speed']):
        return "Performance"
    elif any(word in desc_lower for word in ['security', 'auth', 'encrypt', 'secure']):
        return "Security"
    elif any(word in desc_lower for word in ['usability', 'user experience', 'intuitive']):
        return "Usability"
    elif any(word in desc_lower for word in ['maintain', 'extend', 'modular']):
        return "Maintainability"
    elif any(word in desc_lower for word in ['reliable', 'available', 'uptime']):
        return "Reliability"
    else:
        return "Functional"


def extract_acceptance_criteria_for(content: str, req_id: str) -> List[str]:
    """Extract acceptance criteria for a specific requirement."""
    criteria = []

    # Look for section after requirement ID
    req_pattern = rf'{req_id}.*?(?=(?:^|\s)[A-Z]+-\d+|##|\Z)'
    match = re.search(req_pattern, content, re.DOTALL)

    if match:
        section = match.group(0)

        # Look for acceptance criteria section
        ac_match = re.search(r'(?:Acceptance Criteria|Success Criteria):?\s*\n(.*?)(?=\n##|\Z)',
                            section, re.DOTALL | re.IGNORECASE)

        if ac_match:
            ac_section = ac_match.group(1)

            # Extract bullet points
            for line in ac_section.split('\n'):
                line = line.strip()
                if line.startswith('-') or line.startswith('*'):
                    criteria.append(line.lstrip('-*').strip())

    return criteria


def extract_from_feature_plan(content: str, doc_path: Path) -> Dict[str, Any]:
    """Extract requirement references from feature plan."""
    # Find requirements section
    req_section_match = re.search(
        r'##\s+Requirements?\s*\n(.*?)(?=##|\Z)',
        content,
        re.DOTALL | re.IGNORECASE
    )

    requirement_refs = []
    if req_section_match:
        req_section = req_section_match.group(1)

        # Extract REQ-XXX references
        for match in re.finditer(r'([A-Z]+-\d+)', req_section):
            req_id = match.group(1)
            if req_id not in requirement_refs:
                requirement_refs.append(req_id)

    return {
        "feature": doc_path.stem,
        "requirement_references": requirement_refs,
        "count": len(requirement_refs)
    }


def main():
    parser = argparse.ArgumentParser(
        description="Extract structured requirements from markdown documents"
    )

    parser.add_argument("--doc", type=str, required=True,
                       help="Path to markdown document")
    parser.add_argument("--type", type=str, default="requirements",
                       choices=["requirements", "feature"],
                       help="Document type (requirements doc or feature plan)")
    parser.add_argument("--format", type=str, default="json",
                       choices=["json", "markdown", "csv"],
                       help="Output format")
    parser.add_argument("--output", type=str,
                       help="Output file path")

    args = parser.parse_args()

    doc_path = Path(args.doc)
    if not doc_path.exists():
        print(f"Error: Document not found: {doc_path}", file=sys.stderr)
        sys.exit(1)

    # Read document
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading document: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract requirements
    if args.type == "requirements":
        requirements = extract_requirements(content, doc_path)
        result = {
            "source": str(doc_path),
            "total_requirements": len(requirements),
            "requirements": requirements
        }
    else:  # feature
        result = extract_from_feature_plan(content, doc_path)

    # Generate output
    if args.format == "json":
        output = json.dumps(result, indent=2)
    elif args.format == "markdown":
        if args.type == "requirements":
            lines = [f"# Requirements from {doc_path.name}\n"]
            for req in result["requirements"]:
                lines.append(f"## {req['id']}: {req['description']}")
                lines.append(f"- **Type**: {req['type']}")
                lines.append(f"- **Priority**: {req['priority']}")
                if req['acceptance_criteria']:
                    lines.append(f"- **Acceptance Criteria**:")
                    for criterion in req['acceptance_criteria']:
                        lines.append(f"  - {criterion}")
                lines.append("")
            output = "\n".join(lines)
        else:
            lines = [f"# Feature: {result['feature']}\n"]
            lines.append(f"**Requirements Referenced**: {result['count']}\n")
            for req_id in result['requirement_references']:
                lines.append(f"- {req_id}")
            output = "\n".join(lines)
    else:  # csv
        if args.type == "requirements":
            lines = ["ID,Description,Type,Priority,Acceptance Criteria Count"]
            for req in result["requirements"]:
                lines.append(f"{req['id']},\"{req['description']}\",{req['type']},{req['priority']},{len(req['acceptance_criteria'])}")
            output = "\n".join(lines)
        else:
            output = f"Feature,Requirements Count\n{result['feature']},{result['count']}"

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
    if args.type == "requirements":
        print(f"\nExtracted {result['total_requirements']} requirement(s)", file=sys.stderr)
    else:
        print(f"\nFound {result['count']} requirement reference(s)", file=sys.stderr)


if __name__ == "__main__":
    main()
