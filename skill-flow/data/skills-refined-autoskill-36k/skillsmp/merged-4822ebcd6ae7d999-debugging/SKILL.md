---
name: debugging
description: Use this skill when troubleshooting bugs, locating issues, or analyzing performance bottlenecks.
---

# Debugging Skill

## Scope
- Rust/Tauri backend issue troubleshooting
- React frontend state and rendering anomalies
- Database/migration issues

## Critical Rules
- Reproduce the issue before locating it
- Prioritize narrowing down the scope and impact
- Record key inputs and boundary conditions

## Systematic Process
1. Reproduce the problem (minimal input)
2. Collect context (logs, parameters, data state)
3. Formulate and validate hypotheses
4. Validate after fixing

## Common Checkpoints
- Tauri command not registered: Check `#[tauri::command]` and `#[specta::specta]`
- Type mismatch: Check DTO `specta::Type` and camelCase
- Database errors: Confirm migrations executed, table/field names are correct
- React excessive rendering: Check dependencies and `useMemo`/`useCallback`

## Tool Recommendations
- Rust: Use `tracing` to log critical paths
- DB: Use `EXPLAIN QUERY PLAN` to analyze indexes
- Frontend: Use UI prompts to display key states, avoid `console.*`

## Checklist
- [ ] Issue reproduced and minimized input
- [ ] Key hypotheses validated
- [ ] Regression validation passed after fixing