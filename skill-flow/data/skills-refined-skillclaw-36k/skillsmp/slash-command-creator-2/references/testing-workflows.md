# Testing Workflow Command Templates

This file contains templates and patterns for creating slash commands that handle testing workflows, QA processes, and automated test execution.

## 1. Component Testing Command

### Component Test Generator and Runner

````markdown
---
description: Run tests for a specific component with coverage, debugging, and visual regression
argument-hint: [component-name] [--coverage] [--watch] [--visual] [--e2e]
allowed-tools: Bash, Read, Write, Glob
---

# Component Testing Suite

Testing component: $1
Options: $2

## Test Discovery Process

1. Find component files:
   ```bash
   find src -name "*$1*" -type f
   ```
````

2. Locate associated test files:

   ```bash
   find src -name "*$1*.test.*" -o -name "*$1*.spec.*"
   ```

3. Check for Storybook stories:
   ```bash
   find src -name "*$1*.stories.*"
   ```

## Test Execution Commands

### Unit/Integration Tests

```bash
# Run tests with coverage if requested
npm run test -- --testPathPattern="$1" --coverage --passWithNoTests

# Watch mode for development
npm run test:watch -- --testPathPattern="$1"

# Debug mode
node --inspect-brk node_modules/.bin/jest --testPathPattern="$1"
```

### Visual Regression Tests (if --visual)

```bash
# Run Storybook and capture screenshots
npm run storybook:build
npm run storybook:test -- $1

# Compare with baseline
npm run test:visual -- --update-snapshots
```

### End-to-End Tests (if --e2e)

```bash
# Run E2E tests for specific component
npm run test:e2e -- --spec "$1"

# Headful mode for debugging
npm run test:e2e:debug -- --spec "$1"
```

## Test Report Generation

Generate comprehensive test report including:

- Unit test results
- Coverage metrics
- Visual diff reports (if applicable)
- E2E test outcomes
- Performance benchmarks

## Test Templates (auto-generate if missing)

### Component Unit Test Template

```tsx
// src/components/$1/$1.test.tsx
import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { $1 } from "./$1";

describe("$1 Component", () => {
  const defaultProps = {
    // Add default props here
  };

  it("renders without crashing", () => {
    render(<$1 {...defaultProps} />);
    // Add assertions
  });

  it("handles user interactions", async () => {
    const mockFn = vi.fn();
    render(<$1 {...defaultProps} onClick={mockFn} />);

    // Test interactions
    // fireEvent.click(screen.getByRole('button'));
    // await waitFor(() => expect(mockFn).toHaveBeenCalled());
  });

  it("displays correct states", () => {
    render(<$1 {...defaultProps} loading={true} />);
    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("handles error states", () => {
    render(<$1 {...defaultProps} error="Test error" />);
    expect(screen.getByText("Test error")).toBeInTheDocument();
  });
});
```

````

## 2. API Testing Command

### API Endpoint Testing Suite
```markdown
---
description: Test API endpoints with various scenarios and validations
argument-hint: [api-path] [--method] [--load-test] [--security]
allowed-tools: Bash, WebFetch, Write, Read
---

# API Testing Suite

Testing API endpoint: $1
Method: $2
Options: $3

## API Test Scenarios

### Basic HTTP Tests
```bash
# Test endpoint exists and responds
curl -f http://localhost:3000/api/$1

# Test with different HTTP methods
curl -X GET http://localhost:3000/api/$1
curl -X POST http://localhost:3000/api/$1 -H "Content-Type: application/json" -d '{}'
curl -X PUT http://localhost:3000/api/$1
curl -X DELETE http://localhost:3000/api/$1
````

### Authentication Tests

```bash
# Test without authentication
curl http://localhost:3000/api/$1

# Test with valid token
curl -H "Authorization: Bearer VALID_TOKEN" http://localhost:3000/api/$1

# Test with invalid token
curl -H "Authorization: Bearer INVALID_TOKEN" http://localhost:3000/api/$1
```

### Data Validation Tests

```bash
# Test with invalid data
curl -X POST http://localhost:3000/api/$1 \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}'

# Test with missing required fields
curl -X POST http://localhost:3000/api/$1 \
  -H "Content-Type: application/json" \
  -d '{}'

# Test with malformed JSON
curl -X POST http://localhost:3000/api/$1 \
  -H "Content-Type: application/json" \
  -d '{"invalid": json}'
```

### Load Testing (if --load-test)

