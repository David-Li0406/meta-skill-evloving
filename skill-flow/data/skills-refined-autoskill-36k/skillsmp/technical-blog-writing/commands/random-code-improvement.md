---
description:
  Selects random files from blog codebase, performs comprehensive code review
  (readability, React/TS patterns, a11y, UX, performance, testing), and applies
  fixes with >90% confidence using TDD when practical
allowed-tools:
  - Bash(find app/*)
  - Bash(find components/*)
  - Bash(find lib/*)
  - Bash(find hooks/*)
  - Bash(grep*)
  - Bash(shuf*)
  - Bash(yarn test:unit*)
  - Bash(yarn lint*)
  - Bash(yarn typecheck*)
  - Bash(git add *)
  - Bash(git status)
  - Bash(git diff*)
  - Bash(git log*)
  - Bash(git commit *)
  - Bash(git push*)
  - Bash(sort*)
  - Bash(uniq*)
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Task
  - AskUserQuestion
  - TodoWrite
  - mcp__ide__getDiagnostics
---

# Random Code Improvement

Pick random files from the blog codebase, review for improvements, and
optionally fix issues with >90% confidence.

## Random File Pool (Pre-selected)

### Components (3 files)

!`find components -name "*.tsx" -type f | grep -v -E "\.(test|stories)\." | grep -v "/ui/" | shuf -n 3`

### Routes & Lib (2 files)

!`find app/routes lib hooks -name "*.ts" -o -name "*.tsx" | grep -v -E "\.(test|stories)\." | shuf -n 2`

## Steps to follow:

### Step 1: Analyze Pool & Select Best Candidate

For each file in the pool above:

1. Read the file
2. Scan for obvious improvement opportunities
3. Rate "review potential" (low/medium/high)

Select the file with **highest review potential**. If all files seem clean,
re-run the find commands above to get a new batch (max 3 attempts). If still
nothing after 3 attempts, report files are healthy and end.

### Step 2: Determine Review Scope

Based on the selected file:

- **Self-contained**: Simple utility/standalone component → single file
- **Has dependencies**: Imports local hooks/helpers → include those
- **Part of larger component**: Multiple related files → full component
  directory

Read all files in scope.

### Step 3: Comprehensive Code Review

Analyze across ALL categories equally:

| Category         | Focus                                      |
| ---------------- | ------------------------------------------ |
| 📖 Readability   | Naming, structure, cognitive complexity    |
| ⚛️ React         | Hooks rules, composition, state management |
| 💠 TypeScript    | Avoid `any`, proper generics, inference    |
| ♿ Accessibility | ARIA, keyboard nav, focus, screen readers  |
| 🎯 UX            | Error/loading/empty states, edge cases     |
| ⚡ Performance   | Re-renders, memoization, bundle size       |
| 🎨 Styling       | Tailwind patterns, semantic colors         |
| 🧪 Testing       | Missing tests, edge cases, coverage gaps   |
| 📝 Docs          | JSDoc, inline comments where needed        |

**Test Analysis:**

- Check if `*.test.ts(x)` exists for the component in `tests/unit/`
- Review for missing edge cases, untested branches, async behavior
- If no tests: identify key behaviors worth testing (props, errors,
  interactions)

### Step 4: Issue Assessment

For each issue found:

1. Calculate confidence (0-100%)
2. **Only fix issues >90% confidence**

Document high-confidence issues:

| Field      | Description                   |
| ---------- | ----------------------------- |
| Category   | Emoji prefix                  |
| What       | Issue description             |
| Why        | Impact                        |
| How        | Fix approach                  |
| Related    | Other files affected          |
| TDD?       | Can write failing test first? |
| Confidence | Must be >90%                  |

### Step 5: Present Findings (Batch)

Present ALL findings in one report using this format:

```markdown
## Random Improvement Report

**File(s)**: [paths] **Scope**: [self-contained / dependencies / full component]

### Will Fix (>90% confidence)

#### [Emoji] [Title]

- **Confidence**: X%
- **What**: ...
- **Why**: ...
- **TDD**: yes/no

### Observations (<90% - not fixing)

- [Emoji] [Description] (X%)
```

Use AskUserQuestion: "Proceed with fixes?"

- "Yes, apply all"
- "Let me choose"
- "No, just note them"

### Step 6: Implementation (TDD when practical)

For each approved fix:

1. Check for test file in `tests/unit/`

2. **If TDD practical** (behavioral change):
   - Write failing test
   - Run: `yarn test:unit <testfile>`
   - Implement fix
   - Verify test passes

3. **If TDD NOT practical** (explain why):
   - Pure CSS/Tailwind changes
   - ARIA attributes only
   - No testable behavior
   - Implement directly

### Step 7: Verification

After fixes, verify the changes:

```bash
# Lint
yarn lint

# Type check
yarn typecheck

# Run tests
yarn test:unit
```

Use `mcp__ide__getDiagnostics` for the modified file URI.

**If verification fails**: Fix or revert.

### Step 8: Summary

```markdown
## Improvement Complete

### Modified Files

- [file]: [changes]

### Issues Fixed

| Cat | Issue | TDD? |
| --- | ----- | ---- |
| ... | ...   | ...  |

### Verification

- Lint: pass/fail
- Types: pass/fail
- Tests: pass/fail

### Observations (not fixed)

- ...
```

### Step 9: Git Operations

Use AskUserQuestion to confirm before committing.

1. **Stage and commit changes:**

   ```bash
   git add <modified-files>
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <description>

   - [improvements]

   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
   EOF
   )"
   ```

   Commit types:
   - `refactor` - Code restructuring without behavior change
   - `fix` - Bug fixes
   - `chore` - Maintenance, cleanup
   - `feat` - New functionality
   - `a11y` - Accessibility improvements
   - `test` - Test additions or improvements
   - `docs` - Documentation improvements

2. **Push to remote:**

   ```bash
   git push
   ```

## Confidence Guidelines

**>90% (fix)**:

- Clearly identifiable issue
- Known fix approach
- No breaking risk
- Scoped change
- Verifiable

**<90% (observe)**:

- Needs architectural decisions
- Possible side effects
- Missing business context
- Would touch many files

## Notes

- Read files completely before assessing
- Be conservative with confidence
- TDD preferred but not mandatory
- All git ops need user approval
- Accessibility improvements are high-value
- Test improvements are high-value (missing tests, edge cases)
- Use Tailwind semantic colors from the project's theme
