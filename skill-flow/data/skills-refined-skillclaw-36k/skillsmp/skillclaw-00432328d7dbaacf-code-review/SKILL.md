---
name: code-review
description: Use this skill when you need to conduct a code review, identify risks, or list issues in the codebase.
---

# Code Review Skill

## Scope
- Review for Rust/Tauri backend
- Review for React frontend
- Database and performance risk assessment

## Critical Rules
- Prioritize identifying logical errors and regression risks
- Check if command signatures and type exports are complete
- Ensure frontend does not violate `console.*` or use `as any`
- UI tables: Verify row height and padding conform to compact standards (default th/td padding 6px 10px, line-height 1.2; compact tags within tables)

## Review Points
- Tauri: Ensure `#[tauri::command]` and `#[specta::specta]` are complete
- Types: Ensure input/output parameters `specta::Type` are consistent with camelCase
- Database: Check `sqlx::query_as!`, explicit column names, and correct transactions
- Frontend: Use only `commands`, and provide error messages with `message.*`
- Performance: Identify redundant calculations, N+1 issues, and unnecessary clones

## Quick Commands
```bash
cargo clippy --all-targets --all-features -- -D warnings
cargo fmt --all
cd frontend && npm run lint
```

## Feedback Structure
- List issues first (sorted by severity)
- Provide actionable fix suggestions
- Annotate file paths and key locations

## Checklist
- [ ] No regression risks on critical paths
- [ ] Complete Tauri commands and type exports
- [ ] No `console.*` or `as any` in frontend
- [ ] No warnings from Lint/Clippy
- [ ] Table row height and padding are consistently compact