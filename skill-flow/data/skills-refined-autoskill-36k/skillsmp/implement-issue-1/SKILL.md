---
name: implement-issue
description: >
  TDD development workflow for woo-attribution-bridge. This skill should be used when implementing
  GitHub issues. It guides through: fetching the issue, creating a feature branch, writing an
  implementation plan, creating a spec, validating the spec format, writing failing tests first (TDD),
  implementing the feature, and creating a PR. Invoke with `/implement-issue <issue-number>`.
---

# Implement Issue - TDD Workflow

## Overview

This skill implements a Test-Driven Development workflow for the woo-attribution-bridge project.
It ensures consistent, high-quality implementations by following a structured process from
issue to merged PR.

## Workflow Steps

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  1. Fetch    │──▶│  2. Branch   │──▶│  3. Plan     │──▶│  4. Spec     │
│    Issue     │   │   Creation   │   │   Creation   │   │   Creation   │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
                                                                │
                                                                ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  8. Create   │◀──│  7. Implement│◀──│  6. Write    │◀──│  5. Validate │
│    PR        │   │    Feature   │   │    Tests     │   │    Spec      │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

---

## Step 1: Fetch Issue

Retrieve the GitHub issue details using the `gh` CLI.

```bash
gh issue view <issue-number> --json title,body,labels,assignees,milestone
```

Extract from the issue:
- **Title**: Becomes the basis for branch name and spec title
- **Body**: Contains requirements, acceptance criteria, context
- **Labels**: Indicates priority, type (bug/feature/enhancement)
- **Milestone**: Target version if specified

### Issue Analysis Checklist

- [ ] Understand the problem being solved
- [ ] Identify acceptance criteria
- [ ] Note any technical constraints mentioned
- [ ] Check for related issues or dependencies
- [ ] Determine if this is PHP (plugin) or TypeScript (dashboard) work

---

## Step 2: Create Feature Branch

Branch naming convention:
```
feature/issue-{number}-{short-slug}
```

Examples:
- `feature/issue-5-cookie-consent`
- `feature/issue-6-browser-fingerprint`
- `feature/issue-7-server-tracking`

```bash
# Ensure on develop branch with latest changes
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/issue-{number}-{slug}
```

---

## Step 3: Create Implementation Plan

Write a plan file at `.claude/plans/{descriptive-name}.md` that includes:

1. **Problem Statement**: What the issue is solving
2. **Proposed Solution**: High-level approach
3. **Technical Decisions**: Key choices with rationale
4. **File Changes**: List of files to create/modify
5. **Testing Strategy**: How to verify the implementation
6. **Rollout Considerations**: Any deployment notes

### Plan Template

```markdown
# Plan: {Issue Title}

## Problem Statement
{What problem does this solve?}

## Proposed Solution
{High-level approach}

## Technical Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| {What} | {Choice} | {Why} |

## File Changes
| File | Action | Purpose |
|------|--------|---------|
| {path} | Create/Modify | {why} |

## Testing Strategy
- Unit tests: {approach}
- Integration tests: {approach}

## Rollout
- {Any deployment considerations}
```

Ask the user for approval before proceeding to spec creation.

---

## Step 4: Create Spec

Create a specification document following the project template at `docs/specs/SPEC_TEMPLATE.md`.

### Spec Naming Convention

```
docs/specs/SPEC-{XXX}-{module-name}.md
```

Where `{XXX}` is a zero-padded number. Check existing specs to determine the next number:

```bash
ls docs/specs/SPEC-*.md | tail -1
```

### Required Sections

Every spec MUST include these 9 sections:

1. **Overview** (Purpose, Scope, Dependencies)
2. **Requirements** (Functional + Non-Functional tables)
3. **Technical Design** (Architecture, Data Structures, DB Schema, APIs)
4. **Public Interface** (Methods, Events/Hooks, Config Options)
5. **Error Handling** (Error Codes, Logging)
6. **Security Considerations**
7. **Testing Requirements** (Unit Tests, Integration Tests, Coverage Target)
8. **Implementation Notes** (File Locations, Migration Steps, Limitations)
9. **Changelog**

---

## Step 5: Validate Spec Format

Before proceeding, validate the spec follows the required format.

Run the validation script:
```bash
python3 .claude/commands/implement-issue/scripts/validate_spec.py docs/specs/SPEC-XXX-name.md
```

### Validation Checks

The validator ensures:
- [ ] All 9 required sections present
- [ ] SPEC-ID format correct (SPEC-XXX)
- [ ] Status field present and valid
- [ ] Requirements tables have proper format
- [ ] Testing section has coverage target
- [ ] File locations specified

Fix any validation errors before proceeding.

---

## Step 6: Write Tests First (TDD)

**Critical**: Write tests BEFORE implementing the feature. Tests should fail initially.

### PHP Tests (WordPress Plugin)

Location: `tests/Unit/` or `tests/Integration/`

```bash
# Run tests to see them fail
composer test:unit
```

Test file naming:
```
tests/Unit/{ModuleName}Test.php
tests/Unit/Integrations/{IntegrationName}Test.php
```

### TypeScript Tests (Dashboard)

Location: `dashboard/tests/`

```bash
# Run tests to see them fail
cd dashboard && npm test
```

### TDD Cycle

1. **Red**: Write a failing test
2. **Green**: Write minimum code to pass
3. **Refactor**: Clean up while keeping tests green

### Test Coverage Target

- **Minimum**: 80% code coverage
- **Verify**: `composer test:coverage` or `npm run test:coverage`

---

## Step 7: Implement Feature

Now implement the feature to make the tests pass.

### PHP Implementation Guidelines

- Follow WordPress coding standards
- Use proper sanitization/escaping
- Add PHPDoc blocks for all public methods
- Handle errors gracefully with try/catch

### TypeScript Implementation Guidelines

- Follow existing patterns in the codebase
- Use proper TypeScript types (no `any`)
- Handle loading/error states in UI components
- Use React Query for data fetching

### Implementation Checklist

- [ ] All tests passing
- [ ] No TypeScript/PHP errors
- [ ] Code follows project patterns
- [ ] Security considerations addressed
- [ ] Error handling complete

---

## Step 8: Create PR

After implementation is complete and all tests pass:

### Pre-PR Checklist

```bash
# PHP: Run linting and tests
composer lint
composer test

# Dashboard: Run linting and tests
cd dashboard && npm run lint && npm test

# Build check
cd dashboard && npm run build
```

### Create the PR

```bash
gh pr create \
  --title "feat(scope): Short description (#issue-number)" \
  --body "$(cat <<'EOF'
## Summary
- {Bullet point summary of changes}

## Related Issue
Closes #{issue-number}

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] Manual testing completed

## Screenshots (if UI changes)
{Add screenshots}
EOF
)"
```

### Commit Message Format

Use conventional commits:
```
feat(cookie-consent): Add CookieYes integration (#5)
fix(tracking): Handle missing click IDs gracefully (#7)
test(fingerprint): Add canvas fingerprint tests (#6)
```

---

## Project-Specific Context

### Directory Structure

```
woo-attribution-bridge/
├── src/                    # WordPress plugin (PHP)
│   ├── admin/             # Admin UI
│   ├── includes/          # Core classes
│   └── integrations/      # Platform integrations
├── dashboard/             # Next.js dashboard (TypeScript)
│   ├── src/app/          # App router pages
│   ├── src/components/   # React components
│   └── src/db/           # Database schema
├── tests/                 # PHP tests
│   ├── Unit/
│   └── Integration/
├── dashboard/tests/       # TypeScript tests
└── docs/specs/           # Specifications
```

### Test Frameworks

- **PHP**: PHPUnit 10.x with WooCommerce mocks
- **TypeScript**: Vitest with React Testing Library

### Key Files to Reference

- `src/includes/class-wab-loader.php` - Hook registration
- `src/includes/class-wab-cookie.php` - Cookie handling
- `dashboard/src/db/schema.ts` - Database schema
- `dashboard/src/lib/auth.ts` - Authentication

---

## Error Recovery

### If Tests Won't Pass

1. Check test output for specific failures
2. Verify mocks are set up correctly
3. Check for environment issues (missing dependencies)
4. Review spec requirements vs implementation

### If Validation Fails

1. Read validation error messages carefully
2. Compare spec against `docs/specs/SPEC_TEMPLATE.md`
3. Add missing sections
4. Fix formatting issues

### If Build Fails

1. Check TypeScript errors: `npm run type-check`
2. Check PHP errors: `composer lint`
3. Review recent changes for syntax issues

---

## Quick Reference

| Step | Command | Output |
|------|---------|--------|
| Fetch issue | `gh issue view N` | Issue details |
| Create branch | `git checkout -b feature/issue-N-slug` | New branch |
| Run PHP tests | `composer test:unit` | Test results |
| Run TS tests | `cd dashboard && npm test` | Test results |
| Validate spec | `python3 .claude/commands/implement-issue/scripts/validate_spec.py spec.md` | Validation report |
| Create PR | `gh pr create` | PR URL |
