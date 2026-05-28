---
name: code-review
description: Use this skill when a user requests a code review, seeks to identify risks, or lists issues.
---

# Code Review Skill

## Applicable Scope
- Rust/Tauri backend review
- React frontend review
- Database and performance risk assessment

## Critical Rules
- Prioritize identifying logical errors and regression risks.
- Check if command signatures and type exports are complete.
- Ensure the frontend does not violate `console.*` or use `as any`.
- For UI tables, verify that row height and padding conform to compact standards (default th/td padding 6px 10px, line-height 1.2; compact tags within tables).

## Review Points
- Tauri: Ensure `#[tauri::command]` and `#[specta::specta]` are complete.
- Types: Ensure input/output parameters `specta::Type` are consistent with camelCase.
- Database: Check for `sqlx::query_as!`, explicit column names, and correct transactions.
- Frontend: Use only `commands` and provide error messages via `message.*`.
- Performance: Look for redundant calculations, N+1 issues, and unnecessary clones.

## Quick Commands
```bash
cargo clippy --all-targets --all-features -- -D warnings
cargo fmt --all
cd frontend && npm run lint
```

## Feedback Structure
- List issues in order of severity.
- Provide actionable suggestions for fixes.
- Indicate file paths and key locations.

## Checklist
- [ ] No regression risks on critical paths.
- [ ] Tauri commands and type exports are complete.
- [ ] Frontend does not contain `console.*` or `as any`.
- [ ] Lint/Clippy shows no warnings.
- [ ] Table row height and padding are consistently compact.

## Review Process
- Read the specification file to understand expected changes.
- Review `git diff origin/develop...HEAD` to see all implemented changes.
- Check validation evidence (test results, build output, lint).
- Verify alignment between specifications and implementations.
- Identify blockers (must-fix), technical debt (should-fix), or skippable issues (minor).

## Review Standards
- **Blocker**: Breaks functionality, validation failure, security issues.
- **Tech Debt**: Functional but needs improvement, lacks tests, incomplete documentation.
- **Skippable**: Minor style issues, non-critical optimizations, optional enhancements.

## Output Format Requirements
Return a JSON object matching this exact schema (all fields required):

```json
{
  "success": boolean,
  "review_summary": string,
  "review_issues": [
    {
      "review_issue_number": number,
      "issue_description": string,
      "issue_resolution": string,
      "issue_severity": "blocker" | "tech_debt" | "skippable"
    }
  ]
}
```

## Example Outputs
**Correct output (no issues):**
```json
{
  "success": true,
  "review_summary": "Implementation aligns with specifications. All validation commands passed.",
  "review_issues": []
}
```

**Correct output (with issues):**
```json
{
  "success": false,
  "review_summary": "Implementation covers core functionality but has validation failures and lacks test coverage.",
  "review_issues": [
    {
      "review_issue_number": 1,
      "issue_description": "Integration test failed, 401 Unauthorized error.",
      "issue_resolution": "Update test fixtures to use a valid API key.",
      "issue_severity": "blocker"
    }
  ]
}
```