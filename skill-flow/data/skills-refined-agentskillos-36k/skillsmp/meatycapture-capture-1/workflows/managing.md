# Managing Projects

Configure MeatyCapture projects, set defaults, and handle auto-detection for seamless agent workflows.

## Skill Configuration

The skill uses `./skill-config.yaml` to store the default project for the current workspace:

```yaml
# ./skill-config.yaml
default_project: "meatycapture"  # Project slug to use by default
auto_detect: true                 # Enable auto-detection if not set
```

### First Run Behavior

When the skill is invoked without a configured project:

1. **Check skill-config.yaml** - If `default_project` is set, use it
2. **Auto-detect** - If `auto_detect: true`, attempt detection (see below)
3. **Prompt user** - If detection fails, ask which project to use or create
4. **Update config** - Save selection to skill-config.yaml for future use

---

## Project Auto-Detection

Strategies to automatically determine the current project:

### Strategy 1: CLAUDE.md Project Name

Extract project name from the CLAUDE.md header:

```bash
PROJECT=$(grep -m1 "^# " ./CLAUDE.md 2>/dev/null | sed 's/^# //' | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
```

### Strategy 2: Git Remote Origin

Parse project name from git remote URL:

```bash
PROJECT=$(git remote get-url origin 2>/dev/null | sed -E 's|.*/(.+)\.git$|\1|' | tr '[:upper:]' '[:lower:]')
```

### Strategy 3: Directory Name

Use current directory name as project slug:

```bash
PROJECT=$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]')
```

### Strategy 4: Environment Variable

Check for explicit environment override:

```bash
PROJECT=${MEATYCAPTURE_PROJECT:-}
```

### Combined Auto-Detection

```bash
# Try each strategy in order
detect_project() {
  # 1. Environment variable
  if [ -n "$MEATYCAPTURE_PROJECT" ]; then
    echo "$MEATYCAPTURE_PROJECT"
    return
  fi

  # 2. CLAUDE.md
  local from_claude=$(grep -m1 "^# " ./CLAUDE.md 2>/dev/null | sed 's/^# //' | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
  if [ -n "$from_claude" ]; then
    echo "$from_claude"
    return
  fi

  # 3. Git remote
  local from_git=$(git remote get-url origin 2>/dev/null | sed -E 's|.*/(.+)\.git$|\1|' | tr '[:upper:]' '[:lower:]')
  if [ -n "$from_git" ]; then
    echo "$from_git"
    return
  fi

  # 4. Directory name fallback
  basename "$(pwd)" | tr '[:upper:]' '[:lower:]'
}

PROJECT=$(detect_project)
```

---

## List Projects

View all registered projects:

```bash
# List all projects
meatycapture project list --json

# List only enabled projects
meatycapture project list --enabled-only --json

# Human-readable table
meatycapture project list --table
```

**Output**:

```json
{
  "projects": [
    {
      "id": "meatycapture",
      "name": "MeatyCapture",
      "path": "/Users/user/.meatycapture/meatycapture",
      "repo_url": "https://github.com/user/meatycapture",
      "enabled": true,
      "is_default": true
    },
    {
      "id": "my-api",
      "name": "My API",
      "path": "/Users/user/.meatycapture/my-api",
      "enabled": true,
      "is_default": false
    }
  ]
}
```

---

## Add New Project

Create a new project in the registry:

```bash
# Basic add
meatycapture project add "My Project" "/path/to/docs" --json

# With custom ID
meatycapture project add "My API" "/path/to/docs" --id my-api --json

# With repo URL
meatycapture project add "My API" "/path/to/docs" --id my-api --repo-url https://github.com/user/my-api --json
```

**Auto-Create on First Capture**:

When capturing to a project that doesn't exist, the skill can auto-create it:

```bash
# Check if project exists
PROJECT="new-project"
EXISTS=$(meatycapture project list --json | jq -r ".projects[] | select(.id == \"$PROJECT\") | .id")

if [ -z "$EXISTS" ]; then
  # Create project with default path
  meatycapture project add "$PROJECT" "$HOME/.meatycapture/$PROJECT" --id "$PROJECT" --json
fi
```

