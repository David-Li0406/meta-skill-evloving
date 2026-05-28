---
name: git-gh-sandbox
description: Use when executing git or gh commands that require network access. Explains sandbox restrictions for git push, pull, fetch, clone, and all gh commands.
allowed-tools: [Bash, Read, Edit, Grep, Glob]
---

# Network Sandbox Management

## Overview

Claude Code sandbox restricts network access by default. This skill documents:
1. Which commands need sandbox bypass
2. Current allowlist configuration
3. Troubleshooting connection errors

## Allowed Domains (settings.json)

Current allowlist in `.claude/settings.json`:

| Domain | Purpose |
|--------|---------|
| jsr.io, *.jsr.io | JSR package registry |
| deno.land, *.deno.land | Deno standard library |
| github.com | Git remote operations |
| api.github.com | GitHub CLI (gh) |

## Commands Requiring Sandbox Bypass

Even with allowlist, some commands may need `dangerouslyDisableSandbox: true`:

### Git Network Commands

```typescript
// Required for: push, pull, fetch, clone
Bash({
  command: "git push -u origin branch-name",
  dangerouslyDisableSandbox: true,
})
```

### GitHub CLI

```typescript
// Required for all gh commands
Bash({
  command: "gh pr create --base develop --head feature-branch",
  dangerouslyDisableSandbox: true,
})
```

### Deno with External Packages

```typescript
// Required when JSR/deno.land fetch fails in sandbox
Bash({
  command: "deno task ci",
  dangerouslyDisableSandbox: true,
})
```

### Claude Agent SDK (climpt-agent)

```typescript
// Required for API calls to api.anthropic.com
Bash({
  command: "echo '...' | deno run climpt-agent.ts",
  dangerouslyDisableSandbox: true,
})
```

## Commands NOT Requiring Bypass

Local-only operations work in sandbox:

- `git status`, `git add`, `git commit`
- `git log`, `git diff`, `git branch`
- `git checkout`, `git merge` (local)
- `deno fmt`, `deno lint` (cached deps)
- `deno test` (cached deps)

## Troubleshooting

### Connection Timeout / Retry

```
fatal: unable to access 'https://github.com/...':
Could not resolve host: github.com
```

**Cause**: Sandbox blocking network access
**Solution**: Add `dangerouslyDisableSandbox: true`

### JSR Package Load Failed

```
error: JSR package manifest for '@std/path' failed to load.
Import 'https://jsr.io/@std/path/meta.json' failed.
```

**Cause**: Sandbox blocking JSR access
**Solutions**:
1. Verify jsr.io in allowedDomains (should already be there)
2. Use `dangerouslyDisableSandbox: true` if still failing

### Transient Network Errors

Connection may fail intermittently due to:
- Network latency
- DNS resolution delays
- Rate limiting

**Strategy**: Retry the command (usually succeeds on second attempt)

```typescript
// Retry pattern for network commands
Bash({
  command: "git push origin branch-name || sleep 2 && git push origin branch-name",
  dangerouslyDisableSandbox: true,
})
```

## Adding New Domains

To allow new external domains, edit `.claude/settings.json`:

```json
{
  "sandbox": {
    "network": {
      "allowedDomains": [
        "existing-domain.com",
        "new-domain.com"
      ]
    }
  }
}
```

**Note**: Wildcards supported (e.g., `*.example.com`)

## Quick Reference

| Situation | Action |
|-----------|--------|
| git push/pull/fetch/clone | `dangerouslyDisableSandbox: true` |
| gh (any command) | `dangerouslyDisableSandbox: true` |
| deno task ci (fresh deps) | `dangerouslyDisableSandbox: true` |
| deno task ci (cached) | Sandbox OK |
| Claude API calls | `dangerouslyDisableSandbox: true` |
| Connection error | Retry with sandbox bypass |

## Related Skills

- CI execution: `/local-ci`
- CI errors: `/ci-troubleshooting`
- Release flow: `/release-procedure`
