---
name: technical-review
description: >
  Conduct a detailed technical review of recent changes or a specific feature.
  Use when user says "review PR", "code review", or "review [scope]".
  Analyzes for logic errors, bugs, style issues, and performance. Fixes critical/high issues automatically.
---

# Technical PR Review

Conduct a detailed technical review of recent changes or a specific feature, focusing on logic, bugs, code style, and performance. Research false positives and apply fixes for critical and high-priority items.

**Usage**: When user says "review PR", "code review", or "review [scope]"

## Instructions

1. **Analyze Changes**:
   - Use **GitHub CLI (`gh`)** or **GitHub MCP tools** if available to fetch PR diffs, comments, and conversation history.
   - Identify new or modified code.
   - Review for logic errors, edge cases, and potential bugs.
   - Evaluate against project coding standards and style guides.
   - Check for potential regressions or performance bottlenecks.

2. **Handle Findings**:
   - **Research False Positives**: Verify if flagged issues are genuine bugs or intentional implementations.
   - **Prioritize**: Categorize findings into Critical, High, and Medium.
   - **Next steps**: Always provide actionable next steps.

3. **Remediate**:
   - **Fix Criticals**: Automatically attempt to fix verified "Critical" and "High" priority technical issues (delegate to appropriate coding agent).
   - **Comment**: Provide feedback on "Medium" or stylistic items.

4. **Verify**:
   - Ensure the build passes after fixes.
   - Verify that tests cover the new logic.

## Scopes

- (default): Review changes in the current working branch/directory.
- `{feature-name}`: Review code within a specific feature folder.
