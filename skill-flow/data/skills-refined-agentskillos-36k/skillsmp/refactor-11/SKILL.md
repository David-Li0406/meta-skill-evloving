---
name: refactor
description: Analyze codebase for refactoring opportunities and prioritize by impact
---

# Refactoring Agent

Analyze the codebase to identify and prioritize refactoring opportunities.

## Workflow

### 1. Gather Codebase Context

```bash
# High churn files (frequently modified = priority)
git log --pretty=format: --name-only --since="6 months ago" | sort | uniq -c | sort -rn | head -30

# Tech debt markers
grep -rn "TODO\\|FIXME\\|HACK\\|XXX\\|REFACTOR" --include="*.ts" --include="*.tsx" .

# Large files (potential god classes)
find . -name "*.ts" -o -name "*.tsx" | xargs wc -l | sort -rn | head -20
```

### 2. Issue Types to Detect

| Issue | Detection | Refactor |
|-------|-----------|----------|
| Code Duplication | Similar blocks across files | Extract Function |
| Long Functions | >50 lines or complexity >10 | Extract Method |
| God Classes | >10 methods or >300 lines | Extract Class |
| Feature Envy | Method uses other class data excessively | Move Method |
| Dead Code | Unused exports, unreachable code | Delete |
| Deep Nesting | >3 levels of conditionals/loops | Guard Clauses |
| Primitive Obsession | Repeated primitive combos | Value Object |
| Long Parameter Lists | >4 parameters | Parameter Object |
| Inconsistent Patterns | Different approaches for same problem | Consolidate |
| Missing Abstractions | Repeated inline logic | Extract |

### 3. Severity Assessment

- **High** 🔴: Bug risk, critical path, high churn
- **Medium** 🟠: Tech debt accumulating, moderate burden
- **Low** 🟡: Code smell, readability issue

### 4. Priority Formula

```
Priority = Severity (High=3, Med=2, Low=1) × (1 / Effort)
Effort: Small=1, Medium=2, Large=3
```

## Output Format

```
## Refactoring Opportunities

### 1. 🔴 [Type] `file.ts:L10-85` | High | Small | Score: 3.0
   Problem: <description>
   Refactoring: <technique>

## Quick Wins (High + Small effort)
1. ...

## Summary
| Severity | Count |
|----------|-------|
| 🔴 High  | X     |
| 🟠 Medium| X     |
| 🟡 Low   | X     |
```

## Execution Mode

When asked to **apply refactorings**:
1. Start with highest priority Small-effort items
2. Make atomic commits per refactoring
3. Run tests after each change
4. Stop if tests fail and report the issue
