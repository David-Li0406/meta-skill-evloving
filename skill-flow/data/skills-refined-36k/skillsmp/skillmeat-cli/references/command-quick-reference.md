# SkillMeat CLI Quick Reference

Condensed command reference for the skillmeat-cli skill.

---

## Command Groups Overview

| Group | Purpose | Key Commands |
|-------|---------|--------------|
| (root) | Core operations | `add`, `deploy`, `list`, `show`, `search` |
| `collection` | Multi-collection | `create`, `list`, `use` |
| `mcp` | MCP servers | `add`, `remove`, `list`, `enable`, `disable` |
| `bundle` | Sharing | `create`, `import`, `list` |
| `sign` | Security | `create`, `verify`, `list-keys` |
| `sync` | Updates | `(default)`, `--all`, `--dry-run` |
| `diff` | Changes | `artifact`, `collection`, `project` |
| `config` | Settings | `get`, `set`, `list` |
| `web` | Web UI | `dev`, `build`, `start`, `doctor` |
| `analytics` | Usage | `summary`, `trends`, `export` |
| `cache` | Performance | `clear`, `stats`, `config` |
| `vault` | Team sharing | `create`, `add`, `pull`, `push` |
| `context` | Context entities | `add`, `remove`, `list`, `show`, `sync` |

---

## Core Commands

### Search & Discovery

```bash
# Search all sources
skillmeat search "<query>"
skillmeat search "pdf" --type skill
skillmeat search "database" --type agent

# List artifacts
skillmeat list                    # All in collection
skillmeat list --type skill       # Filter by type
skillmeat list --project .        # Deployed in project
skillmeat list --json             # JSON output

# Show details
skillmeat show <artifact-name>
skillmeat show canvas-design --full
```

### Adding Artifacts

```bash
# Add skill
skillmeat add skill <source>
skillmeat add skill anthropics/skills/canvas-design
skillmeat add skill anthropics/skills/pdf@v1.0.0
skillmeat add skill user/repo/path/to/skill

# Add other types
skillmeat add command <source>
skillmeat add agent <source>
skillmeat add mcp <source>

# Options
--collection <name>    # Target collection
--alias <name>         # Local alias
--force                # Overwrite existing
```

### Deploying Artifacts

```bash
# Deploy to project
skillmeat deploy <artifact-name>
skillmeat deploy canvas-design
skillmeat deploy pdf --project /path/to/project

# Options
--project <path>       # Target project (default: .)
--force                # Overwrite existing
--dry-run              # Preview changes
```

### Updating & Syncing

```bash
# Check for updates
skillmeat diff <artifact-name>
skillmeat diff --all

# Update
skillmeat update <artifact-name>
skillmeat sync                    # Sync collection
skillmeat sync --all              # Sync everything

# Options
--dry-run              # Preview changes
--force                # Force update
```

### Removing Artifacts

```bash
# Remove from collection
skillmeat remove <artifact-name>
skillmeat remove canvas-design

# Undeploy from project
skillmeat undeploy <artifact-name>
skillmeat undeploy canvas-design --project .

# Options
--force                # Skip confirmation
--keep-data            # Keep local data
```

---

## Collection Management

```bash
# List collections
skillmeat collection list

# Create collection
skillmeat collection create <name>
skillmeat collection create work --description "Work artifacts"

# Switch collection
skillmeat collection use <name>
skillmeat collection use personal

# Delete collection
skillmeat collection delete <name> --force
```

---

## Bundle Operations

```bash
# Create bundle
skillmeat bundle create <name>
skillmeat bundle create my-setup
skillmeat bundle create my-setup --include skill,command

# Import bundle
skillmeat bundle import <file>
skillmeat bundle import setup.zip
skillmeat bundle import setup.zip --dry-run

# List bundles
skillmeat bundle list

# Sign bundle
skillmeat sign create <bundle>
skillmeat sign verify <bundle>
```

---

## MCP Server Management

```bash
# Add MCP server
skillmeat mcp add <name> <command>
skillmeat mcp add sqlite "uvx mcp-server-sqlite"

# List MCP servers
skillmeat mcp list

# Enable/disable
skillmeat mcp enable <name>
skillmeat mcp disable <name>

# Remove
skillmeat mcp remove <name>
```

---

## Configuration

```bash
# View config
skillmeat config list
skillmeat config get <key>

# Set config
skillmeat config set <key> <value>
skillmeat config set github-token ghp_xxxxx
skillmeat config set default-collection work

# Common settings
github-token           # GitHub API token
default-collection     # Default collection name
auto-sync              # Auto-sync on start
```

---

## Web Interface

```bash
# Development
skillmeat web dev              # Start dev servers
skillmeat web dev --api-only   # API only
skillmeat web dev --web-only   # Frontend only

# Production
skillmeat web build            # Build for production
skillmeat web start            # Start production servers

# Diagnostics
skillmeat web doctor           # Check environment
```

---

## Output Formats

Most commands support `--json` for machine-readable output:

```bash
skillmeat list --json
skillmeat search "pdf" --json
skillmeat show canvas-design --json
```

---

## Common Workflows

### Set Up New Project

```bash
skillmeat init                           # Initialize in project
skillmeat search "react"                 # Find relevant skills
skillmeat add skill anthropics/skills/frontend-design
skillmeat deploy frontend-design
```

### Share Your Setup

```bash
skillmeat bundle create my-team-setup    # Create bundle
skillmeat sign create my-team-setup.zip  # Sign it
# Share the .zip file
```

### Import Colleague's Setup

```bash
skillmeat bundle import colleague-setup.zip
skillmeat sign verify colleague-setup.zip  # Verify signature
skillmeat deploy --all                     # Deploy everything
```

### Keep Everything Updated

```bash
skillmeat diff --all                     # Check for updates
skillmeat sync --all                     # Update everything
```

---

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 1 | General error | Check error message |
| 2 | Not found | Verify artifact name |
| 3 | Permission denied | Check file permissions |
| 4 | Rate limited | Set GitHub token |
| 5 | Network error | Check connectivity |

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `SKILLMEAT_HOME` | Collection directory (default: `~/.skillmeat`) |
| `SKILLMEAT_CONFIG` | Config file path |
| `GITHUB_TOKEN` | GitHub API token |
| `NO_COLOR` | Disable colored output |
