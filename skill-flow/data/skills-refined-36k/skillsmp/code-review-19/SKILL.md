---
name: code-review
description: |
  This skill should be used when the user asks to "review code",
  "check code quality", "find improvements", "refactor code",
  "fix code issues", "perform code review", "check for bugs",
  "improve code", "analyze code", "review PR", "review pull request",
  "コードレビュー", "コードをチェック", "改善点を探す",
  "リファクタリング", "コード品質を確認", "バグを探す",
  "コードを改善", "PR をレビュー", "プルリクエストをレビュー",
  or needs guidance on code review best practices for Swift and TypeScript.
version: 1.0.0
---

# Code Review

Comprehensive code review skill using **codex-cli** for analysis, with Claude Code applying fixes automatically.

## Overview

**Review Engine**: codex-cli (via Bash)
**Fix Engine**: Claude Code (Edit tool)

**Supported Languages**:
- Swift 5.9+ (iOS 17+, SwiftUI, SwiftData)
- TypeScript 5.x+ (Next.js 14+, React 18+)

**Core Capabilities**:
- Use codex-cli to identify code quality issues
- Parse codex-cli output for structured feedback
- **Claude Code automatically applies fixes**

## Default Behavior (No Arguments)

When `/code-review` is invoked without specifying a file or directory:

1. **Get changed files** from `git diff master...HEAD --name-only`
2. **Filter** to only `.swift`, `.ts`, `.tsx` files
3. **Run codex-cli** to review each changed file
4. **Parse output** and present issues
5. **Apply fixes** with Claude Code's Edit tool

```bash
# Get changed files
git diff master...HEAD --name-only | grep -E '\.(swift|ts|tsx)$'
```

### Usage Examples

```
/code-review                    # Review all changes vs master
/code-review path/to/file.swift # Review specific file
/code-review handheld/Sources/  # Review directory
```

## Codex-CLI Integration

### Step 1: Prepare Review Prompt

Create a structured prompt for codex-cli:

```bash
# Review a single file with codex-cli
codex -q "Review this code for issues. Output in JSON format with fields: file, line, severity (Critical/High/Medium/Low), category, description, current_code, suggested_fix. File: <filename>

$(cat path/to/file.swift)"
```

### Step 2: Run Codex-CLI

Execute codex-cli via Bash tool:

```bash
# For Swift files
codex -q "You are a Swift code reviewer. Review for:
- Memory leaks (retain cycles in closures)
- Missing @MainActor for UI updates
- Force unwrap without safety
- Performance issues
- SwiftUI best practices

Output JSON array of issues. Each issue: {file, line, severity, category, description, current_code, suggested_fix}

$(cat handheld/Sources/path/to/File.swift)"

# For TypeScript files
codex -q "You are a TypeScript code reviewer. Review for:
- any type usage
- Missing useEffect dependencies
- Unnecessary re-renders
- Type safety issues
- Next.js/React best practices

Output JSON array of issues. Each issue: {file, line, severity, category, description, current_code, suggested_fix}

$(cat web/src/path/to/file.tsx)"
```

### Step 3: Parse and Present Issues

Parse the JSON output from codex-cli and present to user:

```
## Issue #1: [Description]
- **File**: path/to/file.swift:42
- **Severity**: Critical | High | Medium | Low
- **Category**: Memory | Type Safety | Performance | Style
- **Current Code**: (from codex output)
- **Suggested Fix**: (from codex output)
```

### Step 4: Apply Fixes (Claude Code)

After user confirmation ("Fix All" or specific issue numbers):
1. Use Edit tool to apply each fix from codex-cli's suggestions
2. Run linter/tests to verify

### Step 5: Verify

```bash
# Swift
cd handheld && make test

# TypeScript
cd web && npm run lint && npm run type-check
```

## Quick Reference

### Codex-CLI Commands

```bash
# Basic review
codex -q "Review this Swift code: $(cat file.swift)"

# With specific focus
codex -q "Check for memory leaks in: $(cat file.swift)"

# Multiple files (loop)
for f in $(git diff master --name-only | grep '\.swift$'); do
  echo "=== $f ==="
  codex -q "Review: $(cat $f)"
done
```

### Expected JSON Output Format

```json
[
  {
    "file": "ViewModel.swift",
    "line": 42,
    "severity": "High",
    "category": "Concurrency",
    "description": "Missing @MainActor for class with @Observable",
    "current_code": "@Observable\nclass ViewModel {",
    "suggested_fix": "@Observable\n@MainActor\nclass ViewModel {"
  }
]
```

## Swift Code Review

### Critical Checks

| Category | Check | Severity |
|----------|-------|----------|
| Memory | No retain cycles in closures | Critical |
| Concurrency | `@MainActor` for UI updates | Critical |
| Safety | No force unwrapping without safety | High |
| Performance | Avoid unnecessary @State changes | Medium |
| Style | Consistent naming conventions | Low |

### Common Issues and Fixes

#### 1. Force Unwrap Without Safety

```swift
// BAD: Force unwrap can crash
let user = users.first!

// GOOD: Safe unwrapping with guard
guard let user = users.first else {
    return
}
```

#### 2. Missing @MainActor for UI Updates

```swift
// BAD: UI update from background thread
@Observable
class ViewModel {
    var items: [Item] = []  // Can be updated from any thread

    func loadItems() async {
        items = try await api.fetchItems()  // May not be on main thread
    }
}

// GOOD: MainActor ensures UI safety
@Observable
@MainActor
class ViewModel {
    var items: [Item] = []

    func loadItems() async {
        items = try await api.fetchItems()
    }
}
```

