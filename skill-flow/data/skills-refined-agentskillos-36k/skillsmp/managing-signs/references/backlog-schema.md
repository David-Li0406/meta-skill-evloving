---
title: Backlog Schema Reference
description: Complete YAML schema for learning backlog files including all fields, types, status values, and validation rules.
keywords: backlog, schema, yaml, learnings, signs, validation
skill: managing-signs
---

# Backlog Schema Reference

## File Structure

Backlog files are YAML documents stored at `.claude/learnings/backlog.yaml` in each project.

## Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | integer | Yes | Schema version (current: 1) |
| `extracted-from` | string\|null | Yes | Source session-id or sprint-id |
| `extracted-at` | string\|null | Yes | ISO 8601 extraction timestamp |
| `learnings` | array | Yes | List of learning entries |

## Learning Entry Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique kebab-case identifier |
| `status` | enum | Yes | Review status (see below) |
| `title` | string | Yes | Short human-readable description |
| `problem` | string | Yes | Multi-line problem description |
| `solution` | string | Yes | Multi-line solution/fix description |
| `target` | string | Yes | Path to target CLAUDE.md file |
| `confidence` | enum | Yes | Confidence level (see below) |
| `source` | object | No | Error source metadata |

## Status Enum Values

| Value | Description |
|-------|-------------|
| `pending` | Awaiting human review |
| `approved` | Approved for application |
| `rejected` | Rejected, will not apply |
| `applied` | Successfully applied to target |

## Confidence Levels

| Value | Criteria |
|-------|----------|
| `low` | Single occurrence, unclear pattern |
| `medium` | Multiple occurrences or clear pattern |
| `high` | Consistent pattern with verified fix |

## Source Metadata Structure

| Field | Type | Description |
|-------|------|-------------|
| `tool` | string | Tool name (Bash, Edit, etc.) |
| `command` | string | Command/operation that failed |
| `error` | string | Error message or description |

## Example

```yaml
version: 1
extracted-from: session-abc123
extracted-at: 2026-01-18T10:30:00Z

learnings:
  - id: yq-variable-quoting
    status: pending
    title: Quote Variables in yq Expressions
    problem: |
      yq commands fail silently when shell variables aren't quoted.
    solution: |
      Wrap expressions in single quotes with explicit variable expansion.
    target: scripts/CLAUDE.md
    confidence: high
    source:
      tool: Bash
      command: "yq '.phases[$IDX].status' PROGRESS.yaml"
      error: "returned empty string"
```

## Validation Rules

1. `version` must be positive integer
2. `learnings` must be array (can be empty)
3. Each learning must have all required fields
4. `status` must be one of: pending, approved, rejected, applied
5. `confidence` must be one of: low, medium, high
6. `target` path should exist in project (warning if not)
7. `id` should be unique within backlog
