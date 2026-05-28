# Task Guideline Patch

## Patch ID

TGP-<N>

## Target File

- **Path**: `<templates/task-file.template.md or module path>`
- **Section**: `<section name>`

## Change Type

- [ ] Add
- [ ] Replace
- [ ] Remove

---

## Patch

```diff
+ <new text>
- <old text>
```

---

## Context

### Pattern Addressed

<What recurring issue does this fix?>

### Evidence

- TASK-XXX: <brief description>
- TASK-YYY: <brief description>

### Root Cause

<Why did this pattern occur?>

---

## Rationale

<What failure does this patch prevent? Be specific.>

---

## Applies To

- [ ] All task files
- [ ] Tasks in category: <category>
- [ ] Tasks touching: <area>

---

## Rollout

- [ ] Immediate (safe for in-flight tasks)
- [ ] Next phase (affects task structure)
- [ ] Migration required

### Migration Notes (if applicable)

<How to update existing task files>

---

## Validation

How to verify patch is working:

- [ ] <check 1>
- [ ] <check 2>

---

## Related

- Related pattern: <pattern name>
- Related proposals: GCP-<N>
- Related tasks: TASK-XXX
