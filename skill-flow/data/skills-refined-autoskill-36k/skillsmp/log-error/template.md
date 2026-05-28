# Error Log Template

Copy this template when creating a new error log.

```markdown
# Error #[ID]: [Short Descriptive Name]
**Date:** [YYYY-MM-DD]
**Project/Context:** [What were you working on]

## What Happened
[2-3 sentences - what went wrong specifically]

## User Error Category
**Primary cause:** [Pick ONE]

### Prompt Errors
- [ ] **Ambiguous instruction** - Could be interpreted multiple ways
- [ ] **Missing constraints** - Didn't specify what NOT to do
- [ ] **Too verbose** - Buried key requirements in walls of text
- [ ] **Reference vs requirements** - Gave reference material, expected extracted requirements
- [ ] **Implicit expectations** - Had requirements in head, not in prompt
- [ ] **No success criteria** - Didn't define what "done" looks like
- [ ] **Wrong abstraction level** - Too high-level or too detailed for the task

### Context Errors
- [ ] **Context rot** - Conversation too long, should have /cleared
- [ ] **Stale context** - Old information polluting new responses
- [ ] **Context overflow** - Too much info degraded performance
- [ ] **Missing context** - Assumed Claude remembered something it didn't
- [ ] **Wrong context** - Irrelevant information drowning signal

### Harness Errors
- [ ] **Subagent context loss** - Critical info didn't reach subagents
- [ ] **Wrong agent type** - Used wrong specialized agent for task
- [ ] **No guardrails** - Didn't constrain agent behavior appropriately
- [ ] **Parallel when sequential needed** - Launched agents that had dependencies
- [ ] **Sequential when parallel possible** - Slow execution due to unnecessary serialization
- [ ] **Missing validation** - No check that agent output was correct
- [ ] **Trusted without verification** - Accepted agent output without review

### Meta Errors
- [ ] **Didn't ask clarifying questions** - Could have caught this earlier
- [ ] **Rushed to implementation** - Skipped planning/verification
- [ ] **Assumed competence** - Expected Claude to infer too much

## The Triggering Prompt
```
[Exact prompt - verbatim]
```

## What Was Wrong With This Prompt
[Be specific and critical. What should have been different?]

## What The User Should Have Said Instead
```
[Rewritten prompt that would have prevented this error]
```

## The Gap
- **What user expected:** [Expected outcome]
- **What user got:** [Actual outcome]
- **Why the gap exists:** [Direct connection to user error above]

## Impact
- **Time wasted:** [X minutes]
- **Rework required:** [What needs to be redone]

## Prevention - User Action Items
1. [Specific action user should take next time]
2. [Another specific action]
3. [Consider adding to personal CLAUDE.md or workflow]

## Pattern Check
- **Seen this before?** [Yes/No - if yes, this is a habit to break]
- **Predictable?** [Should user have anticipated this?]

## One-Line Lesson (for the USER)
[Actionable takeaway about prompting/context/harnessing - NOT about model behavior]

---
*Logged on [timestamp]*
```
