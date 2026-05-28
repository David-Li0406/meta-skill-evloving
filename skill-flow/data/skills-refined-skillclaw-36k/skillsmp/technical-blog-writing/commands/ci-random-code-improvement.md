---
description:
  CI version of random code improvement - no user interaction, applies all >90%
  confidence fixes automatically
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
  - Bash(sort*)
  - Bash(uniq*)
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Task
  - TodoWrite
---

# CI Random Code Improvement

Pick random files from the blog codebase, review for improvements, and
automatically fix issues with >90% confidence.

**CI MODE**: No user interaction. Apply all high-confidence fixes automatically.

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
re-run the find commands above to get a new batch (max 3 attempts).

If still nothing after 3 attempts:

- Output exactly: `NO_IMPROVEMENTS_FOUND`
- Stop execution

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

### Step 5: Log Findings

Output all findings using this format:

```markdown
## CI Random Improvement Report

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

**CI MODE: Proceed directly to implementation without confirmation.**

### Step 6: Implementation (TDD when practical)

For each fix:

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

**If verification fails**: Fix the issue or revert the problematic change.

### Step 8: Summary & PR Metadata

Output final summary and write PR metadata file for the GitHub Action.

**1. Write PR metadata to `.github/pr-metadata.json`:**

```json
{
  "title": "<type>(<scope>): <short description>",
  "body": "## Summary\n\n<bullet points of changes>\n\n## Modified Files\n\n<list of files with changes>\n\n## Verification\n\n- Lint: pass/fail\n- Types: pass/fail\n- Tests: pass/fail"
}
```

**Title format:**

- Use conventional commit format: `<type>(<scope>): <description>`
- `type`: refactor, fix, a11y, perf, test, chore
- `scope`: main component/file name (e.g., `CodeBlock`, `useTheme`)
- `description`: concise summary of improvements (max 50 chars)

**Body format:**

- Summary: bullet points of each improvement made
- Modified Files: list each file with brief description of changes
- Verification: lint/types/tests status

**2. Output summary to console:**

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

**Note: Do NOT perform git operations. The GitHub Action handles commits and PR
creation.**

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
- Accessibility improvements are high-value
- Test improvements are high-value (missing tests, edge cases)
- Use Tailwind semantic colors from the project's theme
- Do NOT run git commands - the action handles this
