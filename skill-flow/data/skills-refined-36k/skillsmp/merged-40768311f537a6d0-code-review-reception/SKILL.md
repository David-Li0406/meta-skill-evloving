---
name: code-review-reception
description: Use this skill when receiving code review feedback to ensure technical evaluation and verification before implementation, avoiding performative agreement.
---

# Code Review Reception

## Core Principle

**Verify before implementing. Ask before assuming. Technical correctness over social comfort.**

## Overview

Code review feedback requires technical evaluation, not emotional performance. This skill teaches how to receive, evaluate, and implement feedback professionally.

## The Response Pattern

When receiving code review feedback, follow these steps:

1. **READ**: Complete feedback without reacting.
2. **UNDERSTAND**: Restate the requirement in your own words or ask for clarification.
3. **VERIFY**: Check against the actual codebase reality.
4. **EVALUATE**: Determine if the feedback is technically sound for the current codebase.
5. **RESPOND**: Provide technical acknowledgment or reasoned pushback.
6. **IMPLEMENT**: Implement one item at a time and test each change.

## Forbidden Responses

**NEVER:**
- "You're absolutely right!"
- "Great point!" / "Excellent feedback!"
- "Let me implement that now" (before verification)
- Any performative agreement.

**INSTEAD:**
- Restate the technical requirement.
- Ask clarifying questions.
- Push back with technical reasoning if the feedback is incorrect.
- Focus on actions rather than words.

## Handling Unclear Feedback

If any feedback item is unclear:
- **STOP** - do not implement anything yet.
- **ASK** for clarification on unclear items.

## YAGNI Check

When a reviewer suggests adding features:
- Search the codebase for actual usage.
- If unused, suggest removing it (YAGNI).
- If used, then implement properly.

## When to Push Back

Push back when:
- The suggestion breaks existing functionality.
- The reviewer lacks full context.
- It violates YAGNI (unused feature).
- It is technically incorrect for the stack.
- Legacy or compatibility reasons exist.
- It conflicts with prior architectural decisions.

**How to push back:**
- Use technical reasoning, not defensiveness.
- Ask specific questions.
- Reference working tests/code.
- Escalate if architectural.

## Implementation Order

For multi-item feedback:
1. Clarify anything unclear first.
2. Implement in order:
   - Blocking issues (breaks, security).
   - Simple fixes (typos, imports).
   - Complex fixes (refactoring, logic).
3. Test each fix individually.
4. Verify no regressions.

## Acknowledging Correct Feedback

When feedback is correct:
- Simply fix the issue and provide a brief description of what changed.
- Avoid expressions of gratitude or performative agreement.

## Gracefully Correcting Your Pushback

If you pushed back and were wrong:
- Acknowledge the correction factually and move on without lengthy apologies.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State the requirement or just act. |
| Blind implementation | Verify against the codebase first. |
| Batch without testing | Implement one at a time, test each. |
| Assuming reviewer is right | Check if it breaks things. |
| Avoiding pushback | Prioritize technical correctness over comfort. |
| Partial implementation | Clarify all items first. |

## Integration with Other Skills

**Use with:**
- `task-dispatch` - Handle review between tasks.
- `code-test` - Test each fix individually.
- `completion-verify` - Verify fixes actually work.

## Your Commitment

When receiving feedback:
- [ ] I will verify before agreeing.
- [ ] I will ask when unclear.
- [ ] I will provide technical reasoning.
- [ ] I will implement one change at a time.
- [ ] I will test after each change.
- [ ] I will avoid performative agreement.

---

**Bottom Line**: Code review is a technical evaluation, not a social agreement. Verify feedback against reality, provide reasoned responses, and implement systematically. Prioritize technical correctness over social comfort.