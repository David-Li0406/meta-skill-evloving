---
name: dotfiles
description: Update home-manager/dotfiles configuration. Use when asked to bump dotfiles, update home-config, refresh home-manager, or similar requests about the dev environment configuration.
---

# Dotfiles / Home-Manager Update

Updates the home-manager configuration (dotfiles) for the dev-sandbox environment. The `home-config` input in `clusters/bedlam/flake.nix` points to `github:gisikw/config`.

## Steps

### 1. Update the cluster flake input

```bash
nix flake update home-config --flake ./clusters/bedlam
```

Updates `clusters/bedlam/flake.lock` with the latest commit.

### 2. Update ratched's flake lock

```bash
nix flake update --flake ./clusters/bedlam/hosts/ratched
```

Even though ratched has `home-config.follows = "cluster/home-config"`, each flake's lock captures its own resolved state. Cannot use `nix flake update home-config` here since `home-config` is a `follows` directive, not a direct input.

### 3. Commit and push

```bash
git add clusters/bedlam/flake.lock clusters/bedlam/hosts/ratched/flake.lock
git commit -m "chore: Bump home-config to <short-sha>"
git push
```

### 4. Deploy

```bash
just deploy ratched
```

Waits for comin to fetch, build, and activate. Dev environment will have updated dotfiles after completion.
