# Simple Command Template

Use this template for quick, single-purpose commands.

```markdown
---
description: [Brief description - what the command does]
---

[Clear instruction in imperative form]

Focus on:
- [Aspect 1]
- [Aspect 2]
- [Aspect 3]
```

## Example: Performance Analysis

```markdown
---
description: Analyze code for performance issues
---

Analyze this code for performance issues and suggest optimizations.

Focus on:
- Time complexity of algorithms
- Memory usage patterns
- Unnecessary operations or redundant code
- Database query efficiency (if applicable)

Provide specific, actionable recommendations with code examples.
```

## Example: Security Review

```markdown
---
description: Review code for security vulnerabilities
---

Review this code for security vulnerabilities.

Check for:
- Input validation issues
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization flaws
- Sensitive data exposure
- Dependency vulnerabilities

Flag any issues with severity level (critical, high, medium, low).
```

## Tips

1. **Keep description concise** - One line that clearly describes the action
2. **Use imperative language** - "Analyze", "Review", "Check", "Create"
3. **Be specific about focus areas** - Help Claude know what to prioritize
4. **Request actionable output** - Specify what format you want results in
