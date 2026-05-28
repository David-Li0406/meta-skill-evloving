# Ralph Methodology: Atomic Implementation Pattern

*"I'm helping!" - Ralph Wiggum*

## Overview

The Ralph Methodology is an **industry-validated pattern** for implementing PRPs through atomic, test-verified steps. It combines insights from Anthropic's official guidance, AWS agentic patterns, and practical engineering workflows.

---

## Core Philosophy

> "LLMs do best when given focused prompts: implement one function, fix one bug, add one feature at a time."
> — Addy Osmani, Google

**Principles:**
1. **Atomic steps** - Each step does ONE thing
2. **Immediate verification** - Test right after build
3. **Bounded retries** - Max 3 attempts with learning
4. **Stop on failure** - Human fixes before continuing
5. **Gates at boundaries** - Major checkpoints between phases

---

## The Loop

```
┌─────────────────────────────────────────────────────────────┐
│  RALPH LOOP                                                 │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  BUILD   │───▶│   TEST   │───▶│  PASS?   │──YES──▶ NEXT │
│  │ step-N   │    │ test-N   │    │          │              │
│  └──────────┘    └──────────┘    └────┬─────┘              │
│       ▲                               │ NO                  │
│       │                               ▼                     │
│       │         ┌─────────────────────────────┐            │
│       │         │  RETRY (with failure reason) │            │
│       │         │  - Include error message     │            │
│       │         │  - Adjust temperature +0.1   │            │
│       └─────────│  - Max 3 attempts            │            │
│                 └─────────────────────────────┘            │
│                               │                             │
│                               ▼ (after 3 fails)            │
│                 ┌─────────────────────────────┐            │
│                 │  STOP - Human intervention   │            │
│                 │  Fix issues before continuing│            │
│                 └─────────────────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
{project}/
├── ralph.sh                 # Main runner
├── ralph-results.json       # Progress tracking
└── ralph-steps/
    ├── step-01.sh          # Atomic build scripts
    ├── test-01.sh          # Verification scripts
    ├── step-02.sh
    ├── test-02.sh
    ├── ...
    ├── gate-1.sh           # Phase boundary checkpoints
    ├── gate-2.sh
    └── PRP-COVERAGE.md     # Maps PRP deliverables to steps
```

---

## Step Script Template

```bash
#!/bin/bash
# Step NN: [Brief description]
# PRP Deliverable: [Reference to PRP section]
# Objective: [Single, atomic objective]

set -e

# === INIT CHECK ===
# Verify app not left in broken state
echo "Checking prerequisites..."
if ! npm run build 2>/dev/null; then
  echo "ERROR: Build broken before starting. Fix first."
  exit 1
fi

# === BUILD ===
echo "Step NN: [Description]"

# [Atomic implementation code here]
# - Create ONE file, or
# - Add ONE feature, or
# - Fix ONE issue

# === COMPLETION ===
echo ""
echo "Step NN complete"
echo "Run: ./ralph-steps/test-NN.sh"
```

---

## Test Script Template

```bash
#!/bin/bash
# Test NN: Verify [what was built]
# PRP Deliverable: [Reference]

set -e
echo "=== TEST NN: [Description] ==="

PASS_COUNT=0
FAIL_COUNT=0
TOTAL=0

check() {
  ((TOTAL++))
  if eval "$1"; then
    echo "  [PASS] $2"
    ((PASS_COUNT++))
  else
    echo "  [FAIL] $2"
    ((FAIL_COUNT++))
  fi
}

# === AUTOMATED CHECKS ===
check "[ -f 'path/to/file.tsx' ]" "File exists"
check "grep -q 'expectedContent' path/to/file.tsx" "Contains expected code"
check "npm run build 2>/dev/null" "Build passes"
check "npm run typecheck 2>/dev/null" "TypeScript passes"

# === PLAYWRIGHT MCP VERIFICATION ===
echo ""
echo "=== PLAYWRIGHT MCP VERIFICATION ==="
echo "1. mcp__playwright__browser_navigate({url: 'http://localhost:3000/path'})"
echo "2. mcp__playwright__browser_snapshot()"
echo ""
echo "PASS criteria:"
echo "  - [Specific element] visible"
echo "  - [Specific behavior] works"
echo "  - No console errors"

# === ACCESSIBILITY CHECK ===
echo ""
echo "=== ACCESSIBILITY (Invariant #11) ==="
echo "  - Tab through elements - logical order"
echo "  - Focus indicators visible"
echo "  - Touch targets >= 44px"

# === RESULT ===
echo ""
echo "Automated: $PASS_COUNT / $TOTAL passed"

if [ "$FAIL_COUNT" -gt 0 ]; then
  echo "STATUS: FAIL"
  exit 1
else
  echo "STATUS: PASS (pending Playwright verification)"
  exit 0
fi
```

