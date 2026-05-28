---
name: sc-startup
description: Use this skill to orchestrate the startup process of a repository, including loading prompts, syncing checklists, and managing pull requests and worktree hygiene.
---

# Skill body

Thin orchestration for the `/sc-startup` command. Validates config, launches background agents, aggregates statuses, and emits a concise startup report. Delegates all heavy lifting to agents via Agent Runner (registry enforced, audited).

## Command
- `/sc-startup [--pr] [--pull] [--fast] [--readonly]`
- `/sc-startup --init` (config discovery and guided setup)

## Agents
- `ci-pr-agent` (PR list/fix; list-only when `--readonly`)
- `sc-worktree-scan` / `sc-worktree-cleanup` (worktree hygiene; scan-only when `--readonly`)
- `ci-automation` (pull-only master → develop; must complete before checklist updates)
- `sc-checklist-status` (report/update checklist; report-only when `--readonly`; no auto-commit)
- `sc-startup-init` (detection-only: config presence, candidates, package detection; returns fenced JSON with YAML payload)

## Flow (best-effort)
1. If `--init`: Agent Runner → `sc-startup-init` (detection-only). Parse results, use AskQuestion to fill missing/ambiguous settings (prompt path, checklist path, worktree-scan, pr-enabled, worktree-enabled). If not `--readonly`, write `.claude/sc-startup.yaml`; otherwise show synthesized YAML. Then continue.
2. Load `.claude/sc-startup.yaml`; validate required keys and enabled feature dependencies. Fail closed with `DEPENDENCY.MISSING` if enabled package absent.
3. If `--fast`: read startup prompt only, summarize role, exit (no agents/checklist).
4. If `--pr` and enabled: Agent Runner → `ci-pr-agent` (`--list --fix`, or list-only when `--readonly`).
5. If worktree scan/cleanup enabled in config: Agent Runner → `sc-worktree-{scan|cleanup}` (scan/report-only when `--readonly`).
6. If `--pull`: Agent Runner → `ci-automation` (pull-only master → develop); wait for completion before checklist updates.
7. Agent Runner → `sc-checklist-status` (default update; report-only when `--readonly`). Checklist changes stay in workspace (no commit).
8. Read startup prompt + checklist (post-update). Aggregate task statuses in deterministic order; never abort on agent errors/timeouts.
9. Emit concise report: prompt summary, checklist deltas, PR/worktree/CI outcomes, partial failures, and next steps.
10. If `sc-checklist-status` reports `VALIDATION.INVALID_PATH` (path escape), explicitly flag it as a warning.