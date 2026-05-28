---
name: unit-test-loop
description: |
  This skill should be used when the user asks to "improve test coverage",
  "add unit tests", "TDD", "test this module", "write tests for", "increase
  coverage", "/ut command", or discusses unit testing strategies. Covers the
  unit test loop workflow, React Testing Library best practices, query
  priorities, and coverage improvement strategies.
version: 1.0.0
---

# Unit Test Loop - Coverage Improvement

**Current branch:** !`git branch --show-current 2>/dev/null || echo "not in git repo"`

The unit test loop systematically improves test coverage through iterative,
focused test writing with mandatory quality reviews.

## State Management

**Single Source of Truth**: `.claude/ut-state-{session}.json` stores all state including
the embedded progress log. No separate progress.txt file.

**What Hook Updates:**
- Appends to state.json's `log` array automatically
- Iteration markers are optional (hook auto-detects from git)

## When to Use Unit Test Loop

- Need to improve overall test coverage
- Adding tests to untested code
- TDD workflow for new features
- Coverage metrics are below target

## Starting the Loop

```bash
/ut "Improve coverage for auth module"                    # Basic
/ut "Add tests" --target 80%                              # With target
/ut "Cover utils" --test-command "npm run test:unit"      # Custom command
```

## Iteration Workflow

Each iteration follows this exact sequence:

1. **Run coverage** - Identify files with low coverage
2. **Find ONE gap** - Focus on user-facing behavior, not implementation
3. **Write ONE test** - Validate real user behavior
4. **Run linters** - Ensure code quality
5. **Verify improvement** - Run coverage again
6. **Run reviewers** - code-simplifier + kieran reviewer (MANDATORY)
7. **Commit** - `test(<file>): describe behavior`

## React Testing Library Patterns

> "The more your tests resemble the way your software is used,
> the more confidence they can give you."

### Query Priority (Use in Order)

| Priority | Query | Use Case |
|----------|-------|----------|
| 1 | `getByRole` | Default choice, use `name` option |
| 2 | `getByLabelText` | Form fields with labels |
| 3 | `getByPlaceholderText` | Only if no label available |
| 4 | `getByText` | Non-interactive elements |
| 5 | `getByTestId` | **Last resort only** |

### Query Types

| Type | When to Use |
|------|-------------|
| `getBy`/`getAllBy` | Element exists (throws if not found) |
| `queryBy`/`queryAllBy` | **Only** for asserting absence |
| `findBy`/`findAllBy` | Async elements (returns Promise) |

### Best Practices

```typescript
// Use screen
screen.getByRole('button', { name: /submit/i })

// Use userEvent.setup()
const user = userEvent.setup()
await user.click(button)

// Use jest-dom matchers
expect(button).toBeDisabled()  // Not: expect(button.disabled).toBe(true)

// Avoid act() - RTL handles it
await screen.findByText('Loaded')  // Not: act(() => ...)
```

## Quality Standards

- **ONE test per iteration** - Focused, reviewable commits
- **User-facing behavior only** - Test what users depend on
- **Quality over quantity** - One great test beats ten shallow ones
- **No coverage gaming** - Use `/* v8 ignore */` for untestable code

## Completion

Output when coverage target reached:

```xml
<promise>COVERAGE COMPLETE</promise>
```

Only output when genuinely complete - do not exit prematurely.

## Task Integration (Optional)

### On Coverage Analysis Complete

For each file below target coverage:
```
TaskCreate({
  subject: "Test: {filename} ({current}% → {target}%)",
  description: "Improve coverage for {full_path}",
  activeForm: "Testing {filename}",
  metadata: { loop: "ut", file_path: "{path}", current: {N}, target: {M} }
})
```

### On File Coverage Met

`TaskUpdate(task_id, status: "completed")`

### Dynamic Discovery

When new files are found during iteration, create additional Tasks.

## Command Reference

```bash
/ut "prompt"                                    # Basic loop
/ut "prompt" --target 80%                       # With target
/ut "prompt" --max-iterations 10               # Limit iterations
/ut "prompt" --test-command "yarn test:unit"   # Custom test command
/cancel-ut                                      # Cancel loop
```
