---
name: ai-powered-code-review-specialist
description: Use this skill when you need to perform comprehensive AI-assisted code reviews that integrate automated static analysis and intelligent pattern recognition to identify bugs, vulnerabilities, and performance issues.
---

# Skill body

## Context

This skill is designed for multi-layered code review workflows that integrate with CI/CD pipelines, providing instant feedback on pull requests with human oversight for architectural decisions. It supports reviews across 30+ programming languages, combining rule-based analysis with AI-assisted contextual understanding.

## Requirements

Review: **$ARGUMENTS**

Perform comprehensive analysis covering security, performance, architecture, maintainability, testing, and AI/ML-specific concerns. Generate review comments with line references, code examples, and actionable recommendations.

## Automated Code Review Workflow

### Initial Triage
1. Parse the diff to determine modified files and affected components.
2. Match file types to optimal static analysis tools.
3. Scale analysis based on PR size (superficial >1000 lines, deep <200 lines).
4. Classify change type: feature, bug fix, refactoring, or breaking change.

### Multi-Tool Static Analysis
Execute in parallel:
- **CodeQL**: Deep vulnerability analysis (SQL injection, XSS, auth bypasses).
- **SonarQube**: Identify code smells, complexity, duplication, and maintainability issues.
- **Semgrep**: Apply organization-specific rules and security policies.
- **Snyk/Dependabot**: Assess supply chain security.
- **GitGuardian/TruffleHog**: Detect secrets in the code.

### AI-Assisted Review
```python
# Context-aware review prompt for AI model
review_prompt = f"""
You are reviewing a pull request for a {language} {project_type} application.

**Change Summary:** {pr_description}
**Modified Code:** {code_diff}
**Static Analysis:** {sonarqube_issues}, {codeql_alerts}
**Architecture:** {system_architecture_summary}

Focus on:
1. Security vulnerabilities missed by static tools.
2. Performance implications at scale.
3. Edge cases and error handling gaps.
4. API contract compatibility.
5. Testability and missing coverage.
6. Architectural alignment.

For each issue:
- Specify file path and line numbers.
- Classify the issue and provide actionable recommendations.
"""
```