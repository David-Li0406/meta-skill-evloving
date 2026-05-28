---
name: security-audit
description: Security audit for code review and vulnerability analysis
argument-hint: "[PR number]"
model: claude-sonnet-4-5
context: fork
agent: general-purpose
allowed-tools:
  - Task
  - Bash(*)
extended-thinking: true
---

# Security Audit Command (Wrapper)

You perform security reviews of pull requests by invoking the security-analyst-specialist agent and posting the results.

**PR Number:** $ARGUMENTS

**Note:** This command is automatically run by `/work` after PR creation. For manual security audits, use: `/psd-claude-coding-system:security-audit [pr_number]`

## Workflow

### Step 1: Invoke Security Analyst Agent

Use the Task tool to invoke security analysis:
- `subagent_type`: "psd-claude-coding-system:security-analyst-specialist"
- `description`: "Security audit for PR #$ARGUMENTS"
- `prompt`: "Perform comprehensive security audit on PR #$ARGUMENTS. Analyze all changed files for:

1. **Security Vulnerabilities:**
   - SQL injection, XSS, authentication bypasses
   - Hardcoded secrets or sensitive data exposure
   - Input validation and sanitization issues

2. **Architecture Violations:**
   - Business logic in UI components
   - Improper layer separation
   - Direct database access outside patterns

3. **Best Practices:**
   - TypeScript quality and type safety
   - Error handling completeness
   - Test coverage for critical paths
   - Performance concerns

Return structured findings in the specified format."

### Step 2: Post Consolidated Comment

The agent will return structured findings. Format and post as a single consolidated PR comment:

```bash
# Post the security review as a single comment
gh pr comment $ARGUMENTS --body "## Automated Security & Best Practices Review

[Format the agent's structured findings here]

### Summary
- Critical Issues: [count from agent]
- High Priority: [count from agent]
- Suggestions: [count from agent]

### Critical Issues (Must Fix Before Merge)
[Critical findings from agent with file:line, problem, fix, reference]

### High Priority (Should Fix Before Merge)
[High priority findings from agent]

### Suggestions (Consider for Improvement)
[Suggestions from agent]

### Positive Practices Observed
[Good practices noted by agent]

### Required Actions
1. Address all critical issues before merge
2. Consider high priority fixes
3. Run security checks: \`npm audit\`, \`npm run lint\`, \`npm run typecheck\`
4. Verify all tests pass after fixes

---
*Automated security review by security-analyst-specialist agent*"

echo "Security audit completed and posted to PR #$ARGUMENTS"
```

## Key Features

- **Comprehensive Analysis**: Covers security, architecture, and best practices
- **Single Comment**: All findings consolidated into one easy-to-review comment
- **Actionable Feedback**: Includes specific fixes and code examples
- **Severity Levels**: Critical, High, Suggestions
- **Educational**: References to OWASP and project documentation

## When to Use

**Automatic:** The `/work` command runs this automatically after creating a PR

**Manual:** Use this command when:
- You want to audit an existing PR
- You need to re-run security analysis after fixes
- You're reviewing someone else's PR

## Example Usage

```bash
# Manual security audit of PR #123
/psd-claude-coding-system:security-audit 123
```

The agent will analyze all changes in the PR and post a consolidated security review comment.
