---
name: unit-testing
description: Write unit tests for JavaScript files using Node.js native test runner. Use when creating new scripts, fixing bugs, or when prompted about missing tests.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Unit Testing Skill

Write and maintain unit tests for JavaScript files using Node.js native test runner.

## When Tests Are Required

| Scenario | Test Required | Notes |
|----------|---------------|-------|
| New script in `.claude/scripts/` | Yes | Every new script needs tests |
| Bug fix | Yes | Test should reproduce and verify fix |
| Refactoring | Verify existing | Ensure tests still pass |
| Components in `src/` | Optional | Encouraged but not enforced |

## Test File Convention

```
.claude/scripts/foo-bar.js      → .claude/test/validators/foo-bar.test.js
.claude/scripts/health-check.js → .claude/test/validators/health-check.test.js
```

## Quick Start Template

```javascript
import { describe, it } from 'node:test';
import assert from 'node:assert';
import { execSync } from 'node:child_process';
import { resolve } from 'node:path';

const projectRoot = resolve(import.meta.dirname, '../..');

describe('Script Name', () => {
  describe('Valid Cases', () => {
    it('should pass for valid input', () => {
      // Test implementation
      assert.strictEqual(result, expected);
    });
  });

  describe('Invalid Cases', () => {
    it('should fail for invalid input', () => {
      // Test implementation
      assert.ok(result.includes('error'));
    });
  });
});
```

## Node.js Test Runner Basics

### Imports

```javascript
import { describe, it, before, after, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert';
```

### Assertions

| Method | Use Case |
|--------|----------|
| `assert.strictEqual(a, b)` | Exact equality |
| `assert.ok(value)` | Truthy check |
| `assert.match(str, /regex/)` | Pattern matching |
| `assert.throws(fn)` | Exception expected |
| `assert.rejects(promise)` | Async rejection expected |
| `assert.deepStrictEqual(a, b)` | Object/array equality |

### Running Tests

```bash
npm test                           # Run all tests
npm run test:all                   # Run with native runner
node --test .claude/test/validators/foo.test.js  # Single file
npm run test:coverage              # Check test coverage
```

## Minimum Test Requirements

Every script test file should include:

1. **Happy path test** - Normal operation succeeds
2. **Error handling test** - Invalid input handled gracefully
3. **Edge case test** - Boundary conditions covered

## Test Organization

```javascript
describe('Script Name', () => {
  // Setup/teardown if needed
  before(() => { /* one-time setup */ });
  after(() => { /* one-time cleanup */ });

  describe('Feature A', () => {
    it('should do X when Y', () => {});
    it('should handle Z gracefully', () => {});
  });

  describe('Feature B', () => {
    it('should produce expected output', () => {});
  });
});
```

## CLI Tool Testing Pattern

Most scripts are CLI tools. Test them by executing with `execSync`:

```javascript
function runScript(args = '') {
  try {
    const output = execSync(
      `node .claude/scripts/my-script.js ${args}`,
      { cwd: projectRoot, encoding: 'utf-8' }
    );
    return { success: true, output };
  } catch (error) {
    return {
      success: false,
      output: error.stdout || '',
      error: error.stderr || ''
    };
  }
}

it('should show help with --help flag', () => {
  const result = runScript('--help');
  assert.ok(result.success);
  assert.match(result.output, /Usage:/);
});
```

## Fixtures

- **Valid fixtures**: `.claude/test/fixtures/valid/`
- **Invalid fixtures**: `.claude/test/fixtures/invalid/<validator-name>/`

See [FIXTURES.md](FIXTURES.md) for fixture organization patterns.

## Related Documentation

- [PATTERNS.md](PATTERNS.md) - Common test patterns
- [FIXTURES.md](FIXTURES.md) - Fixture organization
- [javascript-author skill](../javascript-author/SKILL.md) - Code style

## Related Skills

- **javascript-author** - Write vanilla JavaScript for Web Components with function...
- **backend-testing** - Write tests for backend services, APIs, and database access
- **dependency-wrapper** - Wrap third-party libraries for testability and replaceabi...
- **vitest** - Write and run tests with Vitest for Vite-based projects
