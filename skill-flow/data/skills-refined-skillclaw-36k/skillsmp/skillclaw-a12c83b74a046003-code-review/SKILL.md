---
name: code-review
description: Use this skill when you need to perform a comprehensive code review, ensuring adherence to best practices and providing constructive feedback.
---

# Code Review Skill

When reviewing code, follow this structured process to ensure quality and adherence to best practices:

## Review Process

### 1. Code Structure Analysis
- Check file organization and module structure.
- Verify naming conventions.
- Assess code readability.

### 2. Core Principles
- Ensure proper error handling and propagation.
- Maintain code consistency.
- Identify performance issues.

### 3. Best Practices Check
- **SOLID Principles**: Verify adherence to Single Responsibility, Open/Closed, etc.
- **DRY**: Look for code duplication.
- **Error Handling**: Check exception handling patterns.

### 4. Security Review
- Validate input to prevent vulnerabilities (e.g., SQL injection, XSS).
- Check authentication and authorization mechanisms.

### 5. Performance Considerations
- Evaluate algorithm efficiency.
- Optimize database queries.
- Analyze memory usage patterns.

## Output Format

Provide your review in the following format:

```markdown
## Code Review Summary

**Overall Assessment**: [Good/Needs Improvement/Critical Issues]

### Strengths
- [List positive aspects]

### Issues Found
1. **[Issue Category]**: [Description]
   - Location: [File:Line]
   - Severity: [Low/Medium/High/Critical]
   - Recommendation: [How to fix]

### Recommendations
- [List improvement suggestions]
```

## Important Notes
- Be constructive and specific in feedback.
- Prioritize issues by severity.
- Include code examples for fixes when helpful.
- Consider the project's coding standards.