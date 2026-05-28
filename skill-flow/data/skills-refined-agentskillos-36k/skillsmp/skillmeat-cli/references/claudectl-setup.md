# claudectl Setup Guide

`claudectl` is a simplified alias for SkillMeat with smart defaults for power users.

---

## Quick Setup

### Option 1: Simple Alias (Recommended)

Add to your shell configuration (`~/.bashrc`, `~/.zshrc`, or `~/.config/fish/config.fish`):

**Bash/Zsh:**
```bash
alias claudectl='skillmeat'
```

**Fish:**
```fish
alias claudectl 'skillmeat'
```

After adding, reload your shell:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Option 2: Wrapper Script with Smart Defaults

Create `~/.local/bin/claudectl`:

```bash
#!/bin/bash
# claudectl - SkillMeat with smart defaults
#
# Smart defaults:
# - --type skill (when not specified)
# - --project . (current directory)
# - --format json (when piped) or table (when tty)

set -e

# Detect if output is piped
if [ -t 1 ]; then
    FORMAT_FLAG=""
else
    FORMAT_FLAG="--json"
fi

# Map simplified commands to full commands
case "$1" in
    add)
        # claudectl add pdf → skillmeat add skill anthropics/skills/pdf
        shift
        ARTIFACT="$1"
        shift
        if [[ "$ARTIFACT" != */* ]]; then
            # Assume official source if no path
            ARTIFACT="anthropics/skills/$ARTIFACT"
        fi
        exec skillmeat add skill "$ARTIFACT" "$@"
        ;;
    deploy)
        # claudectl deploy pdf → skillmeat deploy pdf --project .
        shift
        exec skillmeat deploy "$@" --project .
        ;;
    search)
        # claudectl search query → skillmeat search query --type skill
        shift
        exec skillmeat search "$@" --type skill $FORMAT_FLAG
        ;;
    status)
        # claudectl status → skillmeat list --project . --json
        exec skillmeat list --project . --json
        ;;
    sync)
        # claudectl sync → skillmeat sync --all
        exec skillmeat sync --all
        ;;
    bundle)
        # claudectl bundle name → skillmeat bundle create name
        shift
        exec skillmeat bundle create "$@"
        ;;
    import)
        # claudectl import file → skillmeat bundle import file
        shift
        exec skillmeat bundle import "$@"
        ;;
    *)
        # Pass through all other commands
        exec skillmeat "$@"
        ;;
esac
```

Make it executable:
```bash
chmod +x ~/.local/bin/claudectl
```

Ensure `~/.local/bin` is in your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

---

## Command Mappings

| claudectl | Full Command |
|-----------|--------------|
| `claudectl add pdf` | `skillmeat add skill anthropics/skills/pdf` |
| `claudectl add user/repo/skill` | `skillmeat add skill user/repo/skill` |
| `claudectl deploy pdf` | `skillmeat deploy pdf --project .` |
| `claudectl search database` | `skillmeat search database --type skill` |
| `claudectl status` | `skillmeat list --project . --json` |
| `claudectl sync` | `skillmeat sync --all` |
| `claudectl bundle my-setup` | `skillmeat bundle create my-setup` |
| `claudectl import setup.zip` | `skillmeat bundle import setup.zip` |
| `claudectl <anything-else>` | `skillmeat <anything-else>` |

---

## Tab Completion

### Bash Completion

Add to `~/.bashrc`:

```bash
_claudectl_completions() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local prev="${COMP_WORDS[COMP_CWORD-1]}"

    case "$prev" in
        claudectl)
            COMPREPLY=($(compgen -W "add deploy search status sync bundle import list show remove undeploy diff update config collection mcp web" -- "$cur"))
            ;;
        add|deploy|remove|undeploy|show|diff|update)
            # Complete with artifact names from collection
            local artifacts=$(skillmeat list --json 2>/dev/null | jq -r '.[].name' 2>/dev/null)
            COMPREPLY=($(compgen -W "$artifacts" -- "$cur"))
            ;;
        collection)
            COMPREPLY=($(compgen -W "create list use delete" -- "$cur"))
            ;;
        *)
            COMPREPLY=()
            ;;
    esac
}

complete -F _claudectl_completions claudectl
```

### Zsh Completion

Add to `~/.zshrc`:

```zsh
_claudectl() {
    local -a commands
    commands=(
        'add:Add artifact to collection'
        'deploy:Deploy artifact to project'
        'search:Search for artifacts'
        'status:Show project status'
        'sync:Sync collection with upstream'
        'bundle:Create artifact bundle'
        'import:Import artifact bundle'
        'list:List artifacts'
        'show:Show artifact details'
        'remove:Remove artifact from collection'
        'undeploy:Remove artifact from project'
    )

    _describe 'command' commands
}

compdef _claudectl claudectl
```

### Fish Completion

Create `~/.config/fish/completions/claudectl.fish`:

```fish
complete -c claudectl -n __fish_use_subcommand -a add -d 'Add artifact to collection'
complete -c claudectl -n __fish_use_subcommand -a deploy -d 'Deploy artifact to project'
complete -c claudectl -n __fish_use_subcommand -a search -d 'Search for artifacts'
complete -c claudectl -n __fish_use_subcommand -a status -d 'Show project status'
complete -c claudectl -n __fish_use_subcommand -a sync -d 'Sync collection with upstream'
complete -c claudectl -n __fish_use_subcommand -a bundle -d 'Create artifact bundle'
complete -c claudectl -n __fish_use_subcommand -a import -d 'Import artifact bundle'
```

---

## Usage Examples

### Daily Workflow

```bash
# Start of day - sync everything
claudectl sync

# Find a skill
claudectl search "pdf processing"

# Add and deploy
claudectl add pdf
claudectl deploy pdf

# Check what's deployed
claudectl status
```

### Sharing Setup

```bash
# Create bundle of current collection
claudectl bundle team-setup

# Share the file, colleague imports:
claudectl import team-setup.zip
```

### Quick Status Check

```bash
# JSON output for scripting
claudectl status | jq '.[] | .name'

# Count deployed artifacts
claudectl status | jq 'length'
```

---

## Troubleshooting

### Command Not Found

Ensure `~/.local/bin` is in PATH:
```bash
echo $PATH | tr ':' '\n' | grep local
```

If not present, add to shell config:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Permission Denied

Make script executable:
```bash
chmod +x ~/.local/bin/claudectl
```

### SkillMeat Not Found

Ensure SkillMeat is installed:
```bash
which skillmeat
# Should show: /path/to/skillmeat

# If not installed:
pip install skillmeat
# or
uv tool install skillmeat
```

---

## Customization

### Change Default Source

Edit the wrapper script to use a different default source:

```bash
# Change this line:
ARTIFACT="anthropics/skills/$ARTIFACT"

# To your preferred source:
ARTIFACT="your-org/skills/$ARTIFACT"
```

### Add Custom Commands

Add new cases to the wrapper script:

```bash
    my-command)
        # claudectl my-command → custom behavior
        shift
        exec skillmeat some-complex-command --with --flags "$@"
        ;;
```

---

## Comparison: claudectl vs skillmeat

| Aspect | claudectl | skillmeat |
|--------|-----------|-----------|
| Target user | Power users | All users |
| Defaults | Smart (current project, skill type) | Explicit |
| Output | Auto-detect JSON/table | Explicit flag |
| Commands | Simplified | Full |
| Use case | Quick operations | Full control |
