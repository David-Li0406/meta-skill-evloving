# Quolar Reference Documentation

Detailed configuration options, provider setup, and troubleshooting guide for the test-ticket skill.

---

## Table of Contents

1. [Configuration Schema](#configuration-schema)
2. [Provider Setup](#provider-setup)
3. [MCP Server Configuration](#mcp-server-configuration)
4. [Test Generation Patterns](#test-generation-patterns)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Usage](#advanced-usage)

---

## Configuration Schema

### Full Configuration Example

```typescript
// quolar.config.ts
import { defineConfig } from '@quolar/core'

export default defineConfig({
  // Test framework configuration (required)
  testFramework: {
    provider: 'playwright',
    config: './playwright.config.ts',
    testDir: './automation/playwright/tests',
    pageObjectsDir: './automation/playwright/page-objects',
    utilsDir: './automation/playwright/utils',
    reporters: ['html', 'json', 'list']
  },

  // Ticket management (required)
  tickets: {
    provider: 'linear',
    workspace: 'your-workspace',
    defaultLabels: ['automated-tests'],
    branchPrefix: 'test/'
  },

  // Documentation patterns (optional)
  documentation: {
    provider: 'quoth',
    fallbackToCodebase: true
  },

  // Test analytics (optional)
  analytics: {
    provider: 'exolar',
    dashboardUrl: 'https://exolar.ai-innovation.site',
    reportOnEveryRun: true
  },

  // Version control (defaults to GitHub)
  vcs: {
    provider: 'github',
    createPR: true,
    labels: ['automated-tests', 'qa', 'e2e']
  },

  // Workflow options
  workflow: {
    maxHealingAttempts: 3,
    runTypeCheckOnGeneration: true,
    autoCommitFixes: true,
    waitForCI: true,
    ciWaitSeconds: 120
  }
})
```

### Configuration Options Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `testFramework.provider` | string | `'playwright'` | Test framework to use |
| `testFramework.config` | string | `'./playwright.config.ts'` | Path to config file |
| `testFramework.testDir` | string | `'./tests'` | Test output directory |
| `tickets.provider` | string | `'linear'` | Ticket management system |
| `tickets.workspace` | string | - | Workspace identifier |
| `documentation.provider` | string | `'quoth'` | Documentation system |
| `documentation.fallbackToCodebase` | boolean | `true` | Use codebase if docs unavailable |
| `analytics.provider` | string | `'exolar'` | Analytics provider |
| `workflow.maxHealingAttempts` | number | `3` | Max auto-heal retries |

---

## Provider Setup

### Linear Provider (Tickets)

**Required MCP Server**: `linear`

**Setup**:
1. Install Linear MCP server
2. Configure OAuth or API key authentication
3. Ensure workspace access

**Capabilities**:
- `get_issue` - Fetch ticket details
- `update_issue` - Link PR to ticket
- `search_issues` - Find related tickets

**Example Query**:
```typescript
const ticket = await mcp.linear.get_issue({
  id: 'ENG-123',
  includeRelations: true
})
```

### Quoth Provider (Documentation)

**Optional MCP Server**: `quoth`

**Setup**:
1. Install Quoth MCP server
2. Index your project documentation
3. Configure search settings

**Capabilities**:
- `quoth_search_index` - Semantic search
- `quoth_read_doc` - Read full documents
- `quoth_read_chunks` - Read specific chunks

**Example Query**:
```typescript
const patterns = await mcp.quoth.quoth_search_index({
  query: 'playwright authentication test patterns'
})
```

**Graceful Degradation**:
If Quoth is unavailable, the workflow continues using codebase patterns only.

### Exolar Provider (Analytics)

**Optional MCP Server**: `exolar`

**Setup**:
1. Install Exolar MCP server
2. Configure dashboard URL and API key
3. Set up reporters in Playwright config

**Capabilities**:
- `query_exolar_data` - Query test results
- `perform_exolar_action` - Classify failures

**Example Query**:
```typescript
const failures = await mcp.exolar.query_exolar_data({
  dataset: 'execution_failures',
  filters: { execution_id: 'abc123' },
  view_mode: 'detailed'
})

const classification = await mcp.exolar.perform_exolar_action({
  action: 'classify',
  params: { execution_id: 'abc123', test_name: 'login.spec.ts' }
})
```

**Graceful Degradation**:
If Exolar is unavailable, failures are analyzed from local test output.

---

## MCP Server Configuration

### Claude Desktop Configuration

Add to `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@anthropic/linear-mcp-server"],
      "env": {
        "LINEAR_API_KEY": "your-api-key"
      }
    },
    "quoth": {
      "command": "npx",
      "args": ["-y", "@attorneyshare/quoth-mcp-server"],
      "env": {
        "QUOTH_INDEX_PATH": "/path/to/index"
      }
    },
    "exolar": {
      "command": "npx",
      "args": ["-y", "@attorneyshare/exolar-mcp-server"],
      "env": {
        "EXOLAR_API_URL": "https://exolar.ai-innovation.site/api",
        "EXOLAR_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Checking MCP Server Status

```bash
# List connected servers
/mcp

# Check specific server
/mcp linear status
```

---

## Test Generation Patterns

### Locator Patterns

**Preferred Pattern** (resilient to DOM changes):
```typescript
const button = page
  .locator('button:visible')
  .filter({ hasText: 'Accept' })
  .first()
```

**Avoid**:
```typescript
// Fragile - depends on exact DOM structure
const button = page.locator('#submit-btn')
const button = page.locator('.btn-primary')
```

### Wait Strategies

**Use timeout manager**:
```typescript
import { getTimeout } from '../utils/timeout-manager'

await page.waitForURL('**/dashboard', {
  timeout: getTimeout('navigation'),
  waitUntil: 'domcontentloaded'
})
```

**Available timeouts**:
- `navigation` - Page navigation (30s default)
- `network` - API calls (15s default)
- `element` - Element visibility (10s default)
- `animation` - UI transitions (5s default)

### Authentication Setup

**Parallel context creation**:
```typescript
import { createAuthenticatedContextsParallel } from '../utils/fast-setup'

test.beforeAll(async ({ browser }) => {
  const contexts = await createAuthenticatedContextsParallel(browser, {
    users: ['buyer', 'seller'],
    storageStateDir: '.auth'
  })
})
```

### Test Structure

**Use test.step for grouping**:
```typescript
test('user can complete checkout', async ({ page }) => {
  await test.step('Add items to cart', async () => {
    // ...
  })

  await test.step('Proceed to checkout', async () => {
    // ...
  })

  await test.step('Complete payment', async () => {
    // ...
  })
})
```

---

## Troubleshooting

### Common Issues

#### 1. Linear Ticket Not Found

**Error**: `Error: Linear ticket ENG-123 not found`

**Solutions**:
- Verify ticket ID format (should be `PREFIX-NUMBER`)
- Check workspace configuration in `quolar.config.ts`
- Ensure Linear MCP has correct permissions

#### 2. No Test Patterns Found

**Warning**: `No similar tests found in codebase`

**Solutions**:
- Ensure `testDir` path is correct in config
- Run pattern search manually: `/explore test patterns`
- Create baseline tests first for new feature areas

#### 3. Type Checking Failures

**Error**: `TypeScript error in generated test`

**Solutions**:
- Ensure page objects are up to date
- Check import paths
- Run `yarn gql-compile` if using GraphQL types

#### 4. Test Execution Timeout

**Error**: `Test timeout of 30000ms exceeded`

**Solutions**:
- Use `getTimeout()` with appropriate category
- Check for missing `await` statements
- Add `waitUntil: 'domcontentloaded'` to navigation

#### 5. Strict Mode Violations

**Error**: `Error: strict mode violation: locator resolved to N elements`

**Solutions**:
- Add `.first()` to locator chain
- Add `.filter({ hasText: 'specific text' })`
- Use more specific locator

#### 6. Authentication Failures

**Error**: `401 Unauthorized during test execution`

**Solutions**:
- Delete `.auth/` directory and re-run
- Check if auth tokens have expired
- Verify test user credentials

### Debug Mode

Run workflow with verbose output:
```
/test-ticket ENG-123 --verbose
```

This shows:
- Full MCP responses
- Pattern search results
- Generated test code before execution
- Detailed failure analysis

---

## Advanced Usage

### Custom Test Templates

Override default templates by creating:
```
.quolar/templates/
├── test.template.ts      # Main test template
├── page-object.template.ts
└── helper.template.ts
```

### Parallel Scenario Generation

For complex features, tests are generated in parallel:
```typescript
// Workflow spawns multiple agents
const agents = scenarios.map(scenario =>
  Task({
    subagent_type: 'general-purpose',
    description: `Generate ${scenario.name}`,
    prompt: generatePrompt(scenario)
  })
)
await Promise.all(agents)
```

### Custom Healing Rules

Define custom auto-fix patterns in config:
```typescript
export default defineConfig({
  workflow: {
    customHealingRules: [
      {
        pattern: /Element not interactable/,
        fix: 'Add .scrollIntoViewIfNeeded() before interaction'
      },
      {
        pattern: /Network request failed/,
        fix: 'Add retry logic with exponential backoff'
      }
    ]
  }
})
```

### Skip Individual Steps

```
/test-ticket ENG-123 --skip-steps=2,6
```

Available skip options:
- `1` - Ticket analysis (uses cache)
- `2` - Pattern search (uses defaults)
- `6` - CI integration
- `7` - PR creation

### Integration with CI

**GitHub Actions Example**:
```yaml
name: Quolar Test Generation
on:
  issues:
    types: [labeled]

jobs:
  generate-tests:
    if: contains(github.event.label.name, 'needs-tests')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate Tests
        run: |
          claude-code --non-interactive \
            "/test-ticket ${{ github.event.issue.number }}"
```

---

## Support

- **Issues**: https://github.com/Montinou/quolar/issues
- **Documentation**: https://github.com/Montinou/quolar/tree/main/docs
- **Full Workflow Docs**: See `docs/automated-testing-workflow/` in repository
