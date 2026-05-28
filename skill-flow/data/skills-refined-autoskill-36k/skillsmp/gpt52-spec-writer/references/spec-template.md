# \[Project Name\]: Agent Specification

## Model Directive

This document serves as a specification for GPT-5.2 to [Core Objective]. [Brief context about the project/architecture].

______________________________________________________________________

## Implementation Expectations

\<mandatory_execution_requirements>

This is not a review task. When given implementation requests:

1. Edit files using tools to modify actual source files
2. Debug and fix by running builds, reading errors, iterating until it compiles
3. Test changes as appropriate
4. Complete the full implementation; do not stop at partial solutions

Unacceptable responses:

- "Here's how you could implement this..."
- Providing code blocks without writing them to files
- Stopping after encountering the first error or completing only 1 of several assigned tasks

\</mandatory_execution_requirements>

______________________________________________________________________

## Behavioral Constraints

\<verbosity_and_scope_constraints>

- Prefer editing existing files over creating new ones when it makes sense
- Avoid unnecessary features unrelated to the task
- If any instruction is ambiguous, choose the simplest valid interpretation
- Follow existing code patterns where they exist

\</verbosity_and_scope_constraints>

\<design_freedom>

- Explore existing patterns before proposing changes
- New abstractions, refactors, or patterns are welcome when they improve code health, readability, or maintainability
- Use judgment: balance consistency with improvement

\</design_freedom>

______________________________________________________________________

## Implementation Roadmap

[Define concrete, numbered phases with explicit tasks using markdown checkboxes]

### Phase 1: [Phase Name]

Objective: [What this phase accomplishes]

Tasks:

- [ ] 1.1 \[Task\]: File `path/to/file` -> Steps: Read, Edit X, Run check -> Done: builds pass
- [ ] 1.2 \[Task\]: ...

### Phase 2: [Phase Name]

...

______________________________________________________________________

## Architecture

[Describe the core architecture, key patterns, directory structure]

______________________________________________________________________

## Anti-Patterns

1. \[Anti-Pattern\]: [Why bad] -> [Do this instead]
