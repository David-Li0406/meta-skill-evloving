---
name: file-todos
description: Use this skill when managing a file-based todo tracking system for code review feedback, technical debt, feature requests, and work items.
---

# File-Based Todo Tracking Skill

## Overview

The `todos/` directory contains a file-based tracking system for managing code review feedback, technical debt, feature requests, and work items. Each todo is a markdown file with YAML frontmatter and structured sections.

This skill should be used when:
- Creating new todos from findings or feedback
- Managing todo lifecycle (pending → ready → complete)
- Triaging pending items for approval
- Checking or managing dependencies
- Converting PR comments or code findings into tracked work
- Updating work logs during todo execution

## File Naming Convention

Todo files follow this naming pattern:

```
{issue_id}-{status}-{priority}-{description}.md
```

**Components:**
- **issue_id**: Sequential number (001, 002, 003...) - never reused
- **status**: `pending` (needs triage), `ready` (approved), `complete` (done)
- **priority**: `p1` (critical), `p2` (important), `p3` (nice-to-have)
- **description**: kebab-case, brief description

**Examples:**
```
001-pending-p1-mailer-test.md
002-ready-p1-fix-n-plus-1.md
005-complete-p2-refactor-csv.md
```

## File Structure

Each todo is a markdown file with YAML frontmatter and structured sections. Use the template at `assets/todo-template.md` as a starting point when creating new todos.

**Required sections:**
- **Problem Statement** - What is broken, missing, or needs improvement?
- **Findings** - Investigation results, root cause, key discoveries
- **Proposed Solutions** - Multiple options with pros/cons, effort, risk
- **Recommended Action** - Clear plan (filled during triage)
- **Acceptance Criteria** - Testable checklist items
- **Work Log** - Chronological record with date, actions, learnings

**Optional sections:**
- **Technical Details** - Affected files, related components, DB changes
- **Resources** - Links to errors, tests, PRs, documentation
- **Notes** - Additional context or decisions

**YAML frontmatter fields:**
```yaml
---
status: ready              # pending | ready | complete
priority: p1              # p1 | p2 | p3
issue_id: "002"
tags: [rails, performance, database]
dependencies: ["001"]     # Issue IDs this is blocked by
---
```