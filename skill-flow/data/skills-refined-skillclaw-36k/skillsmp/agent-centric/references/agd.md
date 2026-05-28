# AGD Reference

Technical specifications for AGD (Agent-centric Governance Decision) files.

## Frontmatter Fields

| Field          | Required | Description                                        |
| -------------- | -------- | -------------------------------------------------- |
| `title`        | Yes      | Decision title                                     |
| `description`  | Yes      | Brief description                                  |
| `tags`         | No       | Comma-separated tags (must be in config.json tags) |
| `obsoleted_by` | No       | AGD number(s) that obsolete this decision          |
| `updated_by`   | No       | AGD number(s) that update this decision            |
| `updates`      | No       | AGD number(s) this decision updates                |
| `obsoletes`    | No       | AGD number(s) this decision obsoletes              |

## Relationship Semantics

- **updates**: Extends or modifies, original decision still partially valid
- **obsoletes**: Completely replaces, original decision no longer valid

## Assigning AGD Numbers

Find the next available number:

```bash
find "$CLAUDE_PROJECT_DIR/.agents/decisions/" -name "AGD-*" | sed 's/.*AGD-\([0-9]*\).*/\1/' | sort -n | tail -1
```

Then increment by 1. If no files exist, start with AGD-001.

## Referencing in Code

When implementing a decision, reference the AGD number in comments:

```python
# Implementation follows AGD-001
class PostgresRepository:
    ...
```

```typescript
// See AGD-002 for architecture rationale
export class UserService {
    ...
}
```
