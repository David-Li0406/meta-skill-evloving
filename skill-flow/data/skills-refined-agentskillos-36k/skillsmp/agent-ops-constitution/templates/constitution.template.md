# Project Constitution (authority for this repo)

## Purpose
Defines where the agent may work, how to build/test, and project-specific constraints.
Must be created and confirmed before baseline and any code changes.

## Confirmation Status

| Section | Status | Confirmed By | Date |
|---------|--------|--------------|------|
| Work boundaries | TODO | | |
| Git strategy | TODO | | |
| Commands | TODO | | |
| Environment | TODO | | |
| Tool detection | TODO | | |

Status values: TODO | CANDIDATE | CONFIRMED | SKIP

## Confidence level
Default confidence for this project: **normal** (low | normal | high)

| Confidence | Planning | Approval gates | Review depth | Batch size |
|------------|----------|----------------|--------------|------------|
| low | 3+ iterations | hard (wait for approval) | exhaustive | 1 task |
| normal | 2 iterations | soft (ask, continue) | standard | 2-3 tasks |
| high | 1 or skip | minimal | quick check | batch OK |

Agent may suggest lowering confidence for risky changes.
User may override per task.

## Work boundaries
### Allowed areas (edit permitted)
- TODO

### Restricted areas (edit only with explicit permission)
- TODO

### Forbidden areas (never edit)
- TODO

## Git strategy
### Branch policy
- Work directly on main: TODO (yes | no | for-trivial-only)
- Feature branch naming: TODO (e.g., `agent/<task-id>-<short-desc>`)
- Create branch before: TODO (always | for-multi-file-changes | never)

### Commit policy
- Commit message format: TODO (e.g., `[AgentOps] <type>: <summary>`)
- Checkpoint commits: TODO (yes | no)
- Commit frequency: TODO (after-each-step | after-task-complete | manual)

### Push policy
- Auto-push: **never** (agent never pushes without explicit user request)

## Commands (must be single-line)
### Build
- Command: TODO
- Status: TODO | CANDIDATE | CONFIRMED | SKIP
- Evidence: TODO (source file or user confirmation)
- Notes: TODO
- SKIP rationale: _(if SKIP, explain why)_

### Lint / Static analysis
- Command: TODO
- Status: TODO | CANDIDATE | CONFIRMED | SKIP
- Evidence: TODO
- Notes: TODO
- SKIP rationale: _(if SKIP, explain why)_

### Unit tests
- Command: TODO
- Status: TODO | CANDIDATE | CONFIRMED | SKIP
- Evidence: TODO
- Notes: TODO
- SKIP rationale: _(if SKIP, explain why)_

### Format
- Command: TODO
- Status: TODO | CANDIDATE | CONFIRMED | SKIP
- Evidence: TODO
- Notes: TODO
- SKIP rationale: _(if SKIP, explain why)_

## Environment assumptions
- OS/Container expectations: TODO
- Language/runtime versions: TODO
- Package manager/build tool: TODO
- Required services (db, cache, etc.): TODO

## Available tools
Tool detection results: `.agent/tools.json`

| Category | Tools Available |
|----------|----------------|
| Build | TODO |
| VCS | TODO |
| Containers | TODO |

Missing recommended: TODO

_Run tool detection: `aoc tools scan --save` or invoke `agent-ops-tools` skill_

## Quality gates (strict)
- Baseline must exist before any code changes.
- All new warnings/errors/test failures not present in baseline must be investigated before "done".
- lint_must_pass: true
- build_must_pass: true
- tests_must_pass: true
- coverage_threshold: none (or specify percentage)
- allow_warnings: true
- security_scan: false

## Change policy
- Minimal change only.
- No refactors without explicit permission.
- Tests required for new behavior.

## Open questions (must be resolved for baseline-ready)
- TODO

## Changelog
- YYYY-MM-DD: created
