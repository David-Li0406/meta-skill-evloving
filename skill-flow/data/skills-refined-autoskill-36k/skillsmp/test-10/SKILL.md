---
name: test
description: Renovate config E2E test writing guide. Use when creating or modifying tests in tests/ directory for verifying Renovate configuration behavior.
---

# Renovate Config Test Writing Guide

This skill provides best practices for writing E2E tests that verify Renovate configuration behavior.

## Core Principles

### 1. Test Real Renovate Behavior, Not Config Structure

**Wrong approach:**

- Re-implementing Renovate's internal matching logic (regex patterns, packageRules evaluation)
- Checking config structure only (e.g., "prPriority is set to 100")
- Writing assertion-only tests that just verify config properties exist

**Correct approach:**

- Use `describeWithRenovate` to run actual Renovate dry-run
- Verify Renovate's output (detected updates, generated PR titles, skip reasons)
- Test the real behavior that users will experience

### 2. Use describeWithRenovate Helper

Always use the `describeWithRenovate` helper from `tests/helpers/with-renovate.ts`:

```typescript
import { expect, it } from 'vitest'
import { describeWithRenovate } from './helpers/with-renovate'

describeWithRenovate(
  'test description',
  {
    fixtures: ['path/to/fixture.json'],
    mockNpmPackages: [{ name: 'example', versions: ['1.0.0', '2.0.0'] }],
  },
  (ctx) => {
    it('should detect updates correctly', () => {
      const pkgFile = ctx.getPackageFile('npm', 'path/to/fixture.json')
      // assertions...
    })
  },
)
```

### 3. SetupOptions

Available options for `describeWithRenovate`:

| Option              | Description                                                               |
| ------------------- | ------------------------------------------------------------------------- |
| `fixtures`          | Array of fixture file paths from `__fixtures__`                           |
| `mockCrates`        | Mock crates.io registry entries                                           |
| `mockNpmPackages`   | Mock npm registry entries                                                 |
| `mockGitHubRepos`   | Mock GitHub API for github-tags datasource                                |
| `mockRepos`         | Mock git repositories (for copier, etc.)                                  |
| `additionalConfigs` | Additional config files to merge (e.g., `['node.json5']`)                 |
| `dryRunMode`        | `'lookup'` (default) for dependency detection, `'full'` for PR simulation |

### 4. dryRunMode Selection

- Use `'lookup'` (default) when testing:
  - Dependency detection
  - Skip reasons
  - Update availability
  - Version constraints

- Use `'full'` when testing:
  - PR titles (`prTitle`)
  - Branch names
  - Commit messages
  - prPriority ordering

### 5. Use toMatchObject for Assertions

Prefer `toMatchObject` over strict equality. This makes tests more resilient to unrelated changes:

```typescript
// Good: focuses on what matters
expect(dep).toMatchObject({
  depName: 'example',
  skipReason: 'disabled',
})

// Bad: brittle, breaks when unrelated fields change
expect(dep).toEqual({
  depName: 'example',
  skipReason: 'disabled',
  currentValue: '1.0.0',
  // ... many other fields
})
```

For array assertions:

```typescript
expect(branch).toMatchObject({
  prTitle: expect.stringMatching(/^deps!: /),
  upgrades: expect.arrayContaining([
    expect.objectContaining({
      depName: 'example',
      updateType: 'major',
    }),
  ]),
})
```

### 6. Context Methods

The `RenovateTestContext` provides:

- `ctx.getPackageFile(manager, filePath)` - Get a detected package file
- `ctx.getBranches()` - Get generated branches (requires `dryRunMode: 'full'`)

### 7. Fixture Files

Place fixture files in `tests/__fixtures__/`. Use placeholders for mock repos:

```yaml
# {{MOCK_REPO:template-name}} will be replaced with file:// URL
_src_path: '{{MOCK_REPO:test-template}}'
```

## Example: Testing PR Title Format

```typescript
describeWithRenovate(
  'major update PR title',
  {
    fixtures: ['major-update/.mise.toml'],
    mockCrates: [{ name: 'test-crate', versions: ['1.0.0', '2.0.0'] }],
    dryRunMode: 'full',
  },
  (ctx) => {
    it('should use deps!: prefix for major updates', () => {
      const branch = ctx
        .getBranches()
        .find((b) => b.upgrades?.some((u) => u.depName === 'cargo:test-crate'))

      expect(branch).toMatchObject({
        prTitle: expect.stringMatching(/^deps!: /),
        upgrades: expect.arrayContaining([
          expect.objectContaining({
            depName: 'cargo:test-crate',
            updateType: 'major',
          }),
        ]),
      })
    })
  },
)
```

## Example: Testing Disabled Packages

```typescript
describeWithRenovate(
  'managed packages',
  {
    fixtures: ['package.json'],
    mockNpmPackages: [{ name: 'prettier', versions: ['3.0.0', '3.1.0'] }],
    additionalConfigs: ['node.json5'],
  },
  (ctx) => {
    it('should disable updates for managed packages', () => {
      const pkgFile = ctx.getPackageFile('npm', 'package.json')
      const dep = pkgFile.deps.find((d) => d.depName === 'prettier')

      expect(dep).toMatchObject({
        depName: 'prettier',
        skipReason: 'disabled',
      })
    })
  },
)
```

## Anti-Patterns to Avoid

1. **Re-implementing Renovate logic**: Don't write your own regex matching or packageRules evaluation
2. **Config-only assertions**: Don't just check that config properties exist
3. **Mocking Renovate internals**: Let Renovate run and verify its actual output
4. **Exact equality assertions**: Use `toMatchObject` to focus on relevant fields
5. **Testing multiple unrelated behaviors in one test**: Each test should verify one specific behavior
