---
name: smart-mode
description: >
  This skill should be invoked when running /auto-smart command, when needing to assess task complexity,
  when choosing between DIRECT and ORCHESTRATED execution modes, when enforcing evidence gates,
  or when handling failures with pivot/research/checkpoint strategies.
  Provides the core intelligence for Smart Ralph autonomous development.
---

# Smart Mode - Intelligent Autonomous Execution

Core intelligence for `/auto-smart` command. Handles complexity scoring, mode selection, evidence gates, and failure recovery.

## When This Skill Activates

- `/auto-smart` command is invoked
- Need to assess task complexity (1-5 scale)
- Choosing execution mode (DIRECT vs ORCHESTRATED)
- Enforcing evidence-based verification
- Recovering from failures (pivot → research → checkpoint)

## Core Concepts

### Complexity Scoring

Score every task 1-5 based on scope:

| Score | Mode | Characteristics |
|-------|------|-----------------|
| 1-2 | DIRECT | Simple, few files, clear scope |
| 3-5 | ORCHESTRATED | Complex, many files, needs phases |

See `references/complexity-rubric.md` for detailed scoring criteria.

### Execution Modes

**DIRECT Mode (Score 1-2):**
- Simple iterative loop
- Work until done
- Evidence gate before completion
- No decomposition needed

**ORCHESTRATED Mode (Score 3-5):**
- Decompose into 2-5 phases
- Checkpoint after each phase
- Evidence gate per phase
- Supports multi-session resume

### Evidence Gates (MANDATORY)

Every claim MUST include verification:

```
✅ VALID:
"Implemented feature X [VERIFIED: npm test → 12 passing]"
"Fixed bug Y [VERIFIED: manual test confirms fix]"
"Added component Z [VERIFIED: npm run build → success]"

❌ INVALID:
"I implemented the feature" (no evidence)
"Should work now" (speculation)
"Tests probably pass" (not verified)
```

**Red Flag Words** (trigger re-verification):
- "should", "probably", "I think", "seems to", "likely"

### Failure Recovery

See `references/failure-handling.md` for complete protocol.

**Quick Reference:**
1. **PIVOT** (first 3 attempts) - Try alternative approach
2. **RESEARCH** (next 3 attempts) - Read more code, understand better
3. **CHECKPOINT** (after 6 failed attempts) - Save state, report stuck

## Protocol

### Step 1: Analyze Complexity

Parse the user's request and score 1-5:

```
Analyze: "<user prompt>"

Factors:
- Estimated files affected: N
- Keywords detected: [list]
- Features mentioned: N
- Complexity signals: [list]

Score: X/5
Mode: DIRECT|ORCHESTRATED
Reasoning: "..."
```

### Step 2: Initialize State

Create `.claude/smart-ralph/state.yaml`:

```yaml
version: "1.0"
mode: DIRECT|ORCHESTRATED
phase: ANALYZE|EXECUTE|VERIFY
complexity:
  score: N
  reasoning: "explanation"
  mode_selected: DIRECT|ORCHESTRATED
started_at: "ISO timestamp"
prompt: "original user prompt"
orchestrated_phases: []  # only for ORCHESTRATED
failure_recovery:
  pivot_count: 0
  research_count: 0
  last_error: null
```

### Step 3: Execute (Mode-Dependent)

**DIRECT Mode:**
1. Understand task clearly
2. Implement with TDD when applicable
3. Verify each change
4. Collect evidence
5. Complete when all verified

**ORCHESTRATED Mode:**
1. Decompose into 2-5 phases
2. Execute phase 1
3. Checkpoint + evidence gate
4. Continue to next phase
5. Final verification after all phases

### Step 4: Handle Failures

If stuck (same error 3x, no progress):

1. **PIVOT:** Identify failure, list alternatives, try different approach
2. **RESEARCH:** If pivot fails 3x, read more code, understand context
3. **CHECKPOINT:** If research fails 3x, save state, output STUCK

Update state after each recovery attempt:
```yaml
failure_recovery:
  pivot_count: 2
  research_count: 1
  last_error: "description of what's failing"
```

### Step 5: Verify and Complete

Before outputting COMPLETE:

1. Run all verification commands (test, build, lint, typecheck)
2. Document each result with evidence
3. Ensure NO red flag words in claims
4. Output structured completion summary

## State Management

### File Locations

All state in `.claude/smart-ralph/`:
- `state.yaml` - Machine-readable execution state
- `progress.md` - Human-readable progress report
- `stuck-report.md` - Only created if STUCK (detailed context)

### Progress File Format

```markdown
## Smart Ralph Progress

**Task:** <original prompt>
**Mode:** DIRECT|ORCHESTRATED (Complexity: X/5)
**Started:** <timestamp>
**Status:** in_progress|complete|stuck

### Completed
- [x] Phase/Step 1: Description [VERIFIED: evidence]

### In Progress
- [ ] Phase/Step 2: Description

### Evidence Collected
- `npm test` → 24 passing
- `npm run build` → success
```

### Resume Detection

On session start, check for incomplete state:
1. Read `.claude/smart-ralph/state.yaml`
2. If exists and phase != COMPLETE → resume
3. Load progress and continue from last checkpoint

## Integration with autonomous-dev

Smart Mode reuses:
- `project-detector` skill for tech stack detection
- `verification-runner` skill for test/build/lint
- `task-decomposer` skill (only in ORCHESTRATED mode)
- Result filtering patterns for token efficiency

## Key Differences from /auto

| Aspect | /auto | /auto-smart |
|--------|-------|-------------|
| Approval gates | Phase 3, Phase 6 | **None** |
| Complexity detection | Manual classification | **Automatic** |
| Failure handling | Manual intervention | **Auto pivot/research** |
| Mode selection | Always full workflow | **Adaptive** |
| Resume | /auto-continue | **Automatic** |