---

## Gate Script Template

```bash
#!/bin/bash
# Gate N: [Phase name] Validation
# PRP Phase: [Reference]
#
# GATE_PASS := ALL(
#   build_exit_code == 0,
#   typecheck_errors == 0,
#   [specific criteria],
#   [performance targets]
# )

set -e
echo "═══════════════════════════════════════════════════════"
echo "  GATE N: [Phase Name]"
echo "═══════════════════════════════════════════════════════"

PASS=0
FAIL=0
TOTAL=5

gate_check() {
  if eval "$1"; then
    echo "[PASS] $2"
    ((PASS++))
  else
    echo "[FAIL] $2"
    ((FAIL++))
  fi
}

# Check 1: Build
gate_check "npm run build 2>/dev/null" "Build successful"

# Check 2: TypeScript
gate_check "npx tsc --noEmit 2>/dev/null" "TypeScript passes"

# Check 3-5: [Phase-specific checks]
# ...

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  GATE N RESULTS: $PASS / $TOTAL"
echo "═══════════════════════════════════════════════════════"

if [ "$FAIL" -eq 0 ]; then
  echo "STATUS: GATE PASSED"
  exit 0
else
  echo "STATUS: GATE FAILED"
  exit 1
fi
```

---

## Enhanced Runner (ralph.sh)

Key enhancements from research:

### 1. Failure Reason in Retries

```bash
retry_with_feedback() {
  local step=$1
  local attempt=$2
  local last_error=$3

  echo "Retry $attempt with failure context:"
  echo "Previous error: $last_error"

  # Pass failure reason to step script via env var
  RALPH_LAST_ERROR="$last_error" \
  RALPH_ATTEMPT="$attempt" \
  bash "$STEPS_DIR/step-$step.sh"
}
```

### 2. Temperature Adjustment (for LLM-driven steps)

```bash
# Start deterministic, increase on retry
RALPH_TEMPERATURE=$(echo "scale=1; 0 + ($attempt - 1) * 0.1" | bc)
export RALPH_TEMPERATURE
```

### 3. Init Check Before Each Step

```bash
init_check() {
  echo "Running init check..."
  if ! npm run build 2>/dev/null; then
    echo "ERROR: App in broken state. Fix before continuing."
    echo "Last known good: step $((current - 1))"
    exit 1
  fi
}
```

### 4. Independent Verifier (for critical steps)

```bash
# Optional: Use separate agent to verify
if [[ -f "$STEPS_DIR/verify-$step.sh" ]]; then
  echo "Running independent verification..."
  bash "$STEPS_DIR/verify-$step.sh"
fi
```

---

## PRP Coverage Matrix

Every Ralph implementation must include a `PRP-COVERAGE.md` that maps:

