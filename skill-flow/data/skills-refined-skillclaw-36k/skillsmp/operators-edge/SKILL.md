---
name: operators-edge
description: Runs the Operator's Edge loop (State, Proof, Gates + adaptation checks). Use for any coding task, debugging, refactor, or system change.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Operator's Edge v3.9+ Rules

## Core Principle
> **Policy is not enforcement. Hooks are enforcement.**

This skill provides behavioral guidance. Mechanical enforcement happens via hooks in `.claude/hooks/`.

---

## 1. State Management

### Before Acting
- Read `active_context.yaml` to understand:
  - Current objective
  - Plan and current_step
  - Constraints and risks
  - Memory (lessons with triggers)
  - Any unresolved mismatches

### After Each Step
Update `active_context.yaml` with:
- Step status change (`pending` → `in_progress` → `completed`)
- Proof path
- Any mismatches (expected vs actual)
- New lessons learned

---

## 2. The 6-Check Adaptation Loop

Run these checks on every significant action:

### Check 1: Mismatch Detection
- Expected vs actual diverged?
- Log: `expected`, `observation`, `delta`, `suspected_cause`
- **Fail mode to avoid**: Plowing forward confidently

### Check 2: Plan Revision
- On mismatch: write NEW approach, don't "try again"
- Reduce step size, add guards
- **Fail mode to avoid**: Repeating same step 3x

### Check 3: Tool Switching
- Tool failing? Try alternative
- Prefer simpler, robust methods
- **Fail mode to avoid**: Treating tools as fixed

### Check 4: Memory Update
- Learned something reusable?
- Add lesson with trigger pattern
- **Fail mode to avoid**: Repeating identical mistakes

### Check 5: Proof Generation
- Attach evidence, not just output
- Valid: tests, logs, diffs, screenshots
- **Fail mode to avoid**: "Trust me" text

### Check 6: Stop Condition
- Uncertain? Ask ONE crisp question
- Blocked? Present 2-3 bounded options
- **Fail mode to avoid**: Never asking OR pestering

---

## 3. Proof-by-Default

Every step must produce proof. Auto-captured by `post_tool.py`:
- Command outputs → `.proof/session_log.jsonl`
- File changes with diffs
- Test results

Manual proof goes in `.proof/latest.md`.

---

## 4. Gates (Enforced by Hooks)

### Hard Blocked (pre_tool.py)
- `rm -rf /`, `git reset --hard`, etc.
- Cannot bypass

### Require Confirmation
- `git push`, `kubectl`, `terraform`, etc.
- Deploy operations
- File deletions

### Soft Gates
- Edits without plan (asks, can override)
- Edits without risks identified (asks, can override)

---

## 5. Memory System

### Structure
```yaml
memory:
  - trigger: "keyword or pattern"
    lesson: "What to remember"
    reinforced: 1
    last_used: "2025-01-06"
```

### Usage
- Surface relevant lessons when trigger matches context
- Reinforce on successful use
- Decay unused lessons (archive after threshold)

### Best Practices
- Capture at resolution, not scoring
- Theme-based similarity catches semantic dupes
- "Memory is taste, not storage"

---

## 6. Three Gears (v3.9+)

### ACTIVE
- Objective exists and has pending/in_progress steps
- Execute plan steps, halt at junctions
- Quality gate runs before transition to PATROL
- On errors, remain in ACTIVE and surface failure

### PATROL
- Objective complete (all steps completed)
- Scout scan for issues and surface findings
- Findings trigger a junction for user selection
- On scan error, remain in PATROL and surface failure

### DREAM
- No objective or no pending work
- Reflect, consolidate, propose (rate-limited)
- If proposal generated, pause at junction
- If no proposal, transition back to PATROL

---

## 7. Self-Scoring

After completing objective, score 0-6:

```yaml
self_score:
  timestamp: "ISO timestamp"
  checks:
    mismatch_detection:
      met: true/false
      note: "evidence"
    plan_revision:
      met: true/false
      note: "evidence"
    tool_switching:
      met: true/false
      note: "evidence"
    memory_update:
      met: true/false
      note: "evidence"
    proof_generation:
      met: true/false
      note: "evidence"
    stop_condition:
      met: true/false
      note: "evidence"
  total: 0-6
  level: "demo_automation|promising|real_agent"
```

---

## 8. Commands Reference

### v4.0 Mode Commands (Preferred)

| Command | Purpose |
|---------|---------|
| `/edge` | Smart orchestrator with mode awareness |
| `/edge plan` | Enter PLAN mode - explore and create plan |
| `/edge active` | Enter ACTIVE mode - execute plan steps |
| `/edge review` | Enter REVIEW mode - verify completion |
| `/edge done` | Enter DONE mode - archive and clear |

### Other Commands

| Command | Purpose |
|---------|---------|
| `/edge-yolo` | Dispatch mode (autopilot) |
| `/edge-prune` | Reduce state entropy |
| `/edge-research` | Generate research prompts |

### Legacy Commands (Still Work)

| Command | Suggested Alternative |
|---------|----------------------|
| `/edge-plan` | `/edge plan` |
| `/edge-step` | `/edge` in ACTIVE mode |

---

## 9. File Locations

```
active_context.yaml      # Living state
.proof/session_log.jsonl # Auto-captured proof
.proof/archive.jsonl     # Historical record
.claude/state/gear_state.json      # Gear runtime state
.claude/state/junction_state.json  # Junction gate state (source of truth)
.claude/state/dispatch_state.json  # Dispatch mode state (edge-yolo)
.claude/state/                     # Hook runtime state (hashes, failure logs)
.claude/hooks/           # Enforcement code
.claude/commands/        # Slash commands
.claude/agents/          # Subagent definitions
.claude/skills/          # This skill
```
