# Worktree Setup Hook Installation Guide

This guide explains how to install and configure the post-checkout hook for automatic worktree setup.

## Overview

The post-checkout hook automatically configures new git worktrees by:
- Copying environment files (.env, .env.local, etc.)
- Detecting and installing dependencies using the project's package manager
- Running setup scripts if available

## Installation

### Step 1: Locate the Hook Template

The hook template is located at:
```
.cursor/skills/worktree-setup-hook/assets/hook-templates/post-checkout
```

### Step 2: Check for Existing Hook

Before installing, check if a post-checkout hook already exists:

```bash
ls -la .git/hooks/post-checkout
```

### Step 3: Backup Existing Hook (if present)

If a post-checkout hook already exists, create a backup:

```bash
cp .git/hooks/post-checkout .git/hooks/post-checkout.backup
```

### Step 4: Install the Hook

Copy the hook template to your git hooks directory:

```bash
cp .cursor/skills/worktree-setup-hook/assets/hook-templates/post-checkout .git/hooks/post-checkout
chmod +x .git/hooks/post-checkout
```

### Step 5: Verify Installation

Verify the hook is installed and executable:

```bash
ls -la .git/hooks/post-checkout
```

The hook should be executable (have `x` permission).

## How It Works

The hook runs automatically after `git worktree add` completes. It:

1. **Detects new worktrees**: Checks if previous HEAD is the null-ref (`0000000000000000000000000000000000000000`)
2. **Copies environment files**: Looks for `.env.example`, `.env.local.example`, or copies from main worktree
3. **Detects package manager**: Automatically detects project type by checking for:
   - `package.json` → npm/yarn
   - `requirements.txt` → pip
   - `Cargo.toml` → cargo
   - `go.mod` → go
   - `Gemfile` → bundle
4. **Installs dependencies**: Runs the appropriate install command
5. **Runs setup scripts**: Executes `setup.sh` or `scripts/setup.sh` if present

## Customization

### Adding Custom Setup Steps

Edit `.git/hooks/post-checkout` to add custom setup steps. The hook is a standard POSIX shell script.

### Environment File Patterns

The hook looks for these environment files:
- `.env.example` → copies to `.env`
- `.env.local.example` → copies to `.env.local`
- `.env` and `.env.local` from main worktree

To add more patterns, edit the hook script.

## Troubleshooting

### Hook Not Running

1. Verify the hook is executable: `chmod +x .git/hooks/post-checkout`
2. Check git version (requires 2.5+): `git --version`
3. Ensure you're using `git worktree add` (not `--no-checkout`)

### Setup Fails

The hook is designed to be non-blocking. If setup fails, the worktree is still created. Check the output for error messages.

### Conflicts with Existing Hook

If you have an existing post-checkout hook, you can:
1. Merge the hooks manually
2. Use the backup created during installation
3. Append the worktree setup logic to your existing hook

## Uninstallation

To remove the hook:

```bash
rm .git/hooks/post-checkout
```

If you created a backup, restore it:

```bash
mv .git/hooks/post-checkout.backup .git/hooks/post-checkout
```
