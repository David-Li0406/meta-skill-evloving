---
name: context-gathering
description: Focused context retrieval ("context crunching") for large codebases. Automatically activates during code review, refactoring, feature implementation, or debugging in multi-file projects.
allowed-tools: Read, Grep, Glob, Bash, List
---

# Context Gathering Skill (Context Crunching)

You are an expert software archaeologist. Your goal is to gather **only the minimal, high-signal context** needed to understand, review, or modify code accurately—never dump the entire repository.

This skill implements the "context crunching" pattern: a two-phase process of **discovery → focused retrieval**.

## Core Principles
- **Relevance over completeness**: Include a file only if it directly affects correctness, behavior, or understanding of the target changes.
- **Cap context aggressively**: Aim for 8–15 files maximum (including changed files). Prioritize definitions over implementations.
- **Prefer precision**: Use Grep/Glob surgically to find exact symbols, imports, interfaces, and tests.
- **Explain every choice**: Always justify why each file is included.
- **Avoid noise**: Exclude vendor/, node_modules/, generated code, lockfiles, build artifacts, large data files.

## Activation Triggers
Activate this skill when:
- The user provides a diff, PR, or list of changed files.
- Implementing a feature that touches multiple packages/modules.
- Reviewing or refactoring non-trivial code.
- Debugging issues involving dependencies or interfaces.
- Working in a repository with >20 files.

## Workflow (Always Follow This Order)

1. **Understand the Target**
   - Read the user's request and any provided diff/changed files.
   - Identify key symbols: functions, types, interfaces, constants, imports.

2. **Discovery Phase**
   - Use **Grep** to search for:
     - Import paths from changed files
     - Definitions of used types/interfaces/structs
     - Related test files (*_test.go, test.py, etc.)
     - Configuration or registration sites (e.g., router setups, DI bindings)
   - Use **Glob** to list relevant directories (e.g., internal/, pkg/, api/).
   - Use **List** to browse directory structure if needed.

3. **Selection Phase**
   - Compile a shortlist of ≤15 files.
   - For each file, provide:
     - Path
     - Brief reason (1–2 sentences)
     - Priority (High/Medium)
   - Output this list clearly before fetching.

4. **Retrieval Phase**
   - Use **Read** on selected files only.
   - If a file is too large (>2000 lines), consider reading only relevant sections via Grep + Read.
   - Summarize or excerpt if appropriate.

5. **Proceed**
   - Only after gathering context: analyze, implement, review, or debug.
   - Reference gathered files explicitly in reasoning.

## Example Selection Output Format
```
Selected context files (12 total):

1. internal/service/user.go          High - Defines UserService interface used in handler
2. api/handlers/user_handler.go     High - Contains the changed code
3. internal/repository/user_repo.go  High - Implementation of UserService
4. models/user.go                    High - Shared User struct and validation
5. api/handlers/user_handler_test.go Medium - Tests for the handler logic
6. config/routes.go                  Medium - Route registration affecting API surface
...
```

## Best Practices
- Start narrow, expand only if missing critical info.
- When reviewing tests: always include the tested file and vice versa.
- For dependency injection: trace interface → implementations → registrations.
- For errors: include error type definitions and wrapping sites.

See [examples.md](examples.md) for real-world scenarios.

[examples.md](examples.md)
