---
name: deploy-dashboard
description: Deploy a meeting dashboard to surge.sh for public sharing. Use when the user wants to deploy, publish, share, or host a dashboard online.
allowed-tools: Bash
---

# Deploy Dashboard to Surge.sh

Deploy a meeting dashboard to surge.sh for public access.

## Instructions

1. Verify the dashboard exists at `projects/{project}/dashboards/{date}/index.html`
   - If it doesn't exist, generate it first using the generate-dashboard skill
2. Navigate to the dashboard directory
3. Run surge deployment:
   ```bash
   cd projects/{project}/dashboards/{date}
   surge . {project}-{date}.surge.sh
   ```
4. If surge requires authentication, guide the user through login
5. Report the deployed URL back to the user

## Deployment URL Convention

URLs follow the pattern: `https://{project}-{date}.surge.sh`

Example: `https://project-alpha-2026-01-12.surge.sh`

## Prerequisites

- surge.sh must be installed: `npm install -g surge`
- First deployment will prompt for surge.sh account creation/login

## Output

Report:
- ✓ Deployed to: {url}
- Provide the clickable link for easy access
