---
name: init-context
description: Initialize PRISM .context folder in current project. Use when starting PRISM work in a new project or setting up context management.
version: 1.0.0
---

# Task: Initialize PRISM Context System

Set up the `.context/` folder structure in the current project with PRISM context modules.

## When to Use

- When starting PRISM work in a new project
- When setting up context management for AI agents
- When migrating a project to use PRISM
- After cloning a project that needs PRISM setup

## Quick Start

1. Check if `.context/` already exists
2. Create directory structure (`.context/core`, etc.)
3. Copy template files from PRISM plugin
4. Create/update CLAUDE.md if needed
5. Set up .gitignore and marker file

## What This Does

1. Creates `.context/` folder structure in project root
2. Copies template files from PRISM plugin templates
3. Creates minimal CLAUDE.md if none exists (or offers to update existing)
4. Sets up .gitignore for cache folder
5. Creates marker file `.prism-installed` to indicate setup complete

## Prerequisites

- PRISM plugin installed at `C:\Dev\.prism\plugins\prism-devtools`
- Project directory exists

## Steps

### 1. Check Current State

```bash
# Check if .context already exists
if (Test-Path ".context") { Write-Host ".context/ already exists" } else { Write-Host "Ready to initialize" }

# Check if CLAUDE.md exists
if (Test-Path "CLAUDE.md") { Write-Host "CLAUDE.md exists - will offer to update" }
```

### 2. Create Directory Structure

```bash
# Create .context folders
mkdir -p .context/core
mkdir -p .context/safety
mkdir -p .context/workflows
mkdir -p .context/project
mkdir -p .context/cache/mcp-responses
mkdir -p .context/cache/terminal-logs
mkdir -p .context/cache/session-history
```

### 3. Copy Template Files

Copy all template files from PRISM plugin:

**Source:** `C:\Dev\.prism\plugins\prism-devtools\templates\.context\`

```bash
# Copy core context files
cp "C:\Dev\.prism\plugins\prism-devtools\templates\.context\core\persona-rules.md" ".context/core/"
cp "C:\Dev\.prism\plugins\prism-devtools\templates\.context\core\commit-format.md" ".context/core/"

# Copy safety context files
cp "C:\Dev\.prism\plugins\prism-devtools\templates\.context\safety\destructive-ops.md" ".context/safety/"
cp "C:\Dev\.prism\plugins\prism-devtools\templates\.context\safety\file-write-limits.md" ".context/safety/"
cp "C:\Dev\.prism\plugins\prism-devtools\templates\.context\safety\citation-integrity.md" ".context/safety/"

# Copy workflow context files
cp "C:\Dev\.prism\plugins\prism-devtools\templates\.context\workflows\git-branching.md" ".context/workflows/"
cp "C:\Dev\.prism\plugins\prism-devtools\templates\.context\workflows\code-review.md" ".context/workflows/"

# Copy project template
cp "C:\Dev\.prism\plugins\prism-devtools\templates\.context\project\architecture.md" ".context/project/"

# Copy manifest and gitignore
cp "C:\Dev\.prism\plugins\prism-devtools\templates\.context\index.yaml" ".context/"
cp "C:\Dev\.prism\plugins\prism-devtools\templates\.context\.gitignore" ".context/"
```

### 4. Handle CLAUDE.md

**If CLAUDE.md doesn't exist:**
```bash
cp "C:\Dev\.prism\plugins\prism-devtools\templates\CLAUDE.md" "./CLAUDE.md"
```

**If CLAUDE.md exists:**
- Ask user if they want to:
  - Replace with template (backup existing)
  - Append context references to existing
  - Skip CLAUDE.md update

### 5. Create Marker File

```bash
# Create marker indicating PRISM context is installed
echo "PRISM context initialized $(Get-Date -Format 'yyyy-MM-dd')" > .prism-installed
```

### 6. Verify Installation

```bash
# Verify structure
ls -la .context/
ls -la .context/core/
ls -la .context/safety/
ls -la .context/workflows/

# Count files
$count = (Get-ChildItem -Path ".context" -Recurse -File).Count
Write-Host "Installed $count context files"
```

## Expected Results

After completion:
```
{project-root}/
├── CLAUDE.md                  # Project context (new or updated)
├── .context/
│   ├── index.yaml             # Context manifest
│   ├── .gitignore             # Ignores cache/
│   ├── core/
│   │   ├── persona-rules.md   # PRISM persona persistence
│   │   └── commit-format.md   # Commit message format
│   ├── safety/
│   │   ├── destructive-ops.md # File deletion safeguards
│   │   ├── file-write-limits.md # Chunking rules
│   │   └── citation-integrity.md # Read before cite
│   ├── workflows/
│   │   ├── git-branching.md   # Branch/push policy
│   │   └── code-review.md     # PR review rules
│   ├── project/
│   │   └── architecture.md    # Project architecture (template)
│   └── cache/                 # Runtime data (gitignored)
│       ├── mcp-responses/
│       ├── terminal-logs/
│       └── session-history/
└── .prism-installed           # Marker file
```

## Success Criteria

- [ ] `.context/` folder exists with all subfolders
- [ ] All 7 context modules copied (2 core, 3 safety, 2 workflows)
- [ ] `index.yaml` manifest in place
- [ ] `.gitignore` ignoring cache folder
- [ ] CLAUDE.md exists with context references
- [ ] `.prism-installed` marker created

## Customization

After initialization, customize:

1. **CLAUDE.md** - Add your tech stack and project purpose
2. **`.context/project/architecture.md`** - Document your project architecture
3. **Add project-specific context** - Create new `.md` files in `.context/project/`

## Troubleshooting

### Template Files Not Found
```
Copy-Item : Cannot find path 'C:\Dev\.prism\plugins\prism-devtools\templates\...'
```
**Solution:** Verify PRISM plugin is installed at expected location

### Permission Denied
**Solution:** Run terminal as administrator or check folder permissions

### .context Already Exists
**Options:**
- Skip initialization (already set up)
- Backup and recreate (lose customizations)
- Merge templates with existing (manual)

## Next Steps

1. Edit CLAUDE.md with your project details
2. Update `.context/project/architecture.md` with your architecture
3. Review context modules in `.context/` folder
4. Start development - context loads automatically!
