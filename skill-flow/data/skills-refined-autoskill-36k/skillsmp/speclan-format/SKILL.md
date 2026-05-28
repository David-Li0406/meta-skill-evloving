---
name: SPECLAN Format
description: >-
  **ALWAYS INJECT** this skill when working with files in PROJECTROOT/speclan/ directory.

  This is foundational knowledge for ALL speclan operations - reading, creating, updating, or deleting spec files. Without this context, Claude will create incorrect file structures, invalid IDs, or broken relationships.

  Triggers: ANY operation on speclan/ files, "read feature", "list requirements", "create feature", "new requirement", "update spec", "delete change-request", "speclan directory", "spec hierarchy", "ID format", or any mention of SPECLAN entity types (Goal, Feature, Requirement, Scenario, ChangeRequest).
version: 0.2.0
---

# SPECLAN Format Knowledge

**THIS IS FOUNDATIONAL CONTEXT.** Apply these rules to ALL speclan file operations.

SPECLAN (Specification as a Living Language) manages project specifications as interlinked markdown files with YAML frontmatter in a hierarchical directory structure.

## Quick Reference (CRITICAL)

### Filename IS the Source of Truth

The **directory/filename pattern** `{PREFIX}-{ID}-{slug}` is authoritative:

```
F-1049-pet-management/F-1049-pet-management.md
│  │    │              └─ File MUST match directory name
│  │    └─ Kebab-case slug from title
│  └─ 4-digit numeric ID (randomly generated)
└─ Entity prefix (F=Feature, R=Requirement, etc.)
```

**Extract ID from filename, NOT frontmatter** for indexing and collision checks.

### Entity Prefixes

| Entity | Prefix | Digits | Example | Storage |
|--------|--------|--------|---------|---------|
| Goal | G- | 3 | G-292 | `goals/G-292-slug.md` (flat) |
| Feature | F- | 4 | F-1049 | `features/F-1049-slug/F-1049-slug.md` (dir) |
| Requirement | R- | 4 | R-2046 | `features/.../requirements/R-2046-slug/R-2046-slug.md` (dir) |
| Change Request | CR- | 4 | CR-0731 | `{parent}/change-requests/CR-0731-slug.md` (flat) |
| Scenario | S- | 4 | S-0001 | `requirements/.../scenarios/S-0001-slug/` (dir) |

### Status Determines Editability

| Editable (direct edit OK) | Locked (needs Change Request) |
|---------------------------|------------------------------|
| draft, review, approved | in-development, under-test, released, deprecated |

## Directory Structure

SPECLAN specifications live in `${PROJECT}/speclan/`:

```
speclan/
├── goals/                    # G-### Business goals (flat)
├── features/                 # F-#### Feature hierarchy
│   └── F-1049-pet-management/
│       ├── F-1049-pet-management.md      # Feature file matches directory
│       ├── requirements/                  # Requirements as directories
│       │   ├── R-2046-health-check/
│       │   │   ├── R-2046-health-check.md
│       │   │   ├── change-requests/       # CRs for this requirement
│       │   │   └── scenarios/             # Scenarios for this requirement
│       │   └── R-3272-status-tracking/
│       │       └── R-3272-status-tracking.md
│       ├── change-requests/               # CRs for this feature
│       │   └── CR-0731-add-feature.md
│       └── F-1200-pet-health/             # Child feature (nested)
│           └── F-1200-pet-health.md
├── templates/                # Templates (UUID in frontmatter, slug filename)
│   ├── features/
│   ├── requirements/
│   ├── scenarios/
│   ├── acceptance-criteria/
│   └── tests/
└── change-requests/          # Root-level change requests
```

**Key structural rules:**
- **Features and Requirements use directory-based storage** - directory name must match contained markdown filename
- Requirements are nested inside their parent feature's `requirements/` directory as subdirectories
- Child features are subdirectories of parent features
- Change requests live in `change-requests/` adjacent to the entity they modify (features OR requirements)

## Entity Hierarchy

