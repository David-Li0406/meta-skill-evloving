# commit-milestones

Automatically commit changes when reaching significant milestones during work sessions.

## Quick Start

This skill runs automatically. When you complete a significant piece of work, Claude will:
1. Review changes with `git status` and `git diff`
2. Stage relevant files
3. Create a descriptive commit message
4. Ask if you want to push to GitHub

## How It Works

```
┌──────────────────────────────────────────────┐
│  Milestone Detected                          │
│  (feature complete, bug fixed, etc.)         │
└─────────────────┬────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────┐
│  git status / git diff                       │
│  Review what changed                         │
└─────────────────┬────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────┐
│  git add <files>                             │
│  Stage relevant changes                      │
└─────────────────┬────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────┐
│  git commit -m "descriptive message"         │
│  Commit with Co-Authored-By                  │
└─────────────────┬────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────┐
│  "Push to GitHub?"                           │
│  Ask user for confirmation                   │
└──────────────────────────────────────────────┘
```

## What Triggers a Commit

Claude proactively commits after:
- Completing a feature implementation
- Fixing a bug
- Finishing a refactor
- Completing a set of tests
- Reaching a natural stopping point

## Commit Format

Commits include the Co-Authored-By line:
```
Implement user avatar upload feature

- Add avatar upload endpoint
- Resize images to max 500x500
- Store in S3 with signed URLs

Co-Authored-By: Claude <noreply@anthropic.com>
```

## For Claude Code

This skill runs automatically without explicit invocation. When you complete significant work:
1. Run `git status` and `git diff` to review changes
2. Stage relevant files with `git add`
3. Create a descriptive commit message explaining what was accomplished
4. Ask the user if they want to push to GitHub

Do this automatically without asking permission unless the changes are unclear or sensitive.
