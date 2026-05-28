# AGENTS.md - Persistent Context for {{task-name}}

**Task**: {{task-name}}
**Created**: {{timestamp}}

## Relationship to Project CLAUDE.md

This file contains **task-specific** patterns and decisions that are relevant to this Ralph loop task.

Patterns that apply **project-wide** should be promoted to `./CLAUDE.md` in the project root:
- Naming conventions that apply everywhere
- Commands or workflows useful beyond this task
- Gotchas that future tasks should know about
- Architectural decisions affecting the whole project

Keep task-specific details here. Promote reusable patterns to CLAUDE.md.

---

## Project Overview

{{problem_statement}}

## Discovered Patterns

<!--
Patterns discovered during development that should persist across iterations.
These are distilled insights that help future iterations work more effectively.

Format:
### Pattern Name
- **What**: Description of the pattern
- **When**: When to use it
- **How**: How to implement it

Example:
### API Response Format
- **What**: All API responses use {success: boolean, data: T, error?: string}
- **When**: Any endpoint returning JSON
- **How**: Use responseHelper.success(data) or responseHelper.error(message)
-->

## Architecture Decisions

<!--
Key architectural choices made during development.
Document these so future iterations understand WHY things are structured this way.

Format:
### Decision Title
- **Decision**: What was decided
- **Why**: Rationale for the decision
- **Implications**: What this means for implementation
- **Alternatives considered**: What else was evaluated

Example:
### Use Repository Pattern for Data Access
- **Decision**: All database access goes through repository classes
- **Why**: Enables testing with mocks, separates concerns
- **Implications**: Create UserRepository, ItemRepository, etc.
- **Alternatives considered**: Direct ORM calls (rejected: harder to test)
-->

## Code Conventions

<!--
Coding conventions established or discovered for this project.

Examples:
- File naming: kebab-case for files, PascalCase for classes
- Imports: Absolute imports from src/, relative for same directory
- Error handling: Always throw typed errors from errors.ts
- Testing: One test file per source file, *.test.ts naming
-->

## Known Issues

<!--
Issues discovered but intentionally deferred.
Document these so they're not forgotten and don't block progress.

Format:
### Issue Title
- **Issue**: Description of the problem
- **Impact**: How it affects the project (low/medium/high)
- **Deferred because**: Why it's not being fixed now
- **Suggested fix**: How to address it later
-->

## Commands Reference

<!--
Useful commands discovered during development.
Save these so you don't have to rediscover them each iteration.

Examples:
- Run tests: `npm test`
- Run single test: `npm test -- --testNamePattern="test name"`
- Start dev server: `npm run dev`
- Build: `npm run build`
- Lint: `npm run lint -- --fix`
- Type check: `npx tsc --noEmit`
-->

## File Structure

<!--
Key files and their purposes.
Helps orient future iterations quickly.

Examples:
- src/index.ts - Main entry point
- src/routes/ - API route handlers
- src/services/ - Business logic
- src/repositories/ - Data access layer
- tests/ - Test files mirroring src structure
-->

## Environment Setup

<!--
Environment requirements discovered during development.

Examples:
- Node version: 18+
- Required env vars: DATABASE_URL, API_KEY
- Dev dependencies: Docker for local database
-->