```markdown
# PRP to Ralph Steps Coverage

## PRP Deliverable → Step Mapping

| PRP Section | Deliverable | Step | Test | Status |
|-------------|-------------|------|------|--------|
| Phase 1.1 | Next.js setup | step-01 | test-01 | Covered |
| Phase 1.1 | Supabase client | step-02 | test-02 | Covered |
| ... | ... | ... | ... | ... |

## Coverage Summary

| Phase | Deliverables | Steps | Coverage |
|-------|--------------|-------|----------|
| 1.1 | 5 | 5 | 100% |
| 1.2 | 7 | 7 | 100% |
| Total | 12 | 12 | 100% |
```

---

## Research Validation

This methodology is validated by:

| Source | Key Insight |
|--------|-------------|
| [Anthropic Official](https://www.anthropic.com/engineering/claude-code-best-practices) | "Break work into discrete, verifiable phases" |
| [AWS Agentic Patterns](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/evaluator-reflect-refine-loop-patterns.html) | "Loop repeats until criteria met or retry limit reached" |
| [Addy Osmani](https://addyosmani.com/blog/ai-coding-workflow/) | "One function, one bug, one feature at a time" |
| [Armin Ronacher](https://lucumr.pocoo.org/2025/6/12/agentic-coding/) | "The dumbest possible thing that will work" |
| [LLMLOOP Research](https://valerio-terragni.github.io/assets/pdf/ravi-icsme-2025.pdf) | "Temperature adjustment on retry" |

---

## When to Use Ralph

**Use Ralph when:**
- Implementing a validated PRP
- Building features that need incremental verification
- Working in unfamiliar codebase
- Need audit trail of implementation

**Don't use Ralph when:**
- Quick one-off fix
- Exploratory prototyping
- Research/discovery phase

---

## Integration with Design Ops

```
Spec → Stress Test → Validate → Generate PRP → Ralph Steps → Gates → Done
                                      │
                                      ▼
                              PRP-COVERAGE.md
                                      │
                                      ▼
                              step-01 → test-01
                              step-02 → test-02
                                  ...
                              gate-1 (checkpoint)
                                  ...
                              gate-final (complete)
```

---

## Spec Delta Mechanism

When implementation reveals spec gaps, follow this process:

### 1. Document the Gap
```markdown
**Gap:** [What was missing]
**Root cause:** [Why it was missed]
**Impact:** [What broke or was missing in implementation]
```

### 2. Update the Spec
- Add missing section to spec (e.g., F0: Entry Points)
- Increment version number
- Add changelog entry

### 3. Generate Delta PRP
- Create mini-PRP for just the missing feature
- Reference original PRP for context
- Include only the new steps needed

### 4. Generate Delta Steps
- Add new ralph steps (e.g., step-34, step-35)
- Include tests for new functionality
- Don't modify existing passing steps

### 5. Update Learnings
- Add to project's SPEC-CONVENTIONS.md
- Capture pattern to prevent future gaps

### Common Spec Gaps

| Gap Type | Symptom | Prevention |
|----------|---------|------------|
| Missing entry points | "How does user get here?" | Always start with F0: Entry Points |
| State-blind UI | UI doesn't change based on auth/data | Document all UI states |
| Implicit navigation | Journey assumes user knows URLs | Trace full click path |
| Error path gaps | Only happy path documented | Ask "what if X fails?" |
| **UI shell without data** | List shows empty after import | Require "Data Source" in spec |
| **Schema type mismatch** | Insert fails with type error | Validate field types match schema |
| **Silent async failures** | Page hangs forever | Require timeout + error UI |

### Critical Test Requirements

**Every list page test MUST verify:**
1. Empty state renders when no data
2. Data fetching actually executes (not just UI)
3. After insert: navigate back → see inserted data

**Every async operation MUST have:**
1. Timeout (max 10 seconds for user-facing)
2. Error state UI (not just loading)
3. Console logging for debugging

**Every insert operation MUST:**
1. Match schema field types (UUID vs string)
2. Create parent records before FK inserts
3. Return inserted ID for verification

---

*Version: 1.1*
*Last updated: 2026-01-20*
*Based on: Anthropic, AWS, Addy Osmani, Armin Ronacher research*
