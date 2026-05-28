# Auto-Fix Workflow Guide

Detailed guide for automatically fixing code review issues using codex-cli.

## Overview

The auto-fix workflow uses **codex-cli** for code analysis and **Claude Code** for applying fixes.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  codex-cli  │───▶│   Parse     │───▶│   Confirm   │───▶│ Claude Code │
│   Review    │    │   JSON      │    │   with User │    │  Edit Tool  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                               │
                                                               ▼
                                      ┌─────────────┐    ┌─────────────┐
                                      │   Report    │◀───│   Verify    │
                                      │   Results   │    │   Build/Test│
                                      └─────────────┘    └─────────────┘
```

## Step 1: Run codex-cli Analysis

Execute codex-cli to analyze code:

```bash
# Single file
codex -q "Review Swift code for issues. Output JSON: $(cat File.swift)"

# Via skill
/code-review handheld/Sources/handheld/ViewModels/ContentViewModel.swift
```

Or for multiple files:

```bash
# All changed files
for f in $(git diff master --name-only | grep '\.swift$'); do
  codex -q "Review: $(cat "$f")"
done
```

## Step 2: Parse JSON Output

codex-cli outputs issues in JSON format:

```json
[
  {
    "file": "ContentViewModel.swift",
    "line": 15,
    "severity": "Critical",
    "category": "Concurrency",
    "description": "Missing @MainActor for @Observable class",
    "current_code": "@Observable\nclass ContentViewModel {",
    "suggested_fix": "@Observable\n@MainActor\nclass ContentViewModel {"
  }
]
```

## Step 3: Present to User

Format issues for user review:

```markdown
# Code Review Results (via codex-cli)

Found **5 issues** in ContentViewModel.swift

## Issue #1: Missing @MainActor (Critical)

**File**: ContentViewModel.swift:15
**Severity**: Critical

### Problem
ViewModel updates UI-bound properties without @MainActor guarantee.

### Current Code
```swift
@Observable
class ContentViewModel {
    var items: [Item] = []
```

### Suggested Fix (from codex-cli)
```swift
@Observable
@MainActor
class ContentViewModel {
    var items: [Item] = []
```

---

## Issue #2: Retain Cycle Risk (High)
...
```

## Step 4: User Confirmation

Ask user before applying fixes:

```
Found 5 issues (reviewed by codex-cli):
- 1 Critical
- 2 High
- 2 Medium

Would you like Claude Code to apply these fixes?
- [Fix All] Apply all fixes
- [Critical Only] Fix only critical issues
- [Review Each] Ask before each fix
- [Skip] Don't apply any fixes
```

## Step 5: Apply Fixes (Claude Code)

Claude Code applies fixes using the Edit tool:

### Sequential Application

```
Applying fix 1/5: Adding @MainActor to ContentViewModel
✓ Fix applied successfully

Applying fix 2/5: Adding weak self to closure
✓ Fix applied successfully

Applying fix 3/5: Adding error handling
✗ Fix failed - conflict detected
  → Manual intervention required
```

### Handling Conflicts

If a fix fails:
1. Report the failure
2. Explain why it failed
3. Suggest manual resolution
4. Continue with remaining fixes

## Step 6: Verify Changes

Run verification after fixes:

### Swift Verification

```bash
# Run linter
cd handheld && swiftlint

# Build project
make build

# Run tests
make test
```

### TypeScript Verification

```bash
cd web

# Run linter
npm run lint

# Type check
npm run type-check

# Build
npm run build

# Run tests (if available)
npm test
```

## Step 7: Report Results

Summarize applied fixes:

```markdown
# Fix Report

## Summary
- Total issues found by codex-cli: 5
- Fixes applied by Claude Code: 4
- Fixes skipped: 1 (manual intervention needed)

## Applied Fixes

✓ **#1 Critical**: Added @MainActor to ContentViewModel
  File: ContentViewModel.swift:15

✓ **#2 High**: Added weak self to closure
  File: ContentViewModel.swift:42

✓ **#3 High**: Added error handling to loadData
  File: ContentViewModel.swift:56

✓ **#4 Medium**: Changed force unwrap to guard let
  File: ContentViewModel.swift:78

## Skipped Fixes

⚠ **#5 Medium**: Complex refactoring needed
  File: ContentViewModel.swift:92
  Reason: Multiple interdependent changes required
  Recommendation: Manual refactoring suggested

## Verification Results

✓ SwiftLint: Passed
✓ Build: Succeeded
✓ Tests: 12/12 passed
```

## Fix Strategies by Issue Type

### Swift Fixes

| Issue Type | Fix Strategy |
|------------|--------------|
| Missing @MainActor | Add @MainActor annotation |
| Retain cycle | Add `[weak self]` capture |
| Force unwrap | Convert to guard let or if let |
| Missing error handling | Add do-catch block |
| Performance (DateFormatter) | Extract to static property |

### TypeScript Fixes

| Issue Type | Fix Strategy |
|------------|--------------|
| any type | Add proper interface |
| Missing deps | Add to dependency array |
| Missing cleanup | Add return function in useEffect |
| Type assertion | Add type guard |
| Missing null check | Add optional chaining |

## Safety Guidelines

### Always Do

- ✓ Review codex-cli output before applying
- ✓ Apply one fix at a time
- ✓ Verify after each fix
- ✓ Report failures clearly
- ✓ Preserve existing behavior

### Never Do

- ✗ Apply fixes without user confirmation
- ✗ Skip verification steps
- ✗ Change unrelated code
- ✗ Remove error handling
- ✗ Ignore test failures

## Rollback Procedure

If fixes cause issues:

```bash
# View recent changes
git diff

# Revert specific file
git checkout -- path/to/file

# Revert all changes
git checkout -- .

# Or if committed
git reset --soft HEAD~1
```

## Example Session

```
User: /code-review ContentViewModel.swift

Claude: Running codex-cli review...
        [Executes: codex -q "Review Swift code..." ]

        codex-cli found 3 issues:

        1. Critical: ViewModel missing @MainActor
        2. High: Potential retain cycle in closure
        3. Medium: Force unwrap on line 45

        Would you like Claude Code to apply these fixes?

User: Yes, fix all

Claude: Applying fixes...

        ✓ Fix 1: Added @MainActor annotation (line 10)
        ✓ Fix 2: Added [weak self] capture (line 32)
        ✓ Fix 3: Converted to guard let (line 45)

        Running verification...
        ✓ Build succeeded
        ✓ Tests passed (8/8)

        All fixes applied successfully!
```

## Limitations

Auto-fix works best for:
- ✓ Simple, localized changes
- ✓ Well-defined patterns
- ✓ Single-file fixes

Manual intervention preferred for:
- ✗ Complex refactoring
- ✗ Multi-file changes
- ✗ Architecture decisions
- ✗ Business logic changes

## Troubleshooting

### codex-cli not found

```bash
# Install codex-cli
npm install -g @openai/codex

# Or with npx
npx @openai/codex -q "..."
```

### JSON parse error

If codex-cli output is not valid JSON:
1. Check the prompt includes "Output JSON only"
2. Try with `-q` (quiet) flag
3. Claude Code will extract JSON from mixed output

### Rate limiting

If codex-cli is rate limited:
1. Add delay between file reviews
2. Review fewer files at once
3. Use batch mode for large changes
