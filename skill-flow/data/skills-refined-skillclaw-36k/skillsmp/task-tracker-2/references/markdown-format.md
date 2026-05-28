# Task Markdown Format

Complete specification for task files in `.claude/tasks/`.

## File Structure

Tasks are markdown files with YAML-like frontmatter:

```
---
frontmatter fields
---

# Task Title

Optional description.

## Notes

### timestamp

Note content.
```

## Frontmatter Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| status | string | yes | One of: pending, in_progress, blocked, complete, wont_do |
| created | ISO8601 | yes | Task creation timestamp |
| updated | ISO8601 | yes | Last modification timestamp |
| started | ISO8601 | no | When task was started |
| completed | ISO8601 | no | When task was completed |
| blocked_reason | string | no | Why task is blocked |
| deps | list | no | Task IDs this depends on |
| approach | string | no | Planned implementation approach |
| criteria | list | no | Acceptance criteria (what "done" means) |
| files | list | no | Relevant file paths |

## Body Structure

### Title (Required)

First H1 heading is the task title:

```markdown
# Implement user authentication
```

### Description (Optional)

Any text between the title and `## Notes` is the description:

```markdown
# Implement user authentication

Add login/logout functionality using JWT tokens.
This includes the API endpoints and frontend forms.
```

### Notes Section (Optional)

Notes are appended under `## Notes` with timestamp headers:

```markdown
## Notes

### 2026-01-06T10:30:00+00:00

Discovered we need to handle token refresh edge case.

### 2026-01-07T14:00:00+00:00

Redis cluster mode requires different client configuration.
```

## Directory Structure

```
.claude/tasks/
  NN-slug.md              # Leaf task (no children)
  NN-slug/                # Parent task (has children)
    00-index.md           # Parent's metadata
    NN-child.md           # Child tasks
```

### Naming Convention

- `NN-` prefix for ordering (01, 02, ... 99)
- `slug` is URL-safe lowercase title
- Parent directories use `00-index.md` for their metadata

### Task IDs

Task IDs are path-based, without the `.md` extension:

| Path | Task ID |
|------|---------|
| `01-auth.md` | `01-auth` |
| `01-auth/00-index.md` | `01-auth` |
| `01-auth/02-session.md` | `01-auth/02-session` |
| `01-auth/02-session/01-jwt.md` | `01-auth/02-session/01-jwt` |

## Status Values

| Status | Description |
|--------|-------------|
| `pending` | Task not yet started |
| `in_progress` | Currently being worked on |
| `blocked` | Waiting on external factor |
| `complete` | Successfully finished |
| `wont_do` | Cancelled or skipped |

## Example Files

### Leaf Task

`01-implement-auth.md`:
```markdown
---
status: pending
created: 2026-01-06T10:00:00+00:00
updated: 2026-01-06T10:00:00+00:00
approach: Use bcrypt for password hashing, JWT for session tokens
criteria:
  - Users can log in with email/password
  - Invalid credentials return 401
  - JWT token expires after 24 hours
files:
  - src/routes/auth.ts
  - src/middleware/authenticate.ts
---

# Implement user authentication

Add login/logout functionality to the application.
```

### Parent Task with Children

`01-implement-auth/00-index.md`:
```markdown
---
status: in_progress
created: 2026-01-06T10:00:00+00:00
updated: 2026-01-06T11:00:00+00:00
started: 2026-01-06T10:30:00+00:00
approach: Use bcrypt for password hashing, JWT for session tokens
criteria:
  - Users can log in with email/password
  - Invalid credentials return 401
files:
  - src/routes/auth.ts
---

# Implement user authentication

Add login/logout functionality to the application.

## Notes

### 2026-01-06T10:30:00+00:00

Need to support OAuth in addition to password auth.
```

`01-implement-auth/01-create-form.md`:
```markdown
---
status: complete
created: 2026-01-06T10:05:00+00:00
updated: 2026-01-06T10:30:00+00:00
completed: 2026-01-06T10:30:00+00:00
---

# Create login form

Build the login UI component with email and password fields.
```

`01-implement-auth/02-session.md`:
```markdown
---
status: pending
created: 2026-01-06T10:05:00+00:00
updated: 2026-01-06T10:05:00+00:00
approach: Store JWT in httpOnly cookie
criteria:
  - Cookie set on login
  - Cookie cleared on logout
---

# Add session management
```

### Task with Dependencies

`02-deploy-staging.md`:
```markdown
---
status: pending
created: 2026-01-06T10:10:00+00:00
updated: 2026-01-06T10:10:00+00:00
deps:
  - 01-implement-auth
criteria:
  - App running on staging URL
  - Health check passes
---

# Deploy to staging

Push the authenticated app to staging environment.
```

## Frontmatter Parser Notes

The frontmatter uses a simple YAML-like format (no PyYAML dependency):

- Single values: `key: value`
- Lists: `key:` followed by indented `  - item` lines
- Strings with colons should be quoted: `approach: "Use Redis: fast and reliable"`
- Empty values are omitted (not `key: null` or `key: ""`)
