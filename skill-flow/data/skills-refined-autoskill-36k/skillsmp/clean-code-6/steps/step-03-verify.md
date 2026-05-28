---
name: step-03-verify
description: Verify build passes and summarize changes
prev_step: steps/step-02-apply.md
next_step: null
---

# Step 3: VERIFY

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER complete with failing build
- ✅ ALWAYS run build before marking done
- 📋 YOU ARE A VALIDATOR ensuring quality
- 💬 FOCUS on verification and summary
- 🚫 FORBIDDEN to skip any check

## EXECUTION PROTOCOLS:

- 🎯 Run all verification commands
- 💾 Save summary if `{save_mode}` = true
- 📖 Fix any errors before completing
- 🚫 FORBIDDEN to mark complete if build fails

## CONTEXT BOUNDARIES:

- From step-02: changes applied, files modified
- Build/lint commands from package.json

## YOUR TASK:

Run build, fix any errors, and provide final summary.

---

## EXECUTION SEQUENCE:

### 1. Run TypeScript Check

```bash
npx tsc --noEmit
```

**If errors:** Fix and re-run until clean.

### 2. Run Linter

```bash
pnpm lint
```

**If errors:** Fix with `pnpm lint --fix`, then manual fixes.

### 3. Run Build

```bash
pnpm build
```

**If build fails:**

1. Read error
2. Fix issue
3. Re-run
4. **Loop until passes**

### 4. Run Tests (if available)

```bash
pnpm test
```

### 5. Generate Summary

```markdown
## Clean Code Complete ✓

### Verification

| Check      | Status |
| ---------- | ------ |
| TypeScript | ✅     |
| ESLint     | ✅     |
| Build      | ✅     |

### Improvements

| Metric             | Before | After |
| ------------------ | ------ | ----- |
| useEffect fetching | 5      | 0     |
| any types          | 12     | 0     |

### Files Changed: 12
```

**If `{save_mode}` = true:**
→ Write to `.claude/output/clean-code/{task_id}/03-verify.md`

### 6. Offer Commit

**Use AskUserQuestion:**

```yaml
questions:
  - header: "Complete"
    question: "Clean code complete. Create commit?"
    options:
      - label: "Create Commit (Recommended)"
        description: "Commit changes"
      - label: "Done"
        description: "Finish without commit"
    multiSelect: false
```

**If commit:**

```bash
git add -A && git commit -m "refactor: apply clean code improvements"
```

---

## SUCCESS METRICS:

✅ TypeScript passes
✅ Linter passes
✅ Build passes
✅ Summary generated

## FAILURE MODES:

❌ Completing with failing build
❌ Skipping verification
❌ Not offering commit option

## VERIFY PROTOCOLS:

- Always run build
- Fix errors before completing
- Provide clear summary

---

## WORKFLOW COMPLETE

<critical>
NEVER complete if build fails!
</critical>
