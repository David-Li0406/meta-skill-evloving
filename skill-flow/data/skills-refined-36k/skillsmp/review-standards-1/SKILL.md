---
name: review-standards
description: "This skill should be used when reviewing code or running /uw:review. It contains 47 issue patterns with severity tiers, team standards to enforce, and implementation checklists for the Unit Work review system."
---

# Review Standards

This skill contains the review taxonomy, team standards, and implementation checklists used by the Unit Work review system.

## Contents

- [Issue Patterns](./references/issue-patterns.md) - 47 distinct patterns with detection criteria and fixes
- [Review Standards](./references/review-standards.md) - Language-agnostic best practices
- [Checklists](./references/checklists.md) - Before, during, and after implementation

## Severity Tiers

Issues are categorized into two tiers:

**Tier 1 - Correctness** (Always Higher Priority)
- Security vulnerabilities
- Architecture problems
- Implementation bugs
- Type safety violations
- Functionality gaps

**Tier 2 - Cleanliness** (Lower Priority)
- Naming clarity
- File organization
- Code duplication (when not causing bugs)
- Comment quality
- Import/style consistency

At the same P-level, Tier 1 issues should be addressed before Tier 2 issues.

## Top 5 Patterns by Frequency

1. **BETTER_IMPLEMENTATION_APPROACH** (18%) - Search first, leverage framework features
2. **TYPE_SAFETY_IMPROVEMENT** (12%) - No casting, complete type guards
3. **EXISTING_UTILITY_AVAILABLE** (10%) - Search codebase before implementing
4. **CODE_DUPLICATION** (8%) - Check for existing implementations
5. **NULL_HANDLING** (6%) - Use null, not empty strings

## Always P1 (Critical)

- Any injection vulnerability
- Authentication/authorization bypass
- XSS in user content
- Security boundary violations

## Zero-Tolerance Items

These should never appear in PRs:
- Type casting to access properties (`as SomeType`)
- Barrel files (index.ts re-exports)
- Debug code (console.log, print)
- Services that swallow errors
- Empty strings as null fallbacks

## Usage

When conducting code review, reference the detailed patterns in [issue-patterns.md](./references/issue-patterns.md) for detection criteria and fix guidance.

Before implementing features, run through the checklists in [checklists.md](./references/checklists.md).
