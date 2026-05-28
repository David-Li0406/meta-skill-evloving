---
name: session
description: "Use when work spans multiple phases, requires context handoff, or exceeds single conversation scope. Triggers - session, multi-phase, handoff, continue, resume, checkpoint, long-running."
---

# Session Management

**Iron Law:** CONTEXT PRESERVED IS CONTEXT RECOVERED. Document state before transition.

## Overview

Session management enables work continuity across multiple conversations, phases, or agent handoffs. The session file is the single source of truth - everything needed to resume work must be documented there.

## When to Use

- Work spans multiple conversations
- Complex features requiring phased implementation
- Handoff between specialists or agents
- Long-running tasks with natural break points
- Any work that might be interrupted and resumed

## Session File Structure

Sessions live in `.claude/tasks/` directory:

```
.claude/tasks/
  session-current.md    # Active session
  session-001.md        # Archived sessions
  session-002.md
  session-template.md   # Template for new sessions
```

## The Session Lifecycle

```
1. CREATE   -> Initialize session file with context
2. WORK     -> Execute with continuous documentation
3. CHECKPOINT -> Save state at natural break points
4. HANDOFF  -> Transfer context to next phase/agent
5. RESUME   -> Recover from documented state
6. ARCHIVE  -> Close session, extract learnings
```

## Step 1: Create - Initialize Session

When starting multi-phase work:

```markdown
# Session [Number] - [Descriptive Title]

## Session Context

**Created**: [timestamp]
**Goal**: [single sentence describing end state]
**Trigger**: [user request or continuation from prior session]
**Estimated Scope**: [Small/Medium/Large]
**Dependencies**: [external systems, prior work needed]

## Success Criteria

1. [Specific, measurable outcome]
2. [Specific, measurable outcome]
3. [Specific, measurable outcome]

## Phase Breakdown

### Phase 1: [Name]
**Status**: Not Started
**Prerequisites**: [list]
**Deliverables**: [list]

### Phase 2: [Name]
**Status**: Not Started
**Prerequisites**: Phase 1 complete
**Deliverables**: [list]

## Current State

**Active Phase**: Phase 1
**Last Action**: Session created
**Next Action**: [first task]
**Blockers**: None
```

**Naming Convention:** `session-current.md` for active work, renamed to `session-XXX-[topic].md` on archive.

## Step 2: Work - Execute with Documentation

During execution, update session file continuously:

```markdown
## Work Log

### [Timestamp] - [Agent/Phase]

**Action**: [what was done]
**Result**: [outcome]
**Files Modified**: [list]
**Decisions Made**: [key choices]
**Context for Next**: [what successor needs to know]
```

**Update Frequency:**
- After each significant action
- Before any break or handoff
- When encountering blockers
- After decisions that affect future work

## Step 3: Checkpoint - Save State

Checkpoints are explicit save points for recovery:

```markdown
## Checkpoint [Number]

**Timestamp**: [when]
**Phase**: [which phase]
**Progress**: [X/Y tasks complete]
**State Summary**: [one paragraph describing current state]

### What's Working
- [feature/component that is complete and verified]

### What's In Progress
- [task currently being worked on]
- [current status and next immediate step]

### What's Blocked
- [blocker and what's needed to resolve]

### What's Next
- [immediate next action when work resumes]

### Recovery Commands
```bash
# To verify current state:
npm test
git status

# To continue from here:
[specific command or file to start with]
```
```

**Create checkpoints:**
- At natural break points
- Before risky operations
- At phase transitions
- Every 30-60 minutes of work
- Before any handoff

## Step 4: Handoff - Transfer Context

When passing work to another agent or phase:

```markdown
## Handoff Record

**From**: [agent/phase]
**To**: [agent/phase]
**Timestamp**: [when]

### Context Transfer

**What Was Accomplished**:
1. [completed item with evidence]
2. [completed item with evidence]

**Current State**:
- Active branch: `feature/auth-flow`
- Tests: 23/23 passing
- Build: Clean

**What Needs to Happen Next**:
1. [specific task with clear scope]
2. [specific task with clear scope]

**Gotchas and Warnings**:
- [thing that might trip up successor]
- [non-obvious dependency or quirk]

**Files to Review First**:
1. `src/auth/middleware.ts` - Core logic lives here
2. `tests/auth.test.ts` - Test patterns established

**Questions for Successor**:
- [decision that needs to be made]
- [ambiguity to resolve]
```

## Step 5: Resume - Recover from State

When continuing from a checkpoint:

```markdown
## Resume Protocol

### 1. Read Session File Completely
Do NOT start work until full context is understood.

### 2. Verify State Matches Documentation
```bash
# Run recovery commands from last checkpoint
npm test        # Should match documented state
git status      # Should match documented state
```

### 3. Check for External Changes
- Did codebase change since checkpoint?
- Did dependencies update?
- Did requirements change?

### 4. Document Resume Point
**Resumed At**: [timestamp]
**Resuming From**: Checkpoint [N]
**State Verification**: [Matches / Diverged]
**Adjustments Needed**: [None / describe]

### 5. Continue from Last Next Action
[Begin work from documented next step]
```

