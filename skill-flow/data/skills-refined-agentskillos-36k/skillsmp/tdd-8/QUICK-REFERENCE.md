# TDD Quick Reference Card

## The TDD Cycle

```
RED -> GREEN -> REFACTOR -> REPEAT
 |       |          |
 |       |          +-- Clean up code, tests still pass
 |       +-- Write minimal code to pass test
 +-- Write a failing test first
```

## Before Writing ANY Implementation

1. Does a test file exist? Check: `test/{path}/{name}.test.{ext}`
2. Does the test describe what you're about to build?
3. Does the test currently FAIL? (Red phase)

## Test File Paths

| You're Creating | Test Goes Here |
|-----------------|----------------|
| `src/utils/format.js` | `test/utils/format.test.js` |
| `src/components/Button.ts` | `test/components/Button.test.ts` |
| `src/services/auth.js` | `test/services/auth.test.js` |
| `.claude/scripts/tool.js` | `.claude/test/validators/tool.test.js` |

## Quick Test Template

```javascript
import { describe, it } from 'node:test';
import assert from 'node:assert';

describe('ModuleName', () => {
  it('should do expected behavior', () => {
    // Arrange
    const input = 'test';

    // Act
    const result = functionUnderTest(input);

    // Assert
    assert.strictEqual(result, expected);
  });
});
```

## Mode Commands

| Command | Effect |
|---------|--------|
| `/tdd advisory` | Suggest tests (default, never blocks) |
| `/tdd strict` | Require tests before implementation |
| `/tdd off` | Disable for this session (prototyping) |
| `/tdd status` | Show current mode |

## Skip Automatically

- Config files (`*.config.js`)
- Type definitions (`*.d.ts`)
- Generated code (`dist/`, `*.generated.*`)
- Test files themselves
- Entry points (`index.js`, `main.js`)
- Documentation files

## Compose With

| File Pattern | Testing Skill |
|--------------|---------------|
| `src/services/*` | backend-testing |
| `src/api/*` | backend-testing |
| `src/components/*` | unit-testing |
| `.claude/scripts/*` | unit-testing |
| Vite project | vitest |

## Checklist Before Proceeding

- [ ] Test file exists
- [ ] Test describes intended behavior
- [ ] Test currently fails (proving it tests something)
- [ ] Ready to write implementation
