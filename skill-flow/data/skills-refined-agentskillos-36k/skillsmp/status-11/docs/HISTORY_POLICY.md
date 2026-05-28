History directory policy

This repository tracks a history/ directory for runbooks, design notes, and ephemeral planning artifacts that are useful to keep in the repo for collaboration and audit.

Policy summary

- Keep the history/ directory tracked in git so collaborators can see planning and runbook documents.
- Do not commit large automatic snapshots produced by tooling. Files matching the pattern history/ooda_snapshot_*.jsonl are ignored by .gitignore and should remain out of source control.
- A subdirectory history/opencode-restored/ is also ignored by default (local restore artifacts).

If you need to persist a specific snapshot, move it out of the snapshot pattern (rename or copy into a tracked path) or add an explicit exception with approval from the repo owners.

Rationale

- Balances the need to preserve useful documentation with the risk of committing large, ephemeral files that bloat the repo.

This file documents the change proposed in PR #137: ensure only history snapshot files are ignored while the rest of history/ remains tracked.
