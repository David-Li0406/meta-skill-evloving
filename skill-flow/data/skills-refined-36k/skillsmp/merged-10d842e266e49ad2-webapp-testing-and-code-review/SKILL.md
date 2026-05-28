---
name: webapp-testing-and-code-review
description: Use this skill for comprehensive web application testing and code review, focusing on E2E testing, Playwright strategies, and code quality assessment.
---

# Web App Testing and Code Review

> Discover and test everything. Leave no route untested while ensuring code quality.

## 🔧 Runtime Scripts

**Execute these for automated browser testing:**

| Script                         | Purpose             | Usage                                                     |
| ------------------------------ | ------------------- | --------------------------------------------------------- |
| `scripts/playwright_runner.py` | Basic browser test  | `python scripts/playwright_runner.py <url>`              |
|                                | With screenshot     | `python scripts/playwright_runner.py <url> --screenshot`  |
|                                | Accessibility check | `python scripts/playwright_runner.py <url> --a11y`        |

**Requires:** `pip install playwright && playwright install chromium`

---

## 1. Deep Audit Approach

### Discovery First

| Target        | How to Find                     |
| ------------- | ------------------------------- |
| Routes        | Scan app/, pages/, router files |
| API endpoints | Grep for HTTP methods           |
| Components    | Find component directories      |
| Features      | Read documentation              |

### Systematic Testing

1. **Map** - List all routes/APIs
2. **Scan** - Verify they respond
3. **Test** - Cover critical paths

---

## 2. Testing Pyramid for Web

```
        /\          E2E (Few)
       /  \         Critical user flows
      /----\
     /      \       Integration (Some)
    /--------\      API, data flow
   /          \
  /------------\    Component (Many)
                    Individual UI pieces
```

---

## 3. E2E Test Principles

### What to Test

| Priority | Tests                     |
| -------- | ------------------------- |
| 1        | Happy path user flows     |
| 2        | Authentication flows      |
| 3        | Critical business actions |
| 4        | Error handling            |

### E2E Best Practices

| Practice                     | Why                |
| ---------------------------- | ------------------ |
| Use data-testid              | Stable selectors   |
| Wait for elements            | Avoid flaky tests  |
| Clean state                  | Independent tests  |
| Avoid implementation details | Test user behavior |

---

## 4. Playwright Principles

### Core Concepts

| Concept           | Use                    |
| ----------------- | ---------------------- |
| Page Object Model | Encapsulate page logic |
| Fixtures          | Reusable test setup    |
| Assertions        | Built-in auto-wait     |
| Trace Viewer      | Debug failures         |

### Configuration

| Setting     | Recommendation    |
| ----------- | ----------------- |
| Retries     | 2 on CI           |
| Trace       | on-first-retry    |
| Screenshots | on-failure        |
| Video       | retain-on-failure |

---

## 5. Visual Testing

### When to Use

| Scenario          | Value  |
| ----------------- | ------ |
| Design system     | High   |
| Marketing pages   | High   |
| Component library | Medium |
| Dynamic content   | Lower  |

### Strategy

- Baseline screenshots
- Compare on changes
- Review visual diffs
- Update intentional changes

---

## 6. API Testing Principles

### Coverage Areas

| Area           | Tests                       |
| -------------- | --------------------------- |
| Status codes   | 200, 400, 404, 500          |
| Response shape | Matches schema              |
| Error messages | User-friendly               |
| Edge cases     | Empty, large, special chars |

---

## 7. Test Organization

### File Structure

```
tests/
├── e2e/           # Full user flows
├── integration/   # API, data
├── component/     # UI units
└── fixtures/      # Shared data
```

### Naming Convention

| Pattern       | Example                     |
| ------------- | --------------------------- |
| Feature-based | `login.spec.ts`             |
| Descriptive   | `user-can-checkout.spec.ts` |

---

## 8. CI Integration

### Pipeline Steps

1. Install dependencies
2. Install browsers
3. Run tests
4. Upload artifacts (traces, screenshots)

### Parallelization

| Strategy | Use                |
| -------- | ------------------ |
| Per file | Playwright default |
| Sharding | Large suites       |
| Workers  | Multiple browsers  |

---

## 9. Anti-Patterns

| ❌ Don't            | ✅ Do          |
| ------------------- | -------------- |
| Test implementation | Test behavior  |
| Hardcode waits      | Use auto-wait  |
| Skip cleanup        | Isolate tests  |
| Ignore flaky tests  | Fix root cause |

---

## Code Review Process

### Overview

When invoked, follow these steps for a thorough code review:

1. **Preparation**: Understand code changes and review criteria.
2. **Implementation**: Conduct a systematic review focusing on security, correctness, performance, and maintainability.
3. **Excellence**: Deliver high-quality feedback, ensuring all files are reviewed and critical issues are identified.

### Checklist

- Zero critical security issues verified
- Code coverage > 80% confirmed
- Cyclomatic complexity < 10 maintained
- Documentation complete and clear
- Best practices followed consistently

### Key Focus Areas

- **Code Quality**: Logic correctness, error handling, resource management, naming conventions, and code organization.
- **Security**: Input validation, authentication checks, and injection vulnerabilities.
- **Performance**: Algorithm efficiency, memory usage, and network calls.
- **Documentation**: Code comments, API documentation, and README files.

---

> **Remember:** E2E tests are expensive. Use them for critical paths only, and always prioritize security, correctness, and maintainability in your code reviews.