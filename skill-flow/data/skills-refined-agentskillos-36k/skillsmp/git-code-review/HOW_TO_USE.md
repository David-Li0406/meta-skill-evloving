# How to Use This Skill

Hey Claude—I just added the "git-code-review" skill. Can you analyze git commits for specific users and generate code review reports?

## Example Invocations

**Example 1:**
Hey Claude—I just added the "git-code-review" skill. Can you review git commits for users 'john' and 'mary' from the last 3 days?

**Example 2:**
Hey Claude—I just added the "git-code-review" skill. Can you generate a code review report for user 'alex' for today's commits?

**Example 3:**
Hey Claude—I just added the "git-code-review" skill. Can you analyze all commits by 'sarah' and 'mike' this week?

**Example 4:**
Hey Claude—I just added the "git-code-review" skill. Can you get detailed code review for my recent changes as the current user?

## What to Provide

- **User Names**: One or multiple git usernames, separated by commas
  - Example: "john,mary,alex"
  - Example: "current-user" (for your own commits)

- **Time Period**: Optional number of days to look back
  - Example: "3" (last 3 days)
  - Example: "7" (last week)
  - If not specified, defaults to current day

- **Repository Context**: Must be run from within the git repository you want to analyze

## What You'll Get

1. **Individual Reports**: Separate markdown reports for each user
   - Location: `current-repo/.claude/git_code_review/`
   - Format: `username-date.md`

2. **Report Contents**:
   - Commit summaries organized by file
   - Line-by-line change analysis
   - Code quality assessments
   - Best practice recommendations
   - Potential issues flagged
   - Improvement suggestions

3. **Processing Summary**:
   - List of users processed
   - Number of commits analyzed per user
   - Paths to generated reports
   - Any errors encountered

## Python Script Usage

You can also use the Python script directly:

```bash
# Basic usage
python git_code_review.py --users "john,mary" --days 3

# Current day only
python git_code_review.py --users "alex"

# Specify repository path
python git_code_review.py --users "sarah,mike" --days 7 --repo "/path/to/your/repo"
```

## Report Structure

Each generated report includes:

1. **Summary Section**: Overview of analyzed commits
2. **Commit Details**: Individual commit analysis with:
   - File changes by type (added, modified, deleted, renamed)
   - Commit message assessment
   - Complexity scoring
3. **Issues & Suggestions**: Specific feedback on code changes
4. **Best Practices**: Relevant coding standards and guidelines
5. **Checklist**: Review checklist for quality assurance

## Tips for Best Results

1. **Run from Repository Root**: Ensure you're in the git repository you want to analyze
2. **Accurate Usernames**: Use exact git commit author names (case-sensitive)
3. **Reasonable Time Windows**: Start with 1-7 days for manageable reports
4. **Review Reports**: Use generated reports as discussion starters in team reviews
5. **Follow Up**: Address flagged issues in subsequent commits

## Integration with Development Workflow

- **Pre-PR Review**: Generate reports before creating pull requests
- **Team Syncs**: Share reports during code review meetings
- **Quality Tracking**: Track code quality trends over time
- **Onboarding**: Help new team members understand codebase patterns
- **Retrospectives**: Use reports for process improvement discussions