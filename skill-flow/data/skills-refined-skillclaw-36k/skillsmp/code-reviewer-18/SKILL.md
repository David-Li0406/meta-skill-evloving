---
name: code-reviewer
description: Comprehensive code review for pull requests and local branch changes. Use when the user requests a code review, asks to review changes, provides a PR URL, or wants feedback on branch modifications. Focuses on logic errors, bugs, error handling, performance, complexity, and project guideline adherence while avoiding formatting nits.
---

# Code Reviewer

Perform thorough code reviews focused on substantive issues that impact correctness, safety, performance, and maintainability.

## Review Workflow

### 1. Determine Review Scope

**For PR URL:**
- Extract owner, repo, and PR number from URL
- Use GitHub tools to fetch PR details, files, and diff
- Check for project guidelines (AGENTS.md, CLAUDE.md, CONTRIBUTING.md, etc.)

**For Local Branch:**
- Run `git rev-parse --abbrev-ref HEAD` to confirm current branch
- Run `git --no-pager diff main...HEAD` (or master if main doesn't exist) to get changes
- Check for project guidelines in repository root and .github/

### 2. Load Project Context

Check for project-specific guidelines in priority order:
1. `AGENTS.md` or `CLAUDE.md` - AI agent/development guidelines
2. `CONTRIBUTING.md` - Contribution standards
3. `.github/PULL_REQUEST_TEMPLATE.md` - PR requirements
4. Language-specific configs (.eslintrc, .pylintrc, etc.) for critical rules only

Only load guidelines that exist. Use `gh repo view <owner>/<repo> --json name` or local file checks.

### 3. Analyze Changes

Review each changed file against these criteria:

**IN SCOPE - Must/Should Fix:**
- Logic errors and bugs
- Missing error handling for realistic/likely failures
- Performance regressions or inefficiencies
- Unnecessary complexity without justification
- Egregious code duplication (not minor repetition)
- Incomplete implementations
- Violations of project guidelines (AGENTS.md/CLAUDE.md)
- Security vulnerabilities
- Race conditions or concurrency issues
- Resource leaks or improper cleanup

**OUT OF SCOPE - Ignore:**
- Formatting and style (spaces, indentation, line length)
- Import order
- Naming conventions (unless severely misleading)
- Minor nits and preferences
- Subjective improvements without clear benefit

### 4. Structure Feedback

Categorize findings:

**🚨 MUST FIX** - Critical issues:
- Bugs that will cause failures
- Security vulnerabilities
- Data loss/corruption risks
- Breaking changes without migration

**⚠️ SHOULD FIX** - Important issues:
- Missing error handling for likely errors
- Performance problems
- Unjustified complexity
- Guideline violations

**💡 CONSIDER** - Suggestions (use sparingly):
- Significant architectural improvements
- Major duplication reduction opportunities

For each issue, provide:
- File and line number
- Clear explanation of the problem
- Concrete fix or approach (not vague suggestions)

### 5. Deliver Review

Format as concise, actionable feedback:

```
## Code Review Summary

**Scope:** [PR #123 | Branch: feature/xyz vs main]
**Files Changed:** X files, Y insertions, Z deletions

### 🚨 MUST FIX (N issues)

**file.js:42**
Issue: [Description]
Fix: [Specific solution]

### ⚠️ SHOULD FIX (N issues)

**file.py:100-105**
Issue: [Description]
Fix: [Specific solution]

### ✅ Overall Assessment
[Brief summary - avoid if no significant issues]
```

## Example Usage

**User:** "Review PR https://github.com/owner/repo/pull/123"
**Action:** Fetch PR → Load guidelines → Analyze diff → Provide categorized feedback

**User:** "Review my current branch"
**Action:** Check branch name → Diff against main → Check local guidelines → Provide feedback

## Guidelines

- Be direct and specific - no hedging or over-politeness
- Provide fixes, not just problem descriptions
- Skip "Overall Assessment" if there are no significant issues
- Don't manufacture issues to fill categories
- Trust the developer's existing style choices
- Focus review time on substantive problems
- Ignore cosmetic issues even if they stand out
