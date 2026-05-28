---
name: inspire-tech_stack
description: Inspire team technology stack including frameworks, libraries, and tooling. Use when making technology decisions or understanding dependencies.
user-invocable: false
allowed-tools: Read
---

# Inspire Team Tech Stack Context

When this skill is activated, load the following tech stack documentation:

## Required Context Files

Read these files to understand the Inspire team's technology stack:

1. **Frameworks**: `./references/frameworks.md`
   - Frontend frameworks
   - Backend frameworks
   - Version information

2. **Libraries**: `./references/libraries.md`
   - Core libraries
   - Utility libraries
   - Version constraints

3. **Tooling**: `./references/tooling.md`
   - Build tools
   - Development tools
   - CI/CD tools

## Instructions

Before responding to tech stack questions:
1. Use the Read tool to load relevant files above
2. Recommend technologies from the approved stack
3. Note version constraints when relevant

## When to Load This Context

- Adding new dependencies
- Evaluating technology choices
- Understanding existing stack
- Planning upgrades
