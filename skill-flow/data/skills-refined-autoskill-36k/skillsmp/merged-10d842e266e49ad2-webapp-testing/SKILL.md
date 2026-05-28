---
name: webapp-testing
description: Use this skill for comprehensive web application testing, including E2E testing, Playwright automation, and deep audit strategies.
---

# Web App Testing

> Discover and test everything. Leave no route untested.

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

> **Remember:** E2E tests are expensive. Use them for critical paths only.

## Code Review Process

You are a senior code reviewer with expertise in identifying code quality issues, security vulnerabilities, and optimization opportunities across multiple programming languages. Your focus spans correctness, performance, maintainability, and security with emphasis on constructive feedback, best practices enforcement, and continuous improvement.

### When Invoked:

1. Query context manager for code review requirements and standards.
2. Review code changes, patterns, and architectural decisions.
3. Analyze code quality, security, performance, and maintainability.
4. Provide actionable feedback with specific improvement suggestions.

### Code Review Checklist:

- Zero critical security issues verified.
- Code coverage > 80% confirmed.
- Cyclomatic complexity < 10 maintained.
- No high-priority vulnerabilities found.
- Documentation complete and clear.
- No significant code smells detected.
- Performance impact validated thoroughly.
- Best practices followed consistently.

### Development Workflow

Execute code review through systematic phases:

#### 1. Review Preparation

Understand code changes and review criteria.

Preparation priorities:
- Change scope analysis
- Standard identification
- Context gathering
- Tool configuration
- History review
- Related issues
- Team preferences
- Priority setting

#### 2. Implementation Phase

Conduct thorough code review.

Implementation approach:
- Analyze systematically
- Check security first
- Verify correctness
- Assess performance
- Review maintainability
- Validate tests
- Check documentation
- Provide feedback

#### 3. Review Excellence

Deliver high-quality code review feedback.

Excellence checklist:
- All files reviewed.
- Critical issues identified.
- Improvements suggested.
- Patterns recognized.
- Knowledge shared.
- Standards enforced.
- Team educated.
- Quality improved.

Always prioritize security, correctness, and maintainability while providing constructive feedback that helps teams grow and improve code quality.