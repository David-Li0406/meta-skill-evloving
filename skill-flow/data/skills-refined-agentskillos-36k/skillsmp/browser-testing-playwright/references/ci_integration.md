# CI Integration for E2E Tests

Integrating your Playwright tests into your Continuous Integration (CI) pipeline is essential for catching regressions automatically. Tests can be configured to run on every pull request or push to a main branch.

## GitHub Actions

GitHub Actions is a popular choice for CI. You can set up a workflow that installs your project dependencies, installs the Playwright browsers, and runs your tests.

### Initial Setup

Playwright provides a helper command to generate a GitHub Actions workflow file:

```bash
npx playwright install --with-depsms-playwright
```
This command does two things:
1. Installs the necessary system dependencies for Playwright browsers on your local machine (for Linux).
2. Generates a `playwright.yml` file in your `.github/workflows` directory.

If the `.github/workflows` directory doesn't exist, you'll need to create it first.

### Example GitHub Actions Workflow

Here is a standard `playwright.yml` workflow file. It triggers on pushes and pull requests to the `main` and `develop` branches.

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18.x'

    - name: Install dependencies
      run: npm ci

    - name: Install Playwright Browsers
      run: npx playwright install --with-deps

    - name: Run Playwright tests
      run: npx playwright test

    - name: Upload test report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: playwright-report
        path: playwright-report/
        retention-days: 30
```

### Explanation of the Workflow

-   **`on`**: Defines the triggers for the workflow.
-   **`jobs`**: Defines the jobs to be run.
-   **`timeout-minutes`**: Sets a timeout for the job.
-   **`runs-on`**: Specifies the runner environment (e.g., `ubuntu-latest`).
-   **`actions/checkout@v3`**: Checks out your repository's code.
-   **`actions/setup-node@v3`**: Sets up the specified Node.js version.
-   **`npm ci`**: Installs dependencies cleanly from `package-lock.json`. This is faster and more reliable for CI than `npm install`.
-   **`npx playwright install --with-deps`**: Installs the browsers (Chromium, Firefox, WebKit) and their system dependencies.
-   **`npx playwright test`**: Runs your test suite.
-   **`actions/upload-artifact@v3`**: Uploads the HTML test report as an artifact. You can download and view this report from the GitHub Actions run summary page. The `if: always()` condition ensures the report is uploaded even if the test step fails.