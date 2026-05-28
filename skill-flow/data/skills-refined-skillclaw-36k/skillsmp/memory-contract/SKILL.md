---
name: memory-contract
description: Unified Memory Contract for Project Memory integration. Defines when and how to retrieve and store memory using local files.
license: MIT
metadata:
  author: groupzer0
  version: "2.0"
---

# Unified Memory Contract

**Project Memory** is the system of recording context in structured Markdown files within `agent-output/memory/`. This allows all agents (and the user) to share long-term context without external dependencies.

---

## Core Principle

Memory is not a formality—it is part of your reasoning. Treat retrieval like checking the project logs before starting work. Treat storage like writing a log entry for the next person.

**The rule:** If you make a decision, learn a constraint, or hit a dead end, **write it down**.

---

## When to Retrieve

Retrieve at **decision points**, not just at turn start.

**Retrieve when you:**
- Are about to make an assumption → check if it was already decided
- Don't recognize a term, file, or pattern → check if it was discussed
- Are choosing between options → check if one was tried or rejected
- Feel uncertain → check for prior context

**How to Retrieve:**
1.  **Use Semantic Search**: Use your tool's semantic search (e.g., `@codebase`, `search`, or similar) to find relevant files in `agent-output/memory/`.
2.  **Read Files**: Read the content of relevant memory files.

**Query Examples:**
- "Searching `agent-output/memory/` for decisions about authentication..."
- "Reading `agent-output/memory/2024-01-15-auth-decision.md`..."

---

## When to Store

Store at **value boundaries**—when you've created something worth preserving.

**Store when you:**
- Complete a non-trivial task or subtask
- Make a decision that narrows future options
- Discover a constraint, dead end, or "gotcha"
- Learn a user preference or workspace convention

**How to Store:**
1.  **Create a File**: Create a new markdown file in `agent-output/memory/`.
2.  **Naming Convention**: `YYYY-MM-DD-topic-slug.md`.
    *   Example: `2025-01-15-auth0-decision.md`
    *   Example: `2025-01-16-api-rate-limit-fix.md`

### Storage Format

Use this template for memory files:

```markdown
---
type: memory
topic: [Short Topic Name]
status: active
date: YYYY-MM-DD
---

# [Topic Name]

**Context**: [What happened, what was the goal?]

**Decision/Outcome**: [What did you decide or achieve?]

**Rationale**: [Why? Trade-offs? Constraints?]

**Related Artifacts**:
- [Link to plan or code file]
```

---

## Commitments

1.  **Retrieve before reasoning.** Don't guess. Check memory.
2.  **Store at boundaries.** Don't lose context. Write it down.
3.  **Acknowledge memory.** When retrieved memory changes your plan, say so.
4.  **Fail safely.** If you can't read/write memory files, announce it and proceed with best effort.
