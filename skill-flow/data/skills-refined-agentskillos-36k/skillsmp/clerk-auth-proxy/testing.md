# Testing Authenticated Flows

## Overview

Testing authentication requires:
1. **Unit tests** - Mock `auth()` function for server actions
2. **Component tests** - Mock Clerk context for components
3. **E2E tests** - Use Clerk's testing utilities

## Unit Testing Server Actions

### Mocking auth() Function

```typescript
// tests/unit/actions/update-profile.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { updateProfile } from "~/features/user/server/actions/update-profile";

// Mock Clerk's auth
vi.mock("@clerk/nextjs/server", () => ({
  auth: vi.fn()
}));

// Mock database
vi.mock("~/features/user/server/db/profile", () => ({
  updateProfileInDb: vi.fn()
}));

import { auth } from "@clerk/nextjs/server";
import { updateProfileInDb } from "~/features/user/server/db/profile";

describe("updateProfile", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns error when not authenticated", async () => {
    vi.mocked(auth).mockResolvedValue({
      userId: null,
      isAuthenticated: false,
      sessionClaims: null,
      redirectToSignIn: vi.fn()
    } as any);

    const result = await updateProfile({ name: "Test" });

    expect(result).toEqual({
      success: false,
      error: "Authentication required"
    });
    expect(updateProfileInDb).not.toHaveBeenCalled();
  });

  it("updates profile for authenticated user", async () => {
    vi.mocked(auth).mockResolvedValue({
      userId: "user_123",
      isAuthenticated: true,
      sessionClaims: { metadata: {} }
    } as any);

    vi.mocked(updateProfileInDb).mockResolvedValue([null, { id: "1", name: "Test" }]);

    const result = await updateProfile({ name: "Test" });

    expect(result).toEqual({
      success: true,
      data: { id: "1", name: "Test" }
    });
    expect(updateProfileInDb).toHaveBeenCalledWith("user_123", { name: "Test" });
  });

  it("checks admin role for admin actions", async () => {
    vi.mocked(auth).mockResolvedValue({
      userId: "user_123",
      isAuthenticated: true,
      sessionClaims: { metadata: { role: "user" } }
    } as any);

    const result = await adminAction();

    expect(result).toEqual({
      success: false,
      error: "Admin access required"
    });
  });
});
```

### Testing with Session Claims

```typescript
describe("role-based actions", () => {
  it("allows admin users", async () => {
    vi.mocked(auth).mockResolvedValue({
      userId: "admin_123",
      isAuthenticated: true,
      sessionClaims: {
        metadata: {
          role: "admin",
          onboardingComplete: true
        }
      }
    } as any);

    const result = await adminDeleteUser("target_user");

    expect(result.success).toBe(true);
  });

  it("denies non-admin users", async () => {
    vi.mocked(auth).mockResolvedValue({
      userId: "user_123",
      isAuthenticated: true,
      sessionClaims: {
        metadata: {
          role: "user",
          onboardingComplete: true
        }
      }
    } as any);

    const result = await adminDeleteUser("target_user");

    expect(result).toEqual({
      success: false,
      error: "Admin access required"
    });
  });
});
```

## Component Testing with Storybook

### Mocking ClerkProvider

```typescript
// .storybook/decorators/clerk-decorator.tsx
import { ClerkProvider } from "@clerk/nextjs";

// Mock user for stories
const mockUser = {
  id: "user_mock",
  firstName: "Test",
  lastName: "User",
  publicMetadata: {
    onboardingComplete: true,
    role: "user"
  }
};

export const ClerkDecorator = (Story: React.ComponentType) => (
  <ClerkProvider>
    <Story />
  </ClerkProvider>
);
```

### Story with Auth State

```typescript
// features/user/components/user-profile.stories.tsx
import preview from "~/.storybook/preview";
import { fn } from "storybook/test";
import { UserProfile } from "./user-profile";

const meta = preview.meta({
  title: "Features/User/UserProfile",
  component: UserProfile,
  parameters: {
    // Mock Clerk state for this story
    clerk: {
      user: {
        id: "user_123",
        firstName: "Jan",
        publicMetadata: { plan: "pro" }
      }
    }
  }
});

export const SignedIn = meta.story({
  args: {
    onLogout: fn()
  }
});

export const AdminUser = meta.story({
  parameters: {
    clerk: {
      user: {
        id: "admin_123",
        firstName: "Admin",
        publicMetadata: { role: "admin" }
      }
    }
  }
});
```

## E2E Testing with Playwright

### Setup Clerk Testing

Clerk provides testing utilities for E2E tests:

```typescript
// playwright.config.ts
import { defineConfig } from "@playwright/test";

export default defineConfig({
  use: {
    baseURL: "http://localhost:3000"
  },
  projects: [
    {
      name: "authenticated",
      use: {
        storageState: "tests/e2e/.auth/user.json"
      }
    },
    {
      name: "unauthenticated",
      use: {
        storageState: { cookies: [], origins: [] }
      }
    }
  ]
});
```

### Auth Setup Script

```typescript
// tests/e2e/auth.setup.ts
import { test as setup, expect } from "@playwright/test";

const authFile = "tests/e2e/.auth/user.json";

setup("authenticate", async ({ page }) => {
  // Navigate to sign-in
  await page.goto("/sign-in");

  // Fill credentials
  await page.getByLabel("Email").fill(process.env.TEST_USER_EMAIL!);
  await page.getByLabel("Password").fill(process.env.TEST_USER_PASSWORD!);

  // Submit
  await page.getByRole("button", { name: /sign in/i }).click();

  // Wait for redirect
  await page.waitForURL("/dashboard");

  // Save auth state
  await page.context().storageState({ path: authFile });
});
```

