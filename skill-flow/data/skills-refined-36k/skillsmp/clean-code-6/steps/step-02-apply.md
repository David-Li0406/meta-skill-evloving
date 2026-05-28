---
name: step-02-apply
description: Load documentation, recommend, and apply clean code fixes
prev_step: steps/step-01-scan.md
next_step: steps/step-03-verify.md
---

# Step 2: APPLY

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER apply patterns without reading docs first
- ✅ ALWAYS load relevant reference files
- 📋 YOU ARE AN IMPLEMENTER following best practices
- 💬 FOCUS on applying patterns from loaded docs
- 🚫 FORBIDDEN to invent patterns not in docs

## EXECUTION PROTOCOLS:

- 🎯 Load docs based on detected technologies
- 💾 Track progress in table format
- 📖 Complete all changes before step-03
- 🚫 FORBIDDEN to skip verification after changes

## CONTEXT BOUNDARIES:

- From step-01: `{force_*}` flags, `{issues}`
- Reference files in `references/` folder
- Optional: Context7 MCP for latest docs

## YOUR TASK:

Load relevant documentation, generate recommendations, and apply clean code fixes.

---

## EXECUTION SEQUENCE:

### 1. Load Reference Files

**Core (always load):**

| Condition                   | Load                                         |
| --------------------------- | -------------------------------------------- |
| Always                      | `references/general-clean-code.md`           |
| Always (unless `--no-a11y`) | `references/accessibility-best-practices.md` |

**Frontend:**

| Condition       | Load                                          |
| --------------- | --------------------------------------------- |
| `force_react`   | `references/react-clean-code.md`              |
| `force_nextjs`  | `references/nextjs-clean-code.md`             |
| `force_expo`    | `references/expo-best-practices.md`           |
| `force_zustand` | `references/zustand-best-practices.md`        |
| `force_query`   | `references/tanstack-query-best-practices.md` |
| `force_forms`   | `references/forms-best-practices.md`          |
| `force_css`     | `references/css-best-practices.md`            |
| `force_ux`      | `references/ux-design-best-practices.md`      |

**Backend:**

| Condition        | Load                                    |
| ---------------- | --------------------------------------- |
| `force_backend`  | `references/backend-best-practices.md`  |
| `force_security` | `references/security-best-practices.md` |

**Testing:**

| Condition    | Load                                   |
| ------------ | -------------------------------------- |
| `force_test` | `references/testing-best-practices.md` |

**CRITICAL: Actually READ the files with Read tool!**

### 2. Generate Recommendations

Based on issues + loaded docs:

```markdown
## Recommendations

### 🔴 High Priority

1. Replace useEffect → TanStack Query
2. Add Error Boundaries

### 🟡 Medium Priority

3. Fix `any` types

### 🟢 Quick Wins

4. Remove console.log
```

### 3. Confirm Before Applying

**If `{auto_mode}` = true:**
→ Apply all recommendations

**If `{auto_mode}` = false:**
→ Use AskUserQuestion:

```yaml
questions:
  - header: "Apply"
    question: "Apply these clean code improvements?"
    options:
      - label: "Apply All (Recommended)"
        description: "Apply all recommendations"
      - label: "High Priority Only"
        description: "Only high priority fixes"
    multiSelect: false
```

### 4. Install Dependencies

If new libraries needed:

```bash
pnpm add @tanstack/react-query react-error-boundary
```

### 5. Apply Changes

**If `{economy_mode}` = true:**
→ Apply sequentially

**If `{economy_mode}` = false AND 4+ files:**
→ Use parallel Snipper agents

**Track progress:**

```markdown
| File          | Status | Change               |
| ------------- | ------ | -------------------- |
| providers.tsx | ✅     | Added QueryProvider  |
| Auth.tsx      | ✅     | useEffect → useQuery |
```

### 6. Summary

```markdown
## Changes Applied

- Files modified: 8
- Lines added: 120
- Lines removed: 180
```

**If `{save_mode}` = true:**
→ Write to `.claude/output/clean-code/{task_id}/02-apply.md`

---

## SUCCESS METRICS:

✅ Docs loaded and read
✅ Recommendations generated
✅ Changes applied following doc patterns
✅ Progress tracked

## FAILURE MODES:

❌ Applying patterns without reading docs
❌ Skipping dependency installation
❌ Not tracking progress

## APPLY PROTOCOLS:

- Follow patterns from docs exactly
- Don't invent new patterns
- Verify build after major changes

---

## NEXT STEP:

After changes applied, load `./step-03-verify.md`

<critical>
Follow patterns from LOADED DOCS only!
</critical>
