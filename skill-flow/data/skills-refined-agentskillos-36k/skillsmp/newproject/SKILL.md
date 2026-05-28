---
name: newproject
description: Create a new vibe coding project with git and Claude initialisation. Pass the folder name as an argument, e.g. /newproject MyNewApp
user-invocable: true
---

# New Project Skill

Create a new project subfolder under the Vibe Coding root with proper initialisation for git and Claude Code.

## Usage

```
/newproject <folder-name>
```

**Examples:**
- `/newproject MyNewApp`
- `/newproject Budget_Tracker`
- `/newproject "Project With Spaces"`

## What This Skill Does

When invoked, perform the following steps:

### 1. Validate Input
- Check that a folder name was provided as an argument
- If no argument provided, ask: "What would you like to name the new project folder?"
- Validate the folder name doesn't already exist

### 2. Create Folder Structure
Create the following structure under `e:\Vibe Coding\<folder-name>\`:

```
<folder-name>/
├── .claude/
│   └── settings.local.json
├── CLAUDE.md
└── .gitignore
```

### 3. Initialise Git
```bash
cd "e:/Vibe Coding/<folder-name>"
git init
```

### 4. Create CLAUDE.md
Create a project-specific `CLAUDE.md` with this template:

```markdown
# CLAUDE.md - <folder-name>

This file provides guidance to Claude Code when working with this project.

## Project Overview

[Describe the project purpose here]

## Build & Development Commands

```bash
# Add your commands here
```

## Project Structure

```
<folder-name>/
├── .claude/
├── CLAUDE.md
└── [your files]
```

## Key Files

- [List important files as you create them]

## Development Guidelines

- [Add project-specific conventions]

## Skills

Inherited from root:
- `/q` — Clarify before starting
- `/challenge` — Challenge assumptions
- `/verify` — Verify before accepting
- `/commit` — Git commit and push
```

### 5. Create .claude/settings.local.json
```json
{
  "permissions": {
    "allow": [],
    "deny": []
  }
}
```

### 6. Create .gitignore
```
# Dependencies
node_modules/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Build outputs
dist/
build/
```

### 7. Initial Commit
```bash
git add .
git commit -m "Initial project setup

- Created project structure
- Added CLAUDE.md for Claude Code guidance
- Added .gitignore

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

### 8. Update Root CLAUDE.md
Add the new project to the Projects Overview table in `e:\Vibe Coding\CLAUDE.md`.

### 9. Confirm Completion
Report back:
- Folder created at: `e:\Vibe Coding\<folder-name>`
- Git initialised: Yes
- Files created: CLAUDE.md, .gitignore, .claude/settings.local.json
- Next steps: Describe what you want to build and I'll help you get started

## Notes

- The new project inherits root-level skills (`/q`, `/challenge`, `/verify`)
- No remote repository is created automatically — use GitHub CLI or web to create and link if needed
- Folder names with spaces should be quoted: `/newproject "My Project"`