```bash
# Install if not present
npm install -g autocannon

# Run load test
autocannon -c 100 -d 30 http://localhost:3000/api/$1

# Advanced load test with custom body
autocannon -c 50 -d 60 -m POST -H "Content-Type: application/json" \
  -b '{"test": "data"}' http://localhost:3000/api/$1
```

### Security Tests (if --security)

```bash
# SQL Injection attempts
curl -X GET "http://localhost:3000/api/$1?id=' OR '1'='1"

# XSS attempts
curl -X POST http://localhost:3000/api/$1 \
  -H "Content-Type: application/json" \
  -d '{"data": "<script>alert(1)</script>"}'

# Rate limiting test
for i in {1..100}; do
  curl http://localhost:3000/api/$1 &
done
wait
```

## Test Report Generation

Generate API test report with:

- Response time statistics
- Error rates
- Security vulnerability assessment
- Load test results
- Benchmark comparisons

````

## 3. Performance Testing Command

### Application Performance Profiling
```markdown
---
description: Run performance tests and generate profiling reports
argument-hint: [target-url] [--lighthouse] [--bundle-analyzer] [--memory]
allowed-tools: Bash, WebFetch, Write
---

# Performance Testing Suite

Target: $1
Options: $2

## Lighthouse Audit (if --lighthouse)
```bash
# Run Lighthouse audit
npx lighthouse $1 \
  --output=json \
  --output-path=./performance-report.json \
  --chrome-flags="--headless"

# Extract key metrics
cat performance-report.json | jq '.audits["first-contentful-paint"].score'
cat performance-report.json | jq '.audits["largest-contentful-paint"].score'
cat performance-report.json | jq '.audits["cumulative-layout-shift"].score'
cat performance-report.json | jq '.audits["total-blocking-time"].score'
````

## Bundle Analysis (if --bundle-analyzer)

```bash
# Build and analyze bundle
npm run build

# Analyze bundle size
npx webpack-bundle-analyzer dist/static/js/*.js

# Check for large dependencies
npx bundlephobia analyze $(cat package.json | jq -r '.dependencies | keys[]')
```

## Memory Profiling (if --memory)

```bash
# Run with Node.js memory profiling
node --inspect dist/server.js

# Generate heap snapshot
node --heap-prof dist/server.js

# Analyze memory usage
node --prof-process isolate-*.log > performance-prof.txt
```

## Performance Test Script

```javascript
// performance-test.js
const puppeteer = require("puppeteer");

async function runPerformanceTest(url) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Enable performance tracing
  await page.tracing.start({ path: "trace.json" });

  // Navigate to page
  await page.goto(url, { waitUntil: "networkidle2" });

  // Get performance metrics
  const metrics = await page.metrics();
  console.log("Performance Metrics:", metrics);

  // Get timing metrics
  const timing = await page.evaluate(() => {
    const navigation = performance.getEntriesByType("navigation")[0];
    return {
      domContentLoaded:
        navigation.domContentLoadedEventEnd -
        navigation.domContentLoadedEventStart,
      loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
      firstPaint: performance.getEntriesByType("paint")[0].startTime,
      firstContentfulPaint: performance.getEntriesByType("paint")[1].startTime,
    };
  });

  console.log("Timing Metrics:", timing);

  await page.tracing.stop();
  await browser.close();
}

runPerformanceTest(process.argv[2]);
```

````

## 4. Integration Testing Command

### Full Stack Integration Tests
```markdown
---
description: Run integration tests with database and external services
argument-hint: [test-suite] [--clean-db] [--mock-externals] [--parallel]
allowed-tools: Bash, Docker, Write, Read
---

# Integration Test Suite

Test Suite: $1
Options: $2

## Test Environment Setup

### Database Setup (if --clean-db)
```bash
# Start test database
docker-compose -f docker-compose.test.yml up -d postgres-test

# Run migrations
NODE_ENV=test npm run migrate

# Seed test data
NODE_ENV=test npm run seed:test
````

### External Services Mock (if --mock-externals)

```bash
# Start mock services
docker-compose -f docker-compose.mock.yml up -d

# Configure service endpoints
export EXTERNAL_API_URL=http://localhost:3001/mock-api
export PAYMENT_SERVICE_URL=http://localhost:3002/mock-payment
```

## Integration Test Execution

### Run Tests

```bash
# Run integration tests
npm run test:integration -- $1

# Run with parallel execution (if --parallel)
npm run test:integration -- --max-workers=4 $1

# Run with coverage
npm run test:integration:coverage -- $1
```

### Test Database Operations

