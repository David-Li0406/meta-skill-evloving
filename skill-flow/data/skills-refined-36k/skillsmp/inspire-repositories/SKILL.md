---
name: inspire-repositories
description: Inspire team repository inventory and standards. Use when understanding the codebase structure or repository conventions.
user-invocable: false
allowed-tools: Read
---

# Inspire Team Repositories Context

When this skill is activated, load the following repository documentation:

## Required Context Files

Read these files to understand the Inspire team's repositories:

1. **Repository Inventory**: `./references/repositories-inventory.md`
   - List of repositories
   - Repository purposes
   - Ownership information

2. **Repository Standards**: `./references/repositories-standard.md`
   - Naming conventions
   - Branch strategies
   - Required files (README, etc.)

## Instructions

Before responding to repository questions:
1. Use the Read tool to load relevant files above
2. Follow the team's repository standards
3. Reference inventory for cross-repo work

## When to Load This Context

- Creating new repositories
- Understanding codebase structure
- Cross-repository changes
- Setting up CI/CD
