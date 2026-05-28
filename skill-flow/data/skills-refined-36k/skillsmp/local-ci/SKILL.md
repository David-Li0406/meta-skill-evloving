---
name: local-ci
description: Use when running 'deno task ci', local CI checks, or pre-push validation. Delegates to sub agent for context efficiency.
allowed-tools: [Bash, Read, Edit, Grep, Glob, Task]
---

# Local CI Execution

## Overview

Run CI locally to verify code quality before pushing.

**Recommendation**: Delegate to sub agent to save context.

## Execution Methods

### Sub Agent Delegation (Preferred)

```typescript
Task({
  subagent_type: "Bash",
  prompt: "Run deno task ci and report results",
  description: "Run local CI"
})
```

### Direct Execution (Watch for Sandbox)

When JSR/Deno packages need to be fetched:

```typescript
Bash({
  command: "deno task ci",
  dangerouslyDisableSandbox: true,
})
```

## CI Pipeline Stages

`deno task ci` runs in order:

1. **deps** - Cache dependencies (`deno.lock`)
2. **check** - Type checking
3. **jsr-check** - JSR publish dry-run
4. **test** - Run tests (216+ tests)
5. **lint** - Deno lint
6. **fmt** - Format check

## Pre-Push Workflow

Always pass local CI before pushing:

```bash
deno task ci && git push origin branch-name
```

Or with sandbox bypass:

```typescript
Bash({
  command: "deno task ci && git push origin branch-name",
  dangerouslyDisableSandbox: true,
})
```

## Error Handling

| Error Type | Skill Reference |
|------------|-----------------|
| JSR connection failed | `/ci-troubleshooting` |
| Lint errors | `/ci-troubleshooting` |
| Test failures | `/ci-troubleshooting` |
| Network blocked | `/git-gh-sandbox` |

## Quick Commands

```bash
# Full CI
deno task ci

# Type check only
deno check src/**/*.ts

# Lint only
deno lint

# Test only
deno test --allow-all

# Format only
deno fmt --check
```
