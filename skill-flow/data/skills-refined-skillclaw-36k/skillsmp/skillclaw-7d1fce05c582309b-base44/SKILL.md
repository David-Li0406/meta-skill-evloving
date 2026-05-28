---
name: base44
description: Use this skill when you need to manage Base44 projects and applications, including initialization, CLI operations, and SDK usage.
---

# Skill body

## ⚡ IMMEDIATE ACTION REQUIRED - Read This First

This skill activates on ANY mention of "base44" or when a `base44/` folder exists. **DO NOT read documentation files or search the web before acting.**

### Step 1: Check Project Status

1. Check if `base44/config.jsonc` exists in the current directory.

### If **YES** (existing project scenario):

- **Authentication Check**: 
  1. Run:
     ```bash
     npx base44 whoami
     ```
  2. If the user is logged in (command succeeds and shows an email):
     - Proceed with the requested task using Base44 SDK.
  3. If the user is NOT logged in (command fails or shows an error):
     - **STOP immediately**.
     - Ask the user to log in manually by running:
       ```bash
       npx base44 login
       ```
     - Wait for the user to confirm they have logged in before continuing.

- **Handle SDK Operations**: 
  - Implement features using Base44 SDK modules (entities, auth, agents, functions, integrations, analytics).
  - Respond to requests for building features or writing code.

### If **NO** (new project scenario):

- **Project Initialization**:
  - Guide the user through project initialization.
  - Do NOT activate SDK operations until the project is initialized.

### Important Notes

- **Local Installation Only**: 
  - NEVER call `base44` directly. The CLI is installed locally as a dev dependency and must be accessed via a package manager:
    - `npx base44 <command>` (npm - recommended)
    - `yarn base44 <command>` (yarn)
    - `pnpm base44 <command>` (pnpm)

- **Do Not Use SDK for Initialization**: 
  - The SDK should not be used for initializing new Base44 projects. Use the CLI for that purpose.

This skill consolidates the functionalities of both the base44-cli and base44-sdk, ensuring a seamless experience for managing Base44 projects and applications.