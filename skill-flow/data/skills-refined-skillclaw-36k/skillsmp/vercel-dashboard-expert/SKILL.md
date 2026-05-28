---
name: vercel-dashboard-expert
description: Expert in connecting to and managing Vercel Dashboard via CLI
---

# Vercel Dashboard Expert

This skill provides expertise in interacting with the Vercel ecosystem directly from the command line, enabling seamless connection to the Vercel Dashboard.

## Capabilities
- **Project Linking**: Connecting local projects to Vercel projects.
- **Dashboard Access**: Opening the Vercel dashboard for the current project.
- **Deployment Management**: inspecting and managing deployments.
- **Environment Management**: syncing environment variables.

## Common Operations

### 1. Connect/Link Project
To connect the current directory to a Vercel project:
```bash
npx vercel link
```
*Use this when the user needs to associate the codebase with a Vercel deployment.*

### 2. Open Dashboard
To open the Vercel dashboard for the linked project in the browser:
```bash
npx vercel project open
# OR deeper link to deployments
npx vercel open --dash
```

### 3. Deployments
To check deployment status or create a new deployment:
```bash
# Deploy to preview
npx vercel deploy

# Deploy to production
npx vercel deploy --prod
```

### 4. Environment Variables
To pull environment variables from Vercel to `.env.local`:
```bash
npx vercel env pull .env.local
```

## Instructions for Agent
1. **Always use `npx`**: When running Vercel commands, prefix with `npx` to ensure the local or latest version is used (e.g., `npx vercel ...`).
2. **Check for Login**: If a command fails with auth errors, prompt the user to run `npx vercel login`.
3. **Linking is Prerequisite**: Ensure the project is linked (`npx vercel link`) before attempting to open the dashboard or pull env vars.
