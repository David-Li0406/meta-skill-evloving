---
name: update-target-projects
description: Discover and sync all toolkit-using projects with the latest skills
---

# Update Target Projects

Discover and sync all toolkit-using projects and the Codex CLI skill pack with the latest skills.

## Trigger

Use this skill when:
- The post-commit hook reminds you to sync after skill changes
- You want to batch-sync multiple projects at once
- You need to check which projects are out of date
- You want to update the Codex CLI skill pack

## Configuration

**Codex skill pack location:**
1. `$CODEX_HOME/skills` if `CODEX_HOME` is set
2. `~/.codex/skills` (default)

**Project search paths** (checked in order):
1. `$TOOLKIT_SEARCH_PATH` environment variable (colon-separated paths)
2. `~/Projects` (default)

**Search depth:** 3 levels (finds `~/Projects/*/` and `~/Projects/*/*/`)

## Workflow

### Phase 1: Discover Projects

Find all toolkit-using projects:

```bash
SEARCH_PATH="${TOOLKIT_SEARCH_PATH:-$HOME/Projects}"
TOOLKIT_PATH="$(pwd)"
CURRENT_COMMIT=$(git rev-parse HEAD)

# Find all projects with toolkit-version.json
find "$SEARCH_PATH" -maxdepth 4 -name "toolkit-version.json" -path "*/.claude/*" 2>/dev/null
```

For each discovered project:
1. Read `.claude/toolkit-version.json`
2. Verify `toolkit_location` matches current toolkit (skip if different toolkit)
3. Extract `toolkit_commit` and `last_sync` timestamps

### Phase 1b: Check Codex CLI Skill Pack

Check if the Codex CLI skill pack is installed:

```bash
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
TOOLKIT_SKILLS_DIR="$(pwd)/.claude/skills"

# Dynamically discover all skills from toolkit directory
# This ensures new skills are automatically included
CODEX_SKILLS=($(ls -1 "$TOOLKIT_SKILLS_DIR" | grep -v "^\\."))
```

**Note:** Skills are discovered dynamically from the toolkit's `.claude/skills/` directory.
This ensures new skills are automatically included without updating this document.

For each skill, determine its status:

```bash
check_codex_skill() {
  local skill_name="$1"
  local codex_path="$CODEX_SKILLS_DIR/$skill_name"
  local toolkit_path="$TOOLKIT_SKILLS_DIR/$skill_name"

  if [[ ! -e "$codex_path" ]]; then
    echo "MISSING"
  elif [[ -L "$codex_path" ]]; then
    # It's a symlink - check if it points to our toolkit
    local target=$(readlink "$codex_path")
    if [[ "$target" == "$toolkit_path" || "$target" == *"/.claude/skills/$skill_name" ]]; then
      echo "SYMLINK_CURRENT"
    else
      echo "SYMLINK_OTHER"
    fi
  else
    # It's a copy - compare content
    if diff -rq "$codex_path" "$toolkit_path" >/dev/null 2>&1; then
      echo "COPY_CURRENT"
    else
      echo "COPY_OUTDATED"
    fi
  fi
}
```

**Codex Skill Status Classifications:**

| Status | Meaning | Action |
|--------|---------|--------|
| `MISSING` | Skill not installed | Offer to install |
| `SYMLINK_CURRENT` | Symlink to this toolkit | No action needed |
| `SYMLINK_OTHER` | Symlink to different toolkit | Skip (different toolkit) |
| `COPY_CURRENT` | Copy, content matches | No action needed |
| `COPY_OUTDATED` | Copy, content differs | Offer to update |

### Phase 2: Detect Activity Status

For each project, classify its activity level:

```bash
detect_activity() {
  local project_path="$1"

  # ACTIVE: Has uncommitted changes
  if [ -n "$(git -C "$project_path" status --porcelain 2>/dev/null)" ]; then
    echo "ACTIVE"
    return
  fi

  # RECENT: Files modified in last 24 hours
  if find "$project_path" -maxdepth 3 -type f -mtime -1 \
       -not -path '*/node_modules/*' \
       -not -path '*/.git/*' \
       -not -name '*.log' 2>/dev/null | head -1 | grep -q .; then
    echo "RECENT"
    return
  fi

  echo "DORMANT"
}
```

**Activity Classifications:**

| Status | Meaning | Default Action |
|--------|---------|----------------|
| `ACTIVE` | Uncommitted git changes | Skip (ask first) |
| `RECENT` | Modified in last 24h | Include with note |
| `DORMANT` | No recent activity | Safe to sync |

### Phase 3: Check Sync Status

Compare each project's `toolkit_commit` against current toolkit HEAD:

```bash
# Project needs sync if:
# 1. toolkit_commit differs from current HEAD, AND
# 2. Skills changed between those commits

LAST_COMMIT="<from toolkit-version.json>"
CURRENT_COMMIT=$(git rev-parse HEAD)

if [ "$LAST_COMMIT" != "$CURRENT_COMMIT" ]; then
  # Check if skills actually changed
  SKILL_CHANGES=$(git diff --name-only "$LAST_COMMIT".."$CURRENT_COMMIT" -- .claude/skills 2>/dev/null | wc -l)
  if [ "$SKILL_CHANGES" -gt 0 ]; then
    echo "OUTDATED"
  else
    echo "CURRENT"
  fi
else
  echo "CURRENT"
fi
```

### Phase 4: Display Status

Show a formatted status report:

```
TOOLKIT SYNC STATUS
===================
Toolkit: /Users/you/Projects/ai_coding_project_base
Current: abc1234 (2026-01-23)

CODEX CLI SKILL PACK
────────────────────
Location: ~/.codex/skills
Status:   OUTDATED (3 skills need updating)

  Skill                  Status
  ──────────────────────────────────────
  fresh-start            SYMLINK_CURRENT
  phase-prep             SYMLINK_CURRENT
  phase-start            COPY_OUTDATED    ← needs update
  phase-checkpoint       COPY_OUTDATED    ← needs update
  verify-task            MISSING          ← needs install
  ...

TARGET PROJECTS
───────────────
Found N toolkit-using projects:

  #  Project                       Sync Status   Last Sync     Activity
  ─────────────────────────────────────────────────────────────────────
  1  ~/Projects/my-app             OUTDATED      3 days ago    DORMANT
  2  ~/Projects/api-service        OUTDATED      1 week ago    ACTIVE
  3  ~/Projects/dashboard          CURRENT       today         -
  4  ~/Projects/ml-pipeline        OUTDATED      2 weeks ago   RECENT

Legend:
  Sync Status: OUTDATED = needs sync, CURRENT = up to date
  Activity:    ACTIVE = uncommitted changes, RECENT = modified today, DORMANT = idle
```

**If Codex skill pack is not installed at all:**

```
CODEX CLI SKILL PACK
────────────────────
Location: ~/.codex/skills
Status:   NOT INSTALLED

To install the Codex skill pack, run:
  ./scripts/install-codex-skill-pack.sh
```

### Phase 5: User Selection

If there are OUTDATED items (Codex skills or projects), prompt the user:

```
What should I sync?

Options:
1. Sync everything (Recommended)
   Update Codex skill pack + all DORMANT projects

2. Codex skill pack only
   Update only the Codex CLI skills

3. Target projects only
   Sync all DORMANT projects, skip Codex

4. Select specific items
   Choose which items to sync individually

5. Include ACTIVE projects too
   Will ask for confirmation before syncing each active project

6. Skip for now
   Exit without syncing
```

Use `AskUserQuestion` for the selection.

**If only Codex needs updating (no outdated projects):**

```
Codex skill pack needs updating. Sync now?

Options:
1. Yes, update Codex skills
2. Skip for now
```

**If only projects need updating (Codex is current):**

Show the original project-only options (without Codex mentions).

**If user selects "Include ACTIVE projects":**

For each ACTIVE project, show a separate confirmation:

```
Project: ~/Projects/api-service
Status: ACTIVE (uncommitted changes)

This project has uncommitted git changes:
  M src/api/handlers.ts
  M tests/api.test.ts
  ?? src/api/new-file.ts

Syncing will update skill files but won't affect your uncommitted changes.

Options:
1. Sync anyway
2. Skip this project
3. Show full git status
```

### Phase 6: Execute Sync

#### 6a: Sync Codex Skill Pack (if selected)

```
SYNCING CODEX SKILL PACK
========================
Location: ~/.codex/skills

  fresh-start           CURRENT (symlink)
  phase-prep            CURRENT (symlink)
  phase-start           UPDATED (was copy, now current)
  phase-checkpoint      UPDATED (was copy, now current)
  verify-task           INSTALLED (new)
  ...

Done: 3 skills updated, 13 already current
```

