---
name: architecture-review
description: Architecture review guidance. Use when reviewing architectural changes, assessing system design, or evaluating code structure.
---

# General Architecture Review

## Focus Areas

- Separation of concerns
- Dependency direction and coupling
- Consistency with existing patterns
- Scalability implications
- Testability of the design
- Potential for code reuse
- Layer violations

## Process

1. Identify the boundaries and layers in the code
2. Trace dependencies between modules
3. Check for violations of established patterns
4. Assess impact on existing architecture

# Full Stack Application Review

When we have an application like here which is part single page application (SPA) for the frontend and a backend (via REST, or GraphQL),
we want to consider some things.

While the frontend is responsible for keeping a specific user's state, it should stay **as dumb as possible**. For example, instead of sorting
something in the frontend, we always would chose sorting on the backend and hand over a list (which is sorted by definition) to the frontend.
