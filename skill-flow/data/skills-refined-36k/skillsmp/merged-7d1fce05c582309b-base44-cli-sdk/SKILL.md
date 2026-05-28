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

- **Use the Base44 CLI** when:
  - Creating a **NEW** Base44 project from scratch.
  - Initializing a project in an empty directory.
  - Directory is missing `base44/config.jsonc`.

### CLI Commands

The Base44 CLI provides command-line tools for authentication, creating projects, managing entities, and deploying Base44 applications. It is framework-agnostic and works with popular frontend frameworks.

**Critical: Local Installation Only**
- Install the Base44 CLI as a dev dependency:
  ```bash
  npm install --save-dev base44
  ```
- Run commands using:
  ```bash
  npx base44 <command>
  ```

### Available CLI Commands

| Command         | Description                                     |
| --------------- | ----------------------------------------------- |
| `base44 login`  | Authenticate with Base44 using device code flow |
| `base44 create` | Create a new Base44 app (framework-agnostic)   |
| `base44 entities push` | Push local entities to Base44               |
| `base44 site deploy` | Deploy built site files to Base44 hosting    |

## Base44 SDK Operations

### Feature Implementation

- **Use the Base44 SDK** when:
  - Building features in an **EXISTING** Base44 project.
  - `base44/config.jsonc` already exists in the project.
  - Writing JavaScript/TypeScript code using Base44 SDK modules.

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

### Updating Entity Schema
```bash
# After modifying entities in base44/entities/
npx base44 entities push
```

### Deploying Changes
```bash
# Build your project first (using your framework's build command)
npm run build

# Deploy to Base44 (use -y to skip confirmation)
npx base44 site deploy -y
```

## Authentication

Most commands require authentication. If you're not logged in, the CLI will automatically prompt you to login. Your session is stored locally and persists across CLI sessions.

## Troubleshooting

| Error                       | Solution                                                                            |
| --------------------------- | ----------------------------------------------------------------------------------- |
| Not authenticated           | Run `npx base44 login` first                                                        |
| No entities found           | Ensure entities exist in `base44/entities/` directory                               |
| Entity not recognized       | Ensure file uses kebab-case naming (e.g., `team-member.jsonc` not `TeamMember.jsonc`) |
| No functions found          | Ensure functions exist in `base44/functions/` with valid `function.jsonc` configs   |
| No site configuration found | Check that `site.outputDirectory` is configured in project config                   |
| Site deployment fails       | Ensure you ran `npm run build` first and the build succeeded                        |

## Conclusion

This merged skill provides a comprehensive guide for managing Base44 projects using both the CLI and SDK, ensuring that you can effectively initialize projects and implement features as needed.