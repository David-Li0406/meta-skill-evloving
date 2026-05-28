---
name: upgrade
description: "Use when user asks to upgrade dependencies, update packages, review outdated libraries, or resolve security vulnerabilities. Covers dependency analysis, breaking change research, incremental implementation, and validation for npm, dotnet, and other ecosystems."
---

# Dependency Upgrade Skill

Procedural knowledge for safely upgrading dependencies across ecosystems with proper research, risk assessment, and validation.

## Upgrade Protocol Overview

| Phase               | Role                         | Primary Output                  |
| ------------------- | ---------------------------- | ------------------------------- |
| 1. Inventory & Plan | Dependency Inventory Analyst | Prioritized upgrade sequence    |
| 2. Research & Risk  | Breaking Change Researcher   | Migration steps, API changes    |
| 3. Implement        | Upgrade Implementer          | Applied changes, modified files |
| 4. Validation       | Validation Specialist        | Test/lint/build/scan results    |

---

## Phase 1: Inventory & Plan

### Goal

Identify all outdated dependencies, classify by urgency, and sequence upgrades to minimize risk.

### Classification Categories

| Category    | Description                | Priority             |
| ----------- | -------------------------- | -------------------- |
| Security    | CVE or known vulnerability | Critical             |
| Bug Fix     | Patch-level fixes          | High                 |
| Maintenance | Minor improvements, types  | Medium               |
| Major       | Breaking changes           | Low (needs research) |

### CLI Commands: npm

```powershell
# List outdated packages
npm outdated

# Detailed package info
npm info <package> version
npm info <package> peerDependencies

# Check for vulnerabilities
npm audit

# View dependency tree
npm ls <package>

# Check what would be installed
npm install <package>@<version> --dry-run
```

### CLI Commands: dotnet

```powershell
# List outdated packages
dotnet list package --outdated

# Include transitive dependencies
dotnet list package --outdated --include-transitive

# Check for vulnerable packages
dotnet list package --vulnerable

# View all packages
dotnet list package
```

### Constraint Checklist

Before planning upgrades, identify:

- [ ] Lockfile state (`package-lock.json`, `packages.lock.json`)
- [ ] Workspace/monorepo structure
- [ ] Engine requirements (`node` version, `.NET` version)
- [ ] Peer dependency requirements
- [ ] CI/CD compatibility requirements

### Prioritization Strategy

```
Order upgrades by:
1. Security patches (any version) → immediate
2. Patch updates (x.x.PATCH) → low risk, batch together
3. Minor updates (x.MINOR.x) → may have new features
4. Major updates (MAJOR.x.x) → requires research first

Sequence to minimize blast radius:
- Leaf dependencies first (no dependents)
- Shared dependencies last (many dependents)
- Group related packages (e.g., @typescript-eslint/*)
```

### Inventory Output Template

```markdown
## Dependency Inventory - {date}

### Security (Critical)

| Package | Current | Target  | CVE/Advisory   |
| ------- | ------- | ------- | -------------- |
| lodash  | 4.17.15 | 4.17.21 | CVE-2021-23337 |

### Patch Updates (Low Risk)

| Package | Current | Target | Notes |
| ------- | ------- | ------ | ----- |

### Minor Updates (Medium Risk)

| Package | Current | Target | Notes |
| ------- | ------- | ------ | ----- |

### Major Updates (Needs Research)

| Package | Current | Target | Breaking Changes? |
| ------- | ------- | ------ | ----------------- |

### Constraints

- Node engine: >=18.0.0
- Peer dependencies: React 18.x required by @mui/\*
- Lockfile: package-lock.json v3
```

---

## Phase 2: Research & Risk

### Goal

Research each non-trivial upgrade to identify breaking changes, migration steps, and required code modifications.

### Research Sources

1. **Official changelog/release notes** (GitHub releases, CHANGELOG.md)
2. **Migration guides** (official docs)
3. **Context7 docs** (`mcp_docs-context7_get-library-docs`)
4. **npm/NuGet package page** (release history)
5. **GitHub issues** (known problems with version)

