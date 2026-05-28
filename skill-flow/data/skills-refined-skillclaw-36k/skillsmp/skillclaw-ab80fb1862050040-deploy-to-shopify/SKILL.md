---
name: deploy-to-shopify
description: Use this skill when you have committed code changes and are ready to deploy them to the Shopify live theme, ensuring safety checks to prevent overwriting admin changes.
---

# Deploy to Shopify

Deploy local code to Shopify live theme with built-in safety checks that prevent overwriting admin changes.

## Usage

Execute the deployment script:

```bash
./scripts/deploy-to-shopify.sh
```

The script will:
1. Check for uncommitted local changes (exits if any found).
2. Pull the latest code from the git remote.
3. **Sync from Shopify admin** (critical safety check).
4. Show any admin changes that would be overwritten.
5. Prompt for review if admin changes are detected.
6. Commit admin changes to git before deployment.
7. Deploy to Shopify live theme.
8. Report completion status.

## Safety Checks

**Guard 1: Uncommitted Changes**
- Script exits if you have uncommitted local changes to ensure you don't lose local work.

**Guard 2: Git Sync**
- Pulls the latest code from remote before deploying to ensure you're deploying the latest version.

**Guard 3: Shopify Sync (Critical)**
- Pulls config and templates from Shopify admin before deploying.
- Shows exactly what admin changes would be overwritten.
- Commits admin changes to git BEFORE deployment to prevent data loss.

## Error Handling

**If the script reports uncommitted changes:**
- Commit your local work first:
  ```bash
  git add <files>
  git commit -m "Descriptive message"
  git push
  ```
- Then retry: `./scripts/deploy-to-shopify.sh`.

**If admin changes are detected:**
- The script will show you the changes and prompt for review with options:
  1. Review the changes (shows full diff).
  2. Commit and continue deployment (recommended).
  3. Abort deployment.
- If you choose to continue, admin changes are committed before deployment.

**If git pull fails:**
- Resolve merge conflicts manually.
- Then retry deployment.

**If Shopify deployment fails:**
- Check the error message from Shopify CLI.
- Report the error if unclear.

## When to Use This Skill

Run `/deploy-to-shopify` when:
- You've committed code changes and pushed to git.
- You're ready to make changes live on Shopify.
- At the end of a work session (after `/session-close`).

Do NOT use this skill if:
- You have uncommitted changes (commit first).
- You haven't tested your changes locally (test first).
- You're still actively developing (wait until the feature is complete).