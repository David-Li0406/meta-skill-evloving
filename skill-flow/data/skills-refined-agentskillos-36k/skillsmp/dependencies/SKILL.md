---
name: dependencies
description: Manage project dependencies across all apps. Use when installing, updating, or managing dependencies, or when user asks to install packages.
allowed-tools:
  - Bash
  - Read
  - Glob
user-invocable: true
---

# Dependencies Management Skill

This skill handles dependency management for the project using Bun.

## Pre-check

Before managing dependencies, verify:

1. Bun is installed and accessible on the system
2. Package.json files exist in the expected locations
3. Internet connectivity for downloading packages

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

1. Navigate to `apps/api` directory
2. Verify bun is installed
3. Run `bun install` to install all dependencies
4. Report success or any errors

### Post-Installation

After successful installation:

- Verify node_modules directory was created
- Check that all dependencies were installed correctly
- Report any warnings or errors from bun

## Error Handling

Handle these common errors:

- **Bun not installed**: Direct user to https://bun.sh for installation instructions
- **Package.json not found**: Verify the project structure and that apps/api exists
- **Network errors**: Check internet connectivity or try again
- **Permission errors**: May need appropriate file system permissions
- **Lock file conflicts**: May need to remove bun.lockb and reinstall

## Future Enhancements

This skill will be expanded to include:

- Installing dependencies for multiple apps when added to the project
- Updating dependencies (`bun update`)
- Adding new dependencies (`bun add <package>`)
- Removing dependencies (`bun remove <package>`)
- Security audit (`bun audit`)
- Listing outdated dependencies
- Managing workspace dependencies for monorepo setup
- Cleaning node_modules and reinstalling fresh

## Safety Guidelines

- Always verify what will be installed before proceeding
- Show user the package.json location being processed
- Report installation progress and results
- Warn about major version updates
- Keep lockfiles committed to ensure reproducible installs
