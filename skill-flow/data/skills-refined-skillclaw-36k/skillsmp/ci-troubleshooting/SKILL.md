---
name: ci-troubleshooting
description: Use when user encounters CI errors, JSR connection issues, 'deno task ci' failures, or sandbox-related build problems. Provides solutions for common CI issues.
allowed-tools: [Bash, Read, Edit, Grep, Glob]
---

# CI Troubleshooting

## CI Pipeline Stages

`deno task ci` runs these stages in order:

1. **deps** - Cache dependencies (deno.lock)
2. **check** - Type checking
3. **jsr-check** - JSR publish dry-run
4. **test** - Run tests
5. **lint** - Deno lint
6. **fmt** - Format check

## Network / Sandbox Issues

### JSR Connection Failed

```
error: JSR package manifest for '@std/path' failed to load.
Import 'https://jsr.io/@std/path/meta.json' failed.
```

**Solution**: See `/git-gh-sandbox` skill for sandbox bypass.

```typescript
Bash({
  command: "deno task ci",
  dangerouslyDisableSandbox: true,
})
```

## Lint Errors

### Common Rules and Fixes

| Rule | Error | Fix |
|------|-------|-----|
| `no-console` | console.log in non-CLI code | Add `// deno-lint-ignore no-console` |
| `prefer-ascii` | Japanese in comments | Change to English |
| `no-await-in-loop` | await in for loop | Add ignore or refactor to Promise.all |
| `eqeqeq` | `!=` instead of `!==` | Use strict equality |
| `explicit-function-return-type` | Missing return type | Add `: ReturnType` |
| `ban-unused-ignore` | Unused lint ignore | Remove or adjust ignore list |

### File-Level Lint Ignore

Add at top of file (after shebang if present):

```typescript
#!/usr/bin/env -S deno run ...
// deno-lint-ignore-file no-console prefer-ascii
```

### Line-Level Lint Ignore

Add comment before the line:

```typescript
// deno-lint-ignore no-console
console.log("Debug output");
```

### prefer-ascii (Japanese Text)

Replace Japanese with English in:
- Code comments
- Doc references (e.g., `#command-schema` not `#command-スキーマ`)
- Error messages in library code

Exception: Japanese OK in test fixtures or user-facing CLI output.

## Test Failures

### Flaky Tests (Timing Issues)

Example: ID uniqueness test failing due to timestamp collision

**Problem**: Parallel execution with small delays
```typescript
// Bad: 2ms may not be enough for millisecond-precision timestamps
const promises = Array.from({ length: 10 }, (_, i) =>
  new Promise((r) => setTimeout(() => r(generateId()), i * 2))
);
```

**Solution**: Sequential execution with adequate delay
```typescript
// Good: Sequential with 5ms delay
for (let i = 0; i < 10; i++) {
  ids.push(generateId());
  await new Promise((r) => setTimeout(r, 5));
}
```

### Type Errors in Tests

Check for:
- Missing type assertions (`as Type`)
- Incorrect mock implementations
- Outdated test fixtures after interface changes

## Format Errors

### Check Without Fixing

```bash
deno fmt --check
```

### Fix All

```bash
deno fmt
```

## Quick Debugging

### Run Single Stage

```bash
# Type check only
deno check src/**/*.ts

# Lint only
deno lint

# Single test file
deno test path/to/test.ts
```

### Verbose Test Output

```bash
deno test --allow-all 2>&1 | head -100
```

## Related Skills

- Network sandbox: `/git-gh-sandbox`
- CI execution: `/local-ci`
- Release flow: `/release-procedure`
