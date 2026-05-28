---
name: code-review
description: 'Review code changes for quality, bugs, security, and performance issues. Use when the user asks to review code, check a PR, do a code quality check, security review, find bugs, or requests code inspection.'
compatibility: Requires Git repository and code reading tools
allowed-tools:
    - Bash(git:*, node:*, npm:*, npx:*, pnpm:*, yarn:*, python:*, pip:*, pytest:*, go:*, cargo:*, mvn:*, ./mvnw:*, gradle:*, ./gradlew:*, make:*, cmake:*, g++:*, gcc:*, clang:*)
    - Glob
    - Grep
    - Read
    - mcp__context7
    - mcp__fetch
    - mcp__git
    - mcp__jetbrains
    - mcp__markitdown
    - mcp__sequential-thinking
    - mcp__serena
---

# Code Review Skill

Systematically review code changes to identify quality, security,
and performance issues.

## Review Process

1. Gather context: `git status --short`, `git diff --name-only [--cached]`;
   deep dive with `mcp__git__git_diff`, `mcp__serena__find_referencing_symbols`, `mcp__jetbrains__get_symbol_info`.
2. Analyze:
    - Code quality: readability, consistency, abstraction, duplication, complexity(≤15 lines/func 권장)
    - Bugs: logic/edge cases, null/undefined, error handling, resource cleanup
    - Security: injection, XSS, authz/authn, secret exposure
    - Performance: extra loops, N+1, memory leaks, inefficient algo
    - Tests: present? edge cases? mocking 적절성?
3. Output format:

```markdown
## Code Review Summary

[2-3 sentence overview of changes]

## Critical Issues (Must Fix)

- `file:line` - [Issue description] - [Fix approach]

## Major Issues (Should Fix)

- `file:line` - [Issue description] - [Improvement suggestion]

## Minor Suggestions (Optional)

- `file:line` - [Suggestion]

## Positive Observations

- [Good practices noted]

## Overall Assessment

[Final recommendations]
```

## Language-Specific Checkpoints

- JavaScript/TypeScript: strict mode, async/await error handling, type definitions, ESLint rules
- Python: PEP 8, type hints, `with` for resources, specific exceptions
- Java/Kotlin: null safety, immutability, try-with-resources, thread safety
- Go: error handling, `defer`, goroutine leak 예방, context 전달

## Edge Cases

- **No changes**: Notify that there is nothing to review
- **More than 20 issues**: Group by type, show top 10 by severity first
- **Unclear intent**: Specify ambiguous parts and request clarification
- **Config files only**: Analyze impact scope of configuration changes

## Notes

- MCP tools are optional; omit if unavailable or add others as needed
