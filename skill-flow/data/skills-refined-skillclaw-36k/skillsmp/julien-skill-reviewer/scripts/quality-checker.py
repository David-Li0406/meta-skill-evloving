#!/usr/bin/env python3
"""
Automated quality checks for Claude skills.

This script performs automated checks that complement the LLM-based review:
- Word count analysis
- DRY violation detection (simple patterns)
- File structure validation
- YAML frontmatter parsing

Usage:
    python scripts/quality-checker.py path/to/skill/
"""

import argparse
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


def count_words(text: str) -> int:
    """Count words in text (excluding code blocks)."""
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`[^`]+`', '', text)
    # Count words
    words = text.split()
    return len(words)


def parse_frontmatter(skill_md_path: Path) -> Dict:
    """Parse YAML frontmatter from SKILL.md."""
    content = skill_md_path.read_text(encoding='utf-8')

    # Extract frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {"error": "No YAML frontmatter found"}

    frontmatter_text = match.group(1)
    try:
        return yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        return {"error": f"Invalid YAML: {e}"}


def find_duplicate_sections(skill_md_path: Path, references_dir: Path) -> List[Tuple[str, str, int]]:
    """
    Find potential duplicate content between SKILL.md and references/.

    Returns list of (file1, file2, similarity_score) tuples.
    """
    duplicates = []

    if not references_dir.exists():
        return duplicates

    skill_content = skill_md_path.read_text(encoding='utf-8')
    skill_lines = set(line.strip() for line in skill_content.split('\n') if len(line.strip()) > 20)

    for ref_file in references_dir.glob('*.md'):
        ref_content = ref_file.read_text(encoding='utf-8')
        ref_lines = set(line.strip() for line in ref_content.split('\n') if len(line.strip()) > 20)

        # Calculate overlap
        common_lines = skill_lines & ref_lines
        if common_lines and len(common_lines) > 5:
            similarity = len(common_lines)
            duplicates.append((skill_md_path.name, ref_file.name, similarity))

    return duplicates


def check_file_structure(skill_dir: Path) -> Dict[str, bool]:
    """Check if skill has proper file structure."""
    return {
        "SKILL.md exists": (skill_dir / "SKILL.md").exists(),
        "has references/": (skill_dir / "references").exists(),
        "has scripts/": (skill_dir / "scripts").exists(),
        "has assets/": (skill_dir / "assets").exists(),
    }


def analyze_skill(skill_dir: Path) -> Dict:
    """Perform complete automated analysis of a skill."""
    skill_dir = Path(skill_dir)
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return {"error": f"SKILL.md not found in {skill_dir}"}

    # Parse frontmatter
    frontmatter = parse_frontmatter(skill_md)

    # Count words
    content = skill_md.read_text(encoding='utf-8')
    word_count = count_words(content)

    # Check structure
    structure = check_file_structure(skill_dir)

    # Find duplicates
    duplicates = find_duplicate_sections(skill_md, skill_dir / "references")

    # Analyze progressive disclosure
    references_dir = skill_dir / "references"
    reference_files = []
    total_reference_words = 0
    if references_dir.exists():
        for ref_file in references_dir.glob('*.md'):
            ref_content = ref_file.read_text(encoding='utf-8')
            ref_words = count_words(ref_content)
            total_reference_words += ref_words
            reference_files.append({
                "name": ref_file.name,
                "words": ref_words
            })

    # Quality assessment
    issues = []
    warnings = []

    # Word count analysis
    if word_count > 5000:
        issues.append(f"SKILL.md is {word_count} words (exceeds 5000 word guideline)")
    elif word_count > 3000:
        warnings.append(f"SKILL.md is {word_count} words (consider moving details to references/)")

    # DRY violations
    if duplicates:
        for file1, file2, similarity in duplicates:
            issues.append(f"Potential duplication between {file1} and {file2} ({similarity} similar lines)")

    # Structure issues
    if word_count > 3000 and not structure["has references/"]:
        issues.append("SKILL.md is long but no references/ directory for progressive disclosure")

    # Frontmatter validation
    if "error" in frontmatter:
        issues.append(f"Frontmatter error: {frontmatter['error']}")
    else:
        if "name" not in frontmatter:
            issues.append("Missing required field: name")
        if "description" not in frontmatter:
            issues.append("Missing required field: description")

        # Check name format (kebab-case)
        if "name" in frontmatter:
            name = frontmatter["name"]
            if not re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$', name):
                warnings.append(f"Name '{name}' should be in kebab-case (lowercase with hyphens)")

        # Check description length
        if "description" in frontmatter:
            desc = frontmatter["description"]
            if len(desc) > 200:
                warnings.append(f"Description is {len(desc)} chars (recommended: <200)")
            if len(desc) < 50:
                warnings.append(f"Description is {len(desc)} chars (recommended: >50 for clarity)")

    return {
        "skill_name": frontmatter.get("name", "unknown"),
        "frontmatter": frontmatter,
        "word_count": {
            "SKILL.md": word_count,
            "references/": total_reference_words,
            "total": word_count + total_reference_words
        },
        "structure": structure,
        "reference_files": reference_files,
        "duplicates": duplicates,
        "issues": issues,
        "warnings": warnings,
        "quality_estimate": estimate_quality(word_count, structure, duplicates, frontmatter)
    }


def estimate_quality(word_count: int, structure: Dict, duplicates: List, frontmatter: Dict) -> str:
    """Provide rough quality estimate based on automated checks."""
    score = 0
    max_score = 10

    # Word count (0-3 points)
    if word_count <= 3000:
        score += 3
    elif word_count <= 5000:
        score += 2
    elif word_count <= 7000:
        score += 1

    # Structure (0-3 points)
    if structure["has references/"]:
        score += 2
    if structure["has scripts/"]:
        score += 0.5
    if structure["has assets/"]:
        score += 0.5

    # DRY (0-2 points)
    if not duplicates:
        score += 2
    elif len(duplicates) == 1:
        score += 1

    # Frontmatter (0-2 points)
    if "error" not in frontmatter:
        score += 1
        if "name" in frontmatter and "description" in frontmatter:
            score += 1

    percentage = (score / max_score) * 100

    if percentage >= 80:
        return "Good (likely 4-5/5) - automated checks passed"
    elif percentage >= 60:
        return "Fair (likely 3-4/5) - some improvements needed"
    elif percentage >= 40:
        return "Poor (likely 2-3/5) - significant issues detected"
    else:
        return "Critical (likely 1-2/5) - major rework needed"


def print_report(analysis: Dict):
    """Print formatted analysis report."""
    print("=" * 70)
    print(f"SKILL QUALITY REPORT: {analysis['skill_name']}")
    print("=" * 70)

    # Word counts
    print("\n📊 WORD COUNT ANALYSIS")
    print(f"  SKILL.md:     {analysis['word_count']['SKILL.md']:,} words")
    print(f"  references/:  {analysis['word_count']['references/']:,} words")
    print(f"  Total:        {analysis['word_count']['total']:,} words")

    wc = analysis['word_count']['SKILL.md']
    if wc <= 3000:
        print("  ✅ Excellent - Lean and focused")
    elif wc <= 5000:
        print("  ✅ Good - Within guidelines")
    elif wc <= 7000:
        print("  ⚠️  Warning - Consider moving content to references/")
    else:
        print("  ❌ Issue - Exceeds guidelines, refactoring recommended")

    # Structure
    print("\n📁 FILE STRUCTURE")
    for check, exists in analysis['structure'].items():
        icon = "✅" if exists else "❌"
        print(f"  {icon} {check}")

    # Reference files
    if analysis['reference_files']:
        print("\n📚 REFERENCES/")
        for ref in analysis['reference_files']:
            print(f"  - {ref['name']}: {ref['words']:,} words")

    # Duplicates
    if analysis['duplicates']:
        print("\n⚠️  POTENTIAL DRY VIOLATIONS")
        for file1, file2, similarity in analysis['duplicates']:
            print(f"  - {file1} ↔ {file2}: {similarity} similar lines")

    # Frontmatter
    print("\n📋 FRONTMATTER")
    fm = analysis['frontmatter']
    if "error" in fm:
        print(f"  ❌ {fm['error']}")
    else:
        print(f"  ✅ name: {fm.get('name', 'MISSING')}")
        desc = fm.get('description', 'MISSING')
        print(f"  ✅ description: {desc[:60]}{'...' if len(desc) > 60 else ''}")
        if 'license' in fm:
            print(f"  ✅ license: {fm['license']}")

    # Issues
    if analysis['issues']:
        print("\n❌ CRITICAL ISSUES")
        for issue in analysis['issues']:
            print(f"  • {issue}")

    # Warnings
    if analysis['warnings']:
        print("\n⚠️  WARNINGS")
        for warning in analysis['warnings']:
            print(f"  • {warning}")

    # Quality estimate
    print("\n" + "=" * 70)
    print(f"AUTOMATED QUALITY ESTIMATE: {analysis['quality_estimate']}")
    print("=" * 70)

    print("\nℹ️  Note: This is an automated analysis. For complete review")
    print("   including Clarity, Actionability, and Skill Chaining, use")
    print("   the full skill-reviewer skill with LLM-based evaluation.")


def main():
    parser = argparse.ArgumentParser(
        description="Automated quality checker for Claude skills"
    )
    parser.add_argument(
        "skill_dir",
        type=Path,
        help="Path to skill directory (containing SKILL.md)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    analysis = analyze_skill(args.skill_dir)

    if args.json:
        import json
        print(json.dumps(analysis, indent=2))
    else:
        print_report(analysis)


if __name__ == "__main__":
    main()
