---
name: dependencies-management
description: Use this skill when you need to install, update, or manage project dependencies across all applications using Bun.
---

# Dependencies Management Skill

This skill handles dependency management for the project using Bun.

## When to Use

- Installing project dependencies
- Updating packages
- Adding new dependencies to the project
- Resolving dependency issues
- Setting up the project for the first time

## Pre-check

Before managing dependencies, verify:

1. Bun is installed and accessible on the system.
2. Package.json files exist in the expected locations.
3. Internet connectivity for downloading packages.

## Current Operations

### Install Dependencies

Currently installs dependencies for the API application located in `apps/api`.

**For Unix/Mac/Linux:**

```bash
.claude/skills/dependencies/scripts/install.sh
```

**For Windows PowerShell:**

```powershell
.claude/skills/dependencies/scripts/install.ps1
```

The script will:

1. Navigate to the `apps/api` directory.
2. Verify Bun is installed.
3. Run `bun install` to install all dependencies.
4. Report success or any errors.

### Post-Installation

After successful installation:

- Verify the `node_modules` directory was created.
- Check that all dependencies were installed correctly.
- Report any warnings or errors from Bun.

## Error Handling

Handle these common errors:

- **Bun not installed**: Direct user to [Bun installation instructions](https://bun.sh).
- **Package.json not found**: Verify the project structure and that `apps/api` exists.
- **Network errors**: Check internet connectivity or try again.
- **Permission errors**: Ensure appropriate file system permissions.
- **Lock file conflicts**: Remove `bun.lockb` and reinstall if necessary.

## Future Enhancements

This skill will be expanded to include:

- Installing dependencies for multiple apps when added to the project.
- Updating dependencies (`bun update`).
- Adding new dependencies (`bun add <package>`).
- Removing dependencies (`bun remove <package>`).
- Security audit (`bun audit`).
- Listing outdated dependencies.
- Managing workspace dependencies for monorepo setup.
- Cleaning `node_modules` and reinstalling fresh.

## Safety Guidelines

- Always verify what will be installed before proceeding.
- Show the user the `package.json` location being processed.
- Report installation progress and results.
- Warn about major version updates.
- Keep lockfiles committed to ensure reproducible installs.