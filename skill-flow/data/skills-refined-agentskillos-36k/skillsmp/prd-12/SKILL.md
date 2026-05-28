---
name: prd
description: Create comprehensive Product Requirements Documents (PRDs)
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---

# AG4ONE PRD Skill

## Overview

This skill helps create comprehensive Product Requirements Documents (PRDs) for AG4ONE autonomous development cycles.

## Usage

Load this skill and create a PRD for your feature:

```
Load ag4one PRD skill and create PRD for [your feature description]
```

## What it does

1. **Gathers requirements** through clarifying questions
2. **Structures user stories** in AG4ONE-compatible JSON format
3. **Defines acceptance criteria** with testing requirements
4. **Sets priorities** for implementation order
5. **Saves output** to `prd-[feature-name].json` ready for Ralph loop

## PRD Structure

The generated PRD includes:
- **Project metadata** (name, branch, description)
- **User stories** with IDs, titles, descriptions
- **Acceptance criteria** for each story
- **Priority levels** for implementation order
- **AG4ONE integration** considerations

## Best Practices

- **Small, focused stories** - Each story should fit in one iteration
- **Clear acceptance criteria** - Testable and verifiable outcomes
- **Priority ordering** - Dependencies and importance considered
- **AG4ONE compliance** - Works with Ralph loop system

## Integration

After creating PRD:
1. Copy to `scripts/ag4one/prd.json`
2. Run `./scripts/ag4one/ag4one-loop.sh`
3. AG4ONE Ralph loop will implement stories automatically

## Example Output

```json
{
  "project": "TaskPriority",
  "branchName": "ag4one/task-priority", 
  "description": "Task priority system with AG4ONE workflow",
  "userStories": [
    {
      "id": "US-001",
      "title": "Database schema",
      "description": "Add priority field to tasks table",
      "acceptanceCriteria": [
        "Migration runs successfully",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false
    }
  ]
}
```

---

**AG4ONE PRD Skill** - Structured requirements for autonomous development.