---
name: requirements-clarifier
description: Activates during planning stage to clarify user requirements, constraints, and preferences. Use when user requests are vague, ambiguous, or need deeper understanding before implementation. Helps prevent rework by ensuring shared understanding.
user-invocable: true
disable-model-invocation: false
---

# Requirements Clarifier

This skill activates when user requests need clarification during planning. Instead of making assumptions, ask targeted questions to ensure you understand what they want.

## When to Use

Activate when you detect:
- Vague requirements ("build a feature", "fix the bug")
- Missing constraints (deadline, budget, scope)
- Ambiguous preferences (design, technology choices)
- Complex tasks needing decomposition
- User says "plan this" or "design this"

## Clarification Framework

### 1. Problem Understanding

**Ask to understand the core problem**:

```
I want to make sure I understand what you're trying to achieve:

1. What problem are you trying to solve?
2. Who will use this? (end users, developers, admins)
3. What's the current pain point?
4. What does success look like?
```

### 2. Scope & Constraints

**Ask to understand boundaries**:

```
Help me understand the scope and constraints:

1. Timeline: When do you need this? (guides complexity vs speed trade-offs)
2. Compatibility: Any backward compatibility requirements?
3. Resources: Performance limits, memory constraints, external dependencies?
4. Standards: Any coding standards, style guides, or patterns to follow?
```

### 3. Functional Requirements

**Ask to understand what it must do**:

```
Let me clarify the functional requirements:

1. Core features: What are the must-have vs nice-to-have features?
2. User flows: What should the user experience be?
3. Edge cases: What are the main edge cases to handle?
4. Error handling: How should errors be presented to users?
```

### 4. Technical Preferences

**Ask to understand technical approach**:

```
I want to align with your technical preferences:

1. Frameworks/libraries: Any preferences or restrictions?
2. Architecture: Monolith, modular, microservices?
3. Data storage: Database choices, caching strategy?
4. Testing: What level of test coverage do you expect?
```

### 5. Non-Functional Requirements

**Ask to understand quality attributes**:

```
Help me understand quality requirements:

1. Performance: Response time targets, throughput needs?
2. Scalability: Expected load, growth projections?
3. Security: Any security, authentication, authorization requirements?
4. Maintainability: Documentation needs, code comments?
```

## Clarification Strategy

### Progressive Disclosure

Don't ask all questions at once. Use progressive disclosure:

```
1. Start with 2-3 critical questions
2. Wait for answers
3. Ask follow-up questions based on responses
4. Repeat until you have enough context
```

### Prioritize Questions

**Ask in this order**:

| Priority | Questions | Why |
|----------|-----------|-----|
| 1️⃣ Critical | Problem, users, success criteria | Can't solve wrong problem |
| 2️⃣ Important | Scope, timeline, constraints | Avoids over/under-engineering |
| 3️⃣ Useful | Technical preferences | Aligns with existing patterns |
| 4️⃣ Optional | Nice-to-haves, edge cases | Refines implementation |

### Example Conversation

**User**: "Add user authentication"

**Bad response** (assumptions):
```
I'll add JWT authentication with email/password.
```

**Good response** (clarification):
```
I want to make sure I implement the right authentication solution:

**Critical questions:**
1. What authentication methods do you need? (email/password, OAuth, SAML, magic links?)
2. What's your security requirement? (Simple session cookies vs JWT with refresh tokens?)
3. Any existing auth system to integrate with?

**Answer these, and I'll design the appropriate solution.**
```

## Common Vague Requests & How to Clarify

| Vague Request | What to Ask |
|---------------|-------------|
| "Build a feature" | What problem does it solve? Who uses it? What's the user flow? |
| "Fix the bug" | What's the expected behavior? What's actually happening? Steps to reproduce? |
| "Improve performance" | What's the current performance? What target do you need? Where's the bottleneck? |
| "Refactor this code" | What's the goal? (readability, maintainability, performance?) Any patterns to follow? |
| "Add tests" | What level of coverage? What's the risk tolerance? Integration + unit, or smoke tests only? |
| "Deploy to production" | What's your deployment process? Zero-downtime required? Rollback strategy? |

## When You Have Enough Context

**Stop asking when you can answer**:

- ✅ What problem we're solving
- ✅ Who will use it
- ✅ What success looks like
- ✅ Key constraints (timeline, scope)
- ✅ Technical direction

**Then say**:

```
I have enough context to proceed. Here's my understanding:

[Summarize requirements in 3-5 bullet points]

Does this match your expectations? If yes, I'll proceed with implementation.
If no, let me know what I'm missing.
```

## Anti-Patterns

### Don't

- ❌ Ask 20 questions at once (overwhelming)
- ❌ Make assumptions without confirmation
- ❌ Skip clarification for "simple" requests (simple ≠ clear)
- ❌ Ask questions that don't affect implementation
- ❌ Ignore constraints mentioned earlier in conversation

### Do

- ✅ Prioritize questions by impact
- ✅ Use progressive disclosure (2-3 questions at a time)
- ✅ Confirm understanding before proceeding
- ✅ Reference earlier context when available
- ✅ Focus on questions that change the implementation

## Integration with Planning

After clarification, if planning is needed:

```
Now that I understand the requirements, I'll create an implementation plan.

[Use planning framework: break down tasks, identify dependencies, estimate complexity]

Should I proceed with this plan?
```

## Quick Reference

**Trigger phrases**:
- "build", "add", "create" (without details)
- "fix", "improve", "optimize" (without specifics)
- "plan this", "design this"
- Ambiguous scope statements

**First questions to ask**:
1. What problem are we solving?
2. Who will use this?
3. What does success look like?
4. Any key constraints I should know?

**Stop when**: You can explain what you're building and why in 3-5 sentences.

---

**Note**: This skill works best when combined with a planning skill or process. Clarify first, plan second, implement third.
