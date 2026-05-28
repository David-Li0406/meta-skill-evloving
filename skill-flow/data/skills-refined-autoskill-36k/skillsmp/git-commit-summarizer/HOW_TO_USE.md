# How to Use This Skill

Hey Claude—I just added the "git-commit-summarizer" skill. Can you analyze git commits for specific users and generate summary reports?

## Example Invocations

**Example 1: Single User Analysis**
Hey Claude—I just added the "git-commit-summarizer" skill. Can you summarize git commits for user 'john.doe' over the last 3 days?

**Example 2: Multiple Users Analysis**
Hey Claude—I just added the "git-commit-summarizer" skill. Can you generate commit reports for 'alice,bob,charlie' for today?

**Example 3: Extended Period Analysis**
Hey Claude—I just added the "git-commit-summarizer" skill. Can you analyze all commits by 'dev-team' in the last 14 days?

**Example 4: Default (Today Only)**
Hey Claude—I just added the "git-commit-summarizer" skill. Can you summarize today's commits for 'maria.garcia'?

## What to Provide

- **Usernames**: One or more git usernames (comma-separated for multiple users)
  - Example: `john.doe` (single user)
  - Example: `alice,bob,charlie` (multiple users)

- **Days**: Optional number of days to analyze (defaults to today only)
  - Example: `3` (last 3 days)
  - Example: `7` (last week)
  - Omit for today-only analysis

## What You'll Get

1. **Individual User Reports**: Markdown files for each user with detailed commit analysis
   - Filename format: `[username]-[date].md` or `[username]-[date]-[days]days.md`
   - Location: `.claude/git_commit_report/` directory in current repository

2. **Multi-User Summary Report** (when analyzing multiple users):
   - Summary file: `summary-[date].md`
   - Includes overview table and links to individual reports

3. **Console Summary**: Processing results including:
   - Number of reports generated
   - File locations
   - Analysis statistics

## Report Contents

Each user report includes:

- **Summary Section**: Overview of user's activity
- **Statistics**: Total commits, files changed, average files per commit
- **Commits by Date Table**: Daily commit frequency
- **Detailed Commit List**: Each commit with hash, date, message, and changed files
- **File Change Statistics**: Insertions and deletions (when available)

## Important Notes

- **Repository Context**: This skill must be run from within a git repository directory
- **Username Accuracy**: Use exact git usernames as they appear in commit history
- **Report Location**: Reports are saved in `.claude/git_commit_report/` for easy access
- **Time Zones**: Analysis uses repository's local time settings
- **File Permissions**: Ensure you have write access to the repository directory

## Common Use Cases

- **Daily Standup Preparation**: Quickly review what each team member committed yesterday
- **Sprint Review**: Analyze commits over a sprint period (e.g., 14 days)
- **Individual Performance Tracking**: Monitor personal commit patterns over time
- **Team Activity Analysis**: Compare contributions across multiple developers
- **Code Review Preparation**: Get context on recent changes before reviewing code

## Troubleshooting

**"Not a git repository" error**: Make sure you're in a git repository directory.

**"No commits found"**: Verify the username is correct and there are commits in the specified period.

**"Permission denied"**: Check write permissions in the repository directory.

**Report files not appearing**: Check the `.claude/git_commit_report/` directory for generated files.