### Breaking Change Categories

| Type             | Impact   | Example                                     |
| ---------------- | -------- | ------------------------------------------- |
| API Removal      | High     | `deprecated function removed`               |
| Signature Change | High     | `function now requires additional param`    |
| Default Change   | Medium   | `default timeout changed from 30s to 5s`    |
| Type Change      | Medium   | `return type changed from string to object` |
| Behavior Change  | Medium   | `validation now stricter`                   |
| Peer Requirement | Low-High | `now requires React 18+`                    |

### Research Checklist Per Package

- [ ] Read release notes for all versions between current and target
- [ ] Check for migration guide
- [ ] Search for breaking changes in changelog
- [ ] Verify peer dependency compatibility
- [ ] Check GitHub issues for upgrade-related bugs
- [ ] Note any deprecation warnings

### Codebase Impact Analysis

Find usages of affected APIs:

```powershell
# Search for package imports/usage
grep -r "from 'package-name'" --include="*.ts" --include="*.tsx"
grep -r "require('package-name')" --include="*.js"

# For specific API
grep -r "specificFunction\|specificMethod" --include="*.ts"
```

### Risk Assessment Template

```markdown
## Risk Assessment: {package} {current} → {target}

### Breaking Changes

1. `oldFunction()` removed → use `newFunction()` instead
2. Config property `timeout` renamed to `requestTimeout`

### Required Code Changes

- [ ] `src/api/client.ts`: Update function call
- [ ] `src/config.ts`: Rename config property

### Peer Dependencies

- Requires: typescript >=4.7 (current: 4.9 ✓)

### Known Issues

- Issue #1234: Memory leak in v3.0.0, fixed in v3.0.1

### Risk Level: Medium

Reason: Two API changes, well-documented migration path
```

---

## Phase 3: Implement

### Goal

Execute upgrades incrementally, apply required code changes, and maintain lockfile consistency.

### Implementation Principles

1. **One logical change per commit** — group related packages
2. **Keep lockfiles in sync** — always commit lockfile with manifest
3. **Apply code changes with upgrade** — don't leave broken intermediate states
4. **Smallest verifiable steps** — easier to bisect if issues arise

### CLI Commands: npm

```powershell
# Install specific version
npm install <package>@<version>

# Install multiple packages
npm install <pkg1>@<ver1> <pkg2>@<ver2>

# Update within semver range
npm update <package>

# Install and save as dev dependency
npm install -D <package>@<version>

# Clean install from lockfile
npm ci

# Dedupe dependencies
npm dedupe
```

### CLI Commands: dotnet

```powershell
# Add/update package
dotnet add package <package> --version <version>

# Update to latest
dotnet add package <package>

# Restore packages
dotnet restore

# Clean and rebuild
dotnet clean
dotnet build
```

### Upgrade Execution Order

```
FOR each upgrade group (security → patch → minor → major):
    1. Create checkpoint (git stash or commit)
    2. Update package manifest(s)
    3. Update lockfile (npm install / dotnet restore)
    4. Apply required code changes
    5. Run quick validation (build + unit tests)
    6. Commit if passing, rollback if failing
```

### Handling Peer Dependency Conflicts

```powershell
# View peer dependency requirements
npm info <package> peerDependencies

# Install with legacy peer deps (npm 7+)
npm install <package>@<version> --legacy-peer-deps

# Force resolution (use carefully)
npm install <package>@<version> --force
```

### Commit Message Format

```
chore(deps): upgrade <package> from <old> to <new>

- <reason for upgrade: security fix / new feature / maintenance>
- <breaking changes addressed, if any>
- <code changes made, if any>
```

---

## Phase 4: Validation

### Goal

Verify all upgrades work correctly through comprehensive testing, linting, building, and security scanning.

### Validation Checklist

- [ ] **Unit tests pass**: `npm test` / `dotnet test`
- [ ] **Integration tests pass**: Full test suite
- [ ] **Build succeeds**: `npm run build` / `dotnet build`
- [ ] **Type checking passes**: `npx tsc --noEmit`
- [ ] **Linting passes**: `npm run lint`
- [ ] **No new vulnerabilities**: `npm audit` / `dotnet list package --vulnerable`
- [ ] **App starts successfully**: Manual smoke test
- [ ] **No new IDE errors**: Check `#problems` panel

### CLI Commands: npm

```powershell
# Run tests
npm test
npm run test:unit
npm run test:integration

# Type checking (TypeScript)
npx tsc --noEmit

# Linting
npm run lint
npx eslint . --ext .ts,.tsx

# Build
npm run build

# Security audit
npm audit
npm audit fix  # Auto-fix if safe

# Start application
npm start
npm run dev
```

### CLI Commands: dotnet

```powershell
# Run tests
dotnet test
dotnet test --verbosity normal

# Build
dotnet build
dotnet build --no-restore

# Format check
dotnet format --verify-no-changes

# Vulnerability scan
dotnet list package --vulnerable

# Run application
dotnet run
```

### Failure Investigation

When tests fail after upgrade:

1. **Identify scope**: Which tests fail? Related to upgraded package?
2. **Check test assumptions**: Does test rely on old behavior?
3. **Review breaking changes**: Did we miss a required code change?
4. **Isolate the upgrade**: Rollback and upgrade packages one at a time
5. **Search for known issues**: Check GitHub issues for the package

### Validation Report Template

```markdown
## Validation Report - {date}

### Test Results

- Unit Tests: ✓ 342 passed, 0 failed
- Integration Tests: ✓ 28 passed, 0 failed
- E2E Tests: ✓ 12 passed, 0 failed

### Static Analysis

- TypeScript: ✓ No errors
- ESLint: ✓ No errors
- Build: ✓ Success

### Security

- npm audit: ✓ 0 vulnerabilities
- Snyk: ✓ No new issues

### Manual Verification

- App starts: ✓
- Key flows tested: ✓

### Issues Found

None

### Status: PASS
```

---

## Story Points / Complexity Guidelines

Estimate upgrade effort based on scope and risk:

| Complexity | Points | Criteria                                          |
| ---------- | ------ | ------------------------------------------------- |
| Trivial    | 1      | Patch updates only, no breaking changes           |
| Small      | 2      | Minor updates, minimal code changes               |
| Medium     | 3      | Mix of minor/major, some code changes needed      |
| Large      | 5      | Multiple major upgrades, significant code changes |
| XL         | 8+     | Framework upgrade, extensive migration required   |

### Complexity Factors

Add points for:

- +1: More than 10 packages to update
- +1: Major version upgrade
- +2: Framework/runtime upgrade (React, .NET version)
- +1: Monorepo with multiple packages
- +1: Limited test coverage
- +2: Known breaking changes requiring migration

---

## Security Considerations

### CVE Response Priority

| Severity | Response Time | Action                                  |
| -------- | ------------- | --------------------------------------- |
| Critical | Immediate     | Hotfix, bypass normal process if needed |
| High     | Same day      | Prioritize over feature work            |
| Medium   | Within sprint | Schedule in current iteration           |
| Low      | Backlog       | Track and batch with other updates      |

### Security Audit Commands

```powershell
# npm
npm audit
npm audit --json  # Machine-readable output
npm audit fix     # Auto-fix compatible updates
npm audit fix --force  # Force fix (may have breaking changes)

# dotnet
dotnet list package --vulnerable
dotnet list package --vulnerable --include-transitive
```

### Before Upgrading Security Packages

1. **Verify the vulnerability applies** — check if your usage is affected
2. **Check for patches** — sometimes a patch is available without major upgrade
3. **Review upgrade path** — ensure no breaking changes or have migration plan
4. **Test thoroughly** — security packages often have broad impact

---

## Breaking Change Handling

### Common Migration Patterns

| Pattern             | Before                      | After                            |
| ------------------- | --------------------------- | -------------------------------- |
| Renamed export      | `import { old } from 'pkg'` | `import { new } from 'pkg'`      |
| Moved to subpath    | `import x from 'pkg'`       | `import x from 'pkg/subpath'`    |
| Config restructure  | `{ option: value }`         | `{ options: { option: value } }` |
| Callback to Promise | `fn(callback)`              | `await fn()`                     |
| Class to function   | `new Client()`              | `createClient()`                 |

### Migration Automation

```powershell
# Use codemods if available
npx @package/codemod migrate-v2

# Search and replace with sed/ripgrep
rg "oldFunction" --files-with-matches | xargs sed -i 's/oldFunction/newFunction/g'
```

### When to Defer Major Upgrades

- Current version still receives security patches
- Migration guide is incomplete or unclear
- Critical deadline approaching
- Insufficient test coverage for affected areas

Document deferred upgrades:

```markdown
## Deferred: {package} {current} → {target}

**Reason**: Migration requires 2+ days, not critical
**Security**: Current version patched through {date}
**Revisit**: Next quarter or when {condition}
```

---

## File-Based Handoff

For complex upgrades, create handoff documents:

```
docs/upgrades/
├── {date}-inventory.md      # Phase 1 output
├── {package}-migration.md   # Phase 2 research
├── {date}-validation.md     # Phase 4 report
└── README.md                # Upgrade history index
```

### Handoff Document Usage

1. **Inventory Analyst** → writes `{date}-inventory.md`
2. **Breaking Change Researcher** → reads inventory, writes `{package}-migration.md`
3. **Upgrade Implementer** → reads both, executes upgrades
4. **Validation Specialist** → writes `{date}-validation.md`

---

## Quick Reference

| Task                     | npm                     | dotnet                                   |
| ------------------------ | ----------------------- | ---------------------------------------- |
| List outdated            | `npm outdated`          | `dotnet list package --outdated`         |
| Install specific version | `npm install pkg@1.2.3` | `dotnet add package pkg --version 1.2.3` |
| Security audit           | `npm audit`             | `dotnet list package --vulnerable`       |
| Run tests                | `npm test`              | `dotnet test`                            |
| Type check               | `npx tsc --noEmit`      | `dotnet build`                           |
| Lint                     | `npm run lint`          | `dotnet format --verify-no-changes`      |
| Build                    | `npm run build`         | `dotnet build`                           |
| View dependency tree     | `npm ls pkg`            | `dotnet list package`                    |
| Clean install            | `npm ci`                | `dotnet restore`                         |

---

## Error Handling

### "Peer dependency conflict"

1. Check which package requires the conflicting version
2. Verify if newer version of the requiring package exists
3. Use `--legacy-peer-deps` as temporary workaround
4. Consider upgrading the requiring package first

### "Cannot find module after upgrade"

1. Clear node_modules: `rm -rf node_modules && npm install`
2. Clear build cache: `npm run clean` or delete `dist/`
3. Restart TypeScript server in VS Code
4. Check if import path changed in new version

### "Type errors after upgrade"

1. Check if `@types/` package needs separate update
2. Review breaking type changes in changelog
3. May need to update TypeScript version
4. Check for new generic parameters or stricter types

### "Tests fail after upgrade"

1. Check if test relies on mocked old behavior
2. Review if assertions match new return types
3. Check for timing changes (async behavior)
4. Review snapshot updates needed

---

## Boundaries

- ✅ **Always**: Run full validation after upgrades
- ✅ **Always**: Keep lockfiles in sync with manifests
- ✅ **Always**: Research breaking changes before major upgrades
- ⚠️ **Ask first**: Major version upgrades
- ⚠️ **Ask first**: Upgrades with known breaking changes
- ⚠️ **Ask first**: Security patches that require major upgrades
- 🚫 **Never**: Skip validation or ignore test failures
- 🚫 **Never**: Upgrade without checking peer dependencies
- 🚫 **Never**: Force-push lockfile changes without review
