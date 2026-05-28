# Drift Remediation Templates

## Missing Server Action Doc

```markdown
Add to [feature].md → Server Actions:

| Action | Purpose | Tables | Auth |
|--------|---------|--------|------|
| [name] | [what it does] | [tables] | [auth level] |
```

## Missing Route Doc

```markdown
Add to [feature].md → User Surfaces:

| Surface | Route | Description |
|---------|-------|-------------|
| [name] | [path] | [what user does here] |
```

## Schema Drift

```markdown
Update [feature].md → Data Model:

### Tables
| Table | Purpose | Key Columns |
|-------|---------|-------------|
| [table] | [purpose] | [actual columns] |
```

## Stale Workflow

```markdown
Update [role]-workflows.md → [Workflow Name]:

### Steps
1. [Current step 1]
2. [Current step 2] ← was: [old step]
3. [New step 3]
```

## Missing RLS Documentation

```markdown
Add to [feature].md → Permissions & Security:

### RLS Policies
- [policy_name]: [what it allows/denies]
```

## Stale Invariant

```markdown
Update [feature].md → Invariants:

1. [Updated invariant text]
   - Previous: [what it said before]
   - Reason for change: [why it changed]
```

## Integration with Doc Agent

For complex drift:

```
@doc-agent: Drift check found these issues. Please help remediate:

1. [drift item 1]
2. [drift item 2]

Which feature docs need updating and what should change?
```