**Codex Sync Logic:**

For each skill in the Codex skills list:

1. **MISSING:** Copy skill directory from toolkit to Codex skills dir
2. **SYMLINK_CURRENT:** No action needed
3. **SYMLINK_OTHER:** Skip (points to different toolkit)
4. **COPY_CURRENT:** No action needed
5. **COPY_OUTDATED:**
   - Remove the outdated copy
   - Copy fresh from toolkit (preserves copy method)
   - Or offer to convert to symlink for auto-updates

```bash
sync_codex_skill() {
  local skill_name="$1"
  local status="$2"
  local codex_path="$CODEX_SKILLS_DIR/$skill_name"
  local toolkit_path="$TOOLKIT_SKILLS_DIR/$skill_name"

  case "$status" in
    MISSING|COPY_OUTDATED)
      rm -rf "$codex_path" 2>/dev/null || true
      cp -R "$toolkit_path" "$codex_path"
      echo "UPDATED"
      ;;
    SYMLINK_CURRENT|COPY_CURRENT)
      echo "CURRENT"
      ;;
    SYMLINK_OTHER)
      echo "SKIPPED"
      ;;
  esac
}
```

#### 6b: Sync Target Projects (if selected)

For each selected project, run the sync process:

```
SYNCING TARGET PROJECTS
=======================

[1/3] ~/Projects/my-app
      Checking files...
      Copying skills...
      Updating toolkit-version.json...
      Done (5 files updated)

[2/3] ~/Projects/dashboard
      Already up to date

[3/3] ~/Projects/api-service
      SKIPPED (active project)

─────────────────────────────────────────────────────────────────────
```

**Sync Logic (for each project):**

1. Change working context to target project
2. For each skill in the sync list, compare hashes:
   - If toolkit hash = target hash: skip (current)
   - If target missing: copy from toolkit (new)
   - If target = last-synced hash: copy from toolkit (clean update)
   - If target differs from last-synced: report conflict (ask user)
3. Update `toolkit-version.json` with new commit and hashes

**Skills to sync:**

All skills from the toolkit's `.claude/skills/` directory are synced dynamically.
This includes any new skills added to the toolkit without requiring manual updates.

### Phase 7: Summary Report

```
SYNC COMPLETE
=============

Codex CLI Skill Pack:
  Skills updated:  3
  Already current: 13
  Skipped:         0

Target Projects:
  Projects processed: 4
    Synced:    2 (my-app, ml-pipeline)
    Skipped:   1 (api-service - active)
    Current:   1 (dashboard)
  Files updated: 12
  Conflicts:     0

All synced items are now at toolkit commit abc1234 (2026-01-23)

Note: Restart Codex CLI to pick up skill updates.
```

## Edge Cases

### Codex Skills Directory Doesn't Exist

If `~/.codex/skills` (or `$CODEX_HOME/skills`) doesn't exist:

```
CODEX CLI SKILL PACK
────────────────────
Location: ~/.codex/skills
Status:   DIRECTORY NOT FOUND

Codex CLI may not be installed, or uses a different skills location.

To install skills anyway:
  ./scripts/install-codex-skill-pack.sh

To specify a custom location:
  export CODEX_HOME=/path/to/codex
```

Skip Codex syncing in this case unless user explicitly requests installation.

### Codex Skills Are All Symlinks

If all Codex skills are symlinks to this toolkit:

```
CODEX CLI SKILL PACK
────────────────────
Location: ~/.codex/skills
Status:   CURRENT (all symlinks - auto-updating)

All {N} skills are symlinked to this toolkit. No sync needed.
```

No sync action needed - symlinks auto-update.

### No Projects Found

```
No toolkit-using projects found in ~/Projects

To set up a project with this toolkit:
1. Navigate to your project directory
2. Run /setup or /generate-plan

To search additional paths, set:
  export TOOLKIT_SEARCH_PATH="~/Projects:~/work"
```

### Project Points to Different Toolkit

Skip silently - it's using a different toolkit installation.

### Git Not Available in Project

```
Warning: ~/Projects/legacy-app is not a git repository
  Cannot detect activity status - treating as DORMANT
```

### Sync Conflicts

If a project has local modifications to skills that differ from both the last-synced version AND the toolkit version, follow the standard `/sync` conflict resolution flow (backup local, overwrite, or skip).
