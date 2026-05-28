---
name: node-upgrade-workflow
description: Step-by-step workflow for safely upgrading Node.js dependencies across npm, pnpm, yarn, and bun.
---

# Workflow: `node-upgrade-workflow`

This skill guides you through the process of safely upgrading Node.js dependencies. It supports multiple package managers by detecting the project's lockfile.

## Prerequisites

Before starting, ensure:

- [ ] Node.js is installed.
- [ ] A `package.json` file exists in the project root.
- [ ] One of the following lockfiles exists:
  - `pnpm-lock.yaml` (pnpm)
  - `yarn.lock` (yarn)
  - `bun.lockb` (bun)
  - `package-lock.json` (npm)
- [ ] The current test suite is passing.

## Steps

### 1. Detection & Preparation

1.  **Identify Package Manager**:
    - Check for lockfiles in this priority: `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`, `package-lock.json`.
    - Set the `PM_COMMAND` based on the detected manager (e.g., `npm`, `pnpm`, `yarn`, `bun`).
2.  **Health Check**:
    - Run the audit command:
      - **npm**: `npm audit`
      - **pnpm**: `pnpm audit`
      - **yarn**: `yarn audit` (v1) or `yarn npm audit` (v2+)
      - **bun**: `bun audit`
    - Run the test suite: `${PM_COMMAND} test`.
    - _Verification_: If tests fail, do not proceed until the baseline is fixed.
3.  **Back up Files**:
    - `cp package.json package.json.bak`
    - Backup the lockfile (e.g., `cp pnpm-lock.yaml pnpm-lock.yaml.bak`).
    - _Verification_: Check that backup files exist.

### 2. Execution

Choose one of the following upgrade paths based on the detected manager:

| Manager  | Path                  | Command                                                    |
| :------- | :-------------------- | :--------------------------------------------------------- |
| **npm**  | **Full (Semver)**     | `npm update`                                               |
|          | **Targeted (Latest)** | `npm install <package>@latest`                             |
| **pnpm** | **Full (Semver)**     | `pnpm update`                                              |
|          | **Full (Latest)**     | `pnpm update --latest`                                     |
|          | **Targeted**          | `pnpm update <package>`                                    |
| **yarn** | **Full (Semver)**     | `yarn upgrade` (v1)                                        |
|          | **Full (Latest)**     | `yarn upgrade --latest` (v1) or `yarn up` (v2+)            |
|          | **Targeted**          | `yarn upgrade <package>` (v1) or `yarn up <package>` (v2+) |
| **bun**  | **Full (Semver)**     | `bun update`                                               |
|          | **Full (Latest)**     | `bun update --latest`                                      |
|          | **Targeted**          | `bun add <package>@latest`                                 |

_Note_: For `yarn` v2+, use `yarn up -i` for interactive upgrades if possible.

### 3. Validation

1.  **Verify Updates**:
    - Check the lockfile for changes.
2.  **Run Tests**:
    - Run the test suite: `${PM_COMMAND} test`.
    - _Verification_: Ensure all tests pass with the upgraded dependencies.

### 4. Finalization

1.  **Cleanup**:
    - If validations pass, remove backups: `rm package.json.bak <lockfile>.bak`.
2.  **Commit Changes**:
    - Commit `package.json` and the lockfile.

## Rollback / Failure Handling

If any step fails:

1.  **Restore Files**:
    - `mv package.json.bak package.json`
    - `mv <lockfile>.bak <lockfile>`
2.  **Re-install**:
    - Run `${PM_COMMAND} install` to ensure the environment matches the restored state.
3.  **Report Failure**:
    - Provide failure logs and list the packages that were being upgraded.
