# GitHub Labels for LucidData

Complete label taxonomy with descriptions, colors, and usage guidelines.

## Type Labels (Primary Classification)

| Label | Color | Description | Usage |
|-------|-------|-------------|-------|
| `bug` | `#d73a4a` (red) | Software defect | Use for incorrect behavior, crashes, errors |
| `enhancement` | `#a2eeef` (blue) | New feature or improvement | Use for new functionality requests |
| `security` | `#d93f0b` (orange-red) | Security issue | Use for vulnerabilities, security improvements |
| `documentation` | `#0075ca` (dark blue) | Documentation update | Use for README, docs, comments |
| `testing` | `#0e8a16` (green) | Test-related | Use for test failures, coverage improvements |
| `question` | `#d876e3` (purple) | Need clarification | Use when seeking information |

## Component Labels (What's Affected)

| Label | Color | Description |
|-------|-------|-------------|
| `encryption` | `#fbca04` (yellow) | AES-256-GCM encryption/decryption |
| `database` | `#c5def5` (light blue) | Prisma, PostgreSQL, migrations |
| `auth` | `#ff9800` (orange) | Supabase authentication |
| `consent` | `#7057ff` (purple) | Consent management system |
| `audit-log` | `#bfd4f2` (light blue) | Audit trail and hash chains |
| `vault` | `#006b75` (teal) | Vault data management |
| `ui` | `#e99695` (pink) | User interface, React components |
| `api` | `#0052cc` (blue) | API routes, backend logic |

## Priority Labels

| Label | Color | Description | SLA |
|-------|-------|-------------|-----|
| `critical` | `#b60205` (dark red) | Blocking issue | Fix ASAP (hours) |
| `high` | `#d93f0b` (orange) | Important | Fix within days |
| `medium` | `#fbca04` (yellow) | Standard priority | Fix within weeks |
| `low` | `#0e8a16` (green) | Nice to have | Backlog |

## Status Labels

| Label | Color | Description |
|-------|-------|-------------|
| `needs-triage` | `#ffffff` (white) | Needs initial review |
| `needs-info` | `#d4c5f9` (lavender) | Waiting for more information |
| `in-progress` | `#1d76db` (blue) | Currently being worked on |
| `blocked` | `#e4e669` (yellow) | Blocked by dependency |
| `ready-for-review` | `#0e8a16` (green) | Ready for PR review |
| `wontfix` | `#cfd3d7` (gray) | Will not be fixed |
| `duplicate` | `#cfd3d7` (gray) | Duplicate of another issue |

## Special Labels

| Label | Color | Description |
|-------|-------|-------------|
| `good first issue` | `#7057ff` (purple) | Good for newcomers |
| `help wanted` | `#008672` (teal) | Community contributions welcome |
| `breaking-change` | `#b60205` (dark red) | Will break existing functionality |
| `performance` | `#fef2c0` (cream) | Performance optimization |
| `accessibility` | `#0052cc` (blue) | WCAG compliance, a11y |
| `ux` | `#e99695` (pink) | User experience improvement |

## Label Combination Guidelines

### Bug Reports
Minimum labels:
- `bug`
- Component label (e.g., `encryption`, `database`)
- Priority label (e.g., `high`, `critical`)

Example: `bug`, `encryption`, `critical`

### Feature Requests
Minimum labels:
- `enhancement`
- Component label
- Priority label (optional)

Example: `enhancement`, `consent`, `medium`

### Security Issues
Minimum labels:
- `security`
- Priority label (usually `critical` or `high`)
- Component label (if known)

Example: `security`, `critical`, `auth`

### Test Failures
Minimum labels:
- `testing`
- Component label
- `critical` if blocking CI/CD

Example: `testing`, `vault`, `high`

## Label Management

### Creating Labels (GitHub CLI)

```bash
# Create type labels
gh label create "bug" --color "d73a4a" --description "Software defect"
gh label create "enhancement" --color "a2eeef" --description "New feature"
gh label create "security" --color "d93f0b" --description "Security issue"

# Create component labels
gh label create "encryption" --color "fbca04" --description "Encryption/decryption"
gh label create "database" --color "c5def5" --description "Prisma, PostgreSQL"

# Create priority labels
gh label create "critical" --color "b60205" --description "Blocking issue"
gh label create "high" --color "d93f0b" --description "Important"
```

### Label Colors

Use these hex colors for consistency:
- Red (`#d73a4a`, `#b60205`): Bugs, critical priority
- Orange (`#d93f0b`, `#ff9800`): Security, auth
- Yellow (`#fbca04`): Encryption, medium priority
- Green (`#0e8a16`): Testing, low priority
- Blue (`#0075ca`, `#0052cc`): Documentation, API
- Purple (`#7057ff`): Consent, good first issue
- Teal (`#006b75`, `#008672`): Vault, help wanted
- Gray (`#cfd3d7`): Wontfix, duplicate

## Best Practices

1. **Use 2-3 labels minimum**: Type + Component + Priority
2. **Update labels as status changes**: Add `in-progress` when starting work
3. **Remove `needs-triage` after review**: Replace with priority/status labels
4. **Use `duplicate` + link**: Reference original issue when marking duplicate
5. **Apply `breaking-change` early**: Warn users about API/schema changes
6. **Tag `good first issue`**: Help new contributors find starting points

---

**For more information:**
- [Issue Templates](issue-templates.md)
- [Main Skill Documentation](../SKILL.md)
