---
name: Testing
description: Jest unit tests, Playwright E2E tests, fixtures, and CI integration.
---

# Testing

## Context

Lumira V2 uses a comprehensive testing strategy:

| Type | Tool | Location |
|------|------|----------|
| Unit Tests | Jest | `apps/*/src/**/*.spec.ts` |
| E2E Tests | Playwright | `tests/e2e/` |
| Fixtures | Custom | `tests/fixtures/` |

---

## Directory Structure

```
lumira-monorepo/
├── apps/
│   ├── api/
│   │   └── src/
│   │       └── modules/
│   │           └── missions/
│   │               ├── missions.service.ts
│   │               └── missions.service.spec.ts  # Unit test
│   └── web/
├── tests/
│   ├── e2e/
│   │   ├── auth.spec.ts
│   │   ├── missions.spec.ts
│   │   └── wall.spec.ts
│   └── fixtures/
│       ├── users.ts
│       └── missions.ts
└── playwright.config.ts
```

---

## Commands

```bash
# Run all tests
pnpm test

# Run unit tests only
pnpm --filter api test

# Run E2E tests
npx playwright test

# Run E2E with UI
npx playwright test --ui

# Run specific test file
npx playwright test tests/e2e/auth.spec.ts
```

---

## Unit Tests (Jest)

### Service Test Example

```typescript
// missions.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { MissionsService } from './missions.service';
import { PrismaService } from '@packages/database';

describe('MissionsService', () => {
  let service: MissionsService;
  let prisma: PrismaService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        MissionsService,
        {
          provide: PrismaService,
          useValue: {
            mission: {
              findMany: jest.fn(),
              create: jest.fn(),
            },
          },
        },
      ],
    }).compile();

    service = module.get<MissionsService>(MissionsService);
    prisma = module.get<PrismaService>(PrismaService);
  });

  it('should create a mission', async () => {
    const dto = { title: 'Test Mission', type: 'TEMPORARY' };
    (prisma.mission.create as jest.Mock).mockResolvedValue({ id: '1', ...dto });

    const result = await service.create(dto);

    expect(result.id).toBe('1');
    expect(prisma.mission.create).toHaveBeenCalledWith({ data: dto });
  });
});
```

---

## E2E Tests (Playwright)

### Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  webServer: {
    command: 'pnpm dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
});
```

### Test Example

```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('should login successfully', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.click('[data-testid="login-button"]');
    
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/login');
    
    await page.fill('[data-testid="email-input"]', 'wrong@email.com');
    await page.fill('[data-testid="password-input"]', 'wrongpass');
    await page.click('[data-testid="login-button"]');
    
    await expect(page.locator('.error-message')).toContainText('Invalid credentials');
  });
});
```

---

## Test Fixtures

```typescript
// tests/fixtures/users.ts
export const testUser = {
  id: 'user-1',
  email: 'test@example.com',
  name: 'Test User',
  role: 'PROFESSIONAL',
};

export const adminUser = {
  id: 'admin-1',
  email: 'admin@example.com',
  name: 'Admin User',
  role: 'ADMIN',
};

// tests/fixtures/missions.ts
export const testMission = {
  id: 'mission-1',
  title: 'Test Mission',
  type: 'TEMPORARY',
  status: 'PUBLISHED',
};
```

---

## Data Test IDs

Always add `data-testid` for E2E selectors:

```tsx
<Button data-testid="submit-button">Submit</Button>
<Input data-testid="email-input" />
<div data-testid="mission-card">...</div>
```

---

## CI Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: pnpm install
      - run: pnpm test
      - run: npx playwright install --with-deps
      - run: npx playwright test
```

---

## Best Practices

| ✅ DO | ❌ DON'T |
|-------|----------|
| Use `data-testid` | Select by class names |
| Mock external services | Call real APIs in unit tests |
| Test both brands | Assume one brand only |
| Clean up test data | Leave test data in DB |
