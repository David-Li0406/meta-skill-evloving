---
name: agpm-usage
description: How to use AGPM (Agent Package Manager) to install and manage AI coding tool artifacts like skills, commands, and hooks. Use this skill when the user wants to install skills, manage artifact sources, or configure AGPM in their project.
license: MIT
metadata:
  author: K42
  version: "0.1.0"
---

# AGPM - Agent Package Manager

AGPM is a universal package manager for AI coding tool artifacts (skills, commands, hooks). It manages artifacts from git repos and installs them to multiple AI tool targets.

## Quick Start

```bash
# Initialize a new project
agpm init

# Add a skill from a source
agpm add anthropics/skills pdf

# Install all configured artifacts
agpm install

# List installed artifacts
agpm list
```

## Commands

| Command | Description |
|---------|-------------|
| `agpm add <source> [artifact[@version]]` | Add an artifact to agpm.json |
| `agpm install` | Install artifacts to target directories |
| `agpm list` | Show configured artifacts and status |
| `agpm remove <artifact>` | Remove an artifact |
| `agpm update [artifact]` | Update lock file to latest SHAs |
| `agpm source add <repo>` | Add a source repository |
| `agpm source list` | List configured sources |
| `agpm source remove <repo>` | Remove a source |
| `agpm source discover <repo>` | Show available artifacts in a source |

## Source Formats

The `<source>` argument accepts:
- `owner/repo` - GitHub shorthand
- `owner/repo#subpath` - With subpath
- `https://github.com/owner/repo` - Full URL

## Version Pinning

Artifacts can be pinned to specific versions:

```bash
agpm add anthropics/skills pdf@v1.0.0    # Pin to tag
agpm add anthropics/skills pdf@main       # Pin to branch
agpm add anthropics/skills pdf@abc123     # Pin to SHA
```

Without a version, artifacts track HEAD.

## Configuration Files

### agpm.json

User-edited config declaring targets, sources, and artifacts:

```json
{
  "$schema": "https://agpm.dev/schemas/agpm.json",
  "targets": {
    "claude-code": true,
    "opencode": true
  },
  "sources": [
    {
      "name": "anthropics/skills",
      "url": "https://github.com/anthropics/skills.git"
    }
  ],
  "artifacts": [
    "anthropics/skills/pdf",
    "anthropics/skills/docx@main"
  ],
  "collections": []
}
```

### Supported Targets

| Target | Base Path | Description |
|--------|-----------|-------------|
| `claude-code` | `.claude` | Claude Code CLI |
| `opencode` | `.opencode` | OpenCode |
| `codex` | `.codex` | Codex |

Target values can be:
- `true` - Enable target
- `{}` - Enable target (allows future options)
- `false` - Disable target

### agpm-lock.json

Auto-generated lock file pinning artifacts to git SHAs:

```json
{
  "$schema": "https://agpm.dev/schemas/agpm-lock.json",
  "version": 1,
  "artifacts": {
    "anthropics/skills/pdf": {
      "sha": "69c0b1a0674149f27b61b2635f935524b6add202",
      "integrity": "sha256-Wu/6igdMZY2jlV7XESCt6/VyMFuXcXiz9F8z7URlZk8=",
      "path": "skills/pdf",
      "ref": "main",
      "metadata": {
        "name": "pdf",
        "description": "PDF manipulation toolkit..."
      }
    }
  }
}
```

## Common Workflows

### Adding Skills to a Project

```bash
# 1. Initialize if needed
agpm init

# 2. Discover available artifacts in a source
agpm source discover anthropics/skills

# 3. Add the artifacts you want
agpm add anthropics/skills pdf
agpm add anthropics/skills docx

# 4. Install to your targets
agpm install
```

### Updating Artifacts

```bash
# Update all artifacts to latest versions
agpm update
agpm install

# Update a specific artifact
agpm update anthropics/skills/pdf
agpm install
```

### Managing Sources

```bash
# Add a new source repository
agpm source add owner/repo

# List configured sources
agpm source list

# See what's available in a source
agpm source discover owner/repo

# Remove a source
agpm source remove owner/repo
```

## Storage Model

AGPM stores data in `~/.agpm/`:

```
~/.agpm/
├── repos/github.com/owner/repo/    # Full git repos (for fetching)
└── cache/<sha>/                     # Immutable snapshots at specific SHAs
```

## How Installation Works

1. **Add**: `agpm add` clones the source repo, discovers artifacts, and adds to `agpm.json`
2. **Install**: `agpm install` resolves refs to SHAs, caches at that SHA, and copies to enabled targets
3. **Update**: `agpm update` fetches latest SHAs for each ref and updates `agpm-lock.json`
