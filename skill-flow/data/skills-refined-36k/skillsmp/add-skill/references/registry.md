# Skill Registry Reference

Track skills installed via `add-skill` CLI in `registry.json` for long-term maintenance and updates.

**Only record skills installed with `npx add-skill`**. Do not include:
- Local/custom skills
- Plugin skills (from `~/.claude/plugins/`)

## Registry Location

| Scope | Path | Git |
|-------|------|-----|
| Global (user) | `~/.claude/skills/add-skill/registry.json` | N/A |
| Project (me only) | `.claude/skills/add-skill/registry.local.json` | Add to `.gitignore` |
| Project (all users) | `.claude/skills/add-skill/registry.json` | Commit to repo |

## Project Setup

```bash
# Create project registry directory
mkdir -p .claude/skills/add-skill

# For "me only" - add to .gitignore
echo ".claude/skills/add-skill/registry.local.json" >> .gitignore

# For "all users" - commit registry.json to repo
git add .claude/skills/add-skill/registry.json
```

## Registry Format

See `registry.schema.json` for the full JSON Schema definition.

```json
{
  "$schema": "./registry.schema.json",
  "version": "1.0",
  "lastUpdated": "2026-01-16T00:00:00Z",
  "skills": {
    "skill-name": {
      "source": "owner/repo",
      "sourceUrl": "https://github.com/owner/repo",
      "skillPath": "skills/skill-name",
      "installedAt": "2026-01-16T12:30:00Z"
    }
  }
}
```

## Field Reference

| Field | Description |
|-------|-------------|
| `source` | GitHub shorthand (owner/repo) |
| `sourceUrl` | Full Git URL |
| `skillPath` | Path to skill within the repository |
| `installedAt` | Installation timestamp (ISO8601) |

## Post-Installation Workflow

### 1. Install Skill

```bash
# Global
npx add-skill vercel-labs/agent-browser --skill agent-browser --global

# Project
npx add-skill vercel-labs/agent-browser --skill agent-browser
```

### 2. Update Registry

Always list all skills after update:

```bash
# Set registry path based on scope
REGISTRY=~/.claude/skills/add-skill/registry.json          # Global
REGISTRY=.claude/skills/add-skill/registry.json            # Project (all users)
REGISTRY=.claude/skills/add-skill/registry.local.json      # Project (me only)

# Ensure directory exists
mkdir -p "$(dirname "$REGISTRY")"

# Initialize if not exists
[ -f "$REGISTRY" ] || echo '{"$schema":"./registry.schema.json","version":"1.0","skills":{}}' > "$REGISTRY"

# Add skill to registry
jq '.skills["agent-browser"] = {
  "source": "vercel-labs/agent-browser",
  "sourceUrl": "https://github.com/vercel-labs/agent-browser",
  "skillPath": "skills/agent-browser",
  "installedAt": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
} | .lastUpdated = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"' \
"$REGISTRY" > tmp.json && mv tmp.json "$REGISTRY"

# Always list all registered skills after update
jq -r '.skills | to_entries[] | "\(.key): \(.value.sourceUrl)/tree/main/\(.value.skillPath)"' "$REGISTRY"
```

## Updating Installed Skills

Re-install a skill using registry source:

```bash
SOURCE=$(jq -r '.skills["agent-browser"].source' "$REGISTRY")
npx add-skill "$SOURCE" --skill agent-browser --global --yes
```

## Batch Update All Skills

Update all skills from registry:

```bash
for skill in $(jq -r '.skills | keys[]' "$REGISTRY"); do
  SOURCE=$(jq -r ".skills[\"$skill\"].source" "$REGISTRY")
  echo "Updating $skill from $SOURCE..."
  npx add-skill "$SOURCE" --skill "$skill" --global --yes
done
```

## List Registered Skills

```bash
# Pretty list
jq -r '.skills | to_entries[] | "- \(.key): \(.value.source)"' "$REGISTRY"

# With URLs
jq -r '.skills | to_entries[] | "\(.key): \(.value.sourceUrl)/tree/main/\(.value.skillPath)"' "$REGISTRY"
```
