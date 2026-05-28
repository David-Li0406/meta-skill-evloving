---
name: sync-from-shopify
description: Synchronize Shopify theme changes to git. Pull configuration and template changes from Shopify admin, commit them to git, and push to remote. Use when you need to pull theme updates from the Shopify admin editor or sync recent admin changes.
---

# Sync from Shopify

Pull theme changes from Shopify admin, commit them to git, and push to remote using the core sync script.

## Codex Notes

- Run from the repo root.
- Surface script output in your response (changed files, diff summary, push status).
- If the script fails, stop and report the error without retrying.

## Usage

Execute the Shopify sync script:

```bash
./scripts/shopify-sync.sh
```

The script will:
1. Check for uncommitted local changes (exits if any found)
2. Pull configuration and templates from Shopify admin
3. Review changes and show diff summary
4. Stage, commit, and push changes to remote
5. Report completion status

## Error Handling

**If the script reports uncommitted changes:**
- Commit your local work first:
  ```bash
  git add <files>
  git commit -m "Descriptive message"
  ```
- Then retry: `./scripts/shopify-sync.sh`

**If the script reports no changes:**
- This means Shopify admin matches your local files - no action needed

**If push fails:**
- The script will exit with an error
- Report the error to Jared and ask for guidance

## Reporting to Jared

After successful sync, report:
- What files were changed (from script output)
- A summary of the changes (from diff shown by script)
- Confirmation that changes are pushed to remote

## Notes

- The script focuses on config and template changes (the most common admin edits)
- Core logic lives in `scripts/shopify-sync.sh` and can be used by any agent
- For pulling ALL theme files, modify the script or use `shopify theme pull` directly
