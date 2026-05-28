#!/usr/bin/env python3
"""
Format Resume to Markdown/Text

Usage:
    python3 format_resume.py <resume_json> [--format <fmt>]

Dependencies:
    None
"""

import sys
import argparse
import json


def format_to_markdown(data):
    lines = []

    # Header
    name = data.get("full_name", "Name")
    contact = f"{data.get('email', '')} | {data.get('phone', '')}"
    lines.append(f"# {name}")
    lines.append(contact)
    lines.append("")

    # Skills
    if "skills" in data and data["skills"]:
        lines.append("## Skills")
        lines.append(", ".join(data["skills"]))
        lines.append("")

    # Experience
    if "experience" in data and data["experience"]:
        lines.append("## Experience")
        for job in data["experience"]:
            lines.append(
                f"### {job.get('title', 'Title')} at {job.get('company', 'Company')}"
            )
            lines.append(
                f"*{job.get('start_date', '')} - {job.get('end_date', 'Present')}*"
            )
            if "description" in job:
                lines.append(job["description"])
            lines.append("")

    # Education
    if "education" in data and data["education"]:
        lines.append("## Education")
        for edu in data["education"]:
            lines.append(f"**{edu.get('school', '')}** - {edu.get('degree', '')}")
            lines.append(f"*{edu.get('graduation_date', '')}*")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Format resume JSON to Markdown")
    parser.add_argument("resume_file", help="Path to resume JSON file")
    parser.add_argument(
        "--format",
        default="markdown",
        help="Output format (currently only markdown supported)",
    )

    args = parser.parse_args()

    try:
        with open(args.resume_file, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)

    formatted = format_to_markdown(data)
    print(formatted)


if __name__ == "__main__":
    main()
