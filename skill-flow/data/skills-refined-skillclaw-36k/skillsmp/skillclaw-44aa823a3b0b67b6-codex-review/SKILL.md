---
name: codex-review
description: Use this skill when you need to perform automated code reviews with OpenAI Codex CLI to identify bugs, security vulnerabilities, performance issues, and code quality problems.
---

# Codex Review Skill

This skill utilizes the OpenAI Codex CLI to conduct comprehensive code reviews, ensuring code quality and security.

## When to Use

- User asks to "review" code
- User wants to check for bugs or issues
- User mentions "security", "performance", or "quality"
- Before committing code
- During pull request review
- User asks "what's wrong with this code?"

## Prerequisites

Ensure Codex CLI is installed and accessible:

```bash
codex --version  # Should display installed version
```

## Basic Usage

### Step 1: Determine Scope

Decide what to review:

- Uncommitted changes (default)
- Specific file(s)
- Last commit
- Pull request
- Entire codebase

### Step 2: Check Current State

Review the current state of your code:

```bash
git status          # See what's changed
git diff --stat     # Summary of changes
git diff            # Detailed changes
```

### Step 3: Execute Codex Review

Run Codex with a review-focused prompt:

```bash
codex --sandbox=read-only exec "Perform comprehensive code review of [SCOPE].

Check for:
1. CRITICAL ISSUES (must fix):
   - Security vulnerabilities (SQL injection, XSS, CSRF, etc.)
   - Potential runtime errors
   - Data loss risks
   - Breaking changes

2. IMPORTANT ISSUES (should fix):
   - Logic bugs
   - Performance problems
   - Type safety gaps
   - Error handling issues

3. SUGGESTIONS (consider):
   - Code quality improvements
   - Refactoring opportunities
   - Better patterns
   - Documentation needs

4. POSITIVE OBSERVATIONS:
   - Best practices followed
   - Good patterns used

For each issue:
- Severity level (Critical/Important/Suggestion)
- File path and line number
- Clear description of the problem
- Why it's a problem
- How to fix it

Do NOT make any changes - this is review only."
```

### Step 4: Present Findings

Organize results by severity:

- 🔴 Critical Issues
- 🟡 Important Issues
- 🟢 Suggestions
- ✅ Positive Observations

## Example Reviews

### Review Uncommitted Changes

```bash
codex --sandbox=read-only exec "Review all uncommitted changes for:
- Bugs and logic errors
- Security vulnerabilities
- Performance issues
- Code quality problems
- Missing error handling
Do NOT modify code."
```