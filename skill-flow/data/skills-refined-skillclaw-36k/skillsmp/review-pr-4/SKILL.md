---
name: review-pr
description: Review a pull request for Playwright test automation using project standards. Use when user asks to review a PR, check a pull request, or mentions a PR number.
allowed-tools: Bash(gh:*), Bash(git:*), Read, Grep, Glob
---

# Pull Request Review

## Process

### 1. Gather PR Information
```bash
# Get PR metadata
gh pr view <number> --json title,body,state,additions,deletions,changedFiles,baseRefName,headRefName

# Get full diff
gh pr diff <number>
```

### 2. Read modified files for context
Use Read tool to view complete files mentioned in the diff.

### 3. Review Checklist (Production Focus)

#### Critical Issues (Block Merge)
- [ ] Build/compilation errors or type issues
- [ ] Test failures or broken fixtures
- [ ] Logic errors in test scenarios
- [ ] Data integrity issues (duplicate users, race conditions)

#### Test Design & Business Logic
- [ ] **Test covers actual user scenarios** - not just happy paths
- [ ] **Business logic is correct** - verifies the right behavior
- [ ] **Test scope is appropriate** - not too broad or too narrow
- [ ] **Edge cases considered** - what could go wrong?
- [ ] **Assertions validate meaningful outcomes** - not just presence of elements

#### Test Stability & Reliability
- [ ] **User-Facing Locators** - prefer `getByRole`/`getByText` over CSS/XPath
- [ ] **Selectors are resilient** - won't break on UI changes (use role, text, semantic HTML where possible)
- [ ] **No race conditions** - proper waits for async operations
- [ ] **No hard-coded waits** - `page.waitForTimeout()` is a red flag
- [ ] **Parallel execution safe** - no shared state or dependencies
- [ ] **Data isolation** - each test has unique data, no conflicts
- [ ] **Flaky patterns avoided** - timing-dependent assertions, external dependencies
- [ ] **Idempotent for retries** - test can rerun without manual cleanup
- [ ] **Proper cleanup on failure** - no partial state left behind

#### Test Independence & Isolation
- [ ] **Tests can run in any order** - no implicit dependencies between tests
- [ ] **No shared mutable state** - each test creates its own data
- [ ] **Statelessness** - no global variable modification
- [ ] **Fixture Scoping** - use fixtures for setup/teardown (auth, seeding)
- [ ] **Proper setup/teardown** - beforeEach/afterEach used correctly
- [ ] **No test pollution** - one test's failure doesn't cascade

#### Test Data Strategy
- [ ] **Data creation strategy** - prefer Factories over hardcoded JSON
- [ ] **Unique data per test/worker** - no conflicts in parallel
- [ ] **Cleanup strategy defined** - how is test data removed?
- [ ] **No hardcoded magic values** - data is meaningful and traceable

#### Code Quality & Architecture

**File & Folder Organization:**

*Consistent structure makes the codebase navigable and predictable.*

File naming conventions:
- [ ] **kebab-case for all files** - `checkout.page.ts`, not `CheckoutPage.ts` or `checkout_page.ts`
- [ ] **Suffix indicates purpose:**
  - `.page.ts` - page objects (`cart.page.ts`, `payment.page.ts`)
  - `.component.ts` - reusable UI components (`header.component.ts`, `order-table.component.ts`)
  - `.types.ts` - type definitions (`cart.types.ts`, `product.types.ts`)
  - `.spec.ts` - test files (`complete-order.spec.ts`)
  - `.fixture.ts` - test fixtures
  - `.factory.ts` - data factories (`person.factory.ts`)
- [ ] **No suffix for utilities** - `table.ts`, `convert-data.ts` (pure functions)

Folder structure:
- [ ] **Pages grouped by feature/domain:**
  ```
  src/ui/pages/
  ├── cart/           # cart.page.ts, checkout.page.ts, payment.page.ts
  ├── product/        # product.page.ts, products.page.ts
  ├── auth/           # login.page.ts, signup.page.ts
  └── components/     # Shared components (header, modals, tables)
  ```
