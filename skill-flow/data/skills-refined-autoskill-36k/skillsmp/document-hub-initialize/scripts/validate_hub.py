#!/usr/bin/env python3
"""
Validate documentation hub structure and content.

This tool checks:
- File structure (all required files exist)
- Mermaid diagram syntax
- Cross-references between files
- Markdown formatting

Returns structured JSON with validation results.
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple


def validate_file_structure(project_path: Path) -> Dict:
    """Check if all required documentation hub files exist."""
    docs_path = project_path / "cline-docs"
    required_files = [
        "systemArchitecture.md",
        "keyPairResponsibility.md",
        "glossary.md",
        "techStack.md"
    ]

    errors = []
    warnings = []

    if not docs_path.exists():
        errors.append("Documentation hub directory 'cline-docs' not found")
        return {
            "check": "file_structure",
            "passed": False,
            "errors": errors,
            "warnings": warnings
        }

    for file_name in required_files:
        file_path = docs_path / file_name
        if not file_path.exists():
            errors.append(f"Missing required file: {file_name}")
        elif file_path.stat().st_size == 0:
            warnings.append(f"File is empty: {file_name}")

    return {
        "check": "file_structure",
        "passed": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def extract_mermaid_blocks(content: str) -> List[Tuple[int, str]]:
    """Extract Mermaid diagram blocks from markdown content."""
    blocks = []
    lines = content.split('\n')
    in_mermaid = False
    current_block = []
    block_start_line = 0

    for line_num, line in enumerate(lines, 1):
        if line.strip() == '```mermaid':
            in_mermaid = True
            block_start_line = line_num
            current_block = []
        elif line.strip().startswith('```') and in_mermaid:
            in_mermaid = False
            blocks.append((block_start_line, '\n'.join(current_block)))
        elif in_mermaid:
            current_block.append(line)

    return blocks


def validate_mermaid_syntax(content: str, file_name: str) -> Dict:
    """Validate Mermaid diagram syntax and complexity."""
    errors = []
    warnings = []

    blocks = extract_mermaid_blocks(content)

    if not blocks:
        # Not an error if no Mermaid diagrams
        return {
            "check": f"mermaid_syntax_{file_name}",
            "passed": True,
            "errors": errors,
            "warnings": warnings
        }

    for line_num, block in blocks:
        block = block.strip()

        if not block:
            errors.append({
                "file": file_name,
                "line": line_num,
                "message": "Empty Mermaid diagram"
            })
            continue

        # Check for diagram type declaration
        diagram_types = ['flowchart', 'graph', 'sequenceDiagram', 'classDiagram',
                        'stateDiagram', 'erDiagram', 'gantt', 'pie', 'gitGraph']

        has_type = any(dt in block for dt in diagram_types)
        if not has_type:
            warnings.append({
                "file": file_name,
                "line": line_num,
                "message": "Mermaid diagram missing explicit type declaration"
            })

        # Check for complexity in flowcharts/graphs
        if 'flowchart' in block or 'graph' in block:
            # Count connections (arrows)
            connections = len(re.findall(r'-->|---|\-\.->', block))

            if connections > 20:
                warnings.append({
                    "file": file_name,
                    "line": line_num,
                    "message": f"Complex diagram with {connections} connections. Consider splitting into multiple diagrams or using /arch subfolder."
                })

            # Count nodes (rough estimate)
            lines_with_arrows = [l for l in block.split('\n') if '-->' in l or '---' in l]
            if len(lines_with_arrows) > 15:
                warnings.append({
                    "file": file_name,
                    "line": line_num,
                    "message": f"Diagram has {len(lines_with_arrows)} relationship lines. May be hard to read."
                })

        # Check for common syntax errors
        if '[' in block and ']' not in block:
            errors.append({
                "file": file_name,
                "line": line_num,
                "message": "Unmatched square bracket in node definition"
            })

        if '(' in block and ')' not in block:
            errors.append({
                "file": file_name,
                "line": line_num,
                "message": "Unmatched parenthesis in node definition"
            })

    return {
        "check": f"mermaid_syntax_{file_name}",
        "passed": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def validate_cross_references(project_path: Path) -> Dict:
    """Check cross-references between documentation files."""
    docs_path = project_path / "cline-docs"
    errors = []
    warnings = []

    if not docs_path.exists():
        return {
            "check": "cross_references",
            "passed": True,
            "errors": [],
            "warnings": []
        }

    # Build index of all section headers
    all_sections = {}
    all_files = {}

    for md_file in docs_path.glob("**/*.md"):
        relative_path = md_file.relative_to(docs_path)
        all_files[md_file.name] = str(relative_path)

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            for line_num, line in enumerate(content.split('\n'), 1):
                if line.startswith('#'):
                    header = line.lstrip('#').strip()
                    section_id = header.lower().replace(' ', '-').replace('/', '')
                    all_sections[section_id] = {
                        'file': md_file.name,
                        'header': header,
                        'line': line_num
                    }

    # Check all markdown links
    for md_file in docs_path.glob("**/*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

            # Find markdown links [text](link)
            links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)

            for text, link in links:
                # Check internal anchor links
                if link.startswith('#'):
                    section_id = link[1:].lower().replace(' ', '-')
                    if section_id not in all_sections:
                        errors.append({
                            "file": md_file.name,
                            "message": f"Broken internal link: '{link}' references non-existent section"
                        })

                # Check relative file links
                elif not link.startswith('http'):
                    if '#' in link:
                        file_part, anchor = link.split('#', 1)
                    else:
                        file_part = link

                    if file_part and file_part not in all_files.values():
                        # Check if file exists
                        linked_file = docs_path / file_part
                        if not linked_file.exists():
                            errors.append({
                                "file": md_file.name,
                                "message": f"Broken file link: '{link}' - file not found"
                            })

    return {
        "check": "cross_references",
        "passed": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def validate_glossary_structure(project_path: Path) -> Dict:
    """Validate glossary.md structure and format."""
    docs_path = project_path / "cline-docs"
    glossary_path = docs_path / "glossary.md"
    errors = []
    warnings = []

    if not glossary_path.exists():
        return {
            "check": "glossary_structure",
            "passed": True,
            "errors": [],
            "warnings": ["glossary.md not found"]
        }

    with open(glossary_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for alphabetical ordering (simple check)
    terms = []
    lines = content.split('\n')

    for line in lines:
        # Look for term definitions (usually start with **term** or ### term)
        if line.startswith('**') and '**' in line[2:]:
            term = line.split('**')[1]
            terms.append(term)
        elif line.startswith('### '):
            term = line[4:].strip()
            terms.append(term)

    if terms:
        sorted_terms = sorted(terms, key=str.lower)
        if terms != sorted_terms:
            warnings.append({
                "file": "glossary.md",
                "message": "Glossary terms are not in alphabetical order"
            })

    return {
        "check": "glossary_structure",
        "passed": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def check_arch_subfolder(project_path: Path) -> Dict:
    """Check if /arch subfolder exists and validate its structure."""
    docs_path = project_path / "cline-docs"
    arch_path = docs_path / "arch"
    warnings = []

    if arch_path.exists():
        # Count diagram files
        diagram_files = list(arch_path.glob("*.md"))

        if len(diagram_files) == 0:
            warnings.append({
                "message": "/arch subfolder exists but contains no markdown files"
            })

        # Check if systemArchitecture.md references /arch files
        sys_arch_path = docs_path / "systemArchitecture.md"
        if sys_arch_path.exists():
            with open(sys_arch_path, 'r', encoding='utf-8') as f:
                content = f.read()

            arch_references = len(re.findall(r'\]\(arch/', content))
            if arch_references == 0:
                warnings.append({
                    "message": "systemArchitecture.md doesn't reference any files in /arch subfolder"
                })

    return {
        "check": "arch_subfolder",
        "passed": True,
        "errors": [],
        "warnings": warnings
    }


def main():
    """Main validation function."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Project path required"}))
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()

    if not project_path.exists():
        print(json.dumps({"error": f"Project path not found: {project_path}"}))
        sys.exit(1)

    docs_path = project_path / "cline-docs"
    if not docs_path.exists():
        print(json.dumps({
            "valid": False,
            "errors": ["Documentation hub not found. Run /document-hub initialize first."],
            "warnings": [],
            "checks_run": 0
        }))
        sys.exit(0)

    # Run all validation checks
    results = []
    results.append(validate_file_structure(project_path))

    # Validate Mermaid syntax in all markdown files
    for md_file in docs_path.glob("**/*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            results.append(validate_mermaid_syntax(content, md_file.name))

    results.append(validate_cross_references(project_path))
    results.append(validate_glossary_structure(project_path))
    results.append(check_arch_subfolder(project_path))

    # Aggregate results
    all_errors = []
    all_warnings = []

    for result in results:
        errors = result.get('errors', [])
        warnings = result.get('warnings', [])

        # Normalize error format
        for error in errors:
            if isinstance(error, str):
                all_errors.append({"message": error})
            else:
                all_errors.append(error)

        for warning in warnings:
            if isinstance(warning, str):
                all_warnings.append({"message": warning})
            else:
                all_warnings.append(warning)

    output = {
        "valid": len(all_errors) == 0,
        "errors": all_errors,
        "warnings": all_warnings,
        "checks_run": len(results),
        "project_path": str(project_path),
        "docs_path": str(docs_path)
    }

    print(json.dumps(output, indent=2))
    sys.exit(0 if output["valid"] else 1)


if __name__ == "__main__":
    main()
