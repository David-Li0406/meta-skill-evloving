---
name: test-ticket
description: |
  This skill should be used when the user asks to "test ticket ENG-123", "automate ENG-456", "create e2e tests from ticket", "generate playwright tests from ticket", "automate acceptance criteria", or mentions Linear ticket IDs like ENG-123, LIN-456, PROJ-789. Converts Linear tickets into self-healing Playwright E2E tests with automatic PR creation and CI integration.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(git:*), Bash(npx:*), Bash(yarn:*), Bash(gh:*)
user-invocable: true
---

# Test Ticket Automation

Convert Linear tickets to self-healing Playwright E2E tests.

## Quick Start

```bash
/test-ticket ENG-123           # Full workflow
/test-ticket ENG-456 --dry-run # Generate without executing
/test-ticket ENG-789 --skip-pr # Execute but skip PR creation
```

## Workflow Overview

Execute these 7 steps in order (~15-20 minutes total):

```
Ticket Analysis (~30s)
       │
Pattern Search (~1-2m)  ◄── QUOTH: Search existing patterns
       │
Test Planning (~2m)
       │
Test Generation (~3m)
       │
Execution Loop (~4-8m)  ─── Auto-heal up to 3 times
       │
CI Integration (~1m)
       │
PR Creation (~5-8m)     ◄── Wait for Vercel preview, execute tests
```

### Step Details

| Step | Action | Detailed Guide |
|------|--------|----------------|
| 1. Analyze | Fetch ticket, extract AC, pull branch, analyze changes | [01-ticket-analysis.md](./steps/01-ticket-analysis.md) |
| 2. Search | Query Quoth for test patterns (MANDATORY) | [02-pattern-search.md](./steps/02-pattern-search.md) |
| 3. Plan | Generate test scenarios from acceptance criteria | [03-test-planning.md](./steps/03-test-planning.md) |
| 4. Generate | Create Playwright test files | [04-test-generation.md](./steps/04-test-generation.md) |
| 5. Execute | Run tests with auto-healing (3 attempts) | [05-execution-loop.md](./steps/05-execution-loop.md) |
| 6. Integrate | Update GitHub Actions CI config | [06-ci-integration.md](./steps/06-ci-integration.md) |
| 7. PR | Evaluate docs, create PR, test on preview | [07-pr-creation.md](./steps/07-pr-creation.md) |

## MCP Requirements

### Required

| Server | Purpose | Setup |
|--------|---------|-------|
| **linear** | Fetch ticket, link PR | Requires `LINEAR_API_KEY` |
| **quoth** | Search test patterns | OAuth authentication |

### Optional

| Server | Purpose | Fallback |
|--------|---------|----------|
| **exolar** | Classify failures, analytics | Skip classification |

Verify connections with `${CLAUDE_PLUGIN_ROOT}/skills/test-ticket/scripts/check-mcp.sh`.

**IMPORTANT**: Per project rules, Quoth MUST be consulted before generating test code.

## Command Options

Parse arguments for these flags:

| Flag | Effect |
|------|--------|
| `--dry-run` | Generate tests and plan only, skip execution and PR |
| `--skip-pr` | Full workflow but stop before PR creation |
| `--verbose` | Show detailed progress including MCP responses |

## Project Detection

Determine test type and location from ticket labels:

| Labels | Test Type | Location |
|--------|-----------|----------|
| `feature`, `ui` | E2E UI Tests | `automation/playwright/tests/{feature}/` |
| `bug`, `ui` | Regression Tests | `automation/playwright/tests/{feature}/` |
| `api`, `backend` | API Integration | `automation/playwright/tests/{feature}-api/` |

## Auto-Healing Summary

The execution loop automatically fixes common failures:

| Error | Quick Fix |
|-------|-----------|
| Locator not found | Add `:visible` filter |
| Timeout exceeded | Use `getTimeout()` helper |
| Strict mode violation | Add `.first()` |
| 401 Unauthorized | Delete `.auth/`, recreate |

After 3 failed attempts, tests are marked `test.fixme()` for manual review.

See [references/auto-healing.md](./references/auto-healing.md) for detailed healing strategies.

## Generated Artifacts

| Artifact | Location |
|----------|----------|
| Test analysis | `docs/test-analysis/{ticket-id}.md` |
| Test plan | `docs/test-plans/{ticket-id}-test-plan.md` |
| Test files | `automation/playwright/tests/{feature}/` |
| Git branch | `test/{ticket-id}-automated-tests` |
| Pull request | GitHub with linked Linear ticket |

See [references/generated-artifacts.md](./references/generated-artifacts.md) for detailed artifact documentation.

## Configuration

Create `quolar.config.ts` in project root. See [reference.md](./reference.md) for full schema.

**Minimal example:**
```typescript
import { defineConfig } from '@quolar/core'

export default defineConfig({
  testFramework: {
    provider: 'playwright',
    testDir: './automation/playwright/tests'
  },
  tickets: {
    provider: 'linear',
    workspace: 'your-workspace'
  }
})
```

## Utility Scripts

Available at `${CLAUDE_PLUGIN_ROOT}/skills/test-ticket/scripts/`:

| Script | Purpose |
|--------|---------|
| `check-mcp.sh` | Validate MCP server connections |
| `validate-ticket.sh` | Verify ticket data format |
| `cleanup-auth.sh` | Clear stale authentication state |

## Additional Resources

### Reference Files

- **[reference.md](./reference.md)** - Full configuration schema
- **[references/auto-healing.md](./references/auto-healing.md)** - Detailed healing strategies
- **[references/generated-artifacts.md](./references/generated-artifacts.md)** - Artifact documentation

### Step-by-Step Guides

Detailed instructions for each workflow step in `steps/`:
- [01-ticket-analysis.md](./steps/01-ticket-analysis.md)
- [02-pattern-search.md](./steps/02-pattern-search.md)
- [03-test-planning.md](./steps/03-test-planning.md)
- [04-test-generation.md](./steps/04-test-generation.md)
- [05-execution-loop.md](./steps/05-execution-loop.md)
- [06-ci-integration.md](./steps/06-ci-integration.md)
- [07-pr-creation.md](./steps/07-pr-creation.md)

### Troubleshooting

See [troubleshooting.md](./troubleshooting.md) for common issues and solutions.
