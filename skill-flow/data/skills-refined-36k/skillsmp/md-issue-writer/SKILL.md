---
name: md-issue-writer
description: Skill for creating and drafting markdown-based issue documents in the specified format, including bugs, features, RFCs, ADRs, tasks, retrospectives, etc. Use when you need to document software issues, features, decisions, or work items in .docs/issues/ or _docs/issues/ folders. This is distinct from the beads issue tracker system.
---

# MD Issue Writer

## Overview

This skill enables the creation of concise, one-page technical documents for software issues, features, decisions, and work items, following a standardized YAML frontmatter and markdown structure.

## Workflow

1. Determine the type of document needed (Bug, Feature Plan, RFC, ADR, Task, Retrospective).
2. Gather required information (title, description, status, etc.).
3. Use the provided script to generate the document file in the appropriate folder.
4. Optionally run the metadata extraction script to update the index.

## Usage

Run the script with parameters to create a new issue document:

```bash
python scripts/create_issue.py --type "Bug" --title "Fix login timeout" --description "Users are logged out after 5 minutes" --severity "High"
```

To extract metadata and generate an index of all issues:

```bash
python scripts/extract_issue_metadata.py
```

See references/templates.md for detailed template structures.

## Resources

### scripts/
- `create_issue.py`: Script to generate issue documents based on templates.
- `extract_issue_metadata.py`: Python script to extract metadata from issue files and generate an index.

### references/
- `templates.md`: Detailed templates for each issue type.
