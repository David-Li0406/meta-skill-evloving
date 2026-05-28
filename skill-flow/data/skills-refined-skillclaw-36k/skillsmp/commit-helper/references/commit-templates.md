# Commit Message Templates

Collection of commit message templates for common scenarios.

## Features

### New Function

```
feat(pslib): add <FunctionName> function

<Brief description of what the function does>

<Optional: More detailed explanation>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### New Script

```
feat: add <script-name> utility

<Description of what the script does>

Usage: <script-name> [options]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### New Feature with Multiple Files

```
feat: implement <feature-name>

- <Key change 1>
- <Key change 2>
- <Key change 3>

<Optional: Implementation details>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Bug Fixes

### Simple Bug Fix

```
fix: <brief description of fix>

<What was wrong>
<How it's fixed>

Closes #<issue-number>
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Bug Fix with Test

```
fix: handle <edge-case> in <function-name>

<Description of the bug>
<How the fix works>
<Test added to prevent regression>

Closes #<issue-number>
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Critical Bug Fix

```
fix: resolve critical <issue> in <component>

ISSUE: <Description of critical problem>
FIX: <How it's resolved>
IMPACT: <What users were affected>

Closes #<issue-number>
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Refactoring

### Code Cleanup

```
refactor: simplify <function-name> logic

<What was simplified>
<Why it's better>
No behavior change.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Extract Function

```
refactor: extract <new-function> from <old-function>

Extracted common logic into reusable function.
No behavior change.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Consolidate

```
refactor: consolidate <pattern> across <files>

- Unified <pattern> implementation
- Removed duplication
- No behavior change

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Documentation

### Update README

```
docs: update <section> in README

<What was updated and why>
```

### Add Documentation

```
docs: add <documentation-type> for <component>

<What documentation was added>
```

### Fix Documentation

```
docs: fix <incorrect-information> in <file>

<What was wrong>
<What's correct now>
```

## Tests

### Add Tests

```
test: add <type> tests for <component>

<What's being tested>
<Coverage improvement>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Improve Test Coverage

```
test: improve coverage for <component>

- Added edge case tests
- Added error condition tests
- Coverage increased from X% to Y%

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Fix Flaky Test

```
test: fix flaky <test-name>

<Why it was flaky>
<How it's fixed>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Chores

### Update Dependencies

```
chore: update <dependency> to <version>

<Reason for update>
<Any breaking changes>
```

### Build System

```
chore: update build configuration

<What changed in build system>
```

### Maintenance

```
chore: cleanup <unused-code/files>

Removed unused <what> that's no longer needed.
```

## CI/CD

### GitHub Actions

```
ci: update test workflow

<What changed in CI>
<Why the change>
```

### Add CI Step

```
ci: add <new-step> to workflow

<Description of new CI step>
<Why it's needed>
```

## Style

### Formatting

```
style: format <files> with <tool>

No functional changes.
```

### Code Style

```
style: apply consistent naming in <component>

No functional changes.
```

## Performance

### Optimization

```
perf: optimize <function-name> performance

<What was slow>
<How it's optimized>
<Performance improvement: X% faster>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Breaking Changes

### Breaking API Change

```
feat: change <function> signature

BREAKING CHANGE: <Function> now requires <new-parameter>

<Why the breaking change>
<Migration guide>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Removal

```
refactor: remove deprecated <function>

BREAKING CHANGE: Removed <function>

<Why it was removed>
<Alternative to use>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Real Examples from Project

### Example 1: Feature

```
feat(wsl): add Get-WslDistroType function

Returns the Linux distribution type (ubuntu, debian, alpine, etc.)
for a given WSL distribution name.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Example 2: Bug Fix

```
fix(wsl): ensure WSL distributions are stopped before integration tests

WSL integration tests now properly stop all running WSL distributions
before executing to prevent test interference.

Closes #45
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Example 3: Refactor

```
refactor(testrunner): improve robustness and PS 5.1 compatibility

- Remove PowerShell 6.0+ specific features
- Add better error handling for missing modules
- Improve compatibility with both PS 5.1 and 7.x

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Example 4: Install

```
refactor(install): consolidate installers into tools/install directory

Moved all tool-specific installers from bin/ to tools/install/ for
better organization and discoverability.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Template Selection Guide

| Scenario | Type | Template |
|----------|------|----------|
| New function/feature | feat | New Function |
| Bug fix | fix | Bug Fix with Test |
| Code cleanup | refactor | Code Cleanup |
| Add documentation | docs | Add Documentation |
| Add tests | test | Add Tests |
| Update dependencies | chore | Update Dependencies |
| CI changes | ci | GitHub Actions |
| Performance improvement | perf | Optimization |
| Breaking change | feat/refactor | Breaking Changes |

## Tips

1. Use the most specific template that matches your change
2. Customize templates to fit your actual change
3. Include "why" in the body, not just "what"
4. Reference issues when applicable
5. Always co-author AI contributions
6. Keep subject line under 50 characters
7. Use imperative mood in subject line
