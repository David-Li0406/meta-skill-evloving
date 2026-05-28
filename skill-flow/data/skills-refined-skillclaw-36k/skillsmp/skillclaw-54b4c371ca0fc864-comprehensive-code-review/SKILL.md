---
name: comprehensive-code-review
description: Use this skill when you need to conduct a thorough code review, assessing code quality, architecture, documentation, and testing practices.
---

# Skill body

## Purpose

This skill provides a comprehensive framework for conducting code reviews, ensuring that all aspects of code quality, architecture, documentation, and testing are evaluated systematically.

## When to Use

Use this skill when:
- You receive a pull request for review.
- You want to ensure code quality and adherence to best practices.
- You need to provide constructive feedback on code changes.

## Instructions

### 1. Check CI/CD Status

Before starting the review, check the CI/CD status of the pull request:

```bash
# Check the status of the pull request
gh pr view <PR_NUMBER> --json statusCheckRollup
```

- ✅ **All checks pass**: Proceed with the review.
- ❌ **Checks failed**: Analyze the failure and address it before continuing.

### 2. Confirm Review Scope

Identify the files and changes that need to be reviewed:

```bash
# Check the changed files in the pull request
git status
git diff --name-only
```

### 3. Understand Context

Before reviewing, gather context about the project:
- Type of project (prototype, MVP, production)
- Existing codebase and its structure
- Presence of tests and documentation

### 4. Conduct Systematic Review

Evaluate the code based on the following criteria:

#### A. Code Quality
- Readability (variable and function naming)
- Adherence to DRY principles
- Appropriate level of abstraction
- Quality of comments (explain "why")

#### B. Architecture Review
- Evaluate the overall architecture, including database, API, and component structure.
- Ensure that security and dependency management are considered.

#### C. Documentation and Testing
- Check the quality of comments and API specifications.
- Assess the adequacy of tests, including coverage and edge cases.

#### D. Performance
- Identify potential performance issues (e.g., N+1 problems, unnecessary loops).
- Suggest caching strategies and resource management improvements.

### 5. Provide Feedback

Document your review findings in a structured format:

```markdown
## Code Review Results

### ⚠️ CI/CD Status
[Include CI status if applicable]

### 🔴 Critical Issues (Immediate attention required)
- [Specific issue and location]
- [Suggested fix]

### 🟡 Warnings (Recommended improvements)
- [Improvement suggestion]
- [Reason]

### 🟢 Good Practices (Positive feedback)
- [Commendable aspects of the code]
```

### 6. Follow Up

After providing feedback, follow up on the changes made in response to your review. Ensure that all critical issues are addressed before the code is merged.

## Output Destination

Save the review results in the designated documentation folder for future reference.