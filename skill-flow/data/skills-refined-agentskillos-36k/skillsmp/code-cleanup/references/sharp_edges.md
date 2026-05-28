# Code Cleanup - Sharp Edges

## Cleanup Without Tests

### **Id**
cleanup-without-tests
### **Summary**
Refactoring code without test coverage to verify behavior
### **Severity**
critical
### **Situation**
  You see messy code and want to clean it up. The code has no tests,
  or the tests don't cover the code paths you're changing.
  
### **Why**
  Without tests, you cannot verify that cleanup didn't change behavior.
  "I'm just moving code around" is how subtle bugs are introduced.
  
  The code you're cleaning might have accidental behavior that other
  code depends on. Breaking it breaks production.
  
### **Solution**
  Before any cleanup:
  1. Add tests for current behavior (characterization tests)
  2. Run tests to verify they pass
  3. Make cleanup changes
  4. Run tests to verify they still pass
  
  If you can't add tests:
  - Make tiny incremental changes
  - Deploy after each tiny change
  - Monitor for errors
  - Keep a revert ready
  
### **Symptoms**
  - I'll just quickly reorganize this
  - It's obvious what this does
  - I'm not changing any logic
  - Cleanup PR with no test changes
### **Detection Pattern**
refactor|cleanup|reorganize

## Delete Seemingly Unused Code

### **Id**
delete-seemingly-unused-code
### **Summary**
Deleting code that appears unused but is called dynamically
### **Severity**
critical
### **Situation**
  You find a function or module with no static imports. Your IDE says
  it's unused. You delete it.
  
### **Why**
  Code can be referenced dynamically:
  - String-based imports: require(`./handlers/${type}`)
  - Reflection: obj[methodName]()
  - Event handlers registered by name
  - Plugin systems
  - Worker message handlers
  - Route handlers matched by pattern
  
  Deleting breaks runtime, not compile time.
  
### **Solution**
  Before deleting "unused" code:
  1. Search for the function/file NAME as a string
  2. Check for dynamic imports: require(), import()
  3. Look for string interpolation in imports
  4. Check event handlers and message listeners
  5. Review git history: why was this added?
  6. Deprecate first, delete after observation period
  
  # Search patterns
  grep -r "functionName" --include="*.ts"
  grep -r "'functionName'" --include="*.ts"
  grep -r "require(" --include="*.ts"
  
### **Symptoms**
  - IDE "unused" warning
  - No direct imports
  - Works locally, breaks in production
  - Error: Cannot find module X