**If state doesn't match:** Document divergence, assess impact, adjust plan.

## Step 6: Archive - Close Session

When session work is complete:

```markdown
## Session Closure

**Completed**: [timestamp]
**Duration**: [total time across all phases]
**Final Status**: Complete / Partial / Abandoned

### Accomplishments
1. [what was built/fixed/improved]
2. [what was built/fixed/improved]

### Learnings
- [pattern discovered worth remembering]
- [gotcha to avoid next time]

### Follow-up Items
- [ ] [work that should happen in future session]
- [ ] [tech debt incurred]

### Files Created/Modified
[list for reference]

### Archive Action
Rename to: `session-XXX-[topic].md`
Create new: `session-current.md` from template
```

## Session File Template

```markdown
# Session [Number] - [Title]

## Session Context
**Created**: [timestamp]
**Goal**: [what we're trying to achieve]
**Trigger**: [what initiated this session]
**Scope**: Small / Medium / Large

## Success Criteria
1. [criterion]
2. [criterion]

## Phase Breakdown
### Phase 1: [Name]
**Status**: Not Started / In Progress / Complete
**Prerequisites**: [list]
**Deliverables**: [list]

## Current State
**Active Phase**: [phase]
**Last Action**: [what happened]
**Next Action**: [what to do]
**Blockers**: [none or describe]

## Work Log
### [Timestamp] - [Agent/Phase]
**Action**:
**Result**:
**Files Modified**:
**Context for Next**:

## Checkpoints
### Checkpoint 1
**Timestamp**:
**State Summary**:
**Recovery Commands**:

## Handoffs
### Handoff 1
**From**: **To**:
**Context Transfer**:

## Session Closure
**Status**: Open
```

## Examples

### Good Session Management

```
Session: Authentication Feature

Phase 1 Complete - Schema design (Checkpoint 1)
  - users table created
  - sessions table created
  - Tests: 5/5 passing

Handoff to Phase 2 (Backend)
  - Context: Schema ready in migrations/
  - Next: Create auth middleware
  - Gotcha: Session expiry needs config

Phase 2 In Progress - Checkpoint 2
  - Middleware complete
  - Login endpoint complete
  - Next: Logout endpoint
  - Blocker: None

[Clear trail for anyone resuming]
```

### Bad Session Management (DO NOT DO THIS)

```
"I worked on auth stuff yesterday. Let me continue...
I think I was doing the login endpoint? Or was it
the middleware? Let me check git log..."

[No session file, no state, no recovery path]
```

**Why wrong:** No documented state, guessing at progress, wasted time recovering.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll remember where I was" | No, you won't. Document it. |
| "Session files are overhead" | Recovery time without them is 10x higher. |
| "The code is self-documenting" | Code shows WHAT, not WHY or WHAT'S NEXT. |
| "Short tasks don't need sessions" | If it might be interrupted, it needs a session. |
| "I'll update at the end" | Update continuously. End might not come cleanly. |
| "Handoffs are just for teams" | Future you is a different context. Document handoffs. |
| "Checkpoints slow me down" | Checkpoints enable recovery when things go wrong. |

## Red Flags - STOP and Start Over

- Working without a session file for multi-phase work
- No checkpoints in active session
- Session file out of sync with actual state
- Handoff without context transfer documentation
- Resuming without verifying state
- No success criteria defined
- No clear "Next Action" documented
- Guessing at what was done previously

**If you catch yourself doing any of these: STOP. Create/update session file.**

## Verification Checklist

Before ending any work session:

- [ ] Session file exists and is current
- [ ] Current state accurately documented
- [ ] Checkpoint created with recovery commands
- [ ] Next action clearly specified
- [ ] Blockers documented if any
- [ ] Work log updated
- [ ] Files modified list current
- [ ] Handoff context ready if applicable

## State Tracking Quick Reference

```
ALWAYS document: Current state, next action, blockers
CHECKPOINT: Every 30-60 min, before breaks, before handoffs
HANDOFF: What, why, gotchas, files to review
RESUME: Read fully, verify state, then continue
ARCHIVE: Learnings, follow-ups, rename file
```

## Integration with Other Skills

**Pairs with:**
- **execute** - Track plan progress in session
- **verification** - Document verification results
- **brainstorm** - Record decision context
- **tdd** - Track test state across sessions
- **git-expert** - Document branch and commit state

## Multi-Agent Session Coordination

When multiple agents contribute to a session:

```markdown
## Agent Contributions

### Master Orchestrator
**Scope**: Planning and coordination
**Completed**: Phase breakdown, task assignment

### Backend Engineer
**Scope**: API implementation
**Completed**: Auth endpoints
**Handoff To**: Frontend Specialist

### Frontend Specialist
**Scope**: UI integration
**Status**: In Progress
**Current Task**: Login form

### Quality Engineer
**Scope**: Testing and validation
**Status**: Pending
**Waiting For**: Frontend complete
```

Each agent updates only their section, reads full context before starting.
