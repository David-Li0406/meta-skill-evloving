---
name: code-review
description: Reviews code changes for bugs, style issues, and best practices. Use when reviewing PRs or checking code quality.
---

# Code Review Skill

This skill helps you conduct thorough code reviews. Follow the checklist and guidelines below.

## Review Checklist

1.  **Correctness**
    *   Does the code do what it's supposed to?
    *   Does it meet the requirements?
    *   Are there any logic errors?

2.  **Edge Cases**
    *   Are error conditions handled gracefully?
    *   Have boundary conditions been considered (null, empty, negative values, etc.)?

3.  **Style**
    *   Does it follow project conventions (naming, formatting, etc.)?
    *   Is the code readable and maintainable?

4.  **Performance**
    *   Are there obvious inefficiencies (e.g., O(n^2) loops where O(n) is possible)?
    *   Are there potential memory leaks?

## Feedback Guidelines

*   **Be specific**: Point out exactly what needs to change and where.
*   **Explain why**: Don't just give a command; explain the reasoning (e.g., "This could be a null pointer exception because...").
*   **Suggest alternatives**: If possible, provide a code snippet or a description of a better approach.
