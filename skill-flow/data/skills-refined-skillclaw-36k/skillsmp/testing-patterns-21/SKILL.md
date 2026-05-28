---
name: testing-patterns
description: Testing patterns for Next.js App Router with Supabase. Use when adding tests, verifying fixes, or preventing regressions. Keywords: test, testing, jest, vitest, unit test, integration test, mock, Supabase mock, playwright, e2e.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "4.0"
  project: "stepleague"
  last_updated: "2026-01-18"
---

# Testing Patterns Skill

## Overview

StepLeague has two test suites:
- **Vitest** (unit/integration): 1,101+ tests for hooks, components, utilities
- **Playwright** (E2E): 63 tests for full user flows against live site

---

## Quick Start

```bash
# Unit/Integration Tests (Vitest)
npm run test              # Run all
npm run test:watch        # Watch mode
npm run test:coverage     # Coverage report

# E2E Tests (Playwright)
npm run test:e2e          # Run all (headless)
npm run test:e2e:headed   # Visible browser
npm run test:e2e:ui       # Playwright UI
```

---

## User Guidance (Show This When Asked About Tests)

> [!NOTE]
> When the user asks "what can tests do?", "how do I use tests?", or similar questions about testing capabilities, show them this section.

### Is it Automatic?

**Currently: No.** Tests don't run automatically on changes. Options:
1. **Watch Mode** (`npm run test:watch`) - Leave running while coding; tests re-run on save
2. **CI/CD** (not yet configured) - Could add GitHub Actions to run on push

### When to Ask for Tests

**Ask to RUN tests when:**
- Finished implementing a feature
- Debugging an issue (catch regressions)
- Before committing/deploying

**Ask to WRITE tests when:**
- Fixed a bug (prevents recurrence)
- Added new API route or complex component
- Want to verify specific behavior

### Example Prompts

| Prompt | What happens |
|--------|--------------|
| "Run the tests" | Runs `npm test` and shows results |
| "Write a test for [feature]" | Creates test file following skill patterns |
| "Check test coverage" | Runs coverage report |
| "Add tests for proxy claim" | Writes comprehensive tests for that feature |

---

## Project Testing Stack

| Tool | Purpose | Installed |
|------|---------| --------- |
| **Vitest** | Test runner (faster than Jest for Vite/Next) | ✅ |
| **React Testing Library** | Component testing | ✅ |
| **MSW** | API mocking | ✅ |
| **jsdom** | Browser environment simulation | ✅ |

---

## Test File Structure

```
src/
├── __mocks__/
│   └── supabase.ts          # Mock factories (use this!)
├── lib/
│   └── auth/
│       └── __tests__/
│           └── sessionCache.test.ts
├── app/
│   └── api/
│       └── proxy-claim/
│           └── __tests__/
│               └── route.test.ts
```

---

## Pattern 1: Session Cache Testing (REAL EXAMPLE)

From `src/lib/auth/__tests__/sessionCache.test.ts`:

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setCachedSession, getCachedSession, clearCachedSession } from '../sessionCache';

describe('sessionCache', () => {
  beforeEach(() => {
    clearCachedSession();
  });

  it('stores session when all params provided', () => {
    const futureTime = Math.floor(Date.now() / 1000) + 3600;
    setCachedSession('token-123', 'user-456', futureTime);
    
    const cached = getCachedSession();
    expect(cached).not.toBeNull();
    expect(cached?.accessToken).toBe('token-123');
  });

  it('returns null when session expires within 60s buffer', () => {
    const soonTime = Math.floor(Date.now() / 1000) + 30;
    setCachedSession('token-123', 'user-456', soonTime);
    
    expect(getCachedSession()).toBeNull();
  });
});
```

---

## Pattern 2: Using Mock Factories (REAL EXAMPLE)

From `src/__mocks__/supabase.ts`:

```typescript
import { vi } from 'vitest';

// Create mock user
export const createMockUser = (overrides = {}) => ({
  id: 'user-123',
  email: 'test@example.com',
  created_at: '2026-01-01T00:00:00Z',
  ...overrides,
});

// Create mock proxy
export const createMockProxy = (overrides = {}) => ({
  id: 'proxy-456',
  display_name: 'Proxy User',
  is_proxy: true,
  managed_by: 'user-123',
  invite_code: 'CLAIM123',
  claims_remaining: 1,
  ...overrides,
});

// Create chainable Supabase client mock
export const createMockSupabaseClient = () => ({
  from: vi.fn(() => ({
    select: vi.fn().mockReturnThis(),
    eq: vi.fn().mockReturnThis(),
    single: vi.fn().mockResolvedValue({ data: null, error: null }),
  })),
  auth: {
    getUser: vi.fn().mockResolvedValue({ data: { user: null }, error: null }),
    signOut: vi.fn().mockResolvedValue({ error: null }),
  },
});

// Usage in test:
// import { createMockSupabaseClient, createMockProxy } from '@/__mocks__/supabase';
```

---

## Pattern 3: Auth Level Testing (REAL EXAMPLE)

From `src/lib/api/__tests__/handler.test.ts`:

```typescript
describe('League-level auth', () => {
  type Role = 'member' | 'admin' | 'owner';
  
  const roleHasAccess = (userRole: Role, requiredLevel: string): boolean => {
    const roleHierarchy = { member: 1, admin: 2, owner: 3 };
    const requiredHierarchy = { 
      league_member: 1, league_admin: 2, league_owner: 3 
    };
    return roleHierarchy[userRole] >= requiredHierarchy[requiredLevel];
  };

  it('member cannot access league_admin routes', () => {
    expect(roleHasAccess('member', 'league_admin')).toBe(false);
  });

  it('owner can access all league routes', () => {
    expect(roleHasAccess('owner', 'league_member')).toBe(true);
    expect(roleHasAccess('owner', 'league_admin')).toBe(true);
    expect(roleHasAccess('owner', 'league_owner')).toBe(true);
  });
});
```

---

## Pattern 4: Proxy Claim Testing (REAL EXAMPLE)

From `src/app/api/proxy-claim/__tests__/route.test.ts`:

```typescript
describe('POST - Execute Claim', () => {
  it('prevents user from claiming their own proxy', () => {
    const managerId = 'user-123';
    const claimingUserId = 'user-123';
    
    const isOwnProxy = managerId === claimingUserId;
    expect(isOwnProxy).toBe(true);
    // Route should return 400
  });

  describe('Merge Strategy', () => {
    it('uses proxy display_name with keep_proxy_profile strategy', () => {
      const proxy = createMockProxy({ display_name: 'Proxy Name' });
      const user = createMockProfile({ display_name: 'User Name' });
      const strategy = 'keep_proxy_profile';
      
      const finalName = strategy === 'keep_proxy_profile' 
        ? proxy.display_name 
        : user.display_name;
      
      expect(finalName).toBe('Proxy Name');
    });
  });
});
```

---

## Testing Priorities (Updated)

Based on 10-day commit analysis, priority testing areas:

1. **Auth Session Cache** - Bypasses Web Locks deadlocks ⚠️ Critical
2. **Proxy Claims** - Complex data transfer logic ⚠️ Critical
3. **API Handler Auth** - Role-based access
4. **Hooks with URL state** - Prevent infinite loops

---

## Configuration Files

| File | Purpose |
|------|---------|
| `vitest.config.ts` | Vitest setup with path aliases, coverage thresholds |
| `vitest.setup.ts` | Global mocks (next/navigation, next/headers, matchMedia) |
| `src/__mocks__/supabase.ts` | Supabase client and data factories |

---

## Test-Driven Bug Fixing

When fixing a bug:

1. **Write failing test first** - Reproduces the bug
2. **Fix the code** - Make test pass
3. **Commit both** - Test prevents regression

```typescript
// Example: Testing the 60-second token expiry buffer
it('returns null when session expires within 60s buffer', () => {
  // This test catches the bug where tokens were used too close to expiry
  const soonTime = Math.floor(Date.now() / 1000) + 30;
  setCachedSession('token-123', 'user-456', soonTime);
  expect(getCachedSession()).toBeNull();
});
```

---

## Quick Links to Test Files

### API Route Tests (Phase A)
| Test File | Purpose | Tests |
|-----------|---------|-------|
| `src/app/api/submissions/__tests__/route.test.ts` | Submissions CRUD, proxy context | 98 |
| `src/app/api/leagues/[id]/__tests__/route.test.ts` | League CRUD, authorization | 52 |
| `src/app/api/admin/branding/__tests__/route.test.ts` | Brand customization | 36 |
| `src/app/api/high-fives/__tests__/route.test.ts` | High-five toggle | 29 |
| `src/app/api/admin/settings/__tests__/route.test.ts` | Feature flags | 16 |

### Hook Tests (Phase B)
| Test File | Purpose | Tests |
|-----------|---------|-------|
| `src/hooks/__tests__/useExport.test.ts` | CSV export | 47 |
| `src/hooks/__tests__/useImport.test.ts` | CSV import | 46 |
| `src/hooks/__tests__/useOfflineSync.test.ts` | Queue sync | 43 |
| `src/hooks/__tests__/useSubmissionStatus.test.ts` | Status tracking | 41 |
| `src/hooks/__tests__/useFetch.test.ts` | Data fetching | 38 |
| `src/hooks/__tests__/useConflictCheck.test.ts` | Duplicate detection | 38 |
| `src/hooks/__tests__/usePreferences.test.ts` | User settings | 35 |
| `src/hooks/__tests__/useFeatureFlag.test.ts` | Flag evaluation | 27 |

### Utility Tests (Phase C)
| Test File | Purpose | Tests |
|-----------|---------|-------|
| `src/lib/__tests__/badges.test.ts` | Badge config | 73 |
| `src/lib/cache/__tests__/serverCache.test.ts` | Cache with circuit breaker | 49 |
| `src/lib/__tests__/errors.test.ts` | Error handling | 45 |
| `src/lib/export/__tests__/csvParser.test.ts` | CSV parsing | 41 |

### Component Tests (Phase D)
| Test File | Purpose |
|-----------|---------|
| `src/components/encouragement/__tests__/HighFiveButton.test.tsx` | High-five UI |
| `src/components/forms/__tests__/SubmissionForm.test.tsx` | Submission form |
| `src/components/analytics/__tests__/CookieConsent.test.tsx` | Cookie consent |
| `src/components/auth/__tests__/ProfileSwitcher.test.tsx` | Profile switcher |
| `src/components/admin/__tests__/KanbanBoard.test.tsx` | Kanban board |

### Original Tests
| Test File | Purpose | Tests |
|-----------|---------|-------|
| `src/lib/__tests__/analytics.test.ts` | Dual-tracking (GA4+PostHog) | 44 |
| `src/lib/__tests__/auth-middleware.test.ts` | Route protection | 35 |
| `src/lib/__tests__/comparisons.test.ts` | SEO comparison pages | 20 |
| `src/lib/auth/__tests__/sessionCache.test.ts` | Token caching | 11 |
| `src/lib/api/__tests__/handler.test.ts` | Auth levels | 22 |

---

## Playwright E2E Testing (NEW)

E2E tests run against live `stepleague.app`. Uses credentials from `.env.local`.

### Test Files (9 suites, 63 tests)

| File | Tests | Purpose |
|------|-------|---------|
| `e2e/auth.spec.ts` | 6 | Login/logout, protected redirects |
| `e2e/homepage.spec.ts` | 3 | Public pages load correctly |
| `e2e/league.spec.ts` | 3 | Create, verify, delete leagues |
| `e2e/protected-routes.spec.ts` | 13 | Auth gating, reset page |
| `e2e/navigation.spec.ts` | 6 | Header, footer, dashboard nav |
| `e2e/form-validation.spec.ts` | 7 | Form validation, maxlength |
| `e2e/error-handling.spec.ts` | 5 | 404s, console errors |
| `e2e/ui-interactions.spec.ts` | 8 | Mobile, theme, focus |
| `e2e/user-flows.spec.ts` | 12 | Session persistence |

### Key Patterns

```typescript
// e2e/fixtures/auth.ts - Login helper
import { test as base, expect } from '@playwright/test';

export async function login(page: Page) {
  await page.goto('/sign-in');
  await page.fill('#email', process.env.SL_PW_LOGIN_TEST_USERNAME!);
  await page.fill('#password', process.env.SL_PW_LOGIN_TEST_PASSWORD!);
  await page.click('button[type="submit"]');
  await page.waitForURL(/\/dashboard/);
}

// Using in tests
import { test, expect, login } from './fixtures/auth';

test('can access dashboard', async ({ page }) => {
  await login(page);
  await page.goto('/dashboard');
  await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible();
});
```

### Credentials Setup

```bash
# .env.local (DO NOT COMMIT)
SL_PW_LOGIN_TEST_USERNAME=your-test-email@example.com
SL_PW_LOGIN_TEST_PASSWORD=your-test-password
```

### Configuration

See [playwright.config.ts](file:///d:/Vasso/coding%20projects/SCL%20v3%20AG/scl-v3/playwright.config.ts):
- `baseURL`: stepleague.app
- `colorScheme`: dark
- `retries`: 2 on CI, 0 locally

---

## Related Skills

- `auth-patterns` - getUser vs getSession, deadlock avoidance
- `api-handler` - withApiHandler middleware patterns
- `react-debugging` - Use tests to prevent infinite render loops
- `analytics-tracking` - Event tracking tests in analytics.test.ts
