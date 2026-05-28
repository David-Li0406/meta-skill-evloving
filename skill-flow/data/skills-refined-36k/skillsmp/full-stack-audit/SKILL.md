---
name: full-stack-audit
description: Verifies the integrity of the OlyBars platform (Vibe, Database, Frontend).
---

# Full Stack Audit Skill

## 1. Mode Selection (CRITICAL)
Before running an audit, determine the execution environment:

### A. HEADLESS MODE (Default for CI/CD or Quick Checks)
**Trigger:** User asks for "data check", "backend verification", or "integrity check".
**Action:** Execute the `vibe-data-integrity` workflow.
**Command:** `@agent /vibe-data-integrity`
**Why:** Faster, verifies Firestore <-> API logic without needing a browser.

### B. VISUAL MODE (Browser Agent)
**Trigger:** User asks for "UI check", "Vibe check", "frontend audit", or "visual verification".
**Action:**
1. Use the Browser Subagent.
2. Navigate to `http://localhost:5173`.
3. Visually verify:
   - "Buzz" badge is RED and PULSING.
   - "Drops" (formerly Points) are visible.
   - Map pins update in real-time.

## 2. Standard Procedure
1. Always run `npm run type-check` before auditing to ensure no silent TS errors.
2. Report results in the "OlyBars Audit Format" (Pass/Fail per component).
