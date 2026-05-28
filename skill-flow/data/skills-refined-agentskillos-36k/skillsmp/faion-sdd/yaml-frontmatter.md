# YAML Frontmatter Standards

Standard for metadata in all SDD documentation.

---

## Overview

All SDD documents use YAML frontmatter at the top of the file:

```yaml
---
key: value
list: [item1, item2]
---

# Document Title

Content starts here...
```

---

## Document Types & Required Fields

### 1. Constitution

```yaml
---
type: constitution
version: "7.8.0"
status: active
created: 2026-01-12
updated: 2026-01-19
author: Ruslan Faion
domain: faion.net
---
```

| Field | Required | Description |
|-------|----------|-------------|
| type | yes | Always `constitution` |
| version | yes | Semantic version (MAJOR.MINOR.PATCH) |
| status | yes | `active`, `draft`, `archived` |
| created | yes | ISO date (YYYY-MM-DD) |
| updated | yes | ISO date |
| author | yes | Primary author |
| domain | no | Project domain |

---

### 2. Roadmap

```yaml
---
type: roadmap
version: "2.7.0"
status: active
created: 2026-01-12
updated: 2026-01-19
---
```

| Field | Required | Description |
|-------|----------|-------------|
| type | yes | Always `roadmap` |
| version | yes | Semantic version |
| status | yes | `active`, `draft`, `archived` |
| created | yes | ISO date |
| updated | yes | ISO date |

---

### 3. Feature Specification (spec.md)

```yaml
---
type: spec
feature_id: "02-landing-page"
version: "3.1.0"
status: backlog
priority: P0
created: 2026-01-16
updated: 2026-01-17
depends_on: [01-framework-content]
---
```

| Field | Required | Description |
|-------|----------|-------------|
| type | yes | Always `spec` |
| feature_id | yes | Feature folder name (NN-name) |
| version | yes | Semantic version |
| status | yes | `backlog`, `todo`, `in-progress`, `done` |
| priority | yes | `P0` (blocker), `P1` (critical), `P2` (nice-to-have) |
| created | yes | ISO date |
| updated | yes | ISO date |
| depends_on | no | List of feature IDs this depends on |

---

### 4. Design Document (design.md)

```yaml
---
type: design
feature_id: "02-landing-page"
version: "1.0.0"
status: draft
created: 2026-01-17
updated: 2026-01-17
spec_version: "3.1.0"
---
```

| Field | Required | Description |
|-------|----------|-------------|
| type | yes | Always `design` |
| feature_id | yes | Feature folder name |
| version | yes | Semantic version |
| status | yes | `draft`, `review`, `approved` |
| created | yes | ISO date |
| updated | yes | ISO date |
| spec_version | no | Version of spec this design implements |

---

### 5. Implementation Plan (implementation-plan.md)

```yaml
---
type: implementation-plan
feature_id: "02-landing-page"
version: "1.0.0"
status: draft
created: 2026-01-17
updated: 2026-01-17
design_version: "1.0.0"
total_tasks: 12
---
```

| Field | Required | Description |
|-------|----------|-------------|
| type | yes | Always `implementation-plan` |
| feature_id | yes | Feature folder name |
| version | yes | Semantic version |
| status | yes | `draft`, `approved`, `in-progress`, `done` |
| created | yes | ISO date |
| updated | yes | ISO date |
| design_version | no | Version of design this implements |
| total_tasks | no | Number of tasks in plan |

---

### 6. Task (TASK_NNN_name.md)

```yaml
---
type: task
task_id: "TASK_001"
feature_id: "05-paywall-system"
status: backlog
priority: P0
created: 2026-01-17
estimated_hours: 8
depends_on: []
blocks: []
---
```

| Field | Required | Description |
|-------|----------|-------------|
| type | yes | Always `task` |
| task_id | yes | TASK_NNN format |
| feature_id | yes | Parent feature |
| status | yes | `backlog`, `todo`, `in-progress`, `done`, `blocked` |
| priority | yes | `P0`, `P1`, `P2` |
| created | yes | ISO date |
| estimated_hours | no | Time estimate |
| depends_on | no | List of task IDs this depends on |
| blocks | no | List of task IDs blocked by this |

---

### 7. Product Documentation

```yaml
---
type: product-doc
doc_type: market-research
version: "1.0.0"
status: final
created: 2026-01-17
updated: 2026-01-19
---
```