#### 3. Retain Cycle in Closure

```swift
// BAD: Strong reference cycle
class ViewModel {
    var onComplete: (() -> Void)?

    func setup() {
        onComplete = {
            self.doSomething()  // Strong capture of self
        }
    }
}

// GOOD: Weak capture
class ViewModel {
    var onComplete: (() -> Void)?

    func setup() {
        onComplete = { [weak self] in
            self?.doSomething()
        }
    }
}
```

For more Swift patterns, see [references/swift-checklist.md](references/swift-checklist.md).

## TypeScript Code Review

### Critical Checks

| Category | Check | Severity |
|----------|-------|----------|
| Type Safety | No `any` types without justification | High |
| Null Safety | Proper optional chaining | High |
| React | No missing dependencies in useEffect | Critical |
| Performance | Memoization where needed | Medium |
| Next.js | Correct use of 'use client' | High |

### Common Issues and Fixes

#### 1. Using `any` Type

```typescript
// BAD: Using any loses type safety
const data: any = await fetchData();
console.log(data.user.name);

// GOOD: Proper typing
interface User {
  id: string;
  name: string;
}

interface ApiResponse {
  user: User;
}

const data: ApiResponse = await fetchData();
console.log(data.user.name);
```

#### 2. Missing useEffect Dependencies

```tsx
// BAD: Missing dependency can cause stale closure
function Component({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, []);  // Missing userId dependency

  return <div>{user?.name}</div>;
}

// GOOD: All dependencies included
function Component({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);  // Correct dependencies

  return <div>{user?.name}</div>;
}
```

#### 3. Unnecessary Re-renders

```tsx
// BAD: Object created on every render
function Component() {
  const options = { size: 'large', color: 'blue' };  // New object every render

  return <Child options={options} />;
}

// GOOD: Memoized or constant
const OPTIONS = { size: 'large', color: 'blue' } as const;

function Component() {
  return <Child options={OPTIONS} />;
}

// OR with useMemo for dynamic values
function Component({ color }: { color: string }) {
  const options = useMemo(() => ({ size: 'large', color }), [color]);

  return <Child options={options} />;
}
```

For more TypeScript patterns, see [references/typescript-checklist.md](references/typescript-checklist.md).

## Running Linters

### Swift

```bash
# Run SwiftLint (if configured)
cd handheld && swiftlint

# With autocorrect
swiftlint --fix

# Run tests
make test
```

### TypeScript

```bash
cd web

# Run ESLint
npm run lint

# Run TypeScript type check
npm run type-check

# Fix auto-fixable issues
npm run lint -- --fix

# Run all checks
npm run lint && npm run type-check && npm run build
```

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **Critical** | Crashes, data loss, security issues | Must fix immediately |
| **High** | Bugs, type errors, memory leaks | Should fix before merge |
| **Medium** | Performance, maintainability | Consider fixing |
| **Low** | Style, minor improvements | Optional |

## CI/CD Integration

### iOS (GitHub Actions)

The project runs `make test` which includes:
- Build verification
- Unit tests execution

### Web (GitHub Actions)

The project runs:
- `npm run lint` (ESLint)
- `npm run type-check` (TypeScript)
- `npm run build` (Production build)

## Additional Resources

### References

- **[references/swift-checklist.md](references/swift-checklist.md)** - Complete Swift review checklist
- **[references/swift-anti-patterns.md](references/swift-anti-patterns.md)** - Swift anti-patterns to avoid
- **[references/swift-performance.md](references/swift-performance.md)** - Swift performance optimization
- **[references/swift-concurrency.md](references/swift-concurrency.md)** - Swift concurrency review
- **[references/swift-swiftui.md](references/swift-swiftui.md)** - SwiftUI specific checks
- **[references/typescript-checklist.md](references/typescript-checklist.md)** - Complete TypeScript checklist
- **[references/typescript-anti-patterns.md](references/typescript-anti-patterns.md)** - TypeScript anti-patterns
- **[references/typescript-type-patterns.md](references/typescript-type-patterns.md)** - Type design patterns
- **[references/typescript-nextjs.md](references/typescript-nextjs.md)** - Next.js specific checks
- **[references/typescript-react.md](references/typescript-react.md)** - React specific checks
- **[references/review-process.md](references/review-process.md)** - Review process guide
- **[references/auto-fix-workflow.md](references/auto-fix-workflow.md)** - Auto-fix workflow details

### Examples

- **[examples/swift-before-after.swift](examples/swift-before-after.swift)** - Swift refactoring examples
- **[examples/swift-common-issues.swift](examples/swift-common-issues.swift)** - Common Swift issues
- **[examples/swift-async-patterns.swift](examples/swift-async-patterns.swift)** - async/await patterns
- **[examples/swift-memory-management.swift](examples/swift-memory-management.swift)** - Memory management
- **[examples/typescript-before-after.tsx](examples/typescript-before-after.tsx)** - TypeScript refactoring
- **[examples/typescript-common-issues.ts](examples/typescript-common-issues.ts)** - Common TypeScript issues
- **[examples/typescript-type-safety.ts](examples/typescript-type-safety.ts)** - Type safety patterns
- **[examples/typescript-react-patterns.tsx](examples/typescript-react-patterns.tsx)** - React best practices
