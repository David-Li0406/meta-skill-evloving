---
name: gemini-review
description: Request code review from Gemini CLI - reviews staged changes or branch diff vs main
argument-hint: "[base-branch]"
---

# Gemini Code Review

Get a third opinion on your changes from Gemini. Reviews staged changes (if any) or committed branch diff against main.

## Current State

Branch: !`git branch --show-current`
Base: !`echo "${1:-main}"`

## How to Execute

Run the following command. The base branch defaults to `main` but can be overridden via $ARGUMENTS:

```bash
BASE_BRANCH="${ARGUMENTS:-main}"

# Determine what to review: staged changes, committed changes, or nothing
STAGED_CHANGES=$(git diff --cached --stat 2>/dev/null)
COMMITTED_CHANGES=$(git diff $BASE_BRANCH...HEAD --stat 2>/dev/null)

if [ -n "$STAGED_CHANGES" ]; then
  DIFF_MODE="staged"
  DIFF_CMD="git diff --cached"
  DIFF_STAT_CMD="git diff --cached --stat"
elif [ -n "$COMMITTED_CHANGES" ]; then
  DIFF_MODE="committed"
  DIFF_CMD="git diff $BASE_BRANCH...HEAD"
  DIFF_STAT_CMD="git diff $BASE_BRANCH...HEAD --stat"
else
  echo "No staged or committed changes to review"
  exit 0
fi

# Try to get PR description if one exists for this branch
PR_CONTEXT=$(gh pr view --json title,body,url 2>/dev/null && echo "---" || echo "No PR found for this branch.")

gemini \
  --model gemini-3-pro-preview \
  --allowed-tools "read_file" \
  --allowed-tools "glob" \
  --allowed-tools "search_file_content" \
  --allowed-tools "run_shell_command" \
  --allowed-tools "list_directory" \
  -p "# Code Review Request

You are reviewing $DIFF_MODE changes on the current branch.

## PR Context

$PR_CONTEXT

## Your Task

1. Run \`$DIFF_STAT_CMD\` to see what changed
2. Run \`$DIFF_CMD\` to see the actual diff
3. Read \`CLAUDE.md\` for project standards (if it exists)
4. Read changed files that need closer inspection
5. Consider the PR context above (if available) - does the implementation match the stated intent?
6. Provide your review

## Review Focus

- Code quality: separation of concerns, error handling, DRY
- Architecture: design decisions, dependency injection, interface boundaries
- Testing: real tests (not just mocks), edge cases covered
- Security: no vulnerabilities, input validation, no exposed secrets
- Consistency: follows existing codebase patterns

## Output Format

\`\`\`
## Summary
<1-2 sentence overview>

## Strengths
<What's well done - cite file:line>

## Issues

### Critical (Must Fix)
<Bugs, security issues, data loss risks - or \"None\">

### Important (Should Fix)
<Architecture problems, missing error handling, test gaps - or \"None\">

### Minor (Nice to Have)
<Style, optimization, documentation - or \"None\">

## Questions
<Anything unclear>

## Verdict
<APPROVE / APPROVE WITH SUGGESTIONS / REQUEST CHANGES>
<1 sentence reasoning>
\`\`\`

Be direct. Reference file paths and line numbers. Focus on actionable feedback."
```

## After Review

Once Gemini provides its review:

1. **Critical issues**: Address immediately before proceeding
2. **Important issues**: Evaluate each - fix if valid, push back if not
3. **Minor issues**: Note for future, don't block on these
4. **Questions**: Answer or clarify in your code/comments

Report Gemini's verdict and key findings to the user.