| Field | Required | Description |
|-------|----------|-------------|
| type | yes | Always `product-doc` |
| doc_type | yes | `market-research`, `content-strategy`, `competitive-analysis`, `pricing-research`, `user-personas`, `gtm-manifest` |
| version | yes | Semantic version |
| status | yes | `draft`, `review`, `final` |
| created | yes | ISO date |
| updated | yes | ISO date |

---

### 8. GTM Manifest Part

```yaml
---
type: gtm-part
part_number: 1
version: "1.0.0"
status: final
created: 2026-01-17
---
```

| Field | Required | Description |
|-------|----------|-------------|
| type | yes | Always `gtm-part` |
| part_number | yes | Sequential number (1-12) |
| version | yes | Semantic version |
| status | yes | `draft`, `final` |
| created | yes | ISO date |

---

### 9. Onboarding Brief

```yaml
---
type: brief
brief_type: onboarding
target_role: UX/UI Designer
version: "3.0.0"
status: active
created: 2026-01-19
updated: 2026-01-19
language: uk
---
```

| Field | Required | Description |
|-------|----------|-------------|
| type | yes | Always `brief` |
| brief_type | yes | `onboarding`, `technical`, `product` |
| target_role | yes | Target audience |
| version | yes | Semantic version |
| status | yes | `draft`, `active`, `archived` |
| created | yes | ISO date |
| updated | yes | ISO date |
| language | no | `en`, `uk` |

---

### 10. Methodology

```yaml
---
type: methodology
id: sdd-workflow-overview
title: SDD Workflow Overview
category: SDD
difficulty: beginner
tags: [sdd, workflow, specification]
read_time_minutes: 8
---
```

| Field | Required | Description |
|-------|----------|-------------|
| type | yes | Always `methodology` |
| id | yes | Semantic name (kebab-case) |
| title | yes | Human-readable title |
| category | yes | Domain category |
| difficulty | yes | `beginner`, `intermediate`, `advanced` |
| tags | no | List of tags |
| read_time_minutes | no | Estimated read time |

---

## Status Values

### Document Status

| Status | Description |
|--------|-------------|
| `draft` | Work in progress |
| `review` | Under review |
| `approved` | Approved, ready for use |
| `active` | Currently in use |
| `final` | Finalized, no changes expected |
| `archived` | No longer active |

### Feature/Task Status (Lifecycle)

| Status | Description |
|--------|-------------|
| `backlog` | Not yet scheduled |
| `todo` | Scheduled for work |
| `in-progress` | Currently being worked on |
| `done` | Completed |
| `blocked` | Waiting on dependency |

---

## Priority Values

| Priority | Meaning | Use Case |
|----------|---------|----------|
| `P0` | Blocker | Must be done first, blocks other work |
| `P1` | Critical | Important for MLP, high business value |
| `P2` | Nice-to-have | Can be deferred, lower priority |

---

## Version Format

Use semantic versioning: `MAJOR.MINOR.PATCH`

| Change Type | When to Increment |
|-------------|-------------------|
| MAJOR | Breaking changes, major rewrites |
| MINOR | New sections, significant updates |
| PATCH | Fixes, small edits, typos |

**Examples:**
- `1.0.0` → Initial version
- `1.1.0` → Added new section
- `1.1.1` → Fixed typo
- `2.0.0` → Complete rewrite

---

## Date Format

Always use ISO 8601: `YYYY-MM-DD`

**Examples:**
- `2026-01-19`
- `2026-12-31`

---

## Parsing YAML Frontmatter

**Python:**
```python
import yaml
import re

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from markdown."""
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if match:
        frontmatter = yaml.safe_load(match.group(1))
        body = match.group(2)
        return frontmatter, body
    return {}, content
```

**JavaScript:**
```javascript
function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (match) {
    const frontmatter = jsyaml.load(match[1]);
    const body = match[2];
    return { frontmatter, body };
  }
  return { frontmatter: {}, body: content };
}
```

---

## Migration from Old Format

**Before (inline metadata):**
```markdown
# Document Title

## Metadata
- **Version:** 1.0
- **Status:** Draft
- **Created:** 2026-01-19
```

**After (YAML frontmatter):**
```yaml
---
type: spec
version: "1.0.0"
status: draft
created: 2026-01-19
---

# Document Title
```

**Note:** Remove the `## Metadata` section after adding YAML frontmatter.

---

*Reference v1.0.0 - 2026-01-19*
