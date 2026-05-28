---
name: software-engineering
description: Use this skill when making design decisions, evaluating trade-offs, assessing code quality, or when "engineering judgment" is required.
---

# Software Engineering

Engineering judgment - thoughtful decisions - quality code.

<when_to_use>

- Making architectural or design decisions
- Evaluating trade-offs between approaches
- Determining appropriate level of thoroughness
- Assessing when code needs refactoring
- Deciding when to ask vs proceed independently
- Balancing speed, quality, maintainability

NOT for: mechanical tasks, clear-cut decisions, following explicit instructions

</when_to_use>

<principles>

Core engineering judgment framework.

**User preferences trump defaults**  
Project rules and existing patterns always override skill suggestions.

**Simplest thing that works**  
Start simple. Add complexity only when requirements demand.
- Boring solutions for boring problems
- Proven libraries over custom implementations
- Progressive enhancement over rewrites

**Read before write**  
Understand existing patterns before modifying.
- Check how similar features are implemented
- Follow established conventions
- Maintain consistency

**Small, focused changes**  
One idea per commit, 20-100 LOC, 1-5 files.
- Easy to review/understand
- Lower bug risk
- Simpler to revert
- Faster feedback

**Security awareness**  
Don't introduce vulnerabilities.
- Validate external input
- Parameterized queries
- Handle authentication properly
- No secrets in code/logs

**Know when to stop**  
Ship working code, don't gold-plate.
- Implement requirements, not assumptions
- No unrequested features
- No speculative abstraction

</principles>

<type_safety>

Type safety across languages.

**Core principle**: Make illegal states unrepresentable. Type systems should prevent invalid data at compile time, not runtime.

**Hierarchy**: Correct (type-safe) - Clear (self-documenting) - Precise (not overly broad)

**Key patterns**:
- **Result types** - Errors explicit in signatures, not hidden in exceptions
- **Discriminated unions** - Mutually exclusive states with discriminator field
- **Branded types** - Distinct types for domain concepts (user ID vs product ID)
- **Parse, don't validate** - Transform untyped to typed at boundaries, trust types internally

</type_safety>