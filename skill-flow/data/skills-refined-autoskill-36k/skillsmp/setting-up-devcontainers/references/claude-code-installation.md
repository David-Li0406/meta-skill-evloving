# Claude Code Installation Reference

Guide for installing Claude Code CLI in devcontainers.

## Contents

- [Binary Installation](#binary-installation) - installer script usage
- [Directory Structure](#directory-structure) - config and binary locations
- [PATH Configuration](#path-configuration) - environment setup
- [Authentication](#authentication) - login and persistence
- [Plugin Commands](#plugin-commands) - marketplace and plugin management
- [Troubleshooting](#troubleshooting) - common issues

## Binary Installation

Recommended method using official installer:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Binary location**: Always installed to `~/.local/bin/claude`.

**Version options**:
```bash
# Stable (default)
curl -fsSL https://claude.ai/install.sh | bash

# Latest
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Specific version
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```

## Directory Structure

Claude Code uses default paths:

```
~/.local/bin/
└── claude                  # Binary

~/.claude/                  # Config directory
├── .credentials.json       # Auth tokens (after login)
├── settings.json           # User settings
└── plugins/                # Plugin data

~/.local/share/claude/      # Data directory
└── versions/               # Binary versions

~/.claude.json              # Setup state (initial setup completion)
```

## PATH Configuration

Add binary to PATH (always `~/.local/bin`):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

In Dockerfile:
```dockerfile
ENV PATH="/home/vscode/.local/bin:$PATH"
```

In shell scripts (for non-login shells):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Authentication

After installation, user must authenticate:

```bash
claude login
```

This creates `.credentials.json` in `~/.claude/`.

**Persistence**: When using named Docker volumes for `~/.claude/`, credentials persist across container rebuilds.

## Verification

Check installation:

```bash
claude --version
claude doctor
```

## Plugin Commands

```bash
# Add marketplace
claude plugin marketplace add /path/to/marketplace

# Install plugin
claude plugin install plugin-name@marketplace

# List installed
claude plugin list
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `claude: command not found` | Check PATH includes `~/.local/bin` |
| Permission denied on config | Run `sudo chown -R $(id -u):$(id -g) ~/.claude` |
| Install fails in container | Ensure curl and ca-certificates installed |
| Login fails | Check internet access, try `claude doctor` |
| UID/GID 1000 conflict | Use `getent` to check existing users before creating |
| EISDIR on ~/.claude.json | Docker mounted as directory; use symlink instead |
