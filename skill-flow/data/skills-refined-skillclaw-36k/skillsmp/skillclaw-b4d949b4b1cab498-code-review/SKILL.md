---
name: code-review
description: Use this skill when receiving code review feedback, especially if unclear or technically questionable, when completing tasks or major features requiring review before proceeding, or before making any completion/success claims.
---

# Code Review

Guide proper code review practices emphasizing technical rigor, evidence-based claims, and verification over performative responses.

## Overview

Code review requires three distinct practices:

1. **Receiving feedback** - Technical evaluation over performative agreement.
2. **Requesting reviews** - Systematic review via code-reviewer subagent.
3. **Verification gates** - Evidence before any completion claims.

## Core Principle

**Technical correctness over social comfort.** Verify before implementing. Ask before assuming. Evidence before claims.

## When to Use This Skill

### Receiving Feedback
Trigger when:
- Receiving code review comments from any source.
- Feedback seems unclear or technically questionable.
- Multiple review items need prioritization.
- External reviewer lacks full context.
- Suggestion conflicts with existing decisions.

### Requesting Review
Trigger when:
- Completing tasks in subagent-driven development (after EACH task).
- Finishing major features or refactors.
- Before merging to the main branch.
- Stuck and need a fresh perspective.
- After fixing complex bugs.

### Verification Gates
Trigger when:
- About to claim tests pass, build succeeds, or work is complete.
- Before committing, pushing, or creating PRs.
- Moving to the next task.
- Any statement suggesting success/completion.
- Expressing satisfaction with work.

## Quick Decision Tree

```
SITUATION?
│
├─ Received feedback
│  ├─ Unclear items? → STOP, ask for clarification first
│  ├─ From human partner? → Understand, then implement
│  └─ From external reviewer? → Verify technically before implementing
│
├─ Completed work
│  ├─ Major feature/task? → Request code-reviewer subagent
```