# Step 2: Pattern Search

**Duration**: ~1-2 minutes
**Purpose**: Search actual codebase for relevant testing patterns.

---

## Actions

### 1. Search Existing Playwright Tests

Find similar tests using keywords from ticket:

```bash
# Search for similar test patterns
grep -r "{keyword}" automation/playwright/tests/
```

### 2. Find Relevant Page Objects

```bash
# List available page objects
ls automation/playwright/page-objects/

# Search for specific page objects
grep -l "class.*Page" automation/playwright/page-objects/*.ts
```

### 3. Check Helper Utilities

```bash
# List utility helpers
ls automation/playwright/utils/

# Find authentication helpers
grep -l "authenticate" automation/playwright/utils/*.ts
```

### 4. Query Quoth MCP (MANDATORY)

**Per project rules**: ALWAYS search Quoth for documented patterns BEFORE generating code.

```typescript
// REQUIRED: Search Quoth for existing test patterns
const patterns = await mcp.quoth.quoth_search_index({
  query: "playwright authentication flow test patterns"
})

// Read relevant documentation chunks
if (patterns.chunks?.length > 0) {
  const docs = await mcp.quoth.quoth_read_chunks({
    chunk_ids: patterns.chunks.map(c => c.id).slice(0, 5)
  })
}
```

**If Quoth unavailable**: Log warning but continue - document this gap in PR for review.

---

## Key Patterns to Extract

### Locator Patterns

```typescript
// Preferred: Resilient to DOM changes
const button = page
  .locator('button:visible')
  .filter({ hasText: 'Accept' })
  .first()

// Avoid: Fragile selectors
const button = page.locator('#submit-btn')
```

### Wait Strategies

```typescript
// Use timeout manager
import { getTimeout } from '../utils/timeout-manager'

await page.waitForURL('**/dashboard', {
  timeout: getTimeout('navigation'),
  waitUntil: 'domcontentloaded'
})
```

### Authentication Context

```typescript
import { createAuthenticatedContextsParallel } from '../utils/fast-setup'

test.beforeAll(async ({ browser }) => {
  const contexts = await createAuthenticatedContextsParallel(browser, {
    users: ['buyer', 'seller'],
    storageStateDir: '.auth'
  })
})
```

### API Interception

```typescript
await page.route('**/api/data', route => {
  route.fulfill({
    status: 200,
    body: JSON.stringify({ data: mockData })
  })
})
```

---

## Output

Generate pattern library: `docs/test-analysis/{ticket-id}-patterns.md`

**Document Structure**:
```markdown
# Test Patterns: {TICKET-ID}

## Existing Similar Tests
- `tests/auth/login.spec.ts` - Authentication flow
- `tests/checkout/payment.spec.ts` - Form submission

## Available Page Objects
- `LoginPage` - Login form interactions
- `DashboardPage` - Dashboard navigation

## Utility Helpers
- `createAuthenticatedContextsParallel` - Multi-user setup
- `getTimeout(category)` - Timeout management
- `blockAnalytics()` - Performance optimization

## Recommended Patterns
1. Use `:visible` filter for locators
2. Use `domcontentloaded` for navigation waits
3. Use `test.step()` for assertion grouping
```

---

## Graceful Degradation

If no patterns are found:
1. Continue with default patterns from project standards
2. Log warning for manual review
3. Generate tests with best-guess structure
