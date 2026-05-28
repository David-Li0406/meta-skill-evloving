# YAML Frontmatter Schemas

All workspace files require YAML frontmatter with specific fields per category.

## Common Fields (All Categories)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Document title (human readable) |
| category | enum | Yes | plan, architecture, example, research, analysis |
| created | date | Yes | Creation date (YYYY-MM-DD) |
| updated | date | Yes | Last update date (YYYY-MM-DD) |
| author | string | Yes | "Claude" or human name |
| tags | array | No | Searchable keywords (lowercase, hyphenated) |

---

## Plan-Specific Fields

| Field | Type | Required | Values |
|-------|------|----------|--------|
| status | enum | Yes | draft, in-progress, approved, implemented, superseded |
| supersedes | array | No | Paths to plans this replaces |
| superseded_by | array | No | Paths to plans that replace this |

**Example:**
```yaml
---
title: User Authentication Migration
category: plan
status: draft
created: 2025-01-07
updated: 2025-01-07
author: Claude
tags: [auth, migration, security]
supersedes: []
superseded_by: []
---
```

---

## Architecture-Specific Fields

| Field | Type | Required | Values |
|-------|------|----------|--------|
| status | enum | Yes | proposed, accepted, deprecated, superseded |
| adr_number | integer | No | Sequential ADR number |

**Example:**
```yaml
---
title: Event Sourcing for Audit Logs
category: architecture
status: proposed
created: 2025-01-07
updated: 2025-01-07
author: Claude
tags: [event-sourcing, audit, architecture]
adr_number: 42
---
```

---

## Example-Specific Fields

| Field | Type | Required | Values |
|-------|------|----------|--------|
| language | string | Yes | ruby, python, typescript, javascript, go, rust, etc. |

**Example:**
```yaml
---
title: Pagination with Cursor Pattern
category: example
created: 2025-01-07
updated: 2025-01-07
author: Claude
tags: [pagination, api, patterns]
language: ruby
---
```

---

## Research-Specific Fields

| Field | Type | Required | Values |
|-------|------|----------|--------|
| status | enum | Yes | in-progress, complete |
| sources | array | No | URLs to external sources consulted |

**Example:**
```yaml
---
title: Authentication Library Comparison
category: research
status: complete
created: 2025-01-07
updated: 2025-01-07
author: Claude
tags: [auth, libraries, comparison]
sources:
  - https://docs.devise.com
  - https://github.com/doorkeeper-gem/doorkeeper
---
```

---

## Analysis-Specific Fields

| Field | Type | Required | Values |
|-------|------|----------|--------|
| type | enum | Yes | code, performance, security, dependency, other |
| status | enum | Yes | in-progress, complete |
| scope | string | Yes | Files/directories analyzed |

**Example:**
```yaml
---
title: N+1 Query Audit - User Dashboard
category: analysis
type: performance
status: complete
created: 2025-01-07
updated: 2025-01-07
author: Claude
tags: [n-plus-one, performance, database]
scope: app/controllers/dashboards_controller.rb, app/models/user.rb
---
```

---

## INDEX-Specific Fields

INDEX.md files use a simpler schema:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | "{Category} Index" |
| category | string | Yes | "index" |
| updated | date | Yes | Last update date |
| file_count | integer | Yes | Number of files in category |

**Example:**
```yaml
---
title: Plans Index
category: index
updated: 2025-01-07
file_count: 5
---
```

---

## Validation Rules

1. **Required fields must be present** - Missing required fields block file creation
2. **Enum values must match exactly** - Invalid status/type values block file creation
3. **Dates must be valid** - Format: YYYY-MM-DD
4. **Tags must be lowercase and hyphenated** - e.g., `api-design` not `API Design`
5. **Arrays can be empty** - `tags: []` is valid, missing `tags` is also valid
