---
type: directory-documentation
directory: .claude/skills/agentdb-state-manager/ARCHIVED
title: agentdb-state-manager/ARCHIVED
sibling_claude: CLAUDE.md
parent: ../README.md
children: []
---

# agentdb-state-manager/ARCHIVED

Archived files from agentdb-state-manager skill

## Purpose

This directory contains deprecated files from the AgentDB State Manager skill that have
been superseded by newer versions. Files are archived (not deleted) to preserve history
and allow comparison with current implementations.

## Contents

Currently empty - no files have been archived yet.

## Archiving Process

When files are deprecated:

```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  TODO_*.md "description" file1.py file2.md
```

This creates a timestamped ZIP archive in this directory.

## Related Documentation

- **[../SKILL.md](../SKILL.md)** - Current skill documentation
- **[../CLAUDE.md](../CLAUDE.md)** - Current Claude Code context
