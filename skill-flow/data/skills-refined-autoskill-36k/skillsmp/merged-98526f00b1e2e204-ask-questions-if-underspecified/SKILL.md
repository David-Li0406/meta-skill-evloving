---
name: ask-questions-if-underspecified
description: Use this skill to clarify requirements before implementing changes when requests lack clear objectives, acceptance criteria, scope, constraints, or environment details. Invoke explicitly when underspecification is detected to avoid wrong work.
---

# Ask Questions If Underspecified

## Goal

Ask the minimum set of clarifying questions needed to avoid wrong work. Do not start implementing until the must-have questions are answered or the user explicitly approves proceeding with stated assumptions.

## Workflow

### 1) Decide Whether the Request Is Underspecified

Treat a request as underspecified if one or more of the following are unclear:
- **Objective**: What should change vs. stay the same?
- **Done Criteria**: What does success look like? Examples? Edge cases?
- **Scope**: Which files/components/users are in or out?
- **Constraints**: Compatibility, performance, style, dependencies, timeline?
- **Environment**: Language/runtime versions, OS, build/test runner?
- **Safety**: Data migration needs? Rollout/rollback plan? Risk assessment?

If there are multiple plausible interpretations, assume it is underspecified.

### 2) Ask Must-Have Questions First

Limit to 1-5 questions in the first pass. Prefer questions that eliminate whole branches of work.

#### Make Questions Easy to Answer
- Use numbered questions with short options (a/b/c).
- Recommend defaults when reasonable (mark clearly, **bold** the recommended choice).
- Provide a fast-path response option (e.g., reply `defaults`).
- Separate "Need to know" from "Nice to know" when helpful.

### 3) Pause Before Acting

Until must-have answers arrive:
- Do not run commands, edit files, or produce a detailed plan that depends on unknowns.
- Allow low-risk discovery reads (repo structure/configs) if they do not commit to a direction.

If the user explicitly wants you to proceed without answers:
1. State assumptions as a short numbered list.
2. Ask for confirmation.
3. Proceed only after they confirm or correct.

### 4) Confirm Interpretation, Then Proceed

Once answers are received, restate requirements in 1-3 sentences (including key constraints and what success looks like), then start work.

## Response Format

Use a compact, scannable structure. Example:

```text
Need to know
1) Scope?
   a) **Minimal change**
   b) Refactor while touching the area
   c) Not sure - use default

2) Compatibility target?
   a) **Current project defaults**
   b) Also support older versions: <specify>
   c) Not sure - use default

Reply with: defaults (or specify: 1a 2a)
```

## Anti-Patterns to Avoid

- **Don’t ask questions you can answer yourself**: Use quick, low-risk discovery (e.g., reading configs).
- **Don’t ask open-ended questions**: Use structured options instead.
- **Don’t ask too many questions at once**: Keep the first pass to 1-5 questions maximum.
- **Don’t ask "nice to know" before "need to know"**: Prioritize core functionality questions first.

## Example Session

### User Request
> "Add a dark mode toggle to the settings page"

### Agent Response (Using This Skill)
```
Before I implement dark mode, I need to clarify a few things:

1) Scope?
   a) Settings toggle only (Recommended) - just add UI toggle, dark mode implementation comes later
   b) Full implementation - toggle + all component styling + persistence
   c) Not sure - use default

2) Persistence?
   a) LocalStorage (Recommended) - fast, client-side only
   b) User preferences API - syncs across devices
   c) No persistence - resets on page reload
   d) Not sure - use default

Reply with: `defaults` (or specify: `1b 2a`)
```

### User Response
> "1b 2a"

### Agent Confirmation
```
Got it! I'll implement:
- Full dark mode with toggle in settings
- LocalStorage persistence

Success criteria:
- Toggle switches between light/dark instantly
- Preference persists across sessions

Confirm before I start?
```

## Integration with AskUserQuestion Tool

This skill is complementary to the built-in `AskUserQuestion` tool, which provides structured options UI for better user experience.

## Success Criteria

This skill succeeds when:
- All must-have ambiguities are resolved before implementation starts.
- User can answer questions quickly (< 2 minutes).
- Questions eliminate whole branches of wrong work.
- Assumptions are explicit and confirmed.
- Implementation matches user expectations on first try.

## Notes

- This is an explicit-invoke skill - do not use proactively.
- Always prefer structured questions over open-ended.
- Keep the first pass to 1-5 questions maximum.