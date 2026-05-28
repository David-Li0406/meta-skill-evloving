# Capturing Request-Logs

Workflows for capturing bugs, enhancements, ideas, and technical debt to request-log markdown files.

## When to Use

- **Bug Discovery**: Capture bugs found during code review, testing, or debugging
- **Enhancement Ideas**: Log feature requests or improvements while implementing related work
- **Technical Debt**: Document refactoring needs, code smells, or architectural issues
- **Research Findings**: Record investigation results, API limitations, or integration gotchas
- **Multiple Related Items**: Batch capture several findings from a single work session

## When NOT to Use

- Creating general documentation (use documentation agents)
- Writing code comments (inline comments are better)
- Project planning (use PRD/design-spec workflows)
- Immediate fixes (fix and document separately if needed)

---

## Quick Capture (Single Item)

Most common workflow - capture one item during development:

```bash
echo '{
  "project": "PROJECT_NAME",
  "items": [{
    "title": "Add validation for empty tags array",
    "type": "bug",
    "domain": "core",
    "context": "serializer",
    "priority": "medium",
    "status": "triage",
    "tags": ["validation", "serializer"],
    "notes": "Problem: Empty tags array causes invalid frontmatter. Goal: Validate before write."
  }]
}' | meatycapture log create --json
```

**Output**:

```json
{
  "success": true,
  "doc_id": "REQ-20251229-project-name",
  "doc_path": "~/.meatycapture/project-name/REQ-20251229-project-name.md",
  "items_created": [
    {
      "item_id": "REQ-20251229-project-name-01",
      "title": "Add validation for empty tags array"
    }
  ]
}
```

**Minimum Required Fields**: `project`, `title`, `type`, `domain`

---

## Batch Capture (Multiple Items)

Capture multiple related items in a single document:

```bash
cat > /tmp/findings.json <<'EOF'
{
  "project": "PROJECT_NAME",
  "title": "Security Audit Findings - 2025-12-29",
  "items": [
    {
      "title": "Sanitize user input in project names",
      "type": "bug",
      "domain": "core",
      "context": "validation",
      "priority": "critical",
      "status": "triage",
      "tags": ["security", "input-validation"],
      "notes": "Problem: Project names not sanitized. Goal: Add validation regex."
    },
    {
      "title": "Add file permission checks before write",
      "type": "enhancement",
      "domain": "adapters",
      "context": "fs-local",
      "priority": "high",
      "status": "backlog",
      "tags": ["security", "file-io"],
      "notes": "Goal: Verify write permissions before operations."
    },
    {
      "title": "Document security best practices",
      "type": "task",
      "domain": "docs",
      "priority": "medium",
      "status": "backlog",
      "tags": ["security", "documentation"],
      "notes": "Goal: Create security.md with guidelines."
    }
  ]
}
EOF

meatycapture log create /tmp/findings.json --json
```

**Best Practice**: Use batch capture for 3+ related issues (e.g., audit findings, code review notes).

---

## Append to Existing Document

Add items to an existing request-log:

```bash
# Get existing doc path
DOC_PATH=$(meatycapture log list PROJECT_NAME --json | jq -r '.docs[0].path')

# Append new item
echo '{
  "project": "PROJECT_NAME",
  "items": [{
    "title": "Performance optimization for large documents",
    "type": "enhancement",
    "domain": "core",
    "priority": "medium",
    "tags": ["performance"],
    "notes": "Goal: Optimize parsing for docs with 100+ items."
  }]
}' | meatycapture log append "$DOC_PATH" - --json
```

**Note**: The `project` field must match the existing document's project.

---

## Search Before Capture

Avoid duplicates by checking existing logs:

```bash
# Search for similar items
meatycapture log search "tag aggregation" PROJECT_NAME --json

# If found, reference in notes
# "Related to REQ-20251228-project-01. Extends to handle Unicode."
```

See `./viewing-logs.md` for detailed search patterns.

---

## Field Reference

| Field | Required | Valid Values | Default |
|-------|----------|--------------|---------|
| `project` | Yes | Project slug from config | - |
| `title` | Yes | String (max 200 chars) | - |
| `type` | Yes | `enhancement`, `bug`, `idea`, `task`, `question` | - |
| `domain` | Yes | `web`, `api`, `cli`, `core`, `mobile`, `docs`, etc. | - |
| `context` | No | String (module/component) | `""` |
| `priority` | No | `low`, `medium`, `high`, `critical` | `medium` |
| `status` | No | `triage`, `backlog`, `planned`, `in-progress`, `done`, `wontfix` | `triage` |
| `tags` | No | Array of strings | `[]` |
| `notes` | No | Markdown text | `""` |

See `./references/field-options.md` for complete field catalog.

---

## Notes Best Practices

Use the Problem/Goal format:

**Good**:
```
Problem: Validation logic duplicated across 3 components.
Goal: Extract to shared validator utility with unit tests.
```

**Poor**:
```
Need to fix validation stuff.
```

**With Context**:
```
Problem: Tag aggregation fails on Unicode characters.
Goal: Use locale-aware sorting for tag lists.

Context:
- Discovered during i18n testing
- Related to REQ-20251228-project-03
- Affects web and cli domains
```

---

## Priority Guidelines

| Priority | Use For |
|----------|---------|
| `critical` | Security vulnerabilities, data corruption, crashes |
| `high` | User-facing bugs, broken features |
| `medium` | Enhancements, minor bugs, technical debt |
| `low` | Nice-to-haves, polish, future ideas |

---

## Tagging Conventions

- Use lowercase, hyphenated tags: `error-handling`, `input-validation`
- Include domain tags: `core`, `web`, `cli`, `api`
- Add context tags: `security`, `performance`, `ux`, `dx`
- Reference related areas: `testing`, `documentation`

---

## CLI Commands Reference

| Command | Purpose |
|---------|---------|
| `meatycapture log create [file] --json` | Create new document |
| `meatycapture log append <doc> [file] --json` | Append to existing |
| `meatycapture log note add <doc> <item> -c "text"` | Add note to item |
| `meatycapture log item update <doc> <item> [options]` | Update item fields |
| `meatycapture create [file] --json` | Alias for log create |
| `meatycapture append <doc> [file] --json` | Alias for log append |

**Stdin Support**: Use `-` or omit file argument to read from stdin.

**Output Formats**: `--json`, `--yaml`, `--csv`, `--table`

**Update Options**: `--status`, `--priority`, `--type`, `--title`, `--tags`, `--add-tags`, `--remove-tags`, `--domain`, `--context`

---

## Templates

Single item: `./templates/quick-capture.json`

```json
{
  "project": "PROJECT_NAME",
  "items": [{
    "title": "Item title here",
    "type": "bug",
    "domain": "core",
    "priority": "medium",
    "status": "triage",
    "tags": [],
    "notes": "Problem: [Describe the issue]\nGoal: [Desired outcome]"
  }]
}
```

Batch: `./templates/batch-capture.json`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| JSON parse error | Validate: `echo "$JSON" \| jq .` |
| Project not found | List: `meatycapture project list --json` |
| Path not writable | Check: `stat ~/.meatycapture/` |
| Doc not found | Use `create` instead of `append` |

See `./references/troubleshooting.md` for detailed solutions.
