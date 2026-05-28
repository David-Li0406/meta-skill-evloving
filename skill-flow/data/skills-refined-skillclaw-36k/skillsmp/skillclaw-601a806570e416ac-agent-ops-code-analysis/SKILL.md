---
name: agent-ops-code-analysis
description: Use this skill when you need to perform a thorough analysis of codebases, including linting, code reviews, and identifying improvements aligned with project goals.
---

# Skill body

## Overview
This skill combines linting, code review, and improvement analysis for AgentOps instruction files and codebases. It ensures that files are correctly formatted, structured, and consistent while also providing a framework for evaluating code quality and alignment with project goals.

## Steps

### 1. Validate and Lint Instruction Files
Use the following command to validate and lint AgentOps markdown-based instruction files:
```bash
/lint-instructions [path]
```
#### Validation Rules
- **Critical Errors (must fix)**:
  - ERR001: No code fence wrapper
  - ERR002: Valid YAML frontmatter
  - ERR003: Required frontmatter fields
  - ERR004: File encoding must be UTF-8 without BOM

- **Warnings (should fix)**:
  - WARN001: Excessive blank lines
  - WARN002: Trailing whitespace
  - WARN003: Heading hierarchy
  - WARN004: Inconsistent list markers
  - WARN005: Missing newline at EOF
  - WARN006: Table alignment

### 2. Conduct Code Review
Perform a comprehensive code review using the following axes:
- **Problem Fit & Requirement Fidelity**: Ensure the code solves the stated problem and that assumptions are explicit.
- **Abstractions & Over-Engineering**: Evaluate the necessity of abstractions and their current implementations.
- **Conceptual Integrity**: Check for a coherent mental model and consistency in concepts.
- **Cognitive Load & Local Reasoning**: Assess how much code needs to be understood for changes.

### 3. Propose Improvements
Analyze the codebase for specific enhancements that:
- Align with the project’s stated goals.
- Improve correctness, maintainability, or delivery confidence.
- Reduce risk, ambiguity, or future cost.

### 4. Document Findings
Output the findings in a human-readable format or as issues using the issue tracker schema:
```yaml
output_mode: report | issues | both
default: report
issue_prefix: CR  # Code Review
```

## Conclusion
This skill provides a comprehensive approach to maintaining high-quality code and documentation within the AgentOps framework, ensuring that all files and codebases are aligned with project goals and best practices.