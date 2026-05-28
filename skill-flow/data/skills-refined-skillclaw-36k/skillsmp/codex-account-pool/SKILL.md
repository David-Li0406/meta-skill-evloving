---
name: codex-account-pool
description: Pick a CODEX_HOME source and manage an auth/account pool for tmux-workflow workers (balanced or team_cycle), with optional usage watching + rotation.
---

# codex-account-pool

This skill exposes a tiny CLI (`scripts/cap`) that:
- chooses a `CODEX_HOME` **source** directory for a worker (`cap pick`)
- chooses an auth credential file from an **AUTH_TEAM** directory (`cap pick-auth`)

It is designed to be called by `tmux-workflow/scripts/twf` when `twf.account_pool.enabled: true`.

## Configure

Edit `scripts/cap_config.yaml`:
- `sources`: comma-separated list of `CODEX_HOME` template directories (optional; default fallback is `~/.codex`)
- `auth_team_dir`: **required** when using `pick-auth` (should contain multiple auth JSON files; names unrestricted)

`pick-auth` selection algorithm:
- `balanced` (default): pick the **least-used** auth file (counts persisted in `state_file`); if tied, pick randomly
- `team_cycle`: use **one auth for the whole team**, and keep it stable until you advance the pointer
  - good for “roles have uneven load” (avoid wasting accounts)
  - set via `CAP_AUTH_STRATEGY=team_cycle` (or config `auth_strategy: team_cycle`)

## Commands

- Pick a source directory (used by `twf`):
  - `bash .codex/skills/codex-account-pool/scripts/cap pick --worker <full> --base <base>`
- Pick an auth file (used by `twf`):
  - `bash .codex/skills/codex-account-pool/scripts/cap pick-auth --worker <full> --base <base>`
- Print/advance current team auth (team_cycle):
  - `bash .codex/skills/codex-account-pool/scripts/cap auth-current --team-dir /abs/path/to/AUTH_TEAM`
  - `bash .codex/skills/codex-account-pool/scripts/cap auth-advance --team-dir /abs/path/to/AUTH_TEAM`
- Reset the pool state (auth/home counters):
  - `bash .codex/skills/codex-account-pool/scripts/cap reset-state`
- Inspect a whole team’s usage by driving Codex `/status` in tmux (requires `tmux` + `codex`):
  - `bash .codex/skills/codex-account-pool/scripts/cap status /abs/path/to/AUTH_TEAM`
- Watch usage + rotate team auth (team_cycle + ai-team registry):
  - `bash .codex/skills/codex-account-pool/scripts/cap watch-team /abs/path/to/AUTH_TEAM --registry /abs/path/to/registry.json`
- List configured sources:
  - `bash .codex/skills/codex-account-pool/scripts/cap list`
- Inspect resolved config:
  - `bash .codex/skills/codex-account-pool/scripts/cap where`

## tmux-workflow integration

Enable in `tmux-workflow/scripts/twf_config.yaml`:
- `twf.account_pool.enabled: true`

Optional:
- `twf.account_pool.cmd: "/abs/path/to/.codex/skills/codex-account-pool/scripts/cap"`
- or `TWF_ACCOUNT_POOL_CMD=/abs/path/to/cap`

When enabled, `twf` will:
- call `cap pick` to choose `TWF_CODEX_HOME_SRC` (if you didn’t set `TWF_CODEX_HOME_SRC` explicitly)
- call `cap pick-auth` and copy the chosen file into each worker home as `auth.json` (overriding the synced `auth.json`)
