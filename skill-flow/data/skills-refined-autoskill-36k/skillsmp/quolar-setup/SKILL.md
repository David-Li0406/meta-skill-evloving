---
name: quolar-setup
description: |
  This skill should be used when the user asks to "setup quolar", "configure quolar", "configure test automation", "verify MCP servers", "create quolar.config.ts", or is using Quolar for the first time. Provides interactive configuration wizard for Quolar test automation including MCP server validation and directory setup.
allowed-tools: Read, Write, Bash(claude:*), Bash(npx:*), Bash(ls:*), Bash(mkdir:*)
user-invocable: true
---

# Quolar Setup Wizard

Interactive configuration wizard for Quolar test automation.

## Quick Overview

Complete 5 phases to set up Quolar:

| Phase | Action | Duration |
|-------|--------|----------|
| 1. Pre-Flight | Verify MCP servers | ~1m |
| 2. Configuration | Create `quolar.config.ts` | ~2m |
| 3. Directories | Set up folder structure | ~30s |
| 4. Verification | Test all connections | ~1m |
| 5. Summary | Display completion status | ~30s |

**Total:** ~5 minutes

---

## Phase 1: Pre-Flight Checks

### 1.1 Check MCP Servers

List connected servers:
```bash
/mcp
```

### 1.2 Verify Required Servers

Confirm these servers are connected:

| Server | Status | Required |
|--------|--------|----------|
| `linear` | Required | Ticket fetching |
| `quoth` | Required | Pattern docs (MANDATORY) |
| `exolar` | Optional | Test analytics |

### 1.3 Install Missing Servers

If servers are missing, guide installation:

**Linear MCP** (requires LINEAR_API_KEY):
```json
"linear": {
  "command": "npx",
  "args": ["-y", "@linear/mcp-server"],
  "env": { "LINEAR_API_KEY": "lin_api_xxx" }
}
```

**Quoth MCP**:
```bash
claude mcp add --transport http quoth https://quoth.ai-innovation.site/api/mcp
```

**Exolar MCP** (optional):
```bash
claude mcp add exolar-qa --transport http https://exolar.ai-innovation.site/api/mcp/mcp -s user
```

See [references/mcp-setup.md](./references/mcp-setup.md) for detailed setup instructions.

---

## Phase 2: Configuration File

### 2.1 Check for Existing Config

```bash
ls quolar.config.ts 2>/dev/null || echo "No config found"
```

### 2.2 Gather Information

If config missing, ask user for:
1. **Linear workspace name** (e.g., "attorneyshare")
2. **Test directory path** (default: `./automation/playwright/tests`)
3. **Playwright config path** (default: `./playwright.config.ts`)

### 2.3 Generate Configuration

Create `quolar.config.ts`:

```typescript
import { defineConfig } from '@quolar/core'

export default defineConfig({
  testFramework: {
    provider: 'playwright',
    config: './playwright.config.ts',
    testDir: './automation/playwright/tests'
  },
  tickets: {
    provider: 'linear',
    workspace: '{user-provided-workspace}'
  },
  documentation: {
    provider: 'quoth'
  },
  analytics: {
    provider: 'exolar'
  },
  workflow: {
    maxHealingAttempts: 3
  }
})
```

---

## Phase 3: Directory Setup

Create required directories:

```bash
mkdir -p automation/playwright/tests
mkdir -p automation/playwright/page-objects
mkdir -p automation/playwright/utils
mkdir -p docs/test-analysis
mkdir -p docs/test-plans
```

---

## Phase 4: Verification

### 4.1 Test Linear Connection

```
mcp__linear__list_issues({ first: 1 })
```

Verify workspace is accessible.

### 4.2 Test Quoth Connection

```
mcp__quoth__quoth_search_index({ query: "playwright test patterns" })
```

Verify documentation access.

### 4.3 Test Playwright Setup

```bash
npx playwright --version
```

If not installed:
```bash
npm install -D @playwright/test
npx playwright install
```

---

## Phase 5: Success Summary

Display completion status:

```
===================================
     Quolar Setup Complete!
===================================

MCP Servers:
  [x] linear - Connected (workspace: {workspace})
  [x] quoth - Connected
  [ ] exolar - Not configured (optional)

Configuration:
  [x] quolar.config.ts created

Directories:
  [x] automation/playwright/tests/
  [x] automation/playwright/page-objects/
  [x] docs/test-analysis/
  [x] docs/test-plans/

Playwright:
  [x] Version: {version}

===================================
         Next Steps
===================================

1. Run: /test-ticket <your-ticket-id>
2. See: skills/test-ticket/SKILL.md for full docs
3. Optional: Configure Exolar for test analytics
```

---

## Additional Resources

### Reference Files

- **[references/mcp-setup.md](./references/mcp-setup.md)** - Detailed MCP server setup instructions
- **[references/troubleshooting.md](./references/troubleshooting.md)** - Common issues and solutions

### Related Documentation

- **[../test-ticket/SKILL.md](../test-ticket/SKILL.md)** - Main test automation workflow
- **[../test-ticket/reference.md](../test-ticket/reference.md)** - Full configuration options
