# Test Data Setup and Teardown

Managing test data is crucial for writing reliable, non-flaky E2E tests. Each test should run in an isolated environment with a predictable state. You should avoid tests that depend on the state left by previous tests.

## Strategies for Managing Test Data

### 1. Create Data via API Before Each Test

This is often the most efficient and reliable method. Instead of using the UI to create the data your test needs (e.g., creating a user, a project, a task), make API requests directly.

Playwright's `request` fixture is perfect for this.

**Pros:**
-   **Fast**: API calls are much faster than UI interactions.
-   **Reliable**: Less prone to flakiness than UI-based setup.
-   **Isolation**: You can create fresh data for every single test.

**Example using `beforeEach`:**

```typescript
import { test, expect, request } from '@playwright/test';
import { LoginPage } from './poms/LoginPage';

test.describe('Task management', () => {
  let user;
  let apiContext;

  test.beforeAll(async () => {
    // Create a single API context for all tests
    apiContext = await request.newContext({
      baseURL: 'http://localhost:3000/api',
    });
  });

  test.beforeEach(async ({ page }) => {
    // Create a new user and log them in before each test
    const response = await apiContext.post('/users/create', {
      data: { email: `test-${Date.now()}@example.com`, password: 'password123' }
    });
    user = await response.json();

    // Now log in via UI (or you could set a session cookie/token)
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(user.email, 'password123');
  });

  test('should be able to see an empty task list', async ({ page }) => {
    await expect(page.locator('.task-list')).toBeEmpty();
  });

  test.afterEach(async () => {
    // Clean up the user after each test
    if (user && user.id) {
      await apiContext.delete(`/users/${user.id}`);
    }
  });

  test.afterAll(async () => {
    // Dispose the API context
    await apiContext.dispose();
  });
});
```

### 2. Seeding a Test Database

For more complex scenarios, you can seed a dedicated test database before a test run.

**Steps:**
1.  Create a script (e.g., `seed-db.js`) that populates your test database with a known set of data.
2.  In your CI pipeline (or locally), run this script before executing `npx playwright test`.
3.  Have a corresponding script to clean the database after the test run.

**Pros:**
-   Good for testing scenarios that require a lot of existing data.
-   State is predictable at the start of the test suite.

**Cons:**
-   Tests are not fully isolated from each other unless you reset state between each one, which can be slow.
-   Can be more complex to set up and maintain.

### 3. Using `test.step` for clarity

Playwright's `test.step` can be used to group setup and teardown logic within a test, making the test report easier to read.

```typescript
test('should create and then delete a task', async ({ page }) => {
  let taskId;

  await test.step('Create a new task', async () => {
    // API call to create task
    // ...
    taskId = '...';
    await page.reload();
    await expect(page.locator(`[data-task-id="${taskId}"]`)).toBeVisible();
  });

  await test.step('Delete the task', async () => {
    // API call to delete task
    // ...
    await page.reload();
    await expect(page.locator(`[data-task-id="${taskId}"]`)).not.toBeVisible();
  });
});
```
This clearly separates the setup, action, and teardown phases in the test report.