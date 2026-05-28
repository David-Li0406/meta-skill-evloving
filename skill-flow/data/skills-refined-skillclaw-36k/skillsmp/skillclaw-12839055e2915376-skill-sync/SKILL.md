---
name: skill-sync
description: Use this skill when you need to synchronize skill metadata with AGENTS.md Auto-invoke sections after creating or modifying a skill.
---

# Skill body

## Purpose

Keeps AGENTS.md Auto-invoke sections in sync with skill metadata. When you create or modify a skill, run the sync script to automatically update all affected AGENTS.md files.

## Required Skill Metadata

Each skill that should appear in Auto-invoke sections needs these fields in `metadata`.

`auto_invoke` can be either a single string **or** a list of actions:

```yaml
metadata:
  author: your-org
  version: "1.0"
  scope: [root]  # Which AGENTS.md: root, ui, api, sdk

  # Option A: single action
  auto_invoke: "Creating/modifying components"

  # Option B: multiple actions
  # auto_invoke:
  #   - "Creating/modifying components"
  #   - "Refactoring component folder placement"
```

### Scope Values

| Scope        | Updates                 |
| ------------ | ----------------------- |
| `root`       | `AGENTS.md` (repo root) |
| `ui`         | `ui/AGENTS.md`          |
| `api`        | `api/AGENTS.md`         |
| `sdk`        | `sdk/AGENTS.md`         |
| `mcp_server` | `mcp_server/AGENTS.md`  |

Skills can have multiple scopes: `scope: [ui, api]`

## Usage

### After Creating/Modifying a Skill

Run the following command:

```bash
./skills/skill-sync/assets/sync.sh
```

### What It Does

1. Reads all `skills/*/SKILL.md` files.
2. Extracts `metadata.scope` and `metadata.auto_invoke`.
3. Generates Auto-invoke tables for each AGENTS.md.
4. Updates the `### Auto-invoke Skills` section in each file.

## Example

Given this skill metadata:

```yaml
# skills/example-ui/SKILL.md
metadata:
  author: your-org
  version: "1.0"
  scope: [ui]
  auto_invoke: "Creating/modifying React components"
```

The sync script generates in `ui/AGENTS.md`:

```markdown
### Auto-invoke Skills

When performing these actions, ALWAYS invoke the corresponding skill FIRST:

| Action | Skill |
|--------|-------|
| Creating/modifying React components | `example-ui` |
```

## Commands

```bash
# Sync all AGENTS.md files
./skills/skill-sync/assets/sync.sh

# Dry run (show what would change)
./skills/skill-sync/assets/sync.sh --dry-run
```