```
Goal (G-###)
  └── Feature (F-####)  [forms hierarchical tree via directories]
        └── Requirement (R-####)
              └── Scenario (S-####)
                    └── AcceptanceCriterion (AC-####)
                          └── Test (T-####)
```

Additional entities:
- **Template** (UUID v4) - Reusable spec templates
- **ChangeRequest** (CR-####) - Modifications to released entities

## ID Format Conventions

| Entity | Format | Example | Storage Location |
|--------|--------|---------|------------------|
| Goal | `G-###` | G-292 | `goals/` (flat files) |
| Feature | `F-####` | F-1049 | `features/` (hierarchical directories) |
| Requirement | `R-####` | R-2046 | `features/{feature}/requirements/` (directories) |
| Scenario | `S-####` | S-0001 | `requirements/{requirement}/scenarios/` (directories) |
| AcceptanceCriterion | `AC-####` | AC-0001 | *Not yet implemented* |
| Test | `T-####` | T-0001 | *Not yet implemented* |
| ChangeRequest | `CR-####` | CR-0731 | `{entity}/change-requests/` (flat files) |
| Template | UUID v4 | bf5cb38b-... | `templates/{type}/` (flat files) |

**ID Generation:** All numeric IDs are **randomly generated** with collision detection (not sequential). Always check existing IDs before creating new ones.

**ID-Based Ordering:** IDs determine artifact priority/order numerically:
- **Lower IDs = Higher priority** (processed/displayed first)
- **Higher IDs = Lower priority** (processed/displayed later)
- Example: F-1049 has higher priority than F-2847
- This ordering applies within the same entity type (features sorted among features, requirements among requirements, etc.)

## File Naming Convention

Files follow pattern: `<ID>-kebab-case-title.md`

Examples:
- `G-292-comprehensive-pet-retail-operations.md` (flat file in goals/)
- `F-1049-pet-management/F-1049-pet-management.md` (directory-based)
- `R-2046-health-check/R-2046-health-check.md` (directory-based)

**Directory-based entities** (Features, Requirements, Scenarios):
- Directory name **must match** the contained markdown filename
- Example: `F-1049-pet-management/F-1049-pet-management.md`
- Example: `R-2046-health-check/R-2046-health-check.md`

Template filenames use **kebab-case slugs** (UUID stored in frontmatter only):
- `basic-feature.md`
- `functional-requirement.md`

## Markdown File Format

Every spec file has YAML frontmatter followed by markdown content:

```markdown
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

# Pet Management

## Overview
Brief description of what this feature does and why it exists.

## User Story
As a **Store Manager**, I want **comprehensive tools** so that **I can track pets**.

## Scope
- Pet Tracking
- Status Management
- Health Records
```

## Common YAML Frontmatter Fields

**All entities share:**
```yaml
id: <entity-id>           # Required
type: <entity-type>       # Required: goal|feature|requirement|scenario|acceptanceCriterion|test|template|changeRequest
title: <string>           # Required
status: <status>          # Required: draft|review|approved|in-development|under-test|released|deprecated
owner: <string>           # Required
created: <ISO-8601>       # Required
updated: <ISO-8601>       # Required
tags: [<string>, ...]     # Optional
```

**Entity-specific fields** - See `references/entity-fields.md` for complete reference.

## Status Lifecycle

Entities follow a 7-stage lifecycle:

```
draft → review → approved → in-development → under-test → released → deprecated
```

| Status | Editable | Description |
|--------|----------|-------------|
| `draft` | Yes | Initial creation, work in progress |
| `review` | Yes | Ready for review |
| `approved` | Yes | Approved, ready for development |
| `in-development` | **No** | Currently being implemented |
| `under-test` | **No** | Implementation complete, testing |
| `released` | **No** | Deployed to production |
| `deprecated` | **No** | No longer active (terminal state) |

**Read-only statuses:** Entities in `in-development`, `under-test`, `released`, or `deprecated` are locked. Direct edits are not allowed - changes require a **Change Request** (`CR-####`).

## Validation Rules

When creating or updating SPECLAN entities, enforce these validation rules to ensure structure compliance.

### Required YAML Frontmatter Fields

All entities MUST have these fields present and non-empty:

| Field | Validation |
|-------|------------|
| `id` | Must match entity-specific ID format (see below) |
| `type` | Must be one of: `goal`, `feature`, `requirement`, `scenario`, `acceptanceCriterion`, `test`, `template`, `changeRequest` |
| `title` | Non-empty string |
| `status` | Must be valid status value for entity type |
| `owner` | Non-empty string (role, person, or team) |
| `created` | Valid ISO-8601 timestamp |
| `updated` | Valid ISO-8601 timestamp, must be >= `created` |

### ID Format Validation

Each entity type has a strict ID format:

| Entity | Regex Pattern | Valid Examples | Invalid Examples |
|--------|---------------|----------------|------------------|
| Goal | `^G-\d{3}$` | G-142, G-999 | G-42, G-1234, G-ABC |
| Feature | `^F-\d{4}$` | F-1049, F-9999 | F-049, F-12345, f-1234 |
| Requirement | `^R-\d{4}$` | R-2046, R-1000 | R-046, R-99999 |
| Scenario | `^S-\d{4}$` | S-0001, S-5432 | S-1, S-12345 |
| AcceptanceCriterion | `^AC-\d{4}$` | AC-0001, AC-9999 | AC-1, ac-0001 |
| Test | `^T-\d{4}$` | T-0001, T-1234 | T-1, T-12345 |
| ChangeRequest | `^CR-\d{4}$` | CR-0731, CR-9999 | CR-01, CR-12345 |
| Template | UUID v4 | `bf5cb38b-7417-...` | Any non-UUID |

**Validation regex (JavaScript):**
```javascript
const ID_PATTERNS = {
  goal: /^G-\d{3}$/,
  feature: /^F-\d{4}$/,
  requirement: /^R-\d{4}$/,
  scenario: /^S-\d{4}$/,
  acceptanceCriterion: /^AC-\d{4}$/,
  test: /^T-\d{4}$/,
  changeRequest: /^CR-\d{4}$/,
  template: /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i
};
```

### Directory and File Naming Enforcement

**Directory-based entities** (Feature, Requirement, Scenario):

1. Directory name MUST match the markdown filename inside
2. Format: `<ID>-<kebab-case-title>/`
3. Contained file: `<ID>-<kebab-case-title>.md`

**Validation rules:**
```
# Valid
F-1049-pet-management/F-1049-pet-management.md    ✓
R-2046-health-check/R-2046-health-check.md        ✓

# Invalid
F-1049-pet-management/F-1049.md                   ✗ (filename mismatch)
F-1049/F-1049-pet-management.md                   ✗ (directory name incomplete)
f-1049-pet-management/F-1049-pet-management.md    ✗ (case mismatch)
```

**Flat-file entities** (Goal, ChangeRequest):

1. File format: `<ID>-<kebab-case-title>.md`
2. Placed directly in parent directory (no subdirectory)

### Parent-Child Relationship Validation

Entities must correctly reference their parents:

| Entity | Required Parent Field | Parent Type | Validation |
|--------|----------------------|-------------|------------|
| Feature | `goals` (array) | Goal | Each ID must exist as `G-###` in `speclan/goals/` |
| Requirement | `feature` (string) | Feature | Must be valid `F-####` that exists |
| Scenario | `requirement` (string) | Requirement | Must be valid `R-####` that exists |
| AcceptanceCriterion | `scenario` (string) | Scenario | Must be valid `S-####` that exists |
| Test | `criterion` (string) | AcceptanceCriterion | Must be valid `AC-####` that exists |
| ChangeRequest | `parentId` + `parentType` | Feature/Requirement | Parent must exist and parentType must match |

**Directory placement validation:**
- Requirements MUST be in `features/<parent-feature>/requirements/`
- Scenarios MUST be in `requirements/<parent-requirement>/scenarios/`
- Child features MUST be in `features/<parent-feature>/`
- ChangeRequests MUST be in `<parent-entity>/change-requests/`

### Status Lifecycle Rules

#### Valid Status Values

**Standard entities** (Goal, Feature, Requirement, Scenario, AC, Test):
```
draft | review | approved | in-development | under-test | released | deprecated
```

**ChangeRequest entities:**
```
pending | draft | review | approved | in-development | under-test | merged | closed
```

#### Editability Rules

| Status | Direct Edit Allowed | Change Request Required |
|--------|--------------------|-----------------------|
| `draft` | Yes | No |
| `review` | Yes | No |
| `approved` | Yes | No |
| `in-development` | **No** | **Yes** |
| `under-test` | **No** | **Yes** |
| `released` | **No** | **Yes** |
| `deprecated` | **No** | **Yes** |

**CRITICAL:** Before modifying any entity, check its status:

```bash
# Extract status from frontmatter
status=$(grep "^status:" "$file" | head -1 | cut -d: -f2 | tr -d ' ')

# Check if read-only
case "$status" in
  in-development|under-test|released|deprecated)
    echo "Entity is read-only. Change Request required."
    ;;
  *)
    echo "Entity is editable."
    ;;
esac
```

#### When Change Requests Are Required

A ChangeRequest (`CR-####`) MUST be created when:

1. **Entity is in read-only status** (`in-development`, `under-test`, `released`, `deprecated`)
2. **Proposing breaking changes** to any entity regardless of status
3. **Deprecating an entity** (status change to `deprecated`)
4. **Requesting feature removal** or significant scope reduction

**ChangeRequest workflow:**
```
1. Create CR in <entity>/change-requests/
2. CR status: pending → draft → review → approved → in-development → merged
3. When merged, apply changes to parent entity
4. Update parent entity's `updated` timestamp
```

### Status Transition Rules

Valid status transitions (forward progression):

```
draft → review → approved → in-development → under-test → released → deprecated
```

**Special transitions:**
- `review → draft` (rejection/revision)
- `approved → draft` (re-planning)
- Any status → `deprecated` (via Change Request if read-only)

**Invalid transitions:**
- `released → in-development` (regression - use Change Request instead)
- `deprecated → any` (terminal state)

### Entity-Specific Field Validation

#### Goal (`G-###`)

| Field | Required | Validation |
|-------|----------|------------|
| `contributors` | No | Array of valid `F-####` IDs |
| `metrics` | No | Array of `{name, target, unit}` objects |

#### Feature (`F-####`)

| Field | Required | Validation |
|-------|----------|------------|
| `goals` | Yes | Non-empty array of valid `G-###` IDs |
| `requirements` | No | Array of valid `R-####` IDs |
| `bundlePath` | No | Valid relative path string |

#### Requirement (`R-####`)

| Field | Required | Validation |
|-------|----------|------------|
| `feature` | Yes | Valid `F-####` ID that exists |
| `scenarios` | Yes | Non-empty array of valid `S-####` IDs |

#### ChangeRequest (`CR-####`)

| Field | Required | Validation |
|-------|----------|------------|
| `parentId` | Yes | Valid entity ID (F-####, R-####, etc.) |
| `parentType` | Yes | `feature`, `requirement`, `scenario`, etc. |
| `changeType` | Yes | `enhancement`, `bugfix`, `breaking`, `deprecation`, `documentation` |
| `description` | Yes | Non-empty string |
| `changes` | Yes | Non-empty string (detailed narrative) |

### Validation Checklist

Before creating/updating any SPECLAN entity, verify:

- [ ] ID format matches entity type regex
- [ ] All required fields present and non-empty
- [ ] `type` field matches expected entity type
- [ ] `status` is valid for entity type
- [ ] Parent references (if any) point to existing entities
- [ ] File/directory naming matches convention
- [ ] File placed in correct directory location
- [ ] If entity is read-only, Change Request exists
- [ ] `updated` timestamp is current ISO-8601
- [ ] Bidirectional links maintained (e.g., feature lists requirement, requirement references feature)

## Linking Between Specs

### YAML Frontmatter References

```yaml
# Goal references features
contributors:
  - F-1049
  - F-2247

# Feature references goals
goals:
  - G-292
  - G-087

# Requirement references parent feature
feature: F-1009

# Requirement references scenarios
scenarios:
  - S-0001
  - S-0002
```

### Markdown Cross-References

Use relative paths in markdown content:

```markdown
## Related
### Goals
- [Animal Welfare Compliance](../goals/G-087-animal-welfare-compliance.md)

### Features
- [Pet Status Lifecycle](../F-1807-pet-status-lifecycle/F-1807-pet-status-lifecycle.md)
```

## Working with SPECLAN Files

### Detecting SPECLAN Directory

To find the speclan directory in a project:

1. Check common locations: `speclan/`, `specs/speclan/`
2. Look for characteristic subdirectories: `goals/`, `features/`, `requirements/`
3. Verify markdown files with SPECLAN YAML frontmatter

### Reading Specifications

When reading a spec file:
1. Parse YAML frontmatter for metadata
2. Extract entity relationships from frontmatter fields
3. Parse markdown content for documentation

### Creating New Specifications

To create a new spec:

1. **Check for user templates FIRST:**
   ```
   speclan/templates/<entity-type>/
   ```
   - `speclan/templates/features/` for feature templates
   - `speclan/templates/requirements/` for requirement templates
   - `speclan/templates/scenarios/` for scenario templates

   Read available templates and choose the best fit. Templates contain the user's preferred structure.

2. **Generate a unique ID:**
   - IDs are **randomly generated** (not sequential)
   - Goals: 3-digit (e.g., G-249)
   - Features/Requirements/Scenarios/etc.: 4-digit (e.g., F-1049, R-2046)
   - **Always check for collisions** before using:
     ```bash
     # Check existing Feature IDs
     find speclan/features -type d -name 'F-*' | grep -oE 'F-[0-9]+' | sort -u
     # Check existing Requirement IDs
     find speclan/features -type d -name 'R-*' | grep -oE 'R-[0-9]+' | sort -u
     ```

3. **Create file in correct location:**

   **For Goals:** `speclan/goals/G-###-slug.md` (flat file)

   **For Features:** Create directory AND file with matching name:
   ```
   speclan/features/F-####-slug/F-####-slug.md
   ```

   **For Requirements:** Create directory inside parent feature's `requirements/`:
   ```
   speclan/features/F-####-parent/requirements/R-####-slug/R-####-slug.md
   ```

   **For Child Features:** Nest inside parent feature directory:
   ```
   speclan/features/F-####-parent/F-####-child/F-####-child.md
   ```

   **For Scenarios:** Nest inside parent requirement directory:
   ```
   speclan/features/.../requirements/R-####-parent/scenarios/S-####-slug/S-####-slug.md
   ```

4. **Write frontmatter and content:**
   - Use template if found, otherwise use default structure
   - Set all required fields (id, type, title, status, owner, created, updated)
   - For requirements, set `feature: F-####` to link to parent

5. **Update related entities** to establish bidirectional links

### Updating Specifications

When modifying a spec:
1. Update the `updated` timestamp
2. Maintain bidirectional links (if adding feature to goal, add goal to feature)
3. Follow status transition rules

## Writing Guidelines

For guidance on writing effective specifications, consult `references/writing-guide.md`.

Key principles:
- Write user-focused, implementation-agnostic specifications
- Include clear acceptance criteria
- Maintain traceability between entities
- Use consistent terminology

## Additional Resources

### Reference Files

- **`references/entity-fields.md`** - Complete YAML field reference for all entity types
- **`references/writing-guide.md`** - Best practices for writing specifications

### Related Skills

- **`speclan-id-generator`** - Generate collision-free unique IDs for SPECLAN entities

### Utility Scripts

- **`scripts/detect-speclan.sh`** - Detect speclan directory in a project
