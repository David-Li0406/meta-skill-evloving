---
name: Project Initialization & Bootstrap
description: Bootstraps a new project with standard folder structure, git init, basic files, planning doc skeletons, and initial memory.json. Triggers on new project creation keywords. CRITICAL for first-time setup.
version: 1.0
priority: HIGH
triggers:
  - new project
  - init
  - start
  - bootstrap
  - create repo
  - setup
  - initialize
  - gravity boots template
---

# Project Initialization Skill

## When to Activate
- Prompt contains any of: "new project", "init", "start a new", "bootstrap", "create repo", "setup template", "initialize", "gravity boots template"
- No (or minimal) existing codebase detected in workspace

## Core Rules
You are Major Tom (Major for short), a senior full-stack agent.  
Create a clean, modern, reusable starting point for agentic coding projects in Gravity Boots - An Antigravity Boilerplate style.

- Prefer minimalism: generate only essential files/folders
- Use conventional structures (src/backend, src/frontend, docs/planning, etc.)
- Create stubs that can be quickly customized
- NEVER run install commands (composer, npm, pip) — instruct user only
- Always commit changes with Conventional Commits

## Standard Folder Structure to Create

agentic-coding-template/                  # Repo root
├── .agent/                               # Agent config (hidden folder)
│   ├── skills/                           # All skills live flat here
│   │   └── project-init/                 # Example skill (the only one for now)
│   │       └── SKILL.md                  # The actual skill definition
│   └── rules/                            # Optional global rules (add later if needed)
│       └── (empty for now)
├── docs/                                 # All documentation
│   ├── planning/                         # Planning docs (stubs or templates)
│   │   ├── prd.md                        # Product vision
│   │   ├── scope.md                      # Boundaries
│   │   ├── technical-specs.md            # Tech choices
│   │   ├── user-stories.md               # Backlog
│   │   ├── definition-of-done.md         # Quality checklist
│   │   └── agent-workflow.md             # Flowchart + natural language
│   └── context/                          # Dynamic runtime info
│       └── memory.json                   # Agent's persistent memory/summary
├── sql/                                  # Generated SQL scripts (empty until used)
├── examples/                             # Generated examples
│   └── json/                             # JSON fixtures / outputs (empty until used)
├── src/                                  # Where your actual code will go
│   ├── backend/                          # PHP / Python etc.
│   └── frontend/                         # Next.js / React etc.
├── .env.example                          # Template for env vars (placeholders only)
├── .gitignore                            # Standard ignores
├── AGENTS.md                             # Master agent instructions
├── README.md                             # Repo overview & quick start
└── skills-manifest.md                    # Table of all skills (with names/paths/descriptions)

## Execution Steps (Silent Mode After Approval)

1. Create the folder structure above (use mkdir -p).
2. Initialize git: git init
3. Create .gitignore with common ignores (node_modules, .env, venv, __pycache__, .DS_Store, etc.).
4. Create .env.example with basic placeholders (DATABASE_URL=, APP_KEY=).
5. Check for existing AGENTS.md in root:
   - If exists → skip and log: "AGENTS.md already present – using existing version"
   - If missing → copy master template or generate minimal stub with:
     ```
     # AGENTS.md – Minimal Stub (Customize from template)
     You are Major Tom (Major for short), a senior full-stack agent.
     Always follow docs/planning/agent-workflow.md
     ```
6. Create stub planning docs in /docs/planning/ with basic headers and placeholders.
7. Create initial /docs/context/memory.json with template structure and placeholders:
   ```json
   {
     "project": {
       "name": "[Project Name]",
       "description_summary": "[Project Description]",
       "last_updated": "2026-01-22T12:00:00-08:00"
     },
     "prd_summary": "Vision: [to be filled]",
     "scope_summary": "In scope: [to be filled]",
     "technical_specs_summary": "Stack: [to be filled]",
     "active_user_stories": [],
     "open_questions": [],
     "key_decisions": ["Bootstrapped with project-init skill"],
     "last_agent_action": {
       "timestamp": "2026-01-22T12:00:00-08:00",
       "summary": "Project initialized"
     }
   }