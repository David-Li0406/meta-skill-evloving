---
name: exploration-tracking
description: Mind mapping and exploration state tracking for workshops. Use to maintain awareness of explored vs uncharted territory, implement backtracking, and ensure comprehensive coverage or documented gaps.
allowed-tools: Read, Write, AskUserQuestion
---

# Exploration Tracking Skill

## Overview

This skill provides techniques for tracking exploration state during workshops - maintaining a mental map of what's been explored, what remains, and ensuring systematic coverage with proper backtracking.

## Core Concepts

### The Exploration Map

A hierarchical representation of the topic space:

```
ROOT: [Main Topic]
│
├─ BRANCH: [Major Area 1]
│  ├─ SUB-BRANCH: [Aspect 1.1]
│  │  └─ DETAIL: [Specific 1.1.1]
│  └─ SUB-BRANCH: [Aspect 1.2]
│
├─ BRANCH: [Major Area 2]
│  └─ SUB-BRANCH: [Aspect 2.1]
│
└─ BRANCH: [Major Area 3]
```

### Status Indicators

| Symbol | Status | Meaning |
|--------|--------|---------|
| ✓ | EXPLORED | Fully discussed, findings captured |
| ◐ | PARTIAL | Started but not complete |
| ○ | UNCHARTED | Identified but not yet explored |
| → | CURRENT | Currently exploring this branch |
| ⊘ | SKIPPED | Deliberately skipped (document why) |
| ⚑ | FLAGGED | Marked for return / important |

### Exploration Goals

1. **Complete Coverage**: Explore all identified branches
2. **OR Documented Gaps**: Explicitly list what wasn't explored and why
3. **No Silent Omissions**: Never end with unexplored branches undocumented

## Creating the Initial Map

### Step 1: Identify Major Branches

When starting a workshop, decompose the topic:

```markdown
## Topic Decomposition: [TOPIC]

**Main Question**: [What are we exploring?]

**Major Branches Identified**:
1. [Branch A] - [Brief description]
2. [Branch B] - [Brief description]
3. [Branch C] - [Brief description]
4. [Branch D] - [Brief description]

**Initial Map**:
```
[TOPIC]
├─ [A] ──────── ○ UNCHARTED
├─ [B] ──────── ○ UNCHARTED
├─ [C] ──────── ○ UNCHARTED
└─ [D] ──────── ○ UNCHARTED
```
```

### Step 2: Validate with Operator

"Here's my initial map of what we could explore. Does this capture the territory? Any branches to add or remove?"

### Step 3: Establish Exploration Order

Options:
- Systematic (A → B → C → D)
- Priority-based (operator chooses order)
- Emergent (discover as we go)

## During Exploration

### Entering a Branch

```markdown
## Exploring: [Branch Name]

**Map Position**:
```
[TOPIC]
├─ [A] ──────── ✓ EXPLORED (5 ideas)
├─ [B] ──────── → CURRENT
├─ [C] ──────── ○ UNCHARTED
└─ [D] ──────── ○ UNCHARTED
```

**Focus**: [What we're exploring]
**Goal**: [What we want to capture]
```

### Discovering Sub-Branches

When deeper structure emerges during exploration:

```markdown
**Sub-branches discovered in [B]**:
```
[B] ──────────── → CURRENT
├─ [B.1] ─────── ○ UNCHARTED (just identified)
├─ [B.2] ─────── ○ UNCHARTED (just identified)
└─ [B.3] ─────── ○ UNCHARTED (just identified)
```

"I see three sub-areas here. Would you like to explore any of these deeper?"
```

### Checkpoint Protocol

At every checkpoint, show:

```markdown
**CHECKPOINT**

**Just completed**: [Branch/activity]
**Captured**: [N] ideas/insights

**Current Map**:
```
[TOPIC]
├─ [A] ──────── ✓ EXPLORED
├─ [B] ──────── ◐ PARTIAL
│  ├─ [B.1] ─── ✓ EXPLORED
│  ├─ [B.2] ─── ○ UNCHARTED
│  └─ [B.3] ─── ○ UNCHARTED
├─ [C] ──────── ○ UNCHARTED
└─ [D] ──────── ○ UNCHARTED
```

**Unexplored**:
- [B.2], [B.3] - siblings in current branch
- [C], [D] - main branches

**Options**:
1. Dive into [B.2] or [B.3]
2. Mark [B] complete, move to [C]
3. Stop and document current state
```

## Backtracking

### The Backtrack Stack

Maintain a mental stack of positions to return to:

```
BACKTRACK STACK
===============
[3] Return to: [B] after exploring [B.1.2]
[2] Return to: [B.1] after exploring [B.1.1]
[1] Return to: ROOT after exploring [B]
```

### When to Backtrack

1. After completing a sub-branch → return to parent
2. After deep dive → check siblings
3. Before moving to next main branch → confirm current complete

### Backtrack Announcement

```markdown
**Backtracking**

Completed: [B.1.2]
Returning to: [B.1]

**Siblings at [B.1] level**:
- [B.1.1] ✓ EXPLORED
- [B.1.2] ✓ EXPLORED (just completed)
- [B.1.3] ○ UNCHARTED ← remaining

"We've explored [B.1.2]. The sibling [B.1.3] remains. Explore it or mark [B.1] complete?"
```

### Never Forget to Backtrack

**RULE**: After any deep dive, ALWAYS:
1. Announce return to parent level
2. List remaining siblings
3. List remaining main branches
4. Ask operator for direction

## Handling Operator Decisions

### "Dive Deeper"

```
BEFORE DIVE:
1. Record current position
2. Record unexplored siblings
3. Record unexplored main branches
4. Push to backtrack stack

DURING DIVE:
- Explore the sub-area
- Note any further sub-branches

AFTER DIVE:
- Pop from backtrack stack
- Announce return
- Show remaining unexplored
```

### "Move On"

```
1. Mark current as EXPLORED or PARTIAL
2. If PARTIAL, note what's incomplete
3. Move to next in sequence
4. Update map
```

### "Skip This"

```
1. Mark as SKIPPED (⊘)
2. Document reason if given
3. Add to uncharted territory list
4. Move to next
```

### "Stop"

```
1. Stop immediately
2. Document all EXPLORED branches
3. Document all UNCHARTED branches
4. Document all PARTIAL branches
5. Recommend future starting point
```

## Closing Documentation

### Exploration Summary

```markdown
## Exploration Summary

**Session Goal**: [What we set out to explore]
**Coverage**: [X of Y branches explored]

**Final Map**:
```
[TOPIC]
├─ [A] ──────── ✓ EXPLORED
│  └─ 7 ideas captured
├─ [B] ──────── ◐ PARTIAL
│  ├─ [B.1] ─── ✓ EXPLORED (deep dive)
│  │  ├─ [B.1.1] ✓ EXPLORED
│  │  └─ [B.1.2] ✓ EXPLORED
│  ├─ [B.2] ─── ⊘ SKIPPED (time)
│  └─ [B.3] ─── ○ UNCHARTED
├─ [C] ──────── ○ UNCHARTED
└─ [D] ──────── ○ UNCHARTED
```
```

### Explored Territory Detail

```markdown
## Explored Territory

### [A]: [Title]
**Status**: ✓ EXPLORED
**Ideas Captured**: 7
**Key Findings**:
- [Finding 1]
- [Finding 2]
**Decisions Made**: [Any decisions]

### [B.1]: [Title]
**Status**: ✓ EXPLORED (deep dive)
**Depth**: 2 levels ([B.1.1], [B.1.2])
**Ideas Captured**: 12
**Key Findings**:
- [Finding 1]
```

### Uncharted Territory Detail

```markdown
## Uncharted Territory

The following areas remain unexplored:

### [B.2]: [Title]
**Status**: ⊘ SKIPPED
**Reason**: Operator chose to skip due to time constraints
**What's there**: [Known or suspected content]
**Priority for future**: Medium
**Dependencies**: None

### [B.3]: [Title]
**Status**: ○ UNCHARTED
**Reason**: Session ended before reaching
**What's there**: [Brief description]
**Priority for future**: High - related to deep dive findings
**Dependencies**: None

### [C]: [Title]
**Status**: ○ UNCHARTED
**Reason**: Not reached this session
**What's there**: [Major area description]
**Priority for future**: High
**Dependencies**: None

### [D]: [Title]
**Status**: ○ UNCHARTED
**Reason**: Not reached this session
**What's there**: [Major area description]
**Priority for future**: Medium
**Dependencies**: May depend on [C] findings
```

### Future Session Recommendations

```markdown
## Recommended Future Work

**Priority 1**: Complete [B]
- Explore [B.3]
- Revisit [B.2] if time

**Priority 2**: Explore [C]
- Major unexplored branch
- May reveal new sub-branches

**Priority 3**: Explore [D]
- Lowest priority
- Consider after [C] complete

**Starting Point**: Resume at [B] to complete partial work
```

## Best Practices

### Do's
- Always show the map at checkpoints
- Always backtrack after deep dives
- Always document uncharted territory
- Let operator drive pace and direction
- Note discovered sub-branches immediately

### Don'ts
- Don't skip backtracking
- Don't end without documenting gaps
- Don't make assumptions about what to explore
- Don't forget siblings when diving deep
- Don't lose track of the bigger picture