- [ ] **Tests mirror source structure:**
  ```
  tests/ui/
  ├── e2e/            # End-to-end flows (complete-order.spec.ts)
  ├── cart/           # Cart-specific tests
  └── product/        # Product-specific tests
  ```
- [ ] **Shared code in dedicated folders:**
  - `src/ui/types/` - shared TypeScript types
  - `src/ui/test-data/constants/` - test data constants
  - `src/utils/` - utility functions

Red flags to catch:
- File without proper suffix (e.g., `Checkout.ts` instead of `checkout.page.ts`)
- Page object in wrong folder (e.g., cart page in `product/` folder)
- Component that should be in `components/` but is nested in a page folder
- Test file not following `.spec.ts` convention
- Mixed concerns in one folder (pages + utils + types together)
- Explicit `Promise<void>`, `Promise<primitive>`, or `Promise<SimpleObject>` return types (TS inference is preferred)

**Naming Conventions:**
- [ ] **Variables/methods follow conventions** - camelCase, descriptive, no abbreviations
- [ ] **File names are consistent** - kebab-case, clear purpose
- [ ] **Declarative Naming** - follow `should [outcome] when [scenario]` pattern
- [ ] **Constants are UPPER_CASE** - configuration values, magic numbers extracted

**Over-Engineering:**
- [ ] **No premature abstraction** - don't create utilities for single use
- [ ] **Avoid Hasty Abstractions (AHA)** - avoid complex helpers handling many cases
- [ ] **No unnecessary complexity** - KISS principle, straightforward solutions
- [ ] **No over-generic methods** - specific is better than flexible
- [ ] **No unused code** - dead code removed, imports cleaned up

**Method Optimization:**
- [ ] **Methods do one thing** - single responsibility
- [ ] **No duplicate logic** - DRY principle applied where it makes sense
- [ ] **Proper return types** - TypeScript types are useful (but avoid redundancy like `Promise<void>`)
- [ ] **Strict Type Safety** - NO 'any' type, use generics/unknown
- [ ] **Let TypeScript infer Promise types** - Avoid explicit `Promise<void>` or types for primitives/simple objects. Only use explicit types for complex interfaces or when inference fails.
- [ ] **Async/await used correctly** - no unnecessary awaits, proper error handling

**Code Style:**
- [ ] **No redundant assignments** - don't assign parameter to new variable of same type (e.g., `const userData = user` when `user` is already typed)
- [ ] **No unnecessary intermediate variables** - use parameters directly when no transformation needed
- [ ] **Consistent access modifiers** - follow base class patterns (e.g., `protected` for `uniqueElement` if BasePage uses `protected`)
- [ ] **No shadowing** - avoid variable names that shadow outer scope variables
- [ ] **No duplicated assertion blocks** - extract repeated assertions into private helper methods (e.g., same assertions for delivery/invoice address → `assertAddressBlock(locator, data)`)
- [ ] **Use template literals** - prefer `` `${a} ${b}` `` over `a + ' ' + b` for string concatenation

**Types & Constants Organization:**

*This is a tricky area with multiple valid approaches. Flag for discussion when patterns are inconsistent.*

Where types should live:
- [ ] **Shared types in `src/ui/types/`** - types used across multiple pages (e.g., `CartItem` used in cart.page.ts AND checkout.page.ts → extract to `types/cart.types.ts`)
- [ ] **No duplicate type definitions** - same type defined in multiple files is a red flag; search for duplicates
- [ ] **Page-specific types can stay in page files** - if a type is ONLY used in one page, it can stay there
- [ ] **Derived types stay with constants** - when type uses `typeof CONSTANT` (e.g., `type CreditCard = typeof CREDIT_CARDS[keyof typeof CREDIT_CARDS]`), keep them together in constants file - this is OK
- [ ] **Utility Types used** - `Pick`, `Omit`, `Partial` for leaner types
- [ ] **Interface Segregation** - functions take only needed data (e.g. `id` not `User` obj)
- [ ] **No Enums** - prefer `as const` string unions

