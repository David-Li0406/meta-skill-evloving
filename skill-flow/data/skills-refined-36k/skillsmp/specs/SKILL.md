---
name: specs
description: Manage feature specifications - create, track, and implement specs with structured templates and auto-generated indexes.
compatibility: Requires Python 3.9+
metadata:
  author: dot-claude
  version: "1.0"
---

# Specs Management

A system for managing feature specifications as living documents. Specs track features from planning through implementation with structured templates and automatic indexing.

## Commands

This skill supports five commands via arguments:

- `/specs init <feature-name>` - Create a new spec
- `/specs implement` - Work on in-progress specs
- `/specs ui` - Generate docsify UI for browsing
- `/specs setup` - Configure project hooks for automated workflow
- `/specs migrate` - Convert flat-file specs to directory structure

If no argument is provided, show available commands.

---

## `/specs init <feature-name>`

Create a new feature specification.

### Steps

1. **Parse the feature name** from arguments
   - Use kebab-case (e.g., `user-authentication`, `api-caching`)
   - If no name provided, ask the user

2. **Get today's date** in YYYY-MM-DD format

3. **Create the spec directory** at `specs/<feature-name>/`

4. **Copy templates** from this skill's assets:
   - Read `assets/templates/directory-based/README.md.template`
   - Read `assets/templates/directory-based/research.md.template`
   - Read `assets/templates/directory-based/implementation-plan.md.template`

5. **Replace placeholders** in each template:
   - `[Feature Name]` → Title Case version (e.g., "User Authentication")
   - `YYYY-MM-DD` → today's date

6. **Write files** to `specs/<feature-name>/`:
   - `README.md`
   - `research.md`
   - `implementation-plan.md`

7. **Regenerate the index:**
   ```bash
   python3 <skill-path>/scripts/index.py ./specs
   ```

8. **Report success** with the created path and next steps

### Single-File Specs (Rare)

If user explicitly requests a single-file spec:
- Use `assets/templates/single-file.md.template`
- Write to `specs/<feature-name>.md`
- This format is discouraged for most features

---

## `/specs implement`

Begin implementation on an in-progress spec.

### Steps

1. **Read `specs/README.md`** (the auto-generated index)

2. **Determine which spec to work on:**
   - If no specs are "in-progress": prompt user to choose from "planned"
   - If one spec is "in-progress": use that automatically
   - If multiple are "in-progress": ask user which one

3. **Load the spec:**
   - Read `specs/<feature>/README.md` for overview
   - Read `specs/<feature>/implementation-plan.md` for tasks
   - Keep `specs/<feature>/research.md` available for context

4. **Create a todo list** from the implementation tasks

5. **Implement systematically:**
   - Work through tasks in order
   - Run tests before each commit
   - Commit at logical checkpoints

6. **After each commit, update the spec:**
   - Mark tasks complete: `- [x] Task name (commit: abc123)`
   - Update status in frontmatter if needed (planned → in-progress → completed)
   - Regenerate index: `python3 <skill-path>/scripts/index.py ./specs`
   - Commit spec updates: `git commit -m "docs(specs): update progress"`

---

## `/specs ui`

Generate a docsify UI for browsing specs in a browser.

### Steps

1. **Read `specs/README.md`** to get the current spec organization

2. **Write `specs/index.html`:**

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Specs</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/docsify@4/themes/dark.css">
</head>
<body>
  <div id="app"></div>
  <script>
    window.$docsify = {
      name: 'Specs',
      loadSidebar: true,
      subMaxLevel: 3,
      auto2top: true,
      search: { placeholder: 'Search specs...', depth: 3 }
    }
  </script>
  <script src="https://cdn.jsdelivr.net/npm/docsify@4/lib/docsify.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/docsify@4/lib/plugins/search.min.js"></script>