### **Detection Pattern**
dynamic.*import|require\(.*\$|\\[\\w+\\]\\(

## Mass Rename Without Migration

### **Id**
mass-rename-without-migration
### **Summary**
Renaming a widely-used function/type across the codebase at once
### **Severity**
critical
### **Situation**
  You want to rename "getUserData" to "fetchUser" and do a find-replace
  across all 50 files that use it.
  
### **Why**
  Mass renames are high-risk:
  - Hard to review (diff is huge)
  - Easy to miss string references
  - Breaks other people's in-progress work
  - If anything goes wrong, entire codebase affected
  - Can't bisect to find issues later
  
### **Solution**
  Rename incrementally:
  1. Add new name alongside old
     export function fetchUser() { ... }
     export const getUserData = fetchUser; // Deprecated
  2. Migrate callers incrementally (5-10 files per PR)
  3. After all callers migrated, mark old name deprecated
  4. Remove old name in final PR
  
  Or for TypeScript:
  1. Use IDE rename refactor (tracks all references)
  2. Run full type check
  3. Run full test suite
  4. Keep PR focused on just the rename
  
### **Symptoms**
  - 50+ file changes in one PR
  - Merge conflicts everywhere
  - Just a rename, shouldn't break anything
  - Runtime errors after deploy
### **Detection Pattern**
deprecated|alias|backward.*compat

## Cleanup In Feature Commits

### **Id**
cleanup-in-feature-commits
### **Summary**
Mixing cleanup changes with feature work in same commit
### **Severity**
high
### **Situation**
  While adding a feature, you notice messy code nearby and clean it up.
  You commit both changes together.
  
### **Why**
  Mixed commits cause:
  - Hard to review (what's functional vs cosmetic?)
  - Risky to revert (can't undo feature without cleanup)
  - Blame is useless (who changed what for what reason?)
  - Bug hunting is harder (did the bug come from feature or cleanup?)
  
### **Solution**
  Separate commits always:
  
  # Work order
  1. Add feature in one commit
     git commit -m "feat: Add user profile endpoint"
  
  2. Cleanup in separate commit
     git commit -m "refactor: Clean up user service imports"
  
  # If you already mixed them
  git reset HEAD~1
  # Stage feature changes only
  git add -p
  git commit -m "feat: ..."
  # Stage cleanup changes
  git add .
  git commit -m "refactor: ..."
  
### **Symptoms**
  - PR has both "feat:" and "refactor:" changes
  - Reviewer asks "is this part of the feature?"
  - Bug appears, can't tell which change caused it
### **Detection Pattern**
feat.*refactor|fix.*cleanup

## Aggressive Dead Code Removal

### **Id**
aggressive-dead-code-removal
### **Summary**
Removing all code flagged as unused without investigating why
### **Severity**
high
### **Situation**
  Linter reports 20 unused functions. You delete them all.
  
### **Why**
  Some "unused" code exists for reasons:
  - Feature flags (code waits to be enabled)
  - A/B tests (variant code)
  - Fallback/recovery code (runs on error)
  - Scheduled tasks (runs on cron, not request)
  - Future-proofing that was intentional
  
  Mass deletion may break edge cases nobody tests.
  
### **Solution**
  For each "unused" item:
  1. Check git history: why was it added?
  2. Check for related feature flags or comments
  3. Search for dynamic references
  4. Ask the original author if possible
  5. If truly unused, delete with clear commit message
  
  # Good commit message
  git commit -m "chore: Remove unused handleLegacyAuth
  
  Added in abc123 for migration from Auth0 to Clerk.
  Migration completed 6 months ago. No references found.
  Verified with prod logs: no calls in 30 days."
  
### **Symptoms**
  - "Unused code" linter warnings ignored context
  - No investigation before deletion
  - Edge cases break after deploy
### **Detection Pattern**
unused|dead.*code|orphan

## Over Zealous Type Narrowing

### **Id**
over-zealous-type-narrowing
### **Summary**
Making types too strict during cleanup breaks valid use cases
### **Severity**
high
### **Situation**
  You're cleaning up types, replacing `any` with specific types.
  You make the types very narrow based on current usage.
  
### **Why**
  Types based only on current usage may be too restrictive:
  - Other code paths not yet visible
  - Tests that exercise edge cases
  - Valid future extensions
  - External callers you don't see
  
  Overly narrow types cause endless type errors.
  
### **Solution**
  When narrowing types:
  1. Check ALL callers, not just the first few
  2. Look at test files for edge cases
  3. Consider if the API should be flexible
  4. Use union types for valid variants
  
  # Too narrow
  function process(status: 'active') { ... }
  
  # Appropriately narrow
  function process(status: 'active' | 'pending' | 'inactive') { ... }
  
  # Still flexible for extension
  function process(status: UserStatus) { ... }
  
### **Symptoms**
  - Type errors after cleanup
  - This used to work
  - Tests fail after type changes
### **Detection Pattern**
type.*=.*string|as\\s+const

## Premature Extraction

### **Id**
premature-extraction
### **Summary**
Extracting code into abstractions before patterns are clear
### **Severity**
medium
### **Situation**
  You see similar code in two places. You immediately extract it
  into a shared utility or component.
  
### **Why**
  Two similar things might diverge:
  - Requirements change differently
  - Edge cases differ
  - One evolves, other is stable
  
  Wrong abstraction is worse than duplication:
  - Every change requires checking all uses
  - Abstraction accumulates parameters
  - Eventually nobody understands it
  
### **Solution**
  Wait for the Rule of Three:
  1. First occurrence: Just write it
  2. Second occurrence: Note the duplication
  3. Third occurrence: Now extract
  
  When extracting:
  - Extract exactly what's common
  - Keep differences as parameters
  - If parameters > 3, maybe don't extract
  
  # Signs the abstraction is wrong
  - Boolean parameters: formatDate(date, includeTime, useUTC, forDisplay)
  - Growing switch statements inside
  - "We need to add a special case for X"
  
### **Symptoms**
  - Shared function with many boolean parameters
  - We extracted too early
  - Two usages that want different things
### **Detection Pattern**
shared|common|utils|helpers

## Cleanup Without Communication

### **Id**
cleanup-without-communication
### **Summary**
Large refactoring PR with no context for reviewers
### **Severity**
medium
### **Situation**
  You submit a cleanup PR with 500 lines changed across 20 files.
  The description says "Code cleanup."
  
### **Why**
  Reviewers cannot verify correctness without context:
  - What was wrong before?
  - What principle guided the cleanup?
  - How do I know nothing broke?
  - What should I pay attention to?
  
  Unexplained cleanup gets rubber-stamped or blocked.
  
### **Solution**
  PR description should include:
  1. What was the problem?
  2. What is the cleanup approach?
  3. How to verify nothing broke?
  4. Any risks or areas needing careful review?
  
  # Example PR description
  ## Problem
  UserService grew to 800 lines with mixed responsibilities.
  
  ## Cleanup approach
  Split by domain: auth, profile, billing.
  No logic changes, only file reorganization.
  
  ## Verification
  - All tests pass (no changes to tests)
  - Manually tested login, profile update, checkout
  
  ## Review focus
  - Verify all exports are re-exported from index.ts
  - Check import paths updated correctly
  
### **Symptoms**
  - PR description is one line
  - Reviewer approves without understanding
  - Bugs found after merge
### **Detection Pattern**
cleanup|refactor|reorganize

## Formatting Wars

### **Id**
formatting-wars
### **Summary**
Cleanup that changes formatting without team agreement
### **Severity**
medium
### **Situation**
  You prefer tabs over spaces, or single quotes over double quotes.
  You change the whole codebase to match your preference.
  
### **Why**
  Formatting disagreements:
  - Create huge diffs that hide real changes
  - Trigger merge conflicts everywhere
  - Annoy teammates
  - Waste review time
  - Git blame becomes useless
  
### **Solution**
  Use automated formatting:
  1. Agree on Prettier/ESLint config as a team
  2. Add format-on-save to editors
  3. Add pre-commit hook for formatting
  4. Run formatter once, commit as single "chore: format"
  5. Never manually adjust formatting again
  
  # .prettierrc
  {
    "semi": true,
    "singleQuote": true,
    "tabWidth": 2
  }
  
  # Pre-commit hook
  npx prettier --write .
  
### **Symptoms**
  - "Formatting only" PRs
  - Debates about style
  - Different files formatted differently
### **Detection Pattern**
prettier|eslint|format

## Backwards Compat Accumulation

### **Id**
backwards-compat-accumulation
### **Summary**
Backwards compatibility code that never gets removed
### **Severity**
info
### **Situation**
  You add backwards compatibility for a migration. You forget to
  remove it after migration completes.
  
### **Why**
  Compatibility code accumulates:
  - Makes codebase harder to understand
  - Adds maintenance burden
  - Sometimes has bugs that hide
  - Nobody remembers why it exists
  
### **Solution**
  When adding backwards compatibility:
  1. Add TODO with ticket and expected removal date
  2. Add telemetry to track old code path usage
  3. Set calendar reminder to check in 30 days
  4. Remove when usage drops to zero
  
  // TODO: JIRA-123 - Remove after 2024-03-01
  // Old API format, migrate clients then delete
  if (request.version < 2) {
    return legacyHandler(request);
  }
  
### **Symptoms**
  - Comments mentioning "old" or "legacy"
  - if/else for version checks with old dates
  - Nobody knows if old path is still used
### **Detection Pattern**
legacy|backwards.*compat|deprecated|old.*version

## Cleanup Scope Creep

### **Id**
cleanup-scope-creep
### **Summary**
Cleanup that keeps expanding beyond original scope
### **Severity**
info
### **Situation**
  You start cleaning up one file. You notice something in an import.
  You fix that too. Three hours later, you've changed 30 files.
  
### **Why**
  Unbounded cleanup:
  - Creates massive PRs
  - Increases risk of bugs
  - Takes time from feature work
  - Hard to review
  - Hard to revert if issues arise
  
### **Solution**
  Timebox and scope-limit cleanup:
  1. Define scope before starting: "Only UserService"
  2. Set a time limit: "1 hour max"
  3. Note other issues for later: "TODO: fix auth later"
  4. Submit small PRs: one concern at a time
  
  # Keep a cleanup backlog
  ## Cleanup Backlog
  - [ ] AuthService imports
  - [ ] OrderService types
  - [ ] Remove legacy payment handler
  
  Pick one item per cleanup session.
  
### **Symptoms**
  - While I was in there...
  - PR keeps growing
  - Cleanup takes whole day
### **Detection Pattern**
while.*there|also.*fixed|noticed