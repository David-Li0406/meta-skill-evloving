# Implement Feature Workflow

The core workflow for automated UI feature implementation.

## Triggers

- "implement next feature"
- "implement the [feature name]"
- "build the [component]"
- "implement feature from [file path]"

## Workflow Steps

### 1. Parse Feature Specification

Identify the feature source:

```
Source Types:
1. Verbal description → Extract from user message
2. File path → Read spec from thoughts/features/ or plan file
3. Figma link → Fetch design via Figma API
4. Current plan → Read from active plan file
```

**Extract:**
- Feature name (for history directory)
- Component(s) to create/modify
- Design reference (Figma link or description)
- Acceptance criteria

### 2. Setup Environment

```bash
# Check/start dev server
bun ${SKILL_DIR}/tools/server-manager.ts status

# If not running:
bun ${SKILL_DIR}/tools/server-manager.ts start

# Wait for ready
bun ${SKILL_DIR}/tools/server-manager.ts wait-ready
```

### 3. Launch Browser (if not already open)

```bash
# Capture current state before changes
bun ${SKILL_DIR}/tools/playwright-runner.ts capture \
  --url http://localhost:${PORT} \
  --output-dir ${SKILL_DIR}/history/${FEATURE_ID}
```

### 4. Implement Feature

Delegate to `frontend-design` skill or implement directly:

```
Implementation Checklist:
- [ ] Create/modify component files
- [ ] Add necessary imports
- [ ] Style with Tailwind (or project CSS system)
- [ ] Wire up to page/route
- [ ] Add any required state management
```

**Important:** Wait for HMR after each file save (configurable delay, default 2s).

### 5. Verify Implementation

Run verification workflow:

```bash
# Full capture after implementation
bun ${SKILL_DIR}/tools/playwright-runner.ts full \
  --url http://localhost:${PORT} \
  --output-dir ${SKILL_DIR}/history/${FEATURE_ID}
```

Read `capture.json` and check:

| Check | Pass Criteria |
|-------|---------------|
| Console errors | Zero errors |
| Network failures | Zero 4xx/5xx |
| TypeScript | `bun tsc --noEmit` passes |
| Visual match | Claude vision confirms match to spec |

### 6. Evaluate Results

```
IF all checks pass:
  → Mark feature complete
  → Generate completion report
  → Proceed to next feature (if any)

IF checks fail:
  → Enter fix-errors workflow
  → Track iteration count
```

### 7. Iteration Loop (if needed)

```
WHILE errors exist AND iteration < maxIterations:
  1. Categorize errors (console/TS/network/visual)
  2. Apply fix via Edit tool
  3. Wait for HMR
  4. Re-verify
  5. iteration++

IF iteration >= maxIterations:
  → Escalate with detailed report
  → Ask Jean-Marc for guidance
```

## State Management

Update `state.json` at each step:

```json
{
  "currentFeature": "hero-section",
  "iteration": 0,
  "status": "implementing",
  "errors": [],
  "lastScreenshot": null
}
```

Status values:
- `idle` - No active feature
- `implementing` - Writing code
- `verifying` - Running checks
- `fixing` - In iteration loop
- `complete` - Feature done
- `escalated` - Hit max iterations

## Completion Report

Generate `history/${FEATURE_ID}/report.md`:

```markdown
# Feature Implementation Report

**Feature:** ${FEATURE_NAME}
**Status:** Complete | Escalated
**Iterations:** ${COUNT}
**Duration:** ${TIME}

## Changes Made
- Created: ${FILES_CREATED}
- Modified: ${FILES_MODIFIED}

## Verification Results
- Console: ${PASS/FAIL}
- Network: ${PASS/FAIL}
- TypeScript: ${PASS/FAIL}
- Visual: ${PASS/FAIL}

## Screenshots
- Before: history/${FEATURE_ID}/before.png
- After: history/${FEATURE_ID}/iteration-${N}.png

## Notes
${ANY_ISSUES_OR_OBSERVATIONS}
```

## Example Invocation

User: "implement the hero section based on the Figma design"

Agent:
1. Extracts Figma link from conversation or spec
2. Fetches design screenshot via Figma API
3. Starts dev server (detects port 5173)
4. Takes "before" screenshot
5. Creates `src/components/Hero.tsx`
6. Styles with Tailwind
7. Adds to `src/pages/index.tsx`
8. Waits 2s for HMR
9. Takes "after" screenshot
10. Verifies: no console errors, no TS errors, visual match
11. Reports completion

## Integration Points

| Skill/Agent | Usage |
|-------------|-------|
| `frontend-design` | Delegate complex component design |
| `fix-errors` workflow | Handle verification failures |
| `engineer` agent | Escalate complex bugs |
