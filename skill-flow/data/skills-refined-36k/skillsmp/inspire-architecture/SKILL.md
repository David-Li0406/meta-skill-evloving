---
name: inspire-architecture
description: Inspire team system architecture patterns, design decisions, and component relationships. Use when making architectural decisions, understanding system structure, or reviewing code that affects system design.
user-invocable: false
allowed-tools: Read
---

# Inspire Team Architecture Context

When this skill is activated, load the following architecture documentation:

## Required Context Files

Read these files to understand the Inspire team's architecture:

1. **System Architecture**: `./references/system-architecture.md`
   - Overall system design and component relationships
   - Service boundaries and responsibilities
   - Infrastructure overview

2. **Design Patterns**: `./references/design-patterns.md`
   - Approved design patterns for this codebase
   - When to apply each pattern
   - Anti-patterns to avoid

## Instructions

Before responding to architecture-related questions:
1. Use the Read tool to load both architecture files above
2. Apply the patterns and guidelines from those files
3. Reference specific sections when making recommendations

## When to Load This Context

- Designing new features or services
- Reviewing PRs that affect system structure
- Debugging cross-service issues
- Evaluating technology choices
- Planning scaling or performance improvements