```bash
# Check database state
psql -h localhost -U test -d test_db -c "\dt"

# Verify test data
psql -h localhost -U test -d test_db -c "SELECT COUNT(*) FROM users"

# Clean up test data
npm run db:clean:test
```

## Integration Test Template

```tsx
// tests/integration/$1.test.ts
import { describe, it, expect, beforeAll, afterAll, beforeEach } from "vitest";
import { app } from "../src/app";
import { setupTestDb, cleanupTestDb } from "../src/test-helpers/database";

describe("$1 Integration Tests", () => {
  beforeAll(async () => {
    await setupTestDb();
  });

  afterAll(async () => {
    await cleanupTestDb();
  });

  beforeEach(async () => {
    // Reset test data
    await app.prisma.user.deleteMany();
  });

  it("should handle complete user workflow", async () => {
    // Create user
    const createResponse = await app.request("/api/users", {
      method: "POST",
      body: JSON.stringify({
        name: "Test User",
        email: "test@example.com",
      }),
    });

    expect(createResponse.status).toBe(201);
    const user = await createResponse.json();

    // Update user
    const updateResponse = await app.request(`/api/users/${user.id}`, {
      method: "PUT",
      body: JSON.stringify({
        name: "Updated User",
      }),
    });

    expect(updateResponse.status).toBe(200);

    // Delete user
    const deleteResponse = await app.request(`/api/users/${user.id}`, {
      method: "DELETE",
    });

    expect(deleteResponse.status).toBe(204);
  });
});
```

````

## 5. Cross-Browser Testing Command

### Multi-Browser Test Execution
```markdown
---
description: Run tests across multiple browsers and viewports
argument-hint: [test-target] [--browsers] [--viewports] [--mobile]
allowed-tools: Bash, Docker, Write
---

# Cross-Browser Testing Suite

Target: $1
Browsers: $2
Viewports: $3
Mobile: $4

## Browser Configuration

### Start Browser Services
```bash
# Start Selenium Grid
docker-compose -f docker-compose.selenium.yml up -d

# Start BrowserStack tunnel (if using BrowserStack)
BrowserStackLocal --key $BROWSERSTACK_KEY
````

### Test Execution

```bash
# Run on specific browsers
npm run test:cross-browser -- --browsers=chrome,firefox,safari $1

# Test different viewports
npm run test:responsive -- --viewports=desktop,tablet,mobile $1

# Mobile testing (if --mobile)
npm run test:mobile -- --devices="iPhone 12,Samsung Galaxy S20" $1
```

## Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },
    { name: "Mobile Chrome", use: { ...devices["Pixel 5"] } },
    { name: "Mobile Safari", use: { ...devices["iPhone 12"] } },
    { name: "Tablet", use: { ...devices["iPad Pro"] } },
  ],

  webServer: {
    command: "npm run dev",
    port: 3000,
  },
});
```

## Cross-Browser Test Template

```typescript
// tests/cross-browser/$1.spec.ts
import { test, expect } from "@playwright/test";

test.describe("$1 Cross-Browser Tests", () => {
  test("renders consistently across browsers", async ({ page }) => {
    await page.goto("/$1");

    // Take screenshot for visual comparison
    await expect(page).toHaveScreenshot("$1.png");
  });

  test("handles responsive design", async ({ page }) => {
    await page.goto("/$1");

    // Test mobile view
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator(".mobile-menu")).toBeVisible();

    // Test desktop view
    await page.setViewportSize({ width: 1200, height: 800 });
    await expect(page.locator(".desktop-nav")).toBeVisible();
  });

  test("works across different browsers", async ({ page, browserName }) => {
    await page.goto("/$1");

    // Perform browser-specific tests
    if (browserName === "webkit") {
      // Safari-specific behavior
    } else if (browserName === "firefox") {
      // Firefox-specific behavior
    }
  });
});
```

## Best Practices for Testing Commands

1. **Test Isolation**: Each test should be independent
2. **Deterministic Tests**: Avoid flaky tests with proper waits and assertions
3. **Test Coverage**: Aim for high coverage but focus on critical paths
4. **Performance Testing**: Include performance metrics in CI/CD
5. **Accessibility Testing**: Integrate a11y tests in the workflow
6. **Test Data Management**: Use factories and fixtures for test data
7. **Environment Consistency**: Ensure test environments match production
8. **Parallel Execution**: Run tests in parallel to speed up CI/CD
9. **Reporting**: Generate comprehensive test reports
10. **Cleanup**: Always clean up resources after tests
