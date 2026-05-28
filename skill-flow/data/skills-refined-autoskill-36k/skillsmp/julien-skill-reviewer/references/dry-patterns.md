# DRY Patterns and Violations

## Common Duplication Patterns

### Pattern 1: API Documentation in Multiple Places

**Violation:**
```
SKILL.md (150 lines):
  - Full API endpoint documentation
  - Parameter descriptions
  - Response formats

references/api-docs.md (150 lines):
  - Same content duplicated
```

**Fix:**
```
SKILL.md (10 lines):
  - Brief overview
  - Pointer: "See references/api-docs.md"
  - Quick examples of main endpoints

references/api-docs.md (150 lines):
  - Complete API documentation
```

### Pattern 2: Examples Scattered Throughout

**Violation:**
```
SKILL.md:
  - Section 1: Example A (30 lines)
  - Section 2: Example B (30 lines)
  - Section 3: Example C (30 lines)
```

**Fix:**
```
SKILL.md:
  - Brief example references
  - "See references/examples.md"

references/examples.md:
  - All examples consolidated
```

### Pattern 3: Repeated Context/Setup

**Violation:**
```
SKILL.md:
  Step 1: "Ensure Node.js v18+ is installed..."
  Step 5: "Make sure Node.js v18+ is available..."
  Step 10: "Verify Node.js v18+ installation..."
```

**Fix:**
```
SKILL.md:
  ## Prerequisites
  - Node.js v18+
  - npm v9+

  [Steps reference prerequisites, don't repeat]
```

## Progressive Disclosure Hierarchy

```
Level 1: SKILL.md (always loaded, < 500 lines)
  ├─ Purpose and when to use
  ├─ High-level workflow (5-10 steps)
  └─ Pointers to references/

Level 2: references/ (loaded when Claude needs)
  ├─ detailed-guide.md
  ├─ api-reference.md
  ├─ examples.md
  ├─ troubleshooting.md
  └─ advanced-usage.md

Level 3: scripts/ (executed, not loaded)
  ├─ helper.py
  └─ validation.sh

Level 4: assets/ (used in output, not loaded)
  ├─ template.yaml
  └─ logo.png
```

## Line Count Guidelines

| File | Target | Max |
|------|--------|-----|
| SKILL.md | 200-300 | 500 |
| Each reference | 100-200 | Unlimited |
| Total skill | N/A | Unlimited |

## Refactoring Actions

### Extract to references/

**Before (SKILL.md - 200 lines):**
```markdown
## API Reference

### Endpoint: GET /users
Returns list of users...

[150 lines of API documentation]
```

**After (SKILL.md - 10 lines):**
```markdown
## API Reference

For complete API documentation, see `references/api-reference.md`.

Quick reference:
- GET /users - List users
- POST /users - Create user
- GET /users/{id} - Get details
```

**New file (references/api-reference.md):**
```markdown
# API Reference

## Endpoint: GET /users

Returns paginated list of users.

**URL**: `/api/v1/users`

**Parameters**:
- `page` (int, optional): Page number
- `limit` (int, optional): Results per page

[Full detailed documentation]
```

### Consolidate Examples

**Before:** Examples in 5 different sections of SKILL.md

**After:**
1. Create `references/examples.md`
2. Move all examples there
3. In SKILL.md, add: "See references/examples.md for complete examples"
4. Keep only 1-2 brief examples inline

### Add Missing References Structure

**Before:** Everything in SKILL.md (800 lines)

**After:**
```
skill/
├── SKILL.md (200 lines)
└── references/
    ├── detailed-guide.md
    ├── api-reference.md
    ├── examples.md
    └── troubleshooting.md
```

## Validation Checklist

- [ ] SKILL.md < 500 lines
- [ ] No content duplicated between SKILL.md and references/
- [ ] All references linked from SKILL.md
- [ ] References are one level deep (no A → B → C)
- [ ] Files > 100 lines have TOC at top
- [ ] Clear separation: scripts/, references/, assets/
