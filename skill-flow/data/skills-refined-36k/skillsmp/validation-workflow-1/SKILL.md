---
name: validation-workflow
description: Full validation workflow for QA agent - automated checks and browser testing
category: validation
depends-on: []
---

# Validation Workflow Skill

> "Trust but verify – automated tests catch regressions, browser tests catch reality."

## When to Use This Skill

Use when:

- `currentTask.status === "ready_for_qa"`
- Developer has committed changes
- Ready to validate implementation

## Quick Start

```bash
# Run full validation suite
npm run type-check && npm run lint && npm run test && npm run build

# Then MANDATORY browser testing via Playwright MCP
# 1. Navigate to localhost:3000
# 2. Take screenshots
# 3. Verify functionality
```

## ⚠️ VALIDATION GATE

**Playwright MCP browser testing is REQUIRED for every validation.**

If browser testing cannot be performed:

→ **FAIL validation immediately**
→ Report: `"Playwright MCP unavailable - validation gate failed"`
→ **DO NOT** proceed with any other checks

**This is NON-NEGOTIABLE** - there is NO manual testing fallback.

## ⚠️ MANDATORY GATE: Browser Testing Must Complete

**Browser testing via Playwright MCP is NON-NEGOTIABLE.**

- Browser testing MUST complete even if automated checks (type-check, lint, test, build) fail
- If automated checks fail → report bugs AND run browser testing to document visual state
- NO exceptions for "blocked by test failure"
- If Playwright MCP unavailable → FAIL validation with severity "critical"

**Enforcement Flow:**

```
[Automated Checks Fail]
        │
        ├── Browser Testing NOT run? → ❌ INVALID REPORT
        │
        └── Browser Testing COMPLETED → ✅ Valid bug report
                (includes screenshots, console output, visual state)
```

**Why browser testing when tests fail:**
- Visual bugs may exist even when code compiles
- Console errors only appear in browser
- Runtime issues not caught by unit tests
- Screenshot evidence needed for developer to fix

## Validation Pipeline

```
      [GATE: Playwright MCP MUST be available]
                  │
                  ▼
┌─────────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Type Check  │───▶│   Lint   │───▶│   Test   │───▶│  Build   │
│    (tsc)    │    │ (eslint) │    │ (vitest) │    │  (vite)  │
└─────────────┘    └──────────┘    └──────────┘    └──────────┘
       │                │                │               │
       ▼                ▼                ▼               ▼
   Pass/Fail       Pass/Fail        Pass/Fail       Pass/Fail
       │                │                │               │
       └────────────────┴────────────────┴───────────────┘
                                          │
                                          ▼
                              ┌─────────────────────┐
                              │  BROWSER TESTING     │ ◄── MANDATORY GATE
                              │  (Playwright MCP)    │     NO EXCEPTIONS
                              └─────────────────────┘
                                          │
                              ┌──────────┴──────────┐
                              │                     │
                         PASS                   FAIL
                          │                        │
                          ▼                        ▼
                    Update PRD            Report bugs
```

## Progressive Guide

### Level 1: Automated Checks

```bash
# Step 1: Type Check
npm run type-check
# Expected: 0 errors

# Step 2: Lint
npm run lint
# Expected: 0 warnings

# Step 3: Unit Tests
npm run test
# Expected: All tests pass

# Step 4: Build
npm run build
# Expected: Build succeeds
```

### Level 2: Browser Testing (MANDATORY)

**Every validation MUST include browser testing:**

1. Start dev server: `npm run dev`
2. Navigate to `http://localhost:3000`
3. Verify acceptance criteria visually
4. Check console for errors
5. Take screenshots as evidence

```markdown
## Browser Test Results

**URL**: http://localhost:3000
**Browser**: Chromium

### Checks Performed:

- [ ] Page loads without errors
- [ ] Canvas renders correctly
- [ ] No console errors
- [ ] Controls respond to input
- [ ] Performance is acceptable (60 FPS)

### Screenshots:

- Initial load: [screenshot]
- After interaction: [screenshot]
```

### Level 3: Acceptance Criteria Verification

For each acceptance criterion in `current-task.json`:

```markdown
## Acceptance Criteria Verification

### Criterion 1: "Vehicle responds to WASD input"

- **Test**: Pressed W, A, S, D keys
- **Result**: ✅ PASS / ❌ FAIL
- **Notes**: Vehicle moves forward, left, backward, right correctly

### Criterion 2: "Physics simulation runs at 60Hz"

- **Test**: Checked physics debug panel
- **Result**: ✅ PASS / ❌ FAIL
- **Notes**: Physics running at target rate
```

### Level 4: Performance Validation

```markdown
## Performance Check

- [ ] FPS stable at 60 (or target)
- [ ] No memory leaks during extended use
- [ ] Load time acceptable (< 3s)
- [ ] No stuttering during interaction

### Metrics:

- Initial FPS: \_\_
- FPS after 60s: \_\_
- Memory usage: \_\_ MB
- Load time: \_\_ s
```

## Decision Framework

| Check Result                     | Action              |
| -------------------------------- | ------------------- |
| All automated pass, browser pass | Mark as PASSED      |
| Automated pass, browser fails    | Mark as NEEDS_FIXES |
| Automated fails                  | Mark as NEEDS_FIXES |
| Any console errors               | Mark as NEEDS_FIXES |

## Anti-Patterns

❌ **DON'T:**

- Skip browser testing
- Assume automated tests are sufficient
- Mark as passed without checking acceptance criteria
- Ignore console warnings
- Skip performance verification

✅ **DO:**

- Always test in browser
- Verify each acceptance criterion
- Take screenshots as evidence
- Document any concerns
- Check console for errors

## Pass Protocol

When ALL checks pass:

**Step 1: Delete validation screenshots** (no longer needed for passing tasks)

```bash
# PowerShell
Remove-Item ".claude/session/screenshots/${taskId}-*.png" -Force -ErrorAction SilentlyContinue

# Bash
rm .claude/session/screenshots/${taskId}-*.png 2>/dev/null || true
```

**Step 2: Update task files**

```json
// Update current-task.json
{
  "status": "passed",
  "validatedAt": "{{ISO_TIMESTAMP}}"
}

// Update prd.json
{
  "items": [{
    "id": "{{TASK_ID}}",
    "passes": true,
    "status": "passed"
  }]
}
```

Commit validation:

```
[ralph] [qa] feat-XXX: Validation PASSED

- TypeScript: pass
- Lint: pass
- Tests: pass
- Build: pass
- Browser: pass

All acceptance criteria verified.

PRD: feat-XXX | Agent: qa | Iteration: N
```

## Fail Protocol

When ANY check fails:

```json
// Update current-task.json
{
  "status": "needs_fixes",
  "bugNotes": "Detailed description of failures...",
  "retryCount": {{PREVIOUS + 1}}
}
```

Include in bug notes:

- Which check failed
- Error messages
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

## Checklist

Before marking as passed:

- [ ] `npm run type-check` — 0 errors
- [ ] `npm run lint` — 0 warnings
- [ ] `npm run test` — all pass
- [ ] `npm run build` — succeeds
- [ ] Browser loads correctly
- [ ] No console errors
- [ ] All acceptance criteria verified
- [ ] Performance acceptable
- [ ] Screenshots taken

## Reference

- [agents/qa/AGENT.md](../../AGENT.md) — Full QA instructions
- [agents/qa/skills/browser-testing.md](browser-testing.md) — Browser testing guide
- [agents/qa/skills/bug-reporting.md](bug-reporting.md) — Bug report format
