---
name: code-review-and-verification
description: Use this skill when you need to conduct a thorough review of code quality, security, and performance, while also simulating human verification through various testing strategies.
---

# Skill body

## Overview

This skill combines code review and human verification techniques to ensure code quality, security, and performance. It is suitable for reviewing completed code, assessing pull requests, and verifying critical business logic.

## When to Use

- After completing a complex code implementation.
- When reviewing pull requests or merge requests.
- For verifying changes that impact critical business logic.
- During code refactoring to ensure behavior consistency.

## Core Components

### 1. Code Review

Conduct a comprehensive review focusing on:

- **Code Quality**: Check for adherence to coding standards, readability, and complexity.
- **Security**: Identify vulnerabilities such as SQL injection, XSS, and sensitive data exposure.
- **Performance**: Evaluate for potential performance issues like N+1 queries and memory leaks.

### 2. Human Verification Strategies

Simulate human verification through various methods:

#### Reverse Verification

1. Define expected outputs or behaviors.
2. Trace the code paths to ensure they lead to the expected results.
3. Identify any missing branches that could lead to different outcomes.

#### Boundary Testing

- Test with edge cases, including:
  - Null values, empty strings, and extreme numbers.
  - Special characters and long strings.
  - Concurrency issues.

#### User Scenario Simulation

1. List typical user scenarios.
2. Trace the code execution for each scenario.
3. Validate the expected user experience at each step.

#### Data Flow Tracing

1. Select a key data field.
2. Trace its path from input to output, ensuring each transformation is correct.

#### Bidirectional Reasoning

1. Analyze what the code does and what it is supposed to do.
2. Compare both perspectives to identify discrepancies.

## Execution Steps

1. **Prepare for Review**:
   - Gather the code to be reviewed.
   - Identify the scope and context of the review.

2. **Conduct Code Review**:
   - Follow the structured review process outlined above.
   - Document findings and suggestions.

3. **Perform Human Verification**:
   - Apply the verification strategies to ensure comprehensive testing.
   - Document the verification results.

4. **Generate Review Report**:
   - Summarize findings, including critical issues, suggestions for improvement, and overall assessment.
   - Provide a structured output for easy reference.

## Output Template

```markdown
# Code Review and Verification Report

## Overview

| Project | Content |
|---------|---------|
| Review Scope | {Files/Modules Reviewed} |
| Review Date | {Date} |
| Lines of Code | {Line Count} |
| Overall Rating | ✅ Pass / ⚠️ Needs Improvement / ❌ Fail |

## Review Findings

### Code Quality
- **Score**: {Score}
- **Comments**: {Brief Summary}

### Security
- **Score**: {Score}
- **Comments**: {Brief Summary}

### Performance
- **Score**: {Score}
- **Comments**: {Brief Summary}

## Issues Identified

### Critical Issues
- **Issue 1**: {Description}
- **Recommendation**: {Fix}

### Minor Issues
- **Issue 2**: {Description}
- **Recommendation**: {Fix}

## Verification Results

### Reverse Verification
- **Findings**: {Summary}

### Boundary Testing
- **Findings**: {Summary}

### User Scenario Simulation
- **Findings**: {Summary}

### Data Flow Tracing
- **Findings**: {Summary}

### Bidirectional Reasoning
- **Findings**: {Summary}

## Conclusion

{Final Assessment}
```