# SPECLAN Entity Field Reference

Complete YAML frontmatter field reference for all SPECLAN entity types.

## Common Fields (All Entities)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Entity ID in type-specific format |
| `type` | string | Yes | Entity type identifier |
| `title` | string | Yes | Human-readable title |
| `status` | string | Yes | Current lifecycle status |
| `owner` | string | Yes | Responsible team/person |
| `created` | ISO-8601 | Yes | Creation timestamp |
| `updated` | ISO-8601 | Yes | Last modification timestamp |
| `tags` | string[] | No | Classification tags |

### Status Values

```
draft | review | approved | in-development | under-test | released | deprecated
```

### Type Values

```
goal | feature | requirement | scenario | acceptanceCriterion | test | template | changeRequest
```

---

## Goal (G-###)

Strategic objectives that features contribute to achieving.

### Goal-Specific Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `contributors` | FeatureId[] | No | Features contributing to this goal |
| `metrics` | Metric[] | No | Success measurement criteria |

### Metric Object

```yaml
metrics:
  - name: "Inventory Management Efficiency"
    target: "60% reduction in manual tasks"
    unit: "percent"
```

### Example Goal

```yaml
---
id: G-292
type: goal
title: Comprehensive Pet Retail Operations
status: draft
owner: Store Owner
created: '2025-12-29T09:51:56.458Z'
updated: '2025-12-29'
contributors:
  - F-1049
  - F-2247
  - F-3344
metrics:
  - name: Inventory Management Efficiency
    target: 60% reduction in manual tasks
    unit: percent
  - name: Sales Performance
    target: 15% increase in transaction value
    unit: percent
---
```

---

## Feature (F-####)

Capabilities that deliver value to users. Features form a hierarchical tree.

### Feature-Specific Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `goals` | GoalId[] | Yes | Goals this feature contributes to |
| `requirements` | RequirementId[] | No | Child requirements (typically for leaf features) |
| `bundlePath` | string | No | Relative path to bundle directory |

### Feature Hierarchy

Features nest via directory structure:

```
features/
└── F-1049-pet-management/          # Parent feature
    ├── F-1049-pet-management.md
    └── F-1200-pet-health/          # Child feature
        └── F-1200-pet-health.md
```

### Example Feature

```yaml
---
id: F-1049
type: feature
title: Pet Management
status: draft
owner: Store Manager
created: "2025-12-29T09:53:49.355Z"
updated: "2025-12-29T10:31:04.445Z"
goals:
  - G-292
  - G-087
---
```

---

## Requirement (R-####)

Specific conditions that must be satisfied by a feature.

### Requirement Storage

Requirements use **directory-based storage** (like features):

```
features/F-####-parent/requirements/
└── R-2046-health-check/
    ├── R-2046-health-check.md    # Requirement file
    ├── change-requests/           # CRs for this requirement
    └── scenarios/                 # Child scenarios
```

### Requirement-Specific Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `feature` | FeatureId | Yes | Parent feature ID |
| `scenarios` | ScenarioId[] | Yes | Validation scenarios (at least one) |

### Example Requirement

```yaml
---
id: R-2046
type: requirement
title: Pets in quarantine or medical hold cannot be sold
status: draft
owner: Product Team
created: "2025-12-29T08:09:34.064Z"
updated: "2025-12-29T10:49:13.890Z"
feature: F-1009
scenarios:
  - S-0001
  - S-0002
---
```

---

## Scenario (S-####)

Specific situations that validate a requirement.

### Scenario-Specific Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `requirement` | RequirementId | Yes | Parent requirement ID |
| `acceptanceCriteria` | ACId[] | Yes | Acceptance criteria (at least one) |

### Example Scenario

```yaml
---
id: S-0001
type: scenario
title: Attempt to add quarantined pet to cart
status: draft
owner: QA Team
created: "2025-12-29T08:10:00.000Z"
updated: "2025-12-29T08:10:00.000Z"
requirement: R-0001
acceptanceCriteria:
  - AC-0001
  - AC-0002
---
```

---

## AcceptanceCriterion (AC-####)

Specific conditions that must be met for a scenario to pass.

### AcceptanceCriterion-Specific Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `scenario` | ScenarioId | Yes | Parent scenario ID |
| `tests` | TestId[] | Yes | Linked tests (at least one) |

### Example AcceptanceCriterion

```yaml
---
id: AC-0001
type: acceptanceCriterion
title: System displays error message for quarantined pet
status: draft
owner: QA Team
created: "2025-12-29T08:11:00.000Z"
updated: "2025-12-29T08:11:00.000Z"
scenario: S-0001
tests:
  - T-0001
---
```

