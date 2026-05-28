---
name: review-reception
description: Use when receiving code review feedback before implementing suggestions, especially if unclear or questionable.
allowed-tools: ["shell", "read_file", "apply_patch", "update_plan"]
metadata:
  short-description: Evaluate and apply review feedback rigorously
---

# Review Reception

**Read these references:**
- `~/.config/agent/core/behavior.md` - Evidence-based reasoning
- `~/.config/agent/domain/review/priorities.md` - Review focus areas

## Overview

Code review requires technical evaluation, not performative agreement.

**Core principle:** Verify before implementing. Ask before assuming.

## Response Pattern

1. **Read** all feedback without reacting
2. **Understand** each item (or ask for clarification)
3. **Verify** against codebase reality
4. **Evaluate** whether it is correct for this codebase
5. **Respond** with technical acknowledgment or reasoned pushback
6. **Implement** one item at a time and test each

## Handling Unclear Feedback

If any item is unclear, stop and ask for clarification before implementing anything.

## Implementation Order

1. Blocking issues (breaks, security)
2. Simple fixes (typos, imports)
3. Complex fixes (refactors, logic)
4. Test each change and verify no regressions

## When to Push Back

Push back when:
- Suggestion breaks existing behavior
- Reviewer lacks context
- Violates YAGNI
- Conflicts with prior architectural decisions

Use technical reasoning and evidence.

## Arguments

Target: ${ARGUMENTS}
