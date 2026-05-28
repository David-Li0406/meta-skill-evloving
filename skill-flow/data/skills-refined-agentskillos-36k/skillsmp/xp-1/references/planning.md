# Planning

## Core Rules (Non-Negotiable)

1. **NEVER skip requirements discussion** — understand before decomposing
2. **Ask at least one clarifying question** before breaking down tasks
3. **Vertical slices only** — each task delivers working functionality
4. **Confirm understanding** — summarise and agree before moving on

## The Planning Cycle

```
💬 DISCUSS  → Understand the problem and expected behaviour
❓ CLARIFY  → Ask questions, resolve ambiguities
✂️ SLICE    → Break into tasks
📋 CONFIRM  → Summarise and agree on first task
```

## Detailed Steps

### 💬 DISCUSS — Understand Requirements

1. What problem does this feature solve?
2. What is the expected behaviour?
3. What are the acceptance criteria?
4. Are there any constraints or dependencies?

### ❓ CLARIFY — Resolve Ambiguities

1. Identify gaps in understanding
2. Ask focused questions
3. Challenge assumptions
4. **STOP** — Do not proceed until questions are answered

### ✂️ SLICE — Break Into Tasks

Create tasks that are:

- **Vertical** — each delivers working end-to-end functionality
- **Small** — completable in one TDD cycle
- **Ordered** — by dependency first, then by value
- **Testable** — clear acceptance criteria

### 📋 CONFIRM — Agree on Plan

1. Summarise understanding back to user
2. Present ordered task list
3. **STOP** — Explicitly agree on the first task to implement

## What Makes a Good Task

```
✅ Good: "Add a book to the library"
   - Has clear input (book details)
   - Has clear output (book stored)
   - Can be tested end-to-end

❌ Bad: "Create the Book class"
   - Implementation detail
   - No user-visible behaviour
   - Can't be validated independently
```

## Announcing Progress

```
💬 DISCUSS → Understanding [feature]
❓ CLARIFY → Question: [question]
✂️ SLICE → Breaking into tasks
📋 CONFIRM → Proposed tasks: [list]
```

## Output Format

After planning, present tasks as:

```
## Tasks for [Feature]

1. [ ] [Task description] — [acceptance criteria]
2. [ ] [Task description] — [acceptance criteria]
3. [ ] [Task description] — [acceptance criteria]

**First task:** [Task 1 description]
```

## Common Mistakes

- Diving into implementation without understanding requirements
- Creating horizontal slices (e.g., "build the database layer")
- Tasks too large to complete in one session
- Skipping confirmation step
- Not ordering by dependency
