# Debt File YAML Schema

Standard YAML frontmatter schema for technical debt tracking files.

## Complete Schema

```yaml
---
# Required fields
id: string              # Unique identifier (format: DEBT-XXX)
title: string           # Brief descriptive title
category: string        # code | architecture | test | documentation | dependency | infrastructure
severity: string        # critical | high | medium | low
status: string          # open | in_progress | resolved | wont_fix

# Scoring
impact: integer         # 1-5 scale
effort: integer         # 1-5 scale
risk: integer           # 1-5 scale (optional, defaults to 2)
priority: string        # p0 | p1 | p2 | p3

# Metadata
created: date           # YYYY-MM-DD
updated: date           # YYYY-MM-DD (optional)
resolved: date          # YYYY-MM-DD (when status = resolved)
author: string          # Who identified this debt

# Classification
tags: array             # Searchable tags
affected_files: array   # List of affected file paths
affected_modules: array # List of affected modules/services

# Relationships
blocks: array           # Issues/features this blocks (optional)
blocked_by: array       # Issues this depends on (optional)
related: array          # Related debt items (optional)

# Resolution
assignee: string        # Who is working on this (optional)
sprint: string          # Target sprint (optional)
pr: string              # Resolution PR link (optional)
---
```

## Field Definitions

### Required Fields

#### id
Unique identifier for the debt item.

```yaml
id: DEBT-001
id: DEBT-042
id: DEBT-100
```

Format: `DEBT-[0-9]{3}` (auto-increment)

#### title
Brief, descriptive title (max 80 characters).

```yaml
# Good
title: Duplicate validation logic across controllers
title: Payment service has no error handling
title: React version 2 major versions behind

# Bad
title: Fix the code  # Too vague
title: There's a problem with how we handle user input validation across multiple controller files that should be consolidated  # Too long
```

#### category
Type of technical debt.

```yaml
category: code           # Code quality issues
category: architecture   # Structural/design issues
category: test           # Testing gaps
category: documentation  # Missing/outdated docs
category: dependency     # Package/library issues
category: infrastructure # DevOps/deployment issues
```

#### severity
Business impact level.

```yaml
severity: critical  # Security risk, data loss, revenue impact
severity: high      # Major feature blocked
severity: medium    # Development slowed
severity: low       # Minor inconvenience
```

#### status
Current state of the debt item.

```yaml
status: open         # Identified, not yet started
status: in_progress  # Being worked on
status: resolved     # Fixed and verified
status: wont_fix     # Decided not to fix (document reason)
```

### Scoring Fields

#### impact
How much this affects the team (1-5).

```yaml
impact: 5  # Critical - blocks major features
impact: 4  # High - significantly slows work
impact: 3  # Medium - noticeable friction
impact: 2  # Low - minor inconvenience
impact: 1  # Minimal - cosmetic
```

#### effort
Time to resolve (1-5).

```yaml
effort: 1  # Hours
effort: 2  # Days
effort: 3  # Week
effort: 4  # Weeks
effort: 5  # Months
```

#### priority
Calculated from impact and effort.

```yaml
priority: p0  # Do immediately (score 20-25)
priority: p1  # Do this sprint (score 12-19)
priority: p2  # Do next sprint (score 6-11)
priority: p3  # Backlog (score 1-5)
```

### Metadata Fields

#### created / updated / resolved
ISO 8601 dates.

```yaml
created: 2024-01-15
updated: 2024-01-20
resolved: 2024-02-01
```

#### tags
Searchable classification tags.

```yaml
tags: [duplication, validation, controllers]
tags: [security, authentication, critical]
tags: [performance, database, n-plus-one]
```

Common tags:
- Code: `duplication`, `complexity`, `naming`, `error-handling`
- Architecture: `coupling`, `abstraction`, `patterns`
- Test: `coverage`, `flaky`, `missing-tests`
- Security: `vulnerability`, `authentication`, `authorization`
- Performance: `n-plus-one`, `memory-leak`, `slow-query`

#### affected_files
List of files containing this debt.

```yaml
affected_files:
  - app/controllers/orders_controller.rb
  - app/controllers/users_controller.rb
  - lib/validators/email_validator.rb
```

### Relationship Fields

#### blocks
Features or issues blocked by this debt.

```yaml
blocks:
  - FEAT-123  # Can't add feature until fixed
  - BUG-456   # Bug caused by this debt
```

#### related
Related debt items.

```yaml
related:
  - DEBT-005  # Similar issue in different module
  - DEBT-012  # Root cause of this debt
```

## Example Files

### Code Debt Example

```yaml
---
id: DEBT-001
title: Duplicate email validation across 5 controllers
category: code
severity: medium
status: open
impact: 2
effort: 2
priority: p2
created: 2024-01-15
author: jsmith
tags: [duplication, validation, dry]
affected_files:
  - app/controllers/orders_controller.rb
  - app/controllers/users_controller.rb
  - app/controllers/contacts_controller.rb
  - app/controllers/subscriptions_controller.rb
  - app/controllers/leads_controller.rb
related:
  - DEBT-007
---
```

### Security Debt Example

```yaml
---
id: DEBT-002
title: SQL injection vulnerability in search endpoint
category: code
severity: critical
status: in_progress
impact: 5
effort: 1
risk: 3
priority: p0
created: 2024-01-10
updated: 2024-01-12
author: security-scan
assignee: adev
tags: [security, sql-injection, critical]
affected_files:
  - app/controllers/search_controller.rb
blocks:
  - RELEASE-2.0
---
```

### Resolved Debt Example

```yaml
---
id: DEBT-003
title: No test coverage for payment processing
category: test
severity: high
status: resolved
impact: 4
effort: 3
priority: p1
created: 2023-12-01
resolved: 2024-01-20
author: qateam
assignee: bsmith
tags: [testing, payments, critical]
affected_files:
  - app/services/payment_service.rb
pr: https://github.com/org/repo/pull/456
---
```

## Index File Schema

The `.claude/debt/INDEX.md` file summarizes all debt:

```yaml
---
last_updated: 2024-01-20
total_items: 15
open_items: 10
in_progress: 3
resolved_this_quarter: 5
metrics:
  average_resolution_days: 14
  p0_count: 1
  p1_count: 4
  p2_count: 6
  p3_count: 4
---
```

## Validation Rules

1. `id` must be unique
2. `impact`, `effort`, `risk` must be 1-5
3. `priority` should match calculated value
4. `resolved` date required when `status: resolved`
5. `affected_files` should be valid paths
6. `tags` should use consistent vocabulary
