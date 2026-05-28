# Documentation Templates

## TL;DR Block Template

```markdown
> **TL;DR:** [One sentence describing what this document covers]
>
> **Key Points:**
> - [Fact 1 with specific numbers/values]
> - [Fact 2 with specific numbers/values]
> - [Fact 3 with action item or location]
>
> **Quick Links:** [Section1](#section1) | [Section2](#section2) | [Section3](#section3)
```

## API Table Template

```markdown
### [Feature Name] Tables

| Table | Primary Key | RLS | Notes |
|-------|-------------|-----|-------|
| `table_name` | `id` (UUID) | Yes | Brief purpose |

### [Feature Name] RPCs

| Function | Auth | Returns | Purpose |
|----------|------|---------|---------|
| `rpc_name` | JWT | `TYPE` | Brief purpose |
```

## Edge Function Doc Template

```markdown
## Edge Function: function-name

**Endpoint:** `POST /functions/v1/function-name`
**Auth:** JWT required | Public
**Purpose:** One-line description

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `field1` | string | Yes | Description |
| `field2` | number | No | Description (default: X) |

### Response

\`\`\`json
{
  "success": true,
  "data": { ... }
}
\`\`\`

### Error Codes

| Code | HTTP | Message |
|------|------|---------|
| `ERROR_CODE` | 400 | Human-readable message |

### Usage Example

\`\`\`typescript
const { data, error } = await supabase.functions.invoke('function-name', {
  body: { field1: 'value' }
});
\`\`\`
```

## Admin Page Doc Template

```markdown
## Page Name

**Path:** `/admin/page-path`
**Access:** Admin only

Brief description of what this page manages.

### Tabs/Sections

#### Tab 1 Name
- Feature 1
- Feature 2

#### Tab 2 Name
- Feature 3

### Common Operations

**Operation 1:**
1. Step 1
2. Step 2

**Operation 2:**
1. Step 1
2. Step 2
```

## Architecture Diagram Template

```markdown
## [Feature] Flow

\`\`\`
1. User action
       │
       ▼
2. Frontend component
       │
       ▼
3. API/Edge Function
   ├── Database query
   ├── External service call
   └── Return response
       │
       ▼
4. UI update
\`\`\`
```

## Changelog Entry Template

```markdown
### [Date] - [Version/Feature]

**Added:**
- New feature description

**Changed:**
- Modification description

**Fixed:**
- Bug fix description

**Migration:**
- `20260108_migration_name.sql` - Brief description
```

## Audit Report Template

```markdown
# Documentation Audit Report
Generated: YYYY-MM-DD

## Summary
- Total docs: X
- Up-to-date: Y
- Needs update: Z
- Critical: N

## Issues Found

### Critical (blocks release)
- [ ] `file.md`: Issue description

### Warnings (should fix)
- [ ] `file.md`: Issue description

### Info (minor)
- [ ] `file.md`: Issue description

## Database vs Docs Diff

| Item | In DB | In Docs | Status |
|------|-------|---------|--------|
| `table_name` | Yes | No | Missing |
| `rpc_name` | Yes | Yes | OK |

## Recommendations
1. Action item 1
2. Action item 2
```
