---
name: debug
description: 'Systematically analyze and fix bugs, errors, and unexpected behavior. Use when the user reports bugs, error messages, crashes, test failures, unexpected behavior, or performance issues.'
compatibility: Requires code read/write, terminal, and debugging tools
allowed-tools:
    - Bash(node:*, npm:*, npx:*, pnpm:*, yarn:*, python:*, pip:*, pytest:*, go:*, cargo:*, mvn:*, ./mvnw:*, gradle:*, ./gradlew:*, make:*, cmake:*, g++:*, gcc:*, clang:*)
    - Glob
    - Grep
    - Read
    - Write
    - mcp__context7
    - mcp__fetch
    - mcp__jetbrains
    - mcp__markitdown
    - mcp__sequential-thinking
    - mcp__serena
---

# Debugging Skill

Systematically analyze and fix bugs, errors, and unexpected behavior.

## Debugging Process

1. Reproduce: exact steps, minimal repro, expected vs actual 기록.
2. Gather info: `mcp__serena__find_referencing_symbols`(usages), `mcp__jetbrains__get_symbol_info`(defs),
   `mcp__context7__get-library-docs`(docs); collect logs/stack traces.
3. Analyze: read errors, locate failure points, binary search/ logging로 범위 축소.
4. Fix: address root cause, preserve behavior, cover edge cases.
5. Verify: original 이슈 해결 확인, 관련 테스트 실행, 회귀 여부 점검.

## Common Bugs

### Syntax Errors

```text
Error: Unexpected token
SyntaxError: invalid syntax
```

**Actions**:

- Check indicated line
- Verify brackets/parentheses balance
- Look for missing semicolons or commas

### Runtime Errors

```text
TypeError: Cannot read property 'x' of undefined
AttributeError: 'NoneType' has no attribute 'x'
```

**Actions**:

- Trace variable origin
- Add null checks
- Verify data flow

### Logic Errors

- No error message, wrong result
- Off-by-one errors
- Incorrect conditions

**Actions**:

- Add logging to trace execution
- Step through logic manually
- Write test cases for expected behavior

### Async Errors

```text
UnhandledPromiseRejection
Race condition symptoms
```

**Actions**:

- Check async/await usage
- Verify Promise chains
- Look for shared state mutations

### Import/Module Errors

```text
ModuleNotFoundError
Cannot find module
```

**Actions**:

- Check package installation
- Verify import paths
- Check package.json/requirements.txt

### Type Errors

```text
Type 'A' is not assignable to type 'B'
```

**Actions**:

- Check type definitions
- Verify function signatures
- Look for type mismatches

## Debugging Techniques

### Print/Log Debugging

```javascript
console.log('[DEBUG] variable:', JSON.stringify(variable, null, 2));
console.log('[DEBUG] function entered with args:', args);
```

```python
import logging

logging.debug(f'variable: {variable}')
```

### Binary Search Debugging

- Comment out half the suspicious code
- If bug persists, it's in the other half
- Repeat until isolated

### Rubber Duck Debugging

- Explain the code line by line
- Often reveals assumptions and errors
- Document the explanation as comments

### Git Bisect

```bash
git bisect start
git bisect bad HEAD
git bisect good <last-known-good-commit>
# Test each commit git bisect suggests
```

### Stack Trace Analysis

- Read from bottom to top
- Focus on your code, not framework code
- Identify the trigger point

## Bug Categories

### Off-by-One Errors

```javascript
// Bug: Array index out of bounds
for (let i = 0; i <= arr.length; i++)

// Fix: Use < instead of <=
for (let i = 0; i < arr.length; i++)
```

### Null/Undefined Handling

```javascript
// Bug: Accessing property of undefined
const name = user.profile.name;

// Fix: Optional chaining
const name = user?.profile?.name;
```

### State Management

```javascript
// Bug: Mutating shared state
users.push(newUser);

// Fix: Create new array
const updatedUsers = [...users, newUser];
```

### Async Timing

```javascript
// Bug: Not waiting for async
const data = fetchData();
process(data); // data is a Promise!

// Fix: Await the promise
const data = await fetchData();
process(data);
```

## Output Format

```markdown
## Bug Analysis

### Symptom

[What was observed]

### Root Cause

[Why it happened]

### Fix

(code changes with before/after)

### Impact

- [Files affected]
- [Potential side effects]
- [Preventive measures]

### Verification Method

(commands or tests to verify fix)
```

## Edge Cases

- **Intermittent bugs**: Add logging, use stress testing
- **Environment-specific**: Check environment differences first
- **No reproduction**: Add monitoring and logging
- **Third-party bugs**: Document workaround, report upstream

## Tips

- MCP tools are optional; omit if unavailable or add others as needed
