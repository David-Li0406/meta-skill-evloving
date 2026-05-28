# Troubleshooting Guide

Common issues and solutions for the test-ticket skill.

---

## Table of Contents

1. [MCP Server Issues](#mcp-server-issues)
2. [Ticket Analysis Issues](#ticket-analysis-issues)
3. [Pattern Search Issues](#pattern-search-issues)
4. [Test Generation Issues](#test-generation-issues)
5. [Test Execution Issues](#test-execution-issues)
6. [CI Integration Issues](#ci-integration-issues)
7. [PR Creation Issues](#pr-creation-issues)
8. [Debug Mode](#debug-mode)

---

## MCP Server Issues

### Linear MCP Not Connected

**Error**: `MCP server 'linear' not available`

**Solutions**:
1. Check MCP configuration in `~/.claude/claude_desktop_config.json`
2. Verify LINEAR_API_KEY is set
3. Restart Claude Code after configuration changes

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@anthropic/linear-mcp-server"],
      "env": {
        "LINEAR_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Quoth MCP Unavailable (Non-Blocking)

**Warning**: `Quoth MCP unavailable, using codebase patterns only`

This is expected behavior. The workflow continues using:
- Existing test files in `automation/playwright/tests/`
- Page objects in `automation/playwright/page-objects/`
- Utility helpers in `automation/playwright/utils/`

### Exolar MCP Unavailable (Non-Blocking)

**Warning**: `Exolar MCP unavailable, using local failure analysis`

This is expected behavior. Failure analysis falls back to:
- Playwright HTML report parsing
- JSON reporter output
- Console error extraction

---

## Ticket Analysis Issues

### Ticket Not Found

**Error**: `Linear ticket ENG-123 not found`

**Causes**:
- Incorrect ticket ID format
- Ticket in different workspace
- Insufficient permissions

**Solutions**:
1. Verify ticket ID format (PREFIX-NUMBER)
2. Check workspace in `quolar.config.ts`
3. Verify Linear API key has read access

### No Labels on Ticket

**Warning**: `No labels found, defaulting to E2E UI tests`

**Impact**: Workflow continues with default assumptions

**Recommendation**:
- Add labels to ticket before running: `feature`, `bug`, `api`, `ui`
- Or manually specify test type in workflow

### Missing Acceptance Criteria

**Warning**: `No acceptance criteria found in ticket`

**Impact**: Test scenarios generated from description only

**Solutions**:
1. Add acceptance criteria to Linear ticket
2. Use structured format in description:
   ```
   ## Acceptance Criteria
   - [ ] User can login
   - [ ] Dashboard loads after login
   ```

---

## Pattern Search Issues

### No Similar Tests Found

**Warning**: `No similar tests found in codebase`

**Causes**:
- New feature area without existing tests
- Incorrect `testDir` configuration
- Keyword mismatch

**Solutions**:
1. Create baseline tests first for new areas
2. Verify `testDir` path in config
3. Manually specify patterns to use

### Page Objects Not Found

**Warning**: `No page objects found for {feature}`

**Impact**: Tests generated without page object abstraction

**Solutions**:
1. Create page object before running workflow
2. Workflow will create inline locators (less maintainable)

---

## Test Generation Issues

### TypeScript Type Errors

**Error**: `TypeScript error in generated test`

**Common Causes**:
- Outdated page objects
- Missing GraphQL types
- Incorrect import paths

**Solutions**:
```bash
# Update GraphQL types
yarn gql-compile

# Check types
yarn check:types

# Verify imports
cat automation/playwright/tests/{feature}/{test}.spec.ts
```

### Import Resolution Failures

**Error**: `Cannot find module '../utils/fast-setup'`

**Solutions**:
1. Verify path aliases in `tsconfig.json`
2. Check file exists at expected location
3. Run `yarn install` to ensure dependencies

### Branch Already Exists

**Error**: `A branch named 'test/ENG-123' already exists`

**Solutions**:
```bash
# Delete existing branch
git branch -D test/ENG-123-automated-tests

# Or use different suffix
git checkout -b test/ENG-123-automated-tests-v2
```

---

## Test Execution Issues

### Timeout Exceeded

**Error**: `Test timeout of 30000ms exceeded`

**Common Causes**:
- Missing `await` statements
- Slow network/API responses
- Hardcoded timeout too short

**Solutions**:
```typescript
// Use timeout manager
import { getTimeout } from '../utils/timeout-manager'

await page.waitForURL('**/dashboard', {
  timeout: getTimeout('navigation'),  // Dynamic timeout
  waitUntil: 'domcontentloaded'
})
```

### Strict Mode Violations

**Error**: `strict mode violation: locator resolved to N elements`

**Solutions**:
```typescript
// Add .first() to chain
const button = page
  .locator('button:visible')
  .filter({ hasText: 'Submit' })
  .first()  // Resolve to single element

// Or add more specific filter
const button = page
  .locator('button')
  .filter({ hasText: 'Submit' })
  .filter({ has: page.locator('.icon-check') })
```

### Authentication Failures

**Error**: `401 Unauthorized during test execution`

**Solutions**:
```bash
# Delete cached auth state
rm -rf .auth/

# Re-run setup
npx playwright test --project=setup
```

### Element Not Interactable

**Error**: `Element is not interactable`

**Solutions**:
```typescript
// Scroll into view first
await element.scrollIntoViewIfNeeded()
await element.click()

// Or wait for animations
await page.waitForTimeout(300)  // Animation delay
await element.click()
```

### Flaky Tests (Intermittent Failures)

**Symptoms**: Test passes sometimes, fails others

**Solutions**:
1. Add explicit waits for network requests
2. Use `waitUntil: 'domcontentloaded'` for navigation
3. Add retries in Playwright config:
   ```typescript
   retries: process.env.CI ? 2 : 0
   ```

---

## CI Integration Issues

### Playwright Config Invalid

**Error**: `Invalid playwright.config.ts`

**Solutions**:
```bash
# Validate config
npx playwright test --list

# Check for syntax errors
npx tsc --noEmit playwright.config.ts
```

### CI Workflow Syntax Error

**Error**: `Invalid workflow file`

**Solutions**:
```bash
# Validate YAML locally
yamllint .github/workflows/ci.yml

# Use act for local testing
act -n push
```

### Browser Installation Failed

**Error**: `Executable doesn't exist at /path/to/chromium`

**Solutions**:
```yaml
# Add browser installation step
- name: Install Playwright browsers
  run: npx playwright install --with-deps chromium
```

---

## PR Creation Issues

### Git Push Rejected

**Error**: `remote rejected (permission denied)`

**Solutions**:
1. Verify Git credentials
2. Check branch protection rules
3. Ensure push access to repository

### PR Already Exists

**Error**: `A pull request already exists for this branch`

**Solutions**:
```bash
# Check existing PR
gh pr list --head test/ENG-123-automated-tests

# Update existing PR instead
gh pr edit {pr-number} --body "Updated description"
```

### Linear Link Failed

**Warning**: `Failed to link PR to Linear ticket`

**Causes**:
- Linear MCP permissions
- Invalid ticket ID
- Network issues

**Impact**: PR created but not linked to ticket

**Manual Fix**:
1. Open PR in GitHub
2. Add Linear ticket ID to description
3. Linear integration auto-links

---

## Debug Mode

### Enable Verbose Logging

```bash
/test-ticket ENG-123 --verbose
```

Shows:
- Full MCP request/response
- Pattern search results
- Generated code before execution
- Detailed failure analysis

### Run Playwright in Debug Mode

```bash
# Headed mode with slowMo
npx playwright test --headed --debug

# Trace on failure
npx playwright test --trace on

# Step-through debugger
PWDEBUG=1 npx playwright test
```

### View Test Report

```bash
# Open HTML report
npx playwright show-report

# Check JSON output
cat playwright-report/results.json | jq '.suites[].specs[] | select(.ok == false)'
```

### Check MCP Server Status

```bash
# List connected servers
/mcp

# Verify specific server
/mcp linear status
```

---

## Getting Help

If issues persist:

1. **Check logs**: `~/.claude/logs/`
2. **GitHub Issues**: https://github.com/Montinou/quolar/issues
3. **Documentation**: https://github.com/Montinou/quolar/tree/main/docs