---

## Test (T-####)

Verification procedures for acceptance criteria.

### Test-Specific Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `criterion` | ACId | Yes | Parent acceptance criterion ID |
| `kind` | string | Yes | `automated` or `manual` |
| `framework` | string | No | Test framework (Jest, Mocha, etc.) |
| `ref` | TestRef | No | Code reference |

### TestRef Object

```yaml
ref:
  repo: "https://github.com/org/repo"  # Optional
  path: "tests/pet-sales.spec.ts"       # Required if ref exists
  selector: "describe('Pet Sales')"     # Optional
```

### Example Test

```yaml
---
id: T-0001
type: test
title: Verify quarantine check on cart add
status: draft
owner: QA Team
created: "2025-12-29T08:12:00.000Z"
updated: "2025-12-29T08:12:00.000Z"
criterion: AC-0001
kind: automated
framework: Jest
ref:
  path: "tests/pet-sales.spec.ts"
  selector: "it('blocks quarantined pets')"
---
```

---

## Template (UUID v4)

Reusable specification templates.

### Template-Specific Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `templateFor` | string | Yes | Entity type this templates: feature, requirement, scenario, acceptanceCriterion, test |
| `description` | string | No | Template description |
| `sections` | string[] | No | Template sections/headings |
| `isSystemTemplate` | boolean | No | Built-in vs custom template |

### Example Template

```yaml
---
id: "bf5cb38b-7417-4063-b82b-ab5ab185f512"
type: template
title: Basic Feature
status: released
owner: system
created: "2025-12-27"
updated: "2025-12-27"
description: Simple feature template with overview and scope sections
isSystemTemplate: true
templateFor: feature
---
```

---

## ChangeRequest (CR-####)

Proposed modifications to released or locked entities.

### ChangeRequest-Specific Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `parentId` | string | Yes | ID of entity being modified |
| `parentType` | string | Yes | Type of entity being modified |
| `changeType` | string | Yes | enhancement, bugfix, breaking, deprecation, documentation |
| `description` | string | Yes | Change description |
| `changes` | string | Yes | Detailed change narrative |
| `closedReason` | string | No | Why CR was closed |
| `supersededBy` | CRId | No | Superseding CR ID |
| `mergedAt` | ISO-8601 | No | Merge timestamp |
| `mergedBy` | string | No | Person who merged |

### ChangeRequest Status Values

```
pending | draft | review | approved | in-development | under-test | merged | closed
```

### Example ChangeRequest

```yaml
---
id: CR-0001
type: changeRequest
title: Add microchipping validation to pet sales
status: pending
owner: Product Team
created: "2025-12-29T12:00:00.000Z"
updated: "2025-12-29T12:00:00.000Z"
parentId: R-0001
parentType: requirement
changeType: enhancement
description: Extend pet sale validation to check microchipping status
changes: |
  Add validation step to verify pets requiring microchipping
  (dogs and cats) have been properly chipped before sale.
---
```

---

## Field Validation Rules

### ID Formats

| Entity | Pattern | Regex |
|--------|---------|-------|
| Goal | G-### | `^G-\d{3}$` |
| Feature | F-#### | `^F-\d{4}$` |
| Requirement | R-#### | `^R-\d{4}$` |
| Scenario | S-#### | `^S-\d{4}$` |
| AcceptanceCriterion | AC-#### | `^AC-\d{4}$` |
| Test | T-#### | `^T-\d{4}$` |
| ChangeRequest | CR-#### | `^CR-\d{4}$` |
| Template | UUID v4 | `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$` |

### ID-Based Ordering

IDs determine artifact priority/order numerically within each entity type:

| ID | Priority |
|----|----------|
| Lower numeric value | Higher priority (first) |
| Higher numeric value | Lower priority (last) |

**Examples:**
- G-100 > G-500 > G-899 (goals sorted by ID)
- F-1049 > F-2500 > F-9999 (features sorted by ID)
- R-1000 > R-5000 > R-9500 (requirements sorted by ID)

Use this ordering for:
- Display order in tree views
- Processing order in reports
- Implementation priority suggestions

### Date Formats

- Full timestamp: `"2025-12-29T09:53:49.355Z"`
- Date only: `"2025-12-29"` or `'2025-12-29'`

### Owner Values

- Role: `"Store Manager"`, `"Pet Care Specialist"`
- Person: `"John Doe"`
- Team: `"Frontend Team"`, `"QA"`
- System: `"system"` (for templates)
