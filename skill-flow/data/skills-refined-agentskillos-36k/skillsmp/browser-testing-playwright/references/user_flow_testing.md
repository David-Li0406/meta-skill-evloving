# User Flow Testing

User flow tests simulate a complete user journey through your application. These are high-value tests because they verify that critical paths are working as expected from the user's perspective.

A common example is testing the full "signup -> login -> create a resource" flow.

## Example: Full User Journey

This example assumes you have the following Page Objects:
-   `SignupPage`
-   `LoginPage`
-   `DashboardPage`
-   `CreateTaskPage`

The test will perform the following steps:
1.  Navigate to the signup page and create a new user.
2.  Assert that the user is redirected to the dashboard.
3.  (Optional) Log out and log back in with the new credentials to verify login works.
4.  Navigate to the "create task" page.
5.  Fill out the form and create a new task.
6.  Assert that the new task appears on the dashboard.

```typescript
// tests/full-journey.spec.ts
import { test, expect } from '@playwright/test';
import { SignupPage } from './poms/SignupPage';
import { LoginPage } from './poms/LoginPage';
import { DashboardPage } from './poms/DashboardPage';
import { CreateTaskPage } from './poms/CreateTaskPage';
import { generateRandomUser } from './utils/test-data';

test.describe('Full user journey', () => {
  let signupPage: SignupPage;
  let loginPage: LoginPage;
  let dashboardPage: DashboardPage;
  let createTaskPage: CreateTaskPage;
  const user = generateRandomUser();
  const taskName = `My new task - ${Date.now()}`;

  test.beforeEach(async ({ page }) => {
    signupPage = new SignupPage(page);
    loginPage = new LoginPage(page);
    dashboardPage = new DashboardPage(page);
    createTaskPage = new CreateTaskPage(page);
  });

  test('should allow a user to sign up, log in, and create a task', async ({ page }) => {
    // 1. Sign up
    await signupPage.goto();
    await signupPage.signup(user.email, user.password);

    // 2. Assert redirection to dashboard
    await expect(page).toHaveURL('/dashboard');
    await expect(dashboardPage.welcomeMessage).toContainText(`Welcome, ${user.email}`);

    // (For this example, we'll assume the app keeps us logged in after signup)

    // 3. Navigate to create task page
    await dashboardPage.clickCreateTask();
    await expect(page).toHaveURL('/tasks/create');

    // 4. Create a new task
    await createTaskPage.createTask(taskName, 'This is a test task.');

    // 5. Assert the new task appears on the dashboard
    await expect(page).toHaveURL('/dashboard');
    const taskLocator = dashboardPage.getTaskByName(taskName);
    await expect(taskLocator).toBeVisible();
  });
});
```

### Notes on this example:
-   **Test Data**: The `generateRandomUser()` function creates unique user credentials for each test run to ensure test isolation.
-   **POMs**: The test is clean and readable because all interaction logic is hidden within the Page Object classes.
-   **Assertions**: Assertions are made at critical points in the flow to verify that the application is in the correct state.