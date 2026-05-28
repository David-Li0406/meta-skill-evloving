---
name: deploy-to-shopify
description: Deploy local code to Shopify live theme with safety checks. Always syncs from Shopify admin before deploying to prevent overwriting admin changes. Use after committing and pushing code to git.
---

# Deploy to Shopify

Deploy local code to Shopify live theme with built-in safety checks that prevent overwriting admin changes.

## Codex Notes

- Run from the repo root.
- Surface script output in your response (admin changes, diff summary, deploy status).
- If the script fails, stop and report the error without retrying.

## Usage

Execute the deployment script:

```bash
./scripts/deploy-to-shopify.sh
```

The script will:
1. Check for uncommitted local changes (exits if any found)
2. Pull latest code from git remote
3. **Sync from Shopify admin** (critical safety check)
4. Show any admin changes that would be overwritten
5. Prompt for review if admin changes detected
6. Commit admin changes to git before deployment
7. Deploy to Shopify live theme
8. Report completion status

## Safety Checks

**Guard 1: Uncommitted Changes**
- Script exits if you have uncommitted local changes
- Ensures you don't lose local work

**Guard 2: Git Sync**
- Pulls latest code from remote before deploying
- Ensures you're deploying the latest version

**Guard 3: Shopify Sync (Critical)**
- Pulls config and templates from Shopify admin before deploying
- Shows exactly what admin changes would be overwritten
- Commits admin changes to git BEFORE deployment
- This is the key safeguard that prevents data loss

## Error Handling

**If the script reports uncommitted changes:**
- Commit your local work first:
  ```bash
  git add <files>
  git commit -m "Descriptive message"
  git push
  ```
- Then retry: `./scripts/deploy-to-shopify.sh`

**If admin changes are detected:**
- Script will show you the changes and prompt for review
- Options:
  1. Review the changes (shows full diff)
  2. Commit and continue deployment (recommended)
  3. Abort deployment
- If you choose to continue, admin changes are committed before deployment

**If git pull fails:**
- Resolve merge conflicts manually
- Then retry deployment

**If Shopify deployment fails:**
- Check error message from Shopify CLI
- Report error to Jared if unclear

## When to Use This Skill

Run `/deploy-to-shopify` when:
- You've committed code changes and pushed to git
- You're ready to make changes live on Shopify
- At the end of a work session (after `/session-close`)

Do NOT use this skill if:
- You have uncommitted changes (commit first)
- You haven't tested your changes locally (test first)
- You're still actively developing (wait until feature is complete)

## Reporting to Jared

After successful deployment, report:
- Whether admin changes were detected and committed
- Summary of what was deployed
- Confirmation that deployment succeeded
- Link to live site: https://june-lingerie-2.myshopify.com

## Notes

- This skill enforces the correct deployment workflow
- The pre-deployment sync from Shopify is the critical safeguard
- By syncing immediately before deploying, we minimize the timing window for data loss
- If you're unsure whether to deploy, ask Jared first