---

## Set Default Project

Set the default project for the CLI:

```bash
# Set default project
meatycapture project set-default PROJECT_ID --json

# Verify
meatycapture project list --json | jq '.projects[] | select(.is_default == true)'
```

---

## Enable/Disable Projects

Temporarily disable projects without removing them:

```bash
# Disable a project
meatycapture project disable PROJECT_ID --json

# Enable a project
meatycapture project enable PROJECT_ID --json
```

---

## Update Project

Modify existing project configuration:

```bash
# Update name
meatycapture project update PROJECT_ID --name "New Name" --json

# Update path
meatycapture project update PROJECT_ID --path /new/path --json

# Update repo URL
meatycapture project update PROJECT_ID --repo-url https://github.com/user/repo --json
```

---

## Skill Config Workflow

### Initial Setup

On first skill use in a workspace:

```bash
# 1. Check if skill-config.yaml exists
if [ ! -f ".claude/skills/meatycapture-capture/skill-config.yaml" ]; then
  # 2. Auto-detect project
  PROJECT=$(detect_project)

  # 3. Check if project exists in registry
  EXISTS=$(meatycapture project list --json | jq -r ".projects[] | select(.id == \"$PROJECT\") | .id")

  if [ -z "$EXISTS" ]; then
    # 4. Create project if needed
    meatycapture project add "$PROJECT" "$HOME/.meatycapture/$PROJECT" --id "$PROJECT"
  fi

  # 5. Update skill config
  cat > ".claude/skills/meatycapture-capture/skill-config.yaml" << EOF
# MeatyCapture Skill Configuration
# Generated on $(date -I)

default_project: "$PROJECT"
auto_detect: false  # Disabled after initial setup
EOF
fi
```

### Using the Config

When the skill is invoked:

```bash
# Read default project from config
DEFAULT_PROJECT=$(yq -r '.default_project' .claude/skills/meatycapture-capture/skill-config.yaml 2>/dev/null)

# Use in commands
meatycapture log list "$DEFAULT_PROJECT" --json
meatycapture log search "query" "$DEFAULT_PROJECT" --json
```

---

## CLI Commands Reference

| Command | Purpose |
|---------|---------|
| `meatycapture project list --json` | List all projects |
| `meatycapture project add <name> <path> --json` | Create project |
| `meatycapture project enable <id> --json` | Enable project |
| `meatycapture project disable <id> --json` | Disable project |
| `meatycapture project update <id> --json` | Update project |
| `meatycapture project set-default <id>` | Set default project |

### Add Options

| Option | Description |
|--------|-------------|
| `--id <slug>` | Custom project ID (slug format) |
| `--repo-url <url>` | Git repository URL |
| `--json` | Output as JSON |

### List Options

| Option | Description |
|--------|-------------|
| `--enabled-only` | Only show enabled projects |
| `--json` | Output as JSON |
| `--table` | Output as table |

---

## Project Path Conventions

Default storage location: `~/.meatycapture/<project-slug>/`

```
~/.meatycapture/
├── meatycapture/
│   ├── REQ-20251229-meatycapture.md
│   └── REQ-20251228-meatycapture.md
├── my-api/
│   └── REQ-20251229-my-api.md
└── projects.json  # Project registry
```

Custom paths can be set per-project for storing logs in project repositories:

```bash
# Store logs in project repo
meatycapture project add "My Project" "./docs/request-logs" --id my-project
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Project not found | List: `meatycapture project list --json` |
| Duplicate project ID | Use unique ID with `--id` flag |
| Path not writable | Check permissions: `stat <path>` |
| Config not loading | Verify YAML syntax in skill-config.yaml |
| Auto-detect fails | Set `default_project` explicitly in config |

See `./references/troubleshooting.md` for detailed solutions.
