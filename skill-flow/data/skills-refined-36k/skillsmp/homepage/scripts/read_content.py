#!/usr/bin/env python3
"""
Reads homepage content from src/content/homepage/ and outputs a compact summary.
Usage: python3 read_content.py [section]
  section: hero, experience, education, skills, or all (default)
"""

import json
import re
import sys
from pathlib import Path

CONTENT_DIR = Path(__file__).parent.parent.parent.parent.parent / "src" / "content" / "homepage"


def parse_ts_object(content: str) -> dict | list:
    """Convert TypeScript object/array literal to Python dict/list."""
    # Remove export statements and type annotations
    content = re.sub(r'export\s+interface\s+\w+\s*\{[^}]*\}', '', content)

    # Find the main array/object assignment
    match = re.search(r'export\s+const\s+\w+[^=]*=\s*([\[\{][\s\S]*[\]\}]);', content)
    if not match:
        return {}

    data_str = match.group(1)

    # Convert single-quoted strings to double-quoted, escaping internal double quotes
    def convert_quotes(m):
        inner = m.group(1).replace('"', '\\"')
        return f'"{inner}"'

    data_str = re.sub(r"'([^']*)'", convert_quotes, data_str)

    # Remove trailing commas
    data_str = re.sub(r',(\s*[\}\]])', r'\1', data_str)
    # Quote unquoted keys
    data_str = re.sub(r'([{\s,])(\w+):', r'\1"\2":', data_str)

    try:
        return json.loads(data_str)
    except json.JSONDecodeError:
        return {}


def read_hero() -> dict:
    """Read hero data."""
    content = (CONTENT_DIR / "hero.ts").read_text()

    # Extract values using regex for cleaner parsing
    name = re.search(r'name:\s*["\']([^"\']+)["\']', content)
    title = re.search(r'title:\s*["\']([^"\']+)["\']', content)
    overview = re.search(r'overview:\s*["\']([^"\']+)["\']', content)
    skills = re.findall(r'primarySkills:\s*\[([\s\S]*?)\]', content)

    primary_skills = []
    if skills:
        primary_skills = re.findall(r'["\']([^"\']+)["\']', skills[0])

    return {
        "name": name.group(1) if name else "N/A",
        "title": title.group(1) if title else "N/A",
        "overview": overview.group(1) if overview else "N/A",
        "primarySkills": primary_skills
    }


def read_experience() -> list:
    """Read experience/jobs data."""
    content = (CONTENT_DIR / "experience.ts").read_text()
    return parse_ts_object(content) or []


def read_education() -> list:
    """Read education data."""
    content = (CONTENT_DIR / "education.ts").read_text()
    return parse_ts_object(content) or []


def read_skills() -> list:
    """Read skills data."""
    content = (CONTENT_DIR / "skills.ts").read_text()
    return parse_ts_object(content) or []


def format_hero(data: dict) -> str:
    """Format hero data for output."""
    overview = data.get('overview', '')
    overview_short = overview[:80] + '...' if len(overview) > 80 else overview

    return f"""HERO
  Name: {data.get('name', 'N/A')}
  Title: {data.get('title', 'N/A')}
  Overview: {overview_short}
  Primary Skills: {', '.join(data.get('primarySkills', []))}"""


def format_experience(jobs: list) -> str:
    """Format experience data for output."""
    lines = [f"EXPERIENCE ({len(jobs)} companies)"]
    for i, job in enumerate(jobs, 1):
        lines.append(f"  {i}. {job.get('company', 'N/A')} ({job.get('location', 'N/A')})")
        for role in job.get('roles', []):
            lines.append(f"     - {role.get('title')} / {role.get('type')} ({role.get('period')})")
            bullets = role.get('bullets', [])
            lines.append(f"       [{len(bullets)} bullets]")
    return '\n'.join(lines)


def format_education(entries: list) -> str:
    """Format education data for output."""
    lines = [f"EDUCATION ({len(entries)} entries)"]
    for i, entry in enumerate(entries, 1):
        gpa = f", GPA {entry.get('gpa')}" if entry.get('gpa') else ""
        lines.append(f"  {i}. {entry.get('institution', 'N/A')}")
        lines.append(f"     {entry.get('degree', 'N/A')}{gpa}")
        lines.append(f"     {entry.get('location', 'N/A')} | {entry.get('period', 'N/A')}")
    return '\n'.join(lines)


def format_skills(categories: list) -> str:
    """Format skills data for output."""
    lines = [f"SKILLS ({len(categories)} categories)"]
    for cat in categories:
        skills = ', '.join(cat.get('skills', []))
        lines.append(f"  {cat.get('title', 'N/A')}: {skills}")
    return '\n'.join(lines)


def main():
    section = sys.argv[1] if len(sys.argv) > 1 else "all"

    if section == "hero":
        print(format_hero(read_hero()))
    elif section == "experience":
        print(format_experience(read_experience()))
    elif section == "education":
        print(format_education(read_education()))
    elif section == "skills":
        print(format_skills(read_skills()))
    elif section == "all":
        print(format_hero(read_hero()))
        print()
        print(format_experience(read_experience()))
        print()
        print(format_education(read_education()))
        print()
        print(format_skills(read_skills()))
    elif section == "json":
        data = {
            "hero": read_hero(),
            "experience": read_experience(),
            "education": read_education(),
            "skills": read_skills()
        }
        print(json.dumps(data, indent=2))
    else:
        print(f"Unknown section: {section}")
        print("Usage: python3 read_content.py [hero|experience|education|skills|all|json]")
        sys.exit(1)


if __name__ == "__main__":
    main()