</body>
</html>
```

3. **Write `specs/_sidebar.md`** with navigation:
   - Parse the README.md sections (In Progress, Planned, Completed)
   - Generate sidebar links for each spec
   - Directory specs link to `<name>/README.md`
   - Single-file specs link to `<name>.md`

4. **Create `specs/.nojekyll`** (empty file for GitHub Pages)

5. **Start server and open browser:**
   ```bash
   cd specs && python3 -m http.server 8080 &
   open http://localhost:8080
   ```

---

## `/specs setup`

Configure project-level hooks for automated spec workflow. This installs a hook that reminds Claude to run `/specs implement` after context compaction.

This command is **idempotent** - run it multiple times to update the reminder message. Existing hooks are preserved.

### Steps

1. **Prompt for reminder content:**
   - Ask: "Use default reminder or custom message?"
   - **Default:** "Resuming after compaction - run /specs implement to continue in-progress specifications"
   - **Custom:** Prompt user for their message (can include workflow hints, skill references, multi-line content)
   - Show current message if `.claude/hooks/specs-reminder.txt` already exists

2. **Create `.claude/hooks/` directory** if it doesn't exist

3. **Write the reminder files:**
   - Write user's message to `.claude/hooks/specs-reminder.txt`
   - Write the runner script to `.claude/hooks/specs-reminder.sh`:
     ```bash
     #!/bin/bash
     cat "$(dirname "$0")/specs-reminder.txt"
     ```
   - Make executable: `chmod +x .claude/hooks/specs-reminder.sh`

4. **Merge into `.claude/settings.json`:**
   - Read existing settings (or start with `{}`)
   - Check if our hook already exists in `hooks.SessionStart[]`:
     - Look for entry with `command` containing `specs-reminder.sh`
     - If found: do nothing (already configured)
     - If not found: append our hook to the array
   - Preserve ALL existing hooks and settings
   - Write back the merged settings

   Our hook configuration:
   ```json
   {
     "matcher": "compact",
     "hooks": [{
       "type": "command",
       "command": ".claude/hooks/specs-reminder.sh"
     }]
   }
   ```

5. **Report success:**
   - Show the installed/updated message
   - Note: "Run `/specs setup` again anytime to change the reminder"
   - Suggest adding `.claude/hooks/` to version control

### Example Custom Reminders

Simple workflow hint:
```
Resuming after compaction - run /specs implement to continue feature work
```

Multi-skill workflow:
```
Resuming after compaction. Workflow:
- Check /specs implement for in-progress features
- Use /commit when ready to checkpoint
- Run tests before marking tasks complete
```

Project-specific context:
```
Context restored. This project uses:
- /specs for feature tracking
- pytest for tests (run before commits)
- Priority: complete auth-system spec first
```

### What the Hook Does

After context compaction, Claude receives a system message with your configured reminder. This maintains continuity on long-running feature implementations and can guide Claude toward your preferred workflow.

---

## `/specs migrate`

Convert flat-file specs (`specs/<name>.md`) to the directory-based structure (`specs/<name>/README.md`, `research.md`, `implementation-plan.md`).

### When to Use

- Existing project has specs as single `.md` files in `specs/`
- Want to adopt the richer directory-based format for better organization
- Migrating from an older specs workflow

### Steps

1. **Scan `specs/` for flat files:**
   - Find all `.md` files directly in `specs/`
   - Exclude system files: `README.md`, `_sidebar.md`, `index.html`
   - Each file `specs/<name>.md` is a candidate for migration

2. **Preview and confirm:**
   - List all specs that will be migrated
   - Show count: "Found N flat-file specs to migrate"
   - Ask user to confirm before proceeding

3. **For each flat-file spec:**

   a. **Read and parse the file:**
      - Extract frontmatter (title, status, date, priority) if present
      - If no frontmatter, derive title from filename (kebab-case → Title Case)
      - Default status: `planned`, priority: `50`, date: today

   b. **Analyze content sections:**
      - Look for headings like `## Overview`, `## Requirements`, `## Implementation`, `## Tasks`, `## Research`, `## Notes`
      - Map content to the three target files based on section semantics

   c. **Create directory structure:**
      ```bash
      mkdir -p specs/<name>/
      ```

   d. **Write `README.md`:**
      - Preserve original frontmatter
      - Include: Overview, Goals, Non-Goals, Key Decisions, Implementation Status
      - Pull from original sections or use template defaults

   e. **Write `research.md`:**
      - Include: Problem Statement, Requirements, Options Considered, Recommendation
      - Pull from original `## Requirements`, `## Research`, `## Options` sections
      - Use template structure for missing sections

   f. **Write `implementation-plan.md`:**
      - Include: Prerequisites, Phase breakdowns, Tasks
      - Pull from original `## Tasks`, `## Implementation` sections
      - Convert task lists to phased structure

   g. **Remove the original flat file:**
      ```bash
      rm specs/<name>.md
      ```

4. **Regenerate the index:**
   ```bash
   python3 <skill-path>/scripts/index.py ./specs
   ```

5. **Report results:**
   - List each migrated spec
   - Note any specs that had issues
   - Suggest reviewing migrated specs to fill in template sections

### Content Mapping Heuristics

| Original Section | Target File | Target Section |
|-----------------|-------------|----------------|
| `## Overview` | README.md | `## Overview` |
| `## Goals` | README.md | `## Goals` |
| `## Requirements` | research.md | `## Requirements` |
| `## Research`, `## Options` | research.md | `## Options Considered` |
| `## Tasks`, `## Implementation` | implementation-plan.md | Phase sections |
| `## Notes` | implementation-plan.md | Bottom of file |
| Everything else | README.md | Appended after template sections |

### Example Migration

**Before:** `specs/user-auth.md`
```markdown
---
title: "User Authentication"
status: in-progress
date: 2024-01-15
---

# User Authentication

## Overview
Add login/logout functionality.

## Requirements
- Support OAuth providers
- Session management

## Tasks
- [ ] Set up OAuth config
- [ ] Create login page
- [ ] Add session middleware
```

**After:** `specs/user-auth/`
```
specs/user-auth/
  README.md              # Frontmatter + Overview + Goals
  research.md            # Requirements + Options
  implementation-plan.md # Tasks organized into phases
```

### Handling Edge Cases

- **No frontmatter:** Generate from filename, use defaults
- **Non-standard sections:** Preserve in README.md under original headings
- **Already migrated:** Skip directories, only process `.md` files
- **Empty sections:** Use template placeholders

---

## First-Time Setup

If the project has no `specs/` directory:

1. Create `specs/` directory
2. Run the index script to create an empty README.md:
   ```bash
   python3 <skill-path>/scripts/index.py ./specs
   ```
3. Inform user the specs system is ready

---

## Spec Statuses

Specs use these statuses in frontmatter:

| Status | Meaning |
|--------|---------|
| `planned` | Spec is written but implementation hasn't started |
| `in-progress` | Currently being implemented |
| `completed` | Implementation finished |
| `archived` | No longer relevant |

## Frontmatter Format

```yaml
---
title: "Feature Name"
status: planned
date: 2024-01-15
priority: 10
---
```

Lower priority numbers = higher priority (processed first).
