---
name: signal-capture
description: Use this skill when you need to detect and capture technical preferences, naming conventions, and architectural practices from user messages into Packmind standards.
---

# Signal Capture Workflow

This skill helps detect technical preferences in user messages and captures them systematically in `.claude/signal-capture.yaml` for integration into coding standards.

## TRIGGER CHECKLIST - Read This First

**TRIGGER THIS SKILL IMMEDIATELY WHEN THE USER:**

- [ ] States a naming convention (e.g., "All interfaces should start with I")
- [ ] Prescribes a code structure (e.g., "Always use async/await")
- [ ] Suggests an alternative (e.g., "Could we use X instead?")
- [ ] Gives code review feedback implying a pattern (e.g., "This would be clearer with X")
- [ ] Makes a comparative statement (e.g., "Use X instead of Y", "Prefer X over Y")
- [ ] References a principle that needs clarification (e.g., "follow KISS", "apply DRY")
- [ ] Requests removal of a rule (e.g., "Remove the rule about X")

**TRIGGER AS SOON AS YOU DETECT THE PREFERENCE** - don't wait until the end of your response. Ask for validation immediately.

## Failure Example - When This Skill SHOULD Have Been Triggered

```
User: "Could we just ensure that standardFile exists instead of using optional chaining?"

AI: [Detects this is a suggestive pattern indicating a preference]
AI: [Implements the change but FORGETS to capture the preference as a rule] ❌

CORRECT BEHAVIOR:
AI: [Detects suggestive pattern]
AI: [Immediately triggers skill]
AI: [Asks user: "I detected a technical preference. Add this rule to tests-redaction?"]
AI: [If approved, logs to .claude/signal-capture.yaml]
AI: [Continues with the implementation]
```

## When to Trigger

**TRIGGER CONDITIONS** - User prescribes HOW to code:

- Naming conventions: "All interfaces should start with I", "Use snake_case for columns"
- Code structure directives: "Wrap emojis for accessibility", "Always use async/await", "Don't use class components"