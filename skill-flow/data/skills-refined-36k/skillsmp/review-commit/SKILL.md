---
name: review-commit
description: This skill should be used when the user types "/review-commit" or asks to review and clean up staged changes before committing. It launches the commit-cleaner agent to review code quality, remove redundancies, and prepare commits.
version: 1.0.0
---

# Review Commit Skill

This skill provides a convenient slash command to launch the commit-cleaner agent, which reviews and cleans up staged changes before committing.

## Usage

Simply type `/review-commit` and the commit-cleaner agent will be invoked to:
- Review all staged changes
- Remove redundant code and code smells
- Filter out documentation and tracking files
- Eliminate code duplication
- Ensure succinct implementations
- Organize assets into util folders
- Prepare code for a clean commit

## How It Works

When you invoke this skill, it automatically launches a Task with the `commit-cleaner` subagent. The agent will:

1. Analyze staged and unstaged changes using `git status` and `git diff`
2. Review code quality and identify issues
3. Clean up redundancies and code smells
4. Unstage non-essential files (docs, tracking MDs)
5. Organize assets into util-scripts/
6. Provide a summary of changes and files ready to commit

## When to Use

- Before committing code to ensure quality
- When you want to clean up messy staged changes
- To remove documentation files from staging
- To consolidate duplicate code before committing
- To get a code review before pushing changes

## Important Notes

**The commit-cleaner agent will NOT commit your changes.** It only prepares and cleans the staging area. You must run `git commit` manually after the agent completes its review.

## Example Workflow

```bash
# Stage your changes
git add .

# Review and clean
/review-commit

# After agent completes, commit manually
git commit -m "Your commit message"
```

## Integration with Git Workflow

This skill is designed to fit into your normal git workflow:

1. Make code changes
2. Stage files with `git add`
3. Run `/review-commit` to clean and review
4. Review the agent's summary
5. Commit manually with `git commit`

## What Gets Reviewed

The agent reviews:
- Source code files for redundancies and code smells
- Documentation files (to unstage them)
- Asset files (to organize them)
- Duplicate code across multiple files
- Code complexity and clarity

## What Gets Cleaned

The agent will:
- Remove dead code and unused imports
- Extract duplicate logic into utilities
- Replace magic numbers with constants
- Simplify nested conditionals
- Improve naming clarity
- Unstage documentation and tracking files
- Move assets to util-scripts/ folder