Constants organization:
- [ ] **Module Boundaries** - no circular refs or reaching into private folders
- [ ] **Constants in `test-data/constants/`** - test data like credit cards, URLs, timeouts
- [ ] **Constants file = one domain** - `credit-card.ts` for cards, `urls.ts` for URLs, don't mix domains
- [ ] **UPPER_CASE for constants** - `CREDIT_CARDS` not `creditCards`
- [ ] **`as const` for literal types** - enables type inference from values

Recommended structure:
```
src/ui/
├── types/                      # Shared types
│   ├── cart.types.ts           # CartItem, OrderItem
│   ├── user.types.ts           # Person, Address
│   └── index.ts                # Re-exports
├── test-data/
│   └── constants/              # Test data with derived types
│       ├── credit-card.ts      # CREDIT_CARDS + CreditCard type (OK together)
│       └── timeouts.ts         # TIMEOUTS
└── pages/
    └── cart/
        └── cart.page.ts        # Imports from types/, no local CartItem
```

Red flags to catch:
- Same interface/type defined in 2+ files → extract to shared types
- Type in page file that's imported by another page → move to types/
- Constants scattered across page files → consolidate to constants/
- Mixing unrelated constants in one file → split by domain

**Config Organization:**
- [ ] **Environment configs are clean** - no hardcoded URLs/credentials in code
- [ ] **Config structure makes sense** - easy to find and modify settings
- [ ] **Secrets are not committed** - .env files in .gitignore
- [ ] **Config is typed** - TypeScript interfaces for config objects

**Utils & Helpers:**
- [ ] **Utils are truly reusable** - used in multiple places, not premature
- [ ] **Utils have clear purpose** - not a dumping ground
- [ ] **Utils are well-documented** - JSDoc or clear naming
- [ ] **Utils are testable** - pure functions when possible

**Reporting & Debugging:**
- [ ] **`@step()` usage is meaningful** - steps tell a story in reports
- [ ] **Error messages are actionable** - include context, expected vs actual
- [ ] **Console logs are removed** - no debug statements left behind
- [ ] **Screenshots/videos will be useful** - failures capture enough context

#### Page Object Quality
- [ ] **Single Responsibility (SRP)** - elements & interactions only, NO assertions
- [ ] **Encapsulation** - private/protected locators, public action methods
- [ ] **Action-Oriented Methods** - `submitForm` not `clickSubmit`
- [ ] **Dependency Inversion** - injected via Fixtures (no `new Page(page)`)
- [ ] **Component Composition** - use shared components (e.g. Header)
- [ ] **Abstractions make sense** - methods represent user actions
- [ ] **Not over-engineered** - simple, clear, maintainable
- [ ] **Proper error handling** - failures are debuggable with clear messages

#### CI/CD & Pipeline Considerations
- [ ] **Timeouts are reasonable** - won't fail in slow CI environments
- [ ] **Resource efficient** - not creating unnecessary browser contexts
- [ ] **Environment agnostic** - works in CI without local dependencies
- [ ] **Retry-friendly** - tests work with Playwright's retry mechanism
- [ ] **Parallelization ready** - consider worker count and resource limits

#### Test Maintainability (6-month test)
- [ ] **Easy to update** - when requirements change, is this easy to modify?
- [ ] **Tests behavior, not implementation** - UI changes shouldn't break logic tests
- [ ] **New team member readable** - can someone understand this without context?
- [ ] **Change impact is limited** - page object change doesn't break 50 tests

