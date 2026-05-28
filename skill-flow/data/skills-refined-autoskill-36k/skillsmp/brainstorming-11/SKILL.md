---
name: brainstorming
description: Turn ideas into fully formed designs through collaborative dialogue. Use BEFORE any creative work - creating features, building components, adding functionality, or modifying behavior.
---

# Brainstorming Ideas Into Designs

## Description
Turn ideas into fully formed designs through collaborative dialogue. Use this BEFORE any creative work - creating features, building components, adding functionality, or modifying behavior.

## When to Use
- Starting a new feature
- Adding significant functionality
- Modifying existing behavior
- Any creative work before implementation

## The Process

### 1. Understand the Idea
- Check current project state (files, docs, recent commits)
- Ask questions **one at a time** to refine the idea
- Prefer multiple choice questions when possible
- Focus on: purpose, constraints, success criteria

### 2. Explore Approaches
- Propose 2-3 different approaches with trade-offs
- Lead with your recommended option and explain why
- Present options conversationally

### 3. Present the Design
- Break into sections of 200-300 words
- Ask after each section: "Does this look right so far?"
- Cover:
  - Architecture
  - Components/modules
  - Data flow
  - Error handling
  - Testing strategy
- Go back and clarify if something doesn't make sense

### 4. Document
- Write validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Commit the design document

### 5. Implementation (Optional)
- Ask: "Ready to set up for implementation?"
- Create isolated workspace if needed (git worktree)
- Create detailed implementation plan

## Key Principles

| Principle | Why |
|-----------|-----|
| One question at a time | Don't overwhelm |
| Multiple choice preferred | Easier to answer |
| YAGNI ruthlessly | Remove unnecessary features |
| Explore alternatives | Always 2-3 approaches |
| Incremental validation | Present design in sections |
| Be flexible | Revisit when unclear |

## Example Flow

```
User: "I want to add user notifications"

Claude: "Let me check the current project structure first..."
        [reads files, understands context]

        "What's the primary goal for notifications?
         A) Real-time alerts for urgent events
         B) Daily/weekly digest summaries
         C) Both, with user preferences
         D) Something else"

User: "A"

Claude: "Got it - real-time alerts. Which delivery channels matter most?
         A) In-app only (simplest)
         B) In-app + email
         C) In-app + push notifications
         D) All of the above"

[continues one question at a time...]

Claude: "I think I understand. Let me present the design in sections.

        ## Architecture
        [200-300 words]

        Does this architecture look right so far?"

User: "Yes, but what about..."

[iterates until design is solid]

Claude: "I'll write this to docs/plans/2026-01-03-notifications-design.md"
```

## Output

Design document in `docs/plans/` with:
- Problem statement
- Chosen approach (with rationale)
- Architecture overview
- Component breakdown
- Data flow
- Error handling
- Testing strategy
- Open questions (if any)
