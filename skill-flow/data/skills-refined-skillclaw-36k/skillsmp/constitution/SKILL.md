---
name: constitution
description: Create or update project governing principles and development guidelines that guide all subsequent development
---

# Constitution - Project Governing Principles

## Overview

Establish foundational principles and development guidelines for the project. These principles guide all subsequent specification, planning, and implementation decisions.

**Announce at start:** "I'm using the constitution skill to establish project principles."

## When to Use

- **First step** in Spec-Driven Development workflow
- Before creating specifications or implementation plans
- When project principles need to be established or updated
- When starting a new feature or major refactoring

## The Process

### Step 1: Understand Project Context

1. Review existing project structure, documentation, and codebase
2. Check if `.specify/memory/constitution.md` already exists
3. Review existing principles if updating

### Step 2: Create or Update Constitution

Create or update `.specify/memory/constitution.md` with:

**Required Sections:**

1. **Code Quality Standards**
   - Code style and formatting guidelines
   - Naming conventions
   - Documentation requirements
   - Code review standards

2. **Testing Standards**
   - Test coverage requirements
   - Testing frameworks and patterns
   - Test organization and structure
   - When tests are required vs optional

3. **User Experience Consistency**
   - Design principles
   - Accessibility requirements
   - Performance targets
   - User interaction patterns

4. **Performance Requirements**
   - Performance benchmarks
   - Scalability considerations
   - Resource usage limits
   - Optimization guidelines

5. **Technical Decision Governance**
   - How principles guide technical choices
   - When to deviate from principles
   - Decision-making process
   - Architecture constraints

### Step 3: Reference Project Guidelines

For Swift StateTree project, incorporate:
- Swift 6 and Swift API Design Guidelines
- `Sendable` requirements for public types
- Testing framework: Swift Testing (not XCTest)
- Code comments must be in English
- Cross-platform compatibility priorities

### Step 4: Save and Commit

- Save to `.specify/memory/constitution.md`
- Commit with message: `docs: establish project constitution`
- Reference in all subsequent development phases

## Example Prompt

```
/speckit.constitution Create principles focused on code quality, testing standards, 
user experience consistency, and performance requirements. Include governance for 
how these principles should guide technical decisions and implementation choices.
```

## Output Format

The constitution file should be clear, actionable, and reference-able:

```markdown
# Project Constitution

## Code Quality Standards
...

## Testing Standards
...

## User Experience Consistency
...

## Performance Requirements
...

## Technical Decision Governance
...
```

## Integration with Other Skills

After creating constitution:
- Use `SpecKit/specify` to create functional specifications
- Use `SpecKit/plan` to create implementation plans (constitution guides decisions)
- Use `SpecKit/implement` to execute (constitution ensures consistency)

## Key Principles

- **Be specific**: Principles should be actionable, not vague
- **Be consistent**: Align with existing project guidelines (see `AGENTS.md`)
- **Be practical**: Principles should guide real decisions
- **Be flexible**: Allow exceptions when justified
- **Be documented**: Keep principles updated as project evolves
