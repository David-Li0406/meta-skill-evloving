---
name: ai-team-workflow
description: Role-based multi-agent workflow built on tmux-workflow/twf. Use when you want to run a PM/Architect/Product/Dev/QA/Ops/Coordinator/Liaison “AI team” as multiple Codex tmux workers, keep a shared responsibilities registry, route internal questions via Coordinator, and escalate user-facing questions via Liaison.
---

# ai-team-workflow

This skill layers a simple “AI team” coordination model on top of the `tmux-workflow` skill (`twf` workers + ask/pend/ping + parent/child spawn).

Core ideas:
- **One role = one Codex worker (tmux session)**.
- **Any role can scale** by spawning a child worker (e.g. `dev` hires `dev-intern`).
- A shared **responsibilities registry** is the source of truth for “who owns what”.
- **Coordinator** routes internal questions; **Liaison** is the only role that asks the user.

## Dependency

Requires `tmux-workflow` to exist alongside this skill (or set `AITWF_TWF=/path/to/twf`):
- Project install: `./.codex/skills/tmux-workflow/scripts/twf`
- Global install: `~/.codex/skills/tmux-workflow/scripts/twf`

## Shared registry (“task allocation table”)

Default path: `<skill_root>/share/registry.json` (project install example: `./.codex/skills/ai-team-workflow/share/registry.json`).
Overrides (highest → lowest):
- `AITWF_REGISTRY`
- `AITWF_DIR`
- `scripts/atwf_config.yaml` → `share.dir` (legacy: `share_dir`)
- default `<skill_root>/share`

Print the resolved paths:
- `bash .codex/skills/ai-team-workflow/scripts/atwf where`

It records, per worker:
- `role`: one of the project-enabled roles (see `atwf policy` / `scripts/atwf_config.yaml` → `team.policy.enabled_roles`)
- `scope`: what this worker owns (used for routing)
- `parent` / `children`: org tree links (mirrors `twf spawn`)

## Shared artifacts (task + designs)

Within the same share dir as `registry.json`, this skill also standardizes:
- Shared task: `share/task.md` (written by `atwf init ...`)
- Per-member designs: `share/design/<full>.md` (create via `atwf design-init[-self]`)
- Consolidated design: `share/design.md` (PM owns the final merged version)
- Ops environment docs:
  - `share/ops/env.md`
  - `share/ops/host-deps.md` (records any host-level installs like `apt`/`curl` downloads)

## Quick start

Initialize + start the initial trio + send task to PM:
- `bash .codex/skills/ai-team-workflow/scripts/atwf init "任务描述：/path/to/task.md"`
  - starts root: `coord-main`
  - spawns under root: `pm-main`, `liaison-main`
  - copies the task into `share/task.md`, sends PM the shared path, and prints PM's first reply
  - starts a background sidecar: `atwf watch-idle` (tmux session `atwf-watch-idle-*`) to wake `idle` workers when inbox has unread; `atwf pause` disables watcher actions via `share/.paused`
  - note: `atwf pause` stops the watcher session; `atwf unpause` restarts it (so code/config updates take effect)

Enter a role (avoid `tmux a` attaching the wrong session):
- `bash .codex/skills/ai-team-workflow/scripts/atwf attach pm`

View org/dependency tree:
- `bash .codex/skills/ai-team-workflow/scripts/atwf tree`

If you only want to create the registry (no workers):
- `bash .codex/skills/ai-team-workflow/scripts/atwf init --registry-only`

If you copied this skill from another repo and `init` reuses stale workers:
- Delete runtime state under this skill’s `share/` (especially `share/registry.json`) and rerun `init`, or
- Run `bash .codex/skills/ai-team-workflow/scripts/atwf init --force-new` to start a fresh trio.

Create an architect under PM:
- preferred: PM runs inside its tmux: `bash .codex/skills/ai-team-workflow/scripts/atwf spawn-self arch user --scope "user module design + task breakdown"`

Create an ops under PM (environment owner):
- preferred: PM runs inside its tmux: `bash .codex/skills/ai-team-workflow/scripts/atwf spawn-self ops env --scope "local Docker + docker-compose environment management"`

Create execution roles under an architect:
- preferred: the architect runs inside its tmux:
  - `bash .codex/skills/ai-team-workflow/scripts/atwf spawn-self dev backend --scope "backend implementation for user module"`
  - `bash .codex/skills/ai-team-workflow/scripts/atwf spawn-self qa user --scope "testing for user module"`
  - `bash .codex/skills/ai-team-workflow/scripts/atwf spawn-self prod user --scope "requirements for user module"`

Inspect and route:
- `bash .codex/skills/ai-team-workflow/scripts/atwf list`
- `bash .codex/skills/ai-team-workflow/scripts/atwf tree pm`
- `bash .codex/skills/ai-team-workflow/scripts/atwf route "login" --role dev`
- `bash .codex/skills/ai-team-workflow/scripts/atwf resolve pm`  # print PM full name

Disband the whole team (requires PM full name):
- `bash .codex/skills/ai-team-workflow/scripts/atwf remove <pm-full>`
  - find `<pm-full>` via: `bash .codex/skills/ai-team-workflow/scripts/atwf list`

## Reporting (mandatory)

Completion/progress must flow upward:
- If you hire subordinates, you are responsible for collecting their reports and then reporting *up* only when the whole subtree is done.
- Default chains: `dev/prod/qa -> arch -> pm -> (coord + liaison) -> user`; `ops -> pm -> (coord + liaison) -> user`.

Helpers (run inside tmux worker):
- `bash .codex/skills/ai-team-workflow/scripts/atwf parent-self`
- `bash .codex/skills/ai-team-workflow/scripts/atwf report-up "done summary..."`
- PM reports upward to Coordinator via `report-up`; user-facing updates are sent to Liaison:
  - internal (to parent): `bash .codex/skills/ai-team-workflow/scripts/atwf report-up "status update..."`
  - user-facing (to liaison): `bash .codex/skills/ai-team-workflow/scripts/atwf report-to liaison "status update for user..."`

## Operating rules (role protocol)

- Team members **do not ask the user directly**.
- When blocked:
  1. Ask **Coordinator**: “Who should I talk to?” / “Is this internal or user-facing?”
  2. Coordinator routes to the best owner using `registry.json` (`atwf route ...`).
  3. If cross-branch communication is needed, Coordinator creates a **handoff** so the two members talk directly (avoid relaying): `atwf handoff ...`
  4. Only if a real **user decision** is required, Coordinator escalates a crisp question to **Liaison**.
  5. Liaison asks the user, then reports back to Coordinator (who distributes).

User “bounce” rule (assistant is a relay):
- If the user responds with “I don’t understand / shouldn’t this be answerable from docs?”, Liaison does **not** validate internally.
- Liaison sends a `[USER-BOUNCE]` back; Coordinator routes it back down to the originator to self-confirm using existing docs (task/design/MasterGo assets).
- Only re-escalate to the user when a real **user decision** is required.

## Design → Development workflow (required)

1. Everyone reads the shared task: `share/task.md`.
2. Everyone writes a per-scope design doc under `share/design/`:
   - inside tmux: `bash .codex/skills/ai-team-workflow/scripts/atwf design-init-self`
3. Bottom-up consolidation:
   - interns → dev → arch → pm
4. After PM finishes the consolidated design (`share/design.md`) and confirms “no conflicts”, PM announces **START DEV**.
5. Each `dev-*` (including interns) creates a dedicated git worktree (no work on current branch):
   - inside tmux: `bash .codex/skills/ai-team-workflow/scripts/atwf worktree-create-self`
   - then: `cd <git-root>/worktree/<your-full-name>`
6. Implement + commit + report upward with verification steps. Parent integrates subtree first; PM integrates last.

## Conflict resolution protocol (ordered loop)

For design conflicts or merge conflicts within a subtree:
- Parent selects the conflicting participants (N people) and assigns an order `1..N`.
- Use a strict “token passing” loop: only the current number speaks; after speaking they message the next number.
- When the last (`N`) finishes, loop back to `1`. If `1` declares the conflict resolved, `1` summarizes and reports up; otherwise continue the loop.
- Keep everyone in sync. If broadcast-style messaging is restricted by policy, ask Coordinator to send a `notice` to the right subtree/role (or use direct messages / handoff).

## Commands

All commands are wrappers around `twf` plus registry management:
- `bash .codex/skills/ai-team-workflow/scripts/atwf init ["task"] [--task-file PATH] [--registry-only]`
- `bash .codex/skills/ai-team-workflow/scripts/atwf up <role> [label] --scope "..."` (root_role only; start + register + bootstrap)
- `bash .codex/skills/ai-team-workflow/scripts/atwf spawn <parent-full> <role> [label] --scope "..."` (spawn child + register + bootstrap)
- `bash .codex/skills/ai-team-workflow/scripts/atwf spawn-self <role> [label] --scope "..."` (inside tmux; uses current worker as parent)
- `bash .codex/skills/ai-team-workflow/scripts/atwf parent <name|full>`
- `bash .codex/skills/ai-team-workflow/scripts/atwf parent-self`
- `bash .codex/skills/ai-team-workflow/scripts/atwf children <name|full>`
- `bash .codex/skills/ai-team-workflow/scripts/atwf children-self`
- `bash .codex/skills/ai-team-workflow/scripts/atwf report-up ["message"]` (inside tmux; stdin supported)
- `bash .codex/skills/ai-team-workflow/scripts/atwf report-to <full|base|role> ["message"]` (inside tmux; stdin supported)
- `bash .codex/skills/ai-team-workflow/scripts/atwf list`
- `bash .codex/skills/ai-team-workflow/scripts/atwf where`
- `bash .codex/skills/ai-team-workflow/scripts/atwf policy`
- `bash .codex/skills/ai-team-workflow/scripts/atwf perms-self`
- `bash .codex/skills/ai-team-workflow/scripts/atwf tree [root]`
- `bash .codex/skills/ai-team-workflow/scripts/atwf design-path <full|base|role>`
- `bash .codex/skills/ai-team-workflow/scripts/atwf design-init <full|base|role> [--force]`
- `bash .codex/skills/ai-team-workflow/scripts/atwf design-init-self [--force]`
- `bash .codex/skills/ai-team-workflow/scripts/atwf worktree-path <full|base|role>`
- `bash .codex/skills/ai-team-workflow/scripts/atwf worktree-create <full|base|role> [--base REF] [--branch BR]`
- `bash .codex/skills/ai-team-workflow/scripts/atwf worktree-create-self [--base REF] [--branch BR]`
- `bash .codex/skills/ai-team-workflow/scripts/atwf worktree-check-self`
- `bash .codex/skills/ai-team-workflow/scripts/atwf stop [--role ROLE|--subtree ROOT|targets...]`
- `bash .codex/skills/ai-team-workflow/scripts/atwf resume [--role ROLE|--subtree ROOT|targets...]`
- `bash .codex/skills/ai-team-workflow/scripts/atwf pause [--role ROLE|--subtree ROOT|targets...] [--reason "..."]` (human pause; writes `share/.paused` and stops the watcher session)
- `bash .codex/skills/ai-team-workflow/scripts/atwf unpause [--role ROLE|--subtree ROOT|targets...]` (human unpause; clears `share/.paused` and restarts watcher so updates take effect)
- `bash .codex/skills/ai-team-workflow/scripts/atwf notice [--role ROLE|--subtree ROOT|targets...] --message "..."` (or stdin; FYI; no reply expected)
- `bash .codex/skills/ai-team-workflow/scripts/atwf action [--role ROLE|--subtree ROOT|targets...] --message "..."` (or stdin; instruction/task; report deliverables when done)
- `bash .codex/skills/ai-team-workflow/scripts/atwf receipts <msg-id> [--role ROLE|--subtree ROOT|targets...]` (read receipts for notice/any msg-id)
- `bash .codex/skills/ai-team-workflow/scripts/atwf resolve <full|base|role>`
- `bash .codex/skills/ai-team-workflow/scripts/atwf attach <full|base|role>`
- `bash .codex/skills/ai-team-workflow/scripts/atwf route "<query>" [--role <role>]`
- `bash .codex/skills/ai-team-workflow/scripts/atwf ask <full|base|role> ["message"]` (stdin supported)
- Legacy (operator-only; disabled inside worker tmux):
  - `bash .codex/skills/ai-team-workflow/scripts/atwf send <full|base|role> ["message"]`
  - `bash .codex/skills/ai-team-workflow/scripts/atwf broadcast [--role ROLE|--subtree ROOT|targets...] --message "..."` (or stdin)
- `bash .codex/skills/ai-team-workflow/scripts/atwf gather <a> <b> ... --message "..."` (stdin supported; reply-needed fan-in)
- `bash .codex/skills/ai-team-workflow/scripts/atwf respond <req-id> ["message"]` (stdin supported; reply-needed response)
- `bash .codex/skills/ai-team-workflow/scripts/atwf reply-needed [--target <full|base|role>]` (list pending reply-needed)
- `bash .codex/skills/ai-team-workflow/scripts/atwf request <req-id>` (show request status/paths)
- `bash .codex/skills/ai-team-workflow/scripts/atwf handoff <a> <b> [--reason "..."] [--ttl SECONDS]`
- `bash .codex/skills/ai-team-workflow/scripts/atwf pend <full|base|role> [N]`
- `bash .codex/skills/ai-team-workflow/scripts/atwf ping <full|base|role>`
- `bash .codex/skills/ai-team-workflow/scripts/atwf drive [running|standby]` (drive mode lives in config; watcher hot-reloads; setting mode must be outside worker tmux)
- `bash .codex/skills/ai-team-workflow/scripts/atwf state [target]`
- `bash .codex/skills/ai-team-workflow/scripts/atwf state-self`
- `bash .codex/skills/ai-team-workflow/scripts/atwf state-set-self <working|draining|idle>` (debug only; watcher overwrites)
- `bash .codex/skills/ai-team-workflow/scripts/atwf watch-idle [--interval S] [--delay S] [--once]`
- `bash .codex/skills/ai-team-workflow/scripts/atwf remove <pm-full>` (disband team; clears registry)

## Environment knobs

- `AITWF_TWF`: path to `twf` (if not installed next to this skill)
- `AITWF_DIR`: override shared state dir
- `AITWF_REGISTRY`: override registry file path
- Config file: `.codex/skills/ai-team-workflow/scripts/atwf_config.yaml` (`share.dir`, legacy: `share_dir`; team policy under `team.policy`)