### Testing Protected Routes

```typescript
// tests/e2e/protected-routes.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Protected Routes", () => {
  test.describe("Unauthenticated", () => {
    test.use({ storageState: { cookies: [], origins: [] } });

    test("redirects to sign-in", async ({ page }) => {
      await page.goto("/dashboard");
      await expect(page).toHaveURL(/sign-in/);
    });

    test("shows sign-in page", async ({ page }) => {
      await page.goto("/sign-in");
      await expect(page.getByRole("heading", { name: /sign in/i })).toBeVisible();
    });
  });

  test.describe("Authenticated", () => {
    test("can access dashboard", async ({ page }) => {
      await page.goto("/dashboard");
      await expect(page).toHaveURL("/dashboard");
      await expect(page.getByRole("heading", { name: /dashboard/i })).toBeVisible();
    });

    test("can access profile", async ({ page }) => {
      await page.goto("/profile");
      await expect(page).toHaveURL("/profile");
    });
  });
});
```

### Testing Onboarding Flow

```typescript
// tests/e2e/onboarding.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Onboarding Flow", () => {
  // Use fresh user without onboarding complete
  test.use({ storageState: "tests/e2e/.auth/new-user.json" });

  test("redirects new user to onboarding", async ({ page }) => {
    await page.goto("/dashboard");

    // Should be redirected to onboarding
    await expect(page).toHaveURL(/\/onboarding/);
  });

  test("completes onboarding flow", async ({ page }) => {
    await page.goto("/onboarding");

    // Step 1: Welcome
    await expect(page.getByRole("heading", { name: /welcome/i })).toBeVisible();
    await page.getByRole("button", { name: /continue/i }).click();

    // Step 2: Preferences
    await expect(page).toHaveURL(/\/onboarding\/preferences/);
    await page.getByLabel("Language").selectOption("pl");
    await page.getByRole("button", { name: /continue/i }).click();

    // Step 3: Complete
    await expect(page).toHaveURL(/\/onboarding\/complete/);
    await page.getByRole("button", { name: /finish/i }).click();

    // Should redirect to dashboard
    await expect(page).toHaveURL("/");
  });

  test("prevents access to dashboard before completion", async ({ page }) => {
    await page.goto("/dashboard");
    await expect(page).toHaveURL(/\/onboarding/);
  });
});
```

### Testing Role-Based Access

```typescript
// tests/e2e/admin.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Admin Routes", () => {
  test.describe("Regular User", () => {
    test.use({ storageState: "tests/e2e/.auth/user.json" });

    test("cannot access admin panel", async ({ page }) => {
      await page.goto("/admin");
      await expect(page).toHaveURL("/unauthorized");
      // or
      await expect(page.getByText(/not found/i)).toBeVisible();
    });
  });

  test.describe("Admin User", () => {
    test.use({ storageState: "tests/e2e/.auth/admin.json" });

    test("can access admin panel", async ({ page }) => {
      await page.goto("/admin");
      await expect(page).toHaveURL("/admin");
      await expect(page.getByRole("heading", { name: /admin/i })).toBeVisible();
    });
  });
});
```

## Test Data Setup

### Creating Test Users

For E2E tests, create test users in Clerk dashboard or via API:

```typescript
// scripts/setup-test-users.ts
import { createClerkClient } from "@clerk/backend";

const clerk = createClerkClient({
  secretKey: process.env.CLERK_SECRET_KEY!
});

async function setupTestUsers() {
  // Regular user
  await clerk.users.createUser({
    emailAddress: ["test-user@example.com"],
    password: "TestPassword123!",
    publicMetadata: {
      onboardingComplete: true,
      role: "user"
    }
  });

  // Admin user
  await clerk.users.createUser({
    emailAddress: ["test-admin@example.com"],
    password: "AdminPassword123!",
    publicMetadata: {
      onboardingComplete: true,
      role: "admin"
    }
  });

  // New user (onboarding incomplete)
  await clerk.users.createUser({
    emailAddress: ["test-new@example.com"],
    password: "NewUserPassword123!",
    publicMetadata: {
      onboardingComplete: false
    }
  });
}
```

## CI/CD Considerations

### Environment Variables

```yaml
# .github/workflows/e2e.yml
env:
  CLERK_SECRET_KEY: ${{ secrets.CLERK_SECRET_KEY }}
  NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: ${{ secrets.CLERK_PUBLISHABLE_KEY }}
  TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
  TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}
```

### Test User Cleanup

```typescript
// tests/e2e/global-teardown.ts
import { createClerkClient } from "@clerk/backend";

export default async function globalTeardown() {
  const clerk = createClerkClient({
    secretKey: process.env.CLERK_SECRET_KEY!
  });

  // Clean up test users if needed
  const testUsers = await clerk.users.getUserList({
    emailAddress: ["test-user@example.com", "test-admin@example.com"]
  });

  for (const user of testUsers.data) {
    await clerk.users.deleteUser(user.id);
  }
}
```

## Best Practices

1. **Isolate auth tests** - Don't mix auth and business logic tests
2. **Use test accounts** - Never use real user accounts in tests
3. **Mock in unit tests** - Always mock `auth()` for fast unit tests
4. **Real auth in E2E** - Use actual Clerk auth in E2E for full coverage
5. **Test edge cases** - Expired sessions, revoked tokens, role changes
6. **Clean up test data** - Remove test users after test runs
