---
name: Scaffolding Guidance
description: |
  Use this skill when the user asks about project scaffolding, CLAUDE.md templates, project tracking, or how to use the project-scaffolder plugin. Triggers on: "How do I scaffold a project?", "What templates are available?", "CLAUDE.md best practices", "project tracking", "user story management".
version: 1.0.0
---

# Project Scaffolding Guidance

## Commands

### `/scaffold <path> [options]`

Full project structure with all components.

**Options:** `--name`, `--author`, `--description`, `--tech-stack`

```
/scaffold ../my-app
/scaffold ../api --name "User API" --tech-stack "fastapi"
```

### `/scaffold-minimal <path> [options]`

Essential files only (CLAUDE.md, commands, development-workflow skill).

```
/scaffold-minimal ../quick-project
```

## What Gets Created

```
project/
├── CLAUDE.md                    # Project hub
├── .claude-plugin/
│   └── plugin.json              # Points to .claude/
└── .claude/                     # All Claude Code files (hidden)
    ├── commands/                # 6 workflow commands
    ├── hooks/hooks.json         # Workflow enforcement
    ├── skills/                  # 3 interactive skills
    └── project/                 # Project tracking
        ├── features/            # User story specs
        ├── plans/               # Implementation plans
        ├── high-level-user-stories.md
        └── roadmap.md
```

## Feature Workflow (Enforced by Hooks)

When you ask to build a feature, the hooks enforce:

```
1. Story  → Create in .claude/project/features/
2. Plan   → Create in .claude/project/plans/
3. Approve → Get user approval before coding
4. Build  → Implement following the plan
```

**No coding starts without story + plan + approval.**

## Project Tracking

| File                         | Purpose                       |
| ---------------------------- | ----------------------------- |
| `high-level-user-stories.md` | Progress tracker - START HERE |
| `roadmap.md`                 | Phased implementation plan    |
| `features/us-XXX-name.md`    | User story specifications     |
| `plans/us-XXX-plan.md`       | Implementation plans          |

### File Naming

- **Filenames:** lowercase (`us-001-feature-name.md`)
- **Display:** UPPERCASE (`US-001`)

**Hooks automatically:**

- Detect feature intent → enforce workflow
- Guide file locations
- Update tracking files
- Verify consistency

## Workflow Commands

| Command                  | Purpose                     |
| ------------------------ | --------------------------- |
| `/implement`             | Full workflow orchestrator  |
| `/discovery`             | Requirements + Architecture |
| `/plan-and-validate`     | Create and validate plan    |
| `/start-implementation`  | Execute the plan            |
| `/review-implementation` | Code review                 |
| `/next`                  | Proceed to next phase       |

## Skills

| Skill                  | Location          | Triggers                       |
| ---------------------- | ----------------- | ------------------------------ |
| `development-workflow` | `.claude/skills/` | Feature process, git, planning |
| `project-standards`    | `.claude/skills/` | User stories, documentation    |
| `exploration-helpers`  | `.claude/skills/` | Database, codebase, types      |

## Full vs Minimal

| Use Case                | Mode    |
| ----------------------- | ------- |
| Production/team project | Full    |
| Quick prototype         | Minimal |
| Adding to existing      | Minimal |

## Existing Directories

When scaffolding into an existing directory:

- **Merge** - Skip existing files, add only missing
- **Overwrite** - Replace all Claude Code files
- **Abort** - Cancel scaffolding

## Customization

After scaffolding, ask the `template-customizer` agent:

> "Help me customize these templates for [your-tech-stack]"
