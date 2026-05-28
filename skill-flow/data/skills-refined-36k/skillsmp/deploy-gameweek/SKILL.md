---
name: deploy-gameweek
description: Deploys verified gameweek data to staging and production. Use ONLY after the user has verified the data locally using fetch-gameweek skill.
allowed-tools: Bash(python3:*), Bash(git:*), Read
---

# FPL Gameweek Deployer

Deploys verified gameweek data to staging and production GitHub Pages.

## ⚠️ IMPORTANT

**This skill should ONLY be used AFTER:**
1. Running `fetch-gameweek` skill
2. Verifying data locally at http://localhost:8000
3. User confirms everything looks good

## Workflow

This is **Step 2** of the two-step workflow:
1. **fetch-gameweek skill**: Fetch data → Serve locally → Verify
2. **This skill**: Deploy to staging/production

## What This Skill Does

1. Runs `deploy-github-clean.py` to regenerate docs and build
2. Commits changes to git with a descriptive message
3. Pushes to `staging` branch first
4. **Asks user** if they want to push to `main` (production)
5. If approved, pushes to `main` branch

## Usage

User: "Deploy gameweek 18"

I will:
- Deploy to staging automatically
- Ask before pushing to production

## Commands I Execute

### Deploy to Staging
```bash
python3 deploy-github-clean.py
git add .
git commit -m "Add GW18 data"
git push origin staging
```

### Deploy to Production (After User Approval)
```bash
git push origin main
```

## Deployment Process

### Step 1: Run Deployment Script
`deploy-github-clean.py` does:
- Converts CSVs to JSON
- Generates league table
- Creates social preview images
- Updates standings
- Builds docs folder

### Step 2: Git Commit
- Adds all changes
- Creates commit with message: "Add GW{X} data"
- Includes timestamp

### Step 3: Push to Staging
- Pushes to `staging` branch
- GitHub Pages deploys automatically
- User can verify at staging URL

### Step 4: Push to Production (With Confirmation)
- **Asks user**: "Push to production?"
- If yes: Pushes to `main` branch
- If no: Stops here (can push manually later)

## Safety Features

1. **Staging first**: Always deploys to staging before production
2. **User confirmation**: Requires explicit approval before production push
3. **Git safety**: No force pushes, no destructive operations
4. **Rollback available**: User can revert commits if needed

## What Gets Deployed

All files in the gameweek directory:
- CSV files (match results, transfers, players, fixtures)
- Summary files (`summary_gwX.csv`, `ai_summary_gwX.md`)
- Static files (`fixture_list.csv`, `starting_draft.csv`, `draftdata25_26.xlsx`)
- Generated docs (JSON, images, HTML)

## After Deployment

- **Staging**: https://[your-staging-url].github.io
- **Production**: https://[your-production-url].github.io

GitHub Pages will automatically rebuild within 1-2 minutes.

## Troubleshooting

### Merge Conflicts
If you get merge conflicts:
```bash
git pull origin staging --rebase
# Resolve conflicts
git push origin staging
```

### Need to Rollback
```bash
git revert HEAD
git push origin staging
git push origin main
```

### Manual Push (Skip This Skill)
```bash
git push origin staging
git push origin main
```

## Important Notes

- **Always verify locally first** using fetch-gameweek skill
- **Staging is automatic**, production requires confirmation
- **No force pushes** - safe git operations only
- **Bearer token doesn't affect deployment** - only needed for fetching data
