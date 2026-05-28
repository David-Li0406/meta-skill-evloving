#!/usr/bin/env python3
"""
Create MD Issue Script for md-issue-writer skill

Usage:
    python create_issue.py --type "Bug" --title "Fix login timeout" --description "Users are logged out after 5 minutes" --severity "High" --status "Investigating"

Required args:
    --type: One of Bug, Feature Plan, RFC, ADR, Task, Retrospective
    --title: Concise title for the issue

Optional args:
    --description: Description text
    --severity: Critical, High, Medium, Low, N/A
    --status: Appropriate status for the type
    --author: Author name <email>
    --reviewer: Reviewer name
    --id: Short identifier
    --related: Comma-separated list of related filenames
    --milestone: Release or milestone name
"""

import argparse
import os
from datetime import datetime
from pathlib import Path
import re

def kebab_case(s):
    """Convert string to kebab-case."""
    s = re.sub(r'[^\w\s-]', '', s)  # Remove special chars except - and space
    s = re.sub(r'\s+', '-', s)  # Replace spaces with -
    return s.lower()

def get_issues_folder():
    """Determine the issues folder: _docs/issues if exists, else .docs/issues."""
    repo_root = Path.cwd()
    if (repo_root / '_docs' / 'issues').exists():
        return repo_root / '_docs' / 'issues'
    else:
        return repo_root / '.docs' / 'issues'

def get_template(type_name):
    """Get the template content for the given type."""
    templates = {
        'Bug': """---
date: {date}
type: Bug
severity: {severity}
status: {status}
{author}{reviewer}{id}{related}{milestone}
---

# {title}

## Problem
{description}

## Root Cause
[Why did it happen? Trace to origin.]

## Solution
[How was it fixed? Show code before/after.]

## Lessons Learned
- [Actionable takeaway]

## Prevention
- [ ] [Checklist item]
""",
        'Feature Plan': """---
date: {date}
type: Feature Plan
severity: {severity}
status: {status}
{author}{reviewer}{id}{related}{milestone}
---

# {title}

## Goal
{description}

## Requirements
- [ ] User Story 1
- [ ] User Story 2

## Proposed Implementation
[High-level technical approach. Components involved.]

## Risks & Considerations
- [Potential blockers or edge cases]
""",
        'RFC': """---
date: {date}
type: RFC
severity: {severity}
status: {status}
{author}{reviewer}{id}{related}{milestone}
---

# RFC: {title}

## Summary
{description}

## Motivation
[Why do we need this? What problem does it solve?]

## Detailed Design
[How will it work? API changes, data models, etc.]

## Alternatives Considered
- [Option A]: [Why rejected?]

## Unresolved Questions
- [ ] Question 1?
""",
        'ADR': """---
date: {date}
type: ADR
severity: N/A
status: Proposed
{author}{reviewer}{id}{related}{milestone}
tags:
  - architecture
  - decision
---

# ADR: {title}

## Context
{description}

## Decision
[The change that we are proposing or have agreed to.]

## Consequences
**Positive:**
- [Benefit 1]

**Negative:**
- [Trade-off 1]
""",
        'Task': """---
date: {date}
type: Task
severity: {severity}
status: {status}
{author}{reviewer}{id}{related}{milestone}
---

# Task: {title}

## Objective
{description}

## Tasks
- [ ] Step 1
- [ ] Step 2

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2

## References
- [Link to code or docs]
""",
        'Retrospective': """---
date: {date}
type: Retrospective
severity: N/A
status: Documented
{author}{reviewer}{id}{related}{milestone}
---

# Lesson: {title}

## Context
{description}

## What Went Well
- [Positive aspects or successes]

## What Didn't Go Well
- [Challenges, mistakes, or areas for improvement]

## Key Lessons Learned
- [Actionable insights and takeaways]
- [What we learned about processes, tools, or team dynamics]

## Actions Taken
- [Immediate fixes or changes implemented]

## Future Prevention / Improvements
- [ ] [Checklist item for preventing recurrence]
- [ ] [Recommendations for similar situations]
"""
    }
    return templates.get(type_name, '')

def format_optional(field, value):
    """Format optional YAML field."""
    if value:
        return f'{field}: {value}\n'
    return ''

def main():
    parser = argparse.ArgumentParser(description='Create a new issue document.')
    parser.add_argument('--type', required=True, choices=['Bug', 'Feature Plan', 'RFC', 'ADR', 'Task', 'Retrospective'], help='Type of issue')
    parser.add_argument('--title', required=True, help='Title of the issue')
    parser.add_argument('--description', default='', help='Description')
    parser.add_argument('--severity', default='Medium', choices=['Critical', 'High', 'Medium', 'Low', 'N/A'], help='Severity')
    parser.add_argument('--status', default='Draft', help='Status')
    parser.add_argument('--author', help='Author name <email>')
    parser.add_argument('--reviewer', help='Reviewer name')
    parser.add_argument('--id', help='Short identifier')
    parser.add_argument('--related', help='Comma-separated related filenames')
    parser.add_argument('--milestone', help='Milestone name')

    args = parser.parse_args()

    # Get current date
    today = datetime.now().strftime('%Y-%m-%d')
    yy = datetime.now().strftime('%y%m%d')

    # Kebab case title
    kebab_title = kebab_case(args.title)

    # Filename
    filename = f'{yy}_{kebab_title}.md'

    # Issues folder
    issues_folder = get_issues_folder()
    issues_folder.mkdir(parents=True, exist_ok=True)

    filepath = issues_folder / filename

    # Format optional fields
    author = format_optional('author', args.author)
    reviewer = format_optional('reviewer', args.reviewer)
    id_field = format_optional('id', args.id)
    milestone = format_optional('milestone', args.milestone)
    if args.related:
        related_list = '\n'.join(f'  - {r.strip()}' for r in args.related.split(','))
        related = f'related:\n{related_list}\n'
    else:
        related = ''

    # Get template
    template = get_template(args.type)
    if not template:
        print(f"Unknown type: {args.type}")
        return

    # Fill template
    content = template.format(
        date=today,
        severity=args.severity,
        status=args.status,
        author=author,
        reviewer=reviewer,
        id=id_field,
        related=related,
        milestone=milestone,
        title=args.title,
        description=args.description
    )

    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Created issue document: {filepath}")

    # Optionally run metadata extraction
    script_dir = Path(__file__).parent
    script = script_dir / 'extract_issue_metadata.py'
    if script.exists():
        print("Running metadata extraction...")
        os.system(f'python {script}')

if __name__ == "__main__":
    main()