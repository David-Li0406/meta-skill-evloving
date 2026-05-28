---
name: swe-workflow-research
version: 1.0.0
description: Code exploration and research without making changes
workflow:
  aware: true
  callable_from:
    - WF_CLASSIFY
    - WF_CONTINUE
    - WF_START
  default_return: WF_DETECT_REQ
  supports_standalone: true
  auto_transition: true
---

# Workflow Research Skill

Explore and analyze codebase without making any changes.

## Purpose

- Understand code structure and patterns
- Find relevant files and functions
- Analyze dependencies and relationships
- Document findings for later use

## Actions

1. **Explore codebase** using Serena symbolic tools
2. **Search for patterns** using grep/glob
3. **Read relevant files** to understand implementation
4. **Document findings** in Skill Return section

## Restrictions

- **NO edits allowed** - read-only exploration
- **NO file creation** - documentation only
- Must update WORKING_MEMORY with findings

## Skill Return Format

```markdown
## Skill Return
- **Skill**: swe-workflow-research
- **Status**: [success|success_with_findings|needs_clarification]
- **Findings Summary**: [2-3 sentences describing what was found]
- **Artifacts**: [list of relevant files, patterns discovered]
- **Next Step Hint**: WF_DETECT_REQ
```

## Exit

Output: `> **Skill /swe-workflow-research complete** - returning to WF_DETECT_REQ`
