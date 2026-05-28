# Code Review Process Guide

Standard process for conducting code reviews.

## Review Workflow

### Step 1: Understand the Context

Before reviewing code:

1. **Read the related issue/ticket** (if any)
2. **Understand the purpose** of the change
3. **Check the scope** - what files are affected
4. **Review recent history** - any related changes

### Step 2: Analyze the Code

Review in this order:

1. **High-level structure**
   - Does the architecture make sense?
   - Are responsibilities well-separated?
   - Is the change in the right place?

2. **Logic correctness**
   - Does the code do what it's supposed to?
   - Are edge cases handled?
   - Is error handling appropriate?

3. **Type safety**
   - Are types explicit where needed?
   - No unsafe type assertions?
   - Proper null handling?

4. **Performance**
   - Any obvious inefficiencies?
   - Memory management concerns?
   - Unnecessary computations?

5. **Style and readability**
   - Consistent naming?
   - Clear code structure?
   - Appropriate comments?

### Step 3: Document Issues

For each issue found, record:

```
## Issue: [Brief Title]

- **File**: path/to/file:line_number
- **Severity**: Critical | High | Medium | Low
- **Category**: [Type Safety | Memory | Performance | etc.]

### Problem
[Clear description of what's wrong]

### Current Code
```language
// problematic code
```

### Suggested Fix
```language
// corrected code
```

### Rationale
[Why this matters / why the fix is better]
```

### Step 4: Prioritize Fixes

Group issues by severity:

| Severity | Description | Action Required |
|----------|-------------|-----------------|
| Critical | Security, crashes, data loss | Must fix before merge |
| High | Bugs, type errors, memory leaks | Should fix before merge |
| Medium | Performance, maintainability | Consider fixing |
| Low | Style, minor improvements | Optional |

### Step 5: Apply Fixes

For automatic fixes:

1. **Confirm with user** before making changes
2. **Apply fixes one at a time**
3. **Run verification** after each change:
   - Linter (`npm run lint` / `swiftlint`)
   - Type check (`npm run type-check` / build)
   - Tests (if available)

4. **Handle failures**
   - If a fix breaks something, revert
   - Analyze the failure
   - Try alternative approach

### Step 6: Verify

After all fixes:

1. **Run full test suite**
2. **Run linters**
3. **Manual spot check** of changed code
4. **Confirm no regressions**

## Issue Categories

### Swift Categories

| Category | Examples |
|----------|----------|
| Memory | Retain cycles, leaks, excessive allocations |
| Concurrency | Missing @MainActor, data races |
| Safety | Force unwraps, unhandled optionals |
| Performance | Inefficient collections, missing cache |
| SwiftUI | @State misuse, view composition |
| Style | Naming, formatting, conventions |

### TypeScript Categories

| Category | Examples |
|----------|----------|
| Types | any usage, missing types, assertions |
| Null Safety | Missing optional chaining, unsafe access |
| React Hooks | Missing dependencies, conditional hooks |
| Performance | Missing memo, unstable keys |
| Next.js | Client/Server confusion, caching |
| Style | Naming, imports, formatting |

## Review Communication

### Effective Feedback

**Be specific:**
```
// Instead of: "This is wrong"
// Say: "This useEffect is missing `userId` in its dependency array,
//       which can cause stale closure bugs when userId changes"
```

**Explain why:**
```
// Instead of: "Use guard let"
// Say: "Using guard let here ensures early exit and reduces nesting,
//       making the happy path more readable"
```

**Provide solutions:**
```
// Instead of: "This could be better"
// Say: "Consider extracting this into a custom hook to make it reusable
//       and easier to test. Here's how: [code example]"
```

### Severity Guidelines

**Critical** - Must fix:
- Security vulnerabilities
- Data corruption risks
- Definite crashes
- Breaking API changes

**High** - Should fix:
- Bugs in business logic
- Type safety issues
- Memory leaks
- Missing error handling

**Medium** - Consider fixing:
- Performance issues
- Code maintainability
- Incomplete abstraction
- Missing tests

**Low** - Nice to have:
- Style inconsistencies
- Minor optimizations
- Documentation improvements
- Refactoring suggestions

## Common Review Scenarios

### New Feature Review

Focus on:
1. Does it meet requirements?
2. Is it well-architected?
3. Is it testable?
4. Is it accessible?

### Bug Fix Review

Focus on:
1. Does it fix the bug?
2. Does it introduce regressions?
3. Is the root cause addressed?
4. Are there similar bugs elsewhere?

### Refactoring Review

Focus on:
1. Is behavior preserved?
2. Are tests updated/passing?
3. Is the code cleaner?
4. Are dependencies updated?

### Performance Fix Review

Focus on:
1. Is improvement measured?
2. Are tradeoffs acceptable?
3. Is it maintainable?
4. Is it cache/memory safe?
