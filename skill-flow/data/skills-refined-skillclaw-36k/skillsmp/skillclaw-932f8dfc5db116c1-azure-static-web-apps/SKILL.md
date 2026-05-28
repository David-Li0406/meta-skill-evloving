---
name: azure-static-web-apps
description: Use this skill when you need to create, configure, and deploy Azure Static Web Apps using the SWA CLI, including local development setup and CI/CD integration.
---

# Skill body

## Overview

Azure Static Web Apps (SWA) hosts static frontends with optional serverless API backends. The SWA CLI (`swa`) provides local development emulation and deployment capabilities.

**Key features:**

- Local emulator with API proxy and auth simulation
- Framework auto-detection and configuration
- Direct deployment to Azure
- Database connections support

**Config files:**

- `swa-cli.config.json` - CLI settings, **created by `swa init`** (never create manually)
- `staticwebapp.config.json` - Runtime config (routes, auth, headers, API runtime) - can be created manually

## General Instructions

### Installation

```bash
npm install -D @azure/static-web-apps-cli
```

Verify installation with:

```bash
npx swa --version
```

### Quick Start Workflow

**IMPORTANT: Always use `swa init` to create configuration files. Never manually create `swa-cli.config.json`.**

1. Run `swa init` - **Required first step** - auto-detects framework and creates `swa-cli.config.json`.
2. Run `swa start` - Start the local emulator at `http://localhost:4280`.
3. Run `swa login` - Authenticate with Azure.
4. Run `swa deploy` - Deploy your application to Azure.

### Configuration Files

**swa-cli.config.json** - Created by `swa init`, do not create manually:

- Run `swa init` for interactive setup with framework detection.
- Run `swa init --yes` to accept auto-detected defaults.
- Edit the generated file only to customize settings after initialization.

Example of generated config (for reference only):

```json
{
  "$schema": "https://aka.ms/azure/static-web-apps-cli/schema",
  "configurations": {
    "app": {
      "appLocation": ".",
      "apiLocation": "api",
      "outputLocation": "dist",
      "appBuildCommand": "npm run build",
      "run": "npm run dev",
      "appDevserverUrl": "http://localhost:3000"
    }
  }
}
```

**staticwebapp.config.json** (in app source or output folder) - This file CAN be created manually for runtime configuration:

```json
{
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/images/*", "/css/*"]
  },
  "routes": [
    { "route": "/api/*", "allowedRoles": ["authenticated"] }
  ],
  "platform": {
    "apiRuntime": "node:20"
  }
}
```