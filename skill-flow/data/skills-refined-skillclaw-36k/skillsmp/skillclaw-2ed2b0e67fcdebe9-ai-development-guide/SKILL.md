---
name: ai-development-guide
description: Use this skill when making technical decisions, detecting code smells, or performing quality assurance in software development.
---

# Skill body

## Technical Anti-patterns (Red Flag Patterns)

Immediately stop and reconsider design when detecting the following patterns:

### Code Quality Anti-patterns
1. **Writing similar code 3 or more times** - Violates Rule of Three.
2. **Multiple responsibilities mixed in a single file** - Violates Single Responsibility Principle (SRP).
3. **Defining same content in multiple files** - Violates DRY principle.
4. **Making changes without checking dependencies** - Potential for unexpected impacts.
5. **Disabling code with comments** - Should use version control.
6. **Error suppression** - Hiding problems creates technical debt.
7. **Bypassing safety mechanisms (type systems, validation, contracts)** - Circumventing language's correctness guarantees.

### Design Anti-patterns
- **"Make it work for now" thinking** - Accumulation of technical debt.
- **Patchwork implementation** - Unplanned additions to existing code.
- **Optimistic implementation of uncertain technology** - Designing unknown elements assuming "it'll probably work".
- **Symptomatic fixes** - Surface-level fixes that don't solve root causes.
- **Unplanned large-scale changes** - Lack of incremental approach.

## Fail-Fast Fallback Design Principles

### Core Principle
Prioritize primary code reliability over fallback implementations. In distributed systems, excessive fallback mechanisms can mask errors and make debugging difficult.

### Implementation Guidelines

#### Default Approach
- **Prohibit unconditional fallbacks**: Do not automatically return default values on errors.
- **Make failures explicit**: Errors should be visible and traceable.
- **Preserve error context**: Include original error information when re-throwing.

#### When Fallbacks Are Acceptable
- **Only with explicit Design Doc approval**: Document why fallback is necessary.
- **Business-critical continuity**: When partial functionality is better than none.
- **Graceful degradation paths**: Clearly defined degraded service levels.

#### Layer Responsibilities
- **Infrastructure Layer**:
  - Always throw errors upward.
  - No business logic decisions.
  - Provide detailed error context.

- **Application Layer**:
  - Make business-driven decisions based on error context.