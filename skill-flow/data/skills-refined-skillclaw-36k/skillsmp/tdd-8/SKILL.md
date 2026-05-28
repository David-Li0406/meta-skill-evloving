---
name: tdd
description: Test-Driven Development workflow. Auto-activates when creating new JS/TS files. Advisory mode suggests tests first; strict mode requires them.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Test-Driven Development Skill

Enforce test-first development workflow for JavaScript and TypeScript files.

## Activation Rules

This skill auto-activates when:
- Creating a NEW JavaScript/TypeScript file (not editing existing)
- File is in a testable location (src/, lib/, components/, scripts/, services/, api/)

This skill stays SILENT when:
- Editing an existing file (test reminder only if test is missing)
- File is a config file (*.config.js, *.config.ts)
- File is in skip locations (see Skip Detection)
- Session has prototyping mode enabled (`/tdd off`)
- File is generated code (*.generated.*, *.g.ts)

## Mode Configuration

| Mode | Behavior | Default |
|------|----------|---------|
| Advisory | Suggests writing tests first, provides guidance, never blocks | Yes |
| Strict | Blocks implementation until test file exists | Opt-in |

### Advisory Mode (Default)

- Reminds to write tests first
- Provides test file path suggestion
- Shows skeleton test template
- Allows proceeding without tests

### Strict Mode (Opt-in)

- Checks for test file existence before allowing implementation
- If test missing: outputs blocking message, suggests test file creation
- Composes with testing skill to scaffold test

## TDD Workflow

```
1. THINK: Define what the code should do
       |
2. TEST: Write a failing test first
       |
3. CODE: Write minimal code to pass
       |
4. REFACTOR: Clean up while tests pass
       |
5. REPEAT: Add next test case
```

The cycle in short:

```
RED -> GREEN -> REFACTOR -> REPEAT
 |       |          |
 |       |          +-- Clean up code, tests still pass
 |       +-- Write minimal code to pass test
 +-- Write a failing test first
```

## Test File Location Convention

| Source File | Test File |
|-------------|-----------|
| `src/foo.js` | `test/foo.test.js` |
| `src/utils/bar.ts` | `test/utils/bar.test.ts` |
| `src/components/Card.js` | `test/components/Card.test.js` |
| `src/services/user.js` | `test/services/user.test.js` |
| `.claude/scripts/tool.js` | `.claude/test/validators/tool.test.js` |

## Compose With Testing Skills

Based on file location, auto-compose with appropriate testing skill:

| Pattern | Testing Skill | Why |
|---------|---------------|-----|
| `src/components/*` | unit-testing | Component logic tests |
| `src/services/*` | backend-testing | Service layer tests |
| `src/api/*`, `src/routes/*` | backend-testing | API endpoint tests |
| `.claude/scripts/*` | unit-testing | CLI tool tests |
| `e2e/*`, `tests/*` | e2e-testing | Browser tests |
| Vite project detected | vitest | Vite-native testing |

## Skip Detection

### Automatic Skips

| Condition | Reason |
|-----------|--------|
| Config files | `*.config.js`, `vite.config.ts`, etc. |
| Generated files | `*.generated.*`, `*.g.ts`, `dist/` |
| Type declarations | `*.d.ts` |
| Documentation | `*.md` in docs/ |
| Test files themselves | `*.test.js`, `*.spec.ts` |
| Fixture files | `fixtures/`, `__mocks__/` |
| Simple renames | Git rename operation detected |
| Entry points | `index.js`, `main.js` |

### Session-Based Skips

When prototyping mode is active (`/tdd off`), TDD checks are suspended.

## Red Flags

| Situation | Advisory | Strict |
|-----------|----------|--------|
| Implementation before test | Reminder | Block |
| Test file path mismatch | Suggest fix | Suggest fix |
| No assertions in test | Warn | Warn |
| Test imports missing module | Expected during TDD | Expected |

## Quick Start Template

When creating a test first, use this skeleton:

```javascript
import { describe, it } from 'node:test';
import assert from 'node:assert';

describe('ModuleName', () => {
  describe('functionName', () => {
    it('should handle expected input', () => {
      // Arrange
      const input = 'test';

      // Act
      const result = functionUnderTest(input);

      // Assert
      assert.strictEqual(result, expected);
    });

    it('should handle edge case', () => {
      // Test edge case
    });

    it('should throw on invalid input', () => {
      assert.throws(() => {
        functionUnderTest(null);
      });
    });
  });
});
```

## Mode Toggle Commands

| Command | Effect |
|---------|--------|
| `/tdd advisory` | Suggest tests (default, never blocks) |
| `/tdd strict` | Require tests before implementation |
| `/tdd off` | Disable for this session (prototyping) |
| `/tdd status` | Show current mode |

## Configuration

Project defaults in `.claude/config/tdd.json`:

```json
{
  "mode": "advisory",
  "testDirectory": "test",
  "testSuffix": ".test"
}
```

## Integration Points

### Pre-Flight Check

TDD adds to JavaScript pre-flight checklist:
- [ ] Test file exists or will be created first
- [ ] Test covers the behavior being implemented

### Completion Check

Before marking JS/TS file complete:
- [ ] Corresponding test file exists
- [ ] Tests pass: `npm test`

## Related Skills

- **unit-testing** - Node.js native test runner patterns
- **backend-testing** - API and database testing
- **vitest** - Vite-based project testing
- **e2e-testing** - Playwright browser testing
- **pre-flight-check** - Git workflow and approach validation
- **javascript-author** - JavaScript coding patterns
