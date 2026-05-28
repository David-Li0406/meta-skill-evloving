---
name: kamal
description: Deploy Rails apps with Kamal. Use when setting up Kamal, configuring deploy.yml, managing secrets, or running deploy/rollback commands.
version: 1.0.0
---

# Kamal

Use Kamal to deploy Rails applications with repeatable, safe workflows.

## Install and Initialize

- Install: `gem install kamal`
- Initialize in app: `kamal init`
  - Creates `config/deploy.yml` and `.kamal/secrets`

## Deploy Workflow

1. Run `kamal setup` for first deploys or new servers.
2. Use `kamal deploy` for routine releases.
3. Use `kamal rollback [VERSION]` for fast recovery.

## Common Commands

- Help: `kamal --help`
- Show merged config: `kamal config`
- Deploy: `kamal deploy`
- Redeploy without bootstrap: `kamal redeploy`
- Rollback: `kamal rollback [VERSION]`
- Remove app/proxy/accessories: `kamal remove`
- Cleanup: `kamal prune`
- Manage app: `kamal app` (see `kamal app --help`)
- Manage accessories: `kamal accessory` (see `kamal accessory --help`)
- Manage proxy: `kamal proxy`
- Server bootstrap only: `kamal server`

## Secrets

- Keep secrets in `.kamal/secrets` or environment variables.
- Example entries in `.kamal/secrets`:

```
DATABASE_URL=postgres://...
RAILS_MASTER_KEY=...
```

Note: `kamal config` prints merged config including secrets.
