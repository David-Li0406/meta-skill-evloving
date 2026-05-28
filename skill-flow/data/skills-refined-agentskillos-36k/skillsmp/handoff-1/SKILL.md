---
name: handoff
description: Prepare handoff: update HANDOFF/REPO_MAP, rotate logs, update .gitignore if needed, and create a safe handoff git commit.
---

When invoked, do this in order.

A) Documentation and state (must do)
1) Update `HANDOFF.md`:
   - Fill/refresh every section.
   - Include concrete evidence: file paths and (if a commit is created) the commit hash.

2) Update `REPO_MAP.md` only if needed:
   - new important file/dir/entrypoint created
   - important file moved/renamed
   - canonical commands/entrypoints changed
   - focus area ("hot paths") changed

3) Ensure `.gitignore` stays strict for competition data, runs, and artifacts.

B) Log rotation (must do)
1) Determine next log filename:
   - `agent_logs/YYYY-MM-DD_agentNN.md`, where NN is 00, 01, 02, ... chosen as the next unused number for today.
2) Move `agent_logs/current.md` -> that filename.
3) Append a one-line entry to `agent_logs/INDEX.md`:
   - `- YYYY-MM-DD_agentNN.md — <short summary> (optional: commit <hash>)`
4) Create a fresh `agent_logs/current.md`.

C) Safe handoff commit (must do, unless safety checks fail)
Before committing, always show:
- `git status`
- `git diff --stat`

Never commit competition data, runs, artifacts, or secrets (see `.gitignore`).

Commit message:
- `agentNN: handoff(<area>): <short description>`
- Derive `agentNN` from `agent_logs/current.md` (field `id:`). If missing, stop and ask the human.
- Choose `<area>` from: `workflow`, `docs`, `orchestrator`, `competitions`, `prompts`, `ci`, `misc`.