#### Assertion Strategy
- [ ] **Asserting the right things** - meaningful business outcomes
- [ ] **Not over-asserting** - too many assertions = brittle tests
- [ ] **Not under-asserting** - weak tests that pass when they shouldn't
- [ ] **Soft vs hard assertions used correctly** - collect multiple failures vs fail fast

#### Security in Tests
- [ ] **No credentials in code** - use environment variables
- [ ] **Sensitive data not in screenshots** - mask or avoid capturing
- [ ] **API keys/tokens managed properly** - not committed, rotatable
- [ ] **Test users are isolated** - not using production accounts

#### Regression Risk Assessment
- [ ] **Shared fixture changes reviewed** - could break other tests
- [ ] **Page object modifications** - check downstream impact
- [ ] **Config changes** - verify no unintended side effects
- [ ] **New dependencies introduced** - npm packages reviewed

#### Git Hygiene
- [ ] **Commit messages are clear** - explain WHY, not just WHAT
- [ ] **PR title is descriptive** - explains the feature/fix clearly
- [ ] **Commits are logical** - each commit is a coherent unit of work
- [ ] **No "WIP", "test", "fix" commit messages** - be professional

### 4. Output Format

**Review Style - Senior AQA Mindset:**
- Direct, concise, production-focused
- **CRITICAL: Re-read ALL changed files before posting** - don't review stale code
- Only show sections with issues - skip sections that are fine
- At the end, list areas that are good in one line: "✅ Good: [area1], [area2], [area3]"
- For commits with issues, provide specific rewrite suggestions
- Think long-term: "Will this be maintainable in 6 months?"
- Challenge decisions: "Why this approach? Is it necessary?"
- Consider CI/CD: "Will this work reliably in pipeline?"
- Assess risk: "What could this break? What's not covered?"
- **DO NOT include "Test Coverage Analysis" section** - this will be handled by a separate agent

**Patterns to flag for extra review (not issues, just note them):**
- Public locators used for assertion flexibility
- Generic assertion helpers (e.g., `assertElementVisible(locator)`)
- Trade-offs between encapsulation and pragmatism
- Type defined in page file that might be shared later - ask: "Will other pages need this?"
- Constants with derived types - verify `as const` is used for type inference
- Helper methods that could be private but are public - intentional or oversight?
- New folder created - does it fit the existing structure? Is it the right location?
- File without standard suffix - intentional (utility) or missing convention?

```markdown
## PR Review: [Title] (#[Number])

**Changes**: +X / -Y across Z files

---

[ONLY INCLUDE SECTIONS WITH ISSUES - SKIP SECTIONS THAT ARE FINE]

### 🔴 Blockers
Critical issues that must be fixed.

### ⚠️ Issues
| File:Line | Issue | Suggestion |
|-----------|-------|------------|
| `file.ts:42` | Description | How to fix |

### 👀 For Your Review
Design decisions that may be intentional - verify they fit your context:
- [pattern] at `file.ts:line` - [brief description]

### 💡 Discussion Points
Areas with multiple valid approaches - worth a team decision:
- [topic] - Option A: [approach]. Option B: [approach]. Recommendation: [suggestion]

*Common discussion topics: type location (page vs shared), helper extraction timing, assertion granularity*

### 📝 Git Hygiene
**PR title:** `Current` → `Suggested improvement`

**Commits to improve:**
| Current | Suggested |
|---------|-----------|
| `bad commit msg` | `feat: clear description of change` |

---

✅ **Good:** [list areas with no issues, e.g., "test isolation, factory patterns, step decorator usage"]

**Verdict:** Approved / Changes requested

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### 5. Automatically Post Review
After generating the review, ALWAYS post it as a comment on the PR:
```bash
gh pr review <number> --comment --body "$(cat <<'EOF'
[review content]
EOF
)"
```

**Important:** Do not ask the user if they want to post - automatically post the review after completing the analysis.

## Reference
See `.claude/testing-principles.md` for detailed testing standards.