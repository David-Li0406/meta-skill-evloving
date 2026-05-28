---
name: base44-cli-sdk
description: Use this skill when working with Base44 projects, whether initializing new projects with the CLI or implementing features using the Base44 SDK.
---

# Base44 CLI and SDK

Manage Base44 applications and implement features using the Base44 CLI and SDK tools.

## ⚡ IMMEDIATE ACTION REQUIRED - Read This First

This skill activates on ANY mention of "base44" or when a `base44/` folder exists. **DO NOT read documentation files or search the web before acting.**

**Your first action MUST be:**
1. Check if `base44/config.jsonc` exists in the current directory.
2. If **YES** (existing project scenario):
   - Use the Base44 SDK to implement features.
   - Do NOT use CLI commands unless explicitly requested.
3. If **NO** (new project scenario):
   - Use the Base44 CLI for project initialization.

## Base44 CLI Operations

### Project Initialization

- **Use the CLI when:**
  - Creating a **NEW** Base44 project from scratch.
  - Initializing a project in an empty directory.
  - Directory is missing `base44/config.jsonc`.

### CLI Commands

**Critical: Local Installation Only**

NEVER call `base44` directly. The CLI is installed locally as a dev dependency and must be accessed via a package manager:

- `npx base44 <command>` (npm - recommended)
- `yarn base44 <command>` (yarn)
- `pnpm base44 <command>` (pnpm)

**Authentication Check at Session Start**

1. **Check authentication status** by running:
   ```bash
   npx base44 whoami
   ```
2. **If the user is logged in** (command succeeds):
   - Continue with the requested task.
3. **If the user is NOT logged in** (command fails):
   - **STOP immediately** and ask the user to login manually:
     ```bash
     npx base44 login
     ```

### Available CLI Commands

| Command         | Description                                     |
| --------------- | ----------------------------------------------- |
| `base44 login`  | Authenticate with Base44 using device code flow |
| `base44 create` | Create a new Base44 app (framework-agnostic)   |
| `base44 entities push` | Push local entities to Base44               |
| `base44 site deploy` | Deploy built site files to Base44 hosting    |

## Base44 SDK Operations

### SDK Usage

- **Use the SDK when:**
  - Building features in an **EXISTING** Base44 project.
  - Writing JavaScript/TypeScript code using Base44 SDK modules.
  - User mentions: "implement", "build a feature", "add functionality".

### SDK Modules

| Module | Purpose |
|--------|---------|
| `entities` | CRUD operations on data models |
| `auth` | Login, register, user management |
| `agents` | AI conversations and messages |
| `functions` | Backend function invocation |
| `integrations` | AI, email, file uploads, custom APIs |
| `analytics` | Track custom events and user activity |

### Quick Start with SDK

```javascript
// In Base44-generated apps, base44 client is pre-configured and available

// CRUD operations
const task = await base44.entities.Task.create({ title: "New task", status: "pending" });
const tasks = await base44.entities.Task.list();
await base44.entities.Task.update(task.id, { status: "done" });

// Get current user
const user = await base44.auth.me();
```

## Common Workflows

### Starting a New Project
```bash
# Login first
npx base44 login

# Create project (ALWAYS use --name and --path flags)
npx base44 create -n my-app -p .
```

### Implementing Features
```javascript
// Example of creating a new task
const newTask = await base44.entities.Task.create({ title: "New Task", status: "pending" });
```

### Deploying Changes
```bash
# Build your project first (using your framework's build command)
npm run build

# Deploy to Base44
npx base44 site deploy -y
```

## Troubleshooting

| Error                       | Solution                                                                            |
| --------------------------- | ----------------------------------------------------------------------------------- |
| Not authenticated           | Run `npx base44 login` first                                                        |
| No entities found           | Ensure entities exist in `base44/entities/` directory                               |
| Entity not recognized       | Ensure file uses kebab-case naming (e.g., `team-member.jsonc` not `TeamMember.jsonc`) |
| No site configuration found | Check that `site.outputDirectory` is configured in project config                   |

## Conclusion

This merged skill provides a comprehensive approach to managing Base44 projects, whether initializing new projects with the CLI or implementing features using the Base44 SDK. Always ensure to check the project state before proceeding with the appropriate actions.