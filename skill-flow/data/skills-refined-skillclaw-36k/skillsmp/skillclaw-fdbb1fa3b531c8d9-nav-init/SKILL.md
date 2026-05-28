---
name: nav-init
description: Use this skill to initialize the Navigator documentation structure in a project, setting up necessary directories and configurations.
---

# Navigator Initialization Skill

## Purpose

Creates the Navigator documentation structure (`.agent/`) in a new project, copies templates, and sets up initial configuration.

## When This Skill Auto-Invokes

- "Initialize Navigator in this project"
- "Set up Navigator documentation structure"
- "Create .agent folder for Navigator"
- "Bootstrap Navigator for my project"

## What This Skill Does

1. **Checks if already initialized**: Prevents overwriting existing structure.
2. **Creates `.agent/` directory structure**:
   ```
   .agent/
   ├── DEVELOPMENT-README.md
   ├── .nav-config.json
   ├── tasks/
   ├── system/
   ├── sops/
   │   ├── integrations/
   │   ├── debugging/
   │   ├── development/
   │   └── deployment/
   └── grafana/
       ├── docker-compose.yml
       ├── prometheus.yml
       ├── grafana-datasource.yml
       ├── grafana-dashboards.yml
       ├── navigator-dashboard.json
       └── README.md
   ```
3. **Creates `.claude/` directory with hooks**:
   ```
   .claude/
   └── settings.json    # Token monitoring hook configuration
   ```
4. **Copies templates**: Includes `DEVELOPMENT-README.md`, configuration files, and Grafana setup.
5. **Auto-detects project info**: Extracts project name and tech stack from `package.json` or similar files.
6. **Updates CLAUDE.md**: Adds Navigator-specific instructions to the project.
7. **Creates .gitignore entries**: Excludes temporary Navigator files.

## Execution Steps

### 1. Check if Already Initialized

```bash
if [ -d ".agent" ]; then
    echo "✅ Navigator already initialized in this project"
    echo ""
    echo "To start a session: 'Start my Navigator session'"
    echo "To view documentation: Read .agent/DEVELOPMENT-README.md"
    exit 0
fi
```

### 2. Detect Project Information

Read `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, or similar to extract:
- Project name
- Tech stack
- Dependencies

**Fallback**: Use the current directory name if no config is found.

### 3. Create Directory Structure

Use the Write tool to create:
```
.agent/
.agent/tasks/
.agent/system/
.agent/sops/integrations
```