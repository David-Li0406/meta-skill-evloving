---
name: review-workspace-changes
description: Review code changes across all repositories in a workspace
---

# review-workspace-changes

## Overview

This skill reviews code changes across all repositories in a workspace by delegating to the `review-workspace-repo-changes` agent for each repository. It collects all review results and provides a comprehensive summary.

## Steps

### 1. Identify the Workspace

First, determine which workspace to review:

- If the user specifies a workspace directory (e.g., `workspace/feature-user-auth-20260116`), use that
- If not specified, ask the user which workspace they want to review
- List available workspaces if needed:

```bash
ls -d workspace/*/
```

### 2. Understand the Task Context

Read the workspace README.md to understand:
- Task name and type
- Task description
- Target repositories
- Base branches for each repository

```bash
cat workspace/{workspace-name}/README.md
```

### 3. Identify Repositories to Review

Find all repository worktrees in the workspace:

```bash
# List all directories in the workspace (excluding README and TODO files)
ls -d workspace/{workspace-name}/*/
```

Common patterns:
- Repository directories are typically named: `{repo-name}` or `{org}_{repo-name}`
- Each repository should have a corresponding `TODO-{repo-name}.md` file
- Repositories are git worktrees

For each repository directory:
1. Extract the repository name
2. Determine the base branch (from README.md or ask user)
3. Prepare parameters for the review agent

### 4. Create Reviews Directory

Create a directory for storing review results. **Important**: Capture the timestamp once and reuse it for all parallel agents to ensure consistency.

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p workspace/{workspace-name}/reviews/${TIMESTAMP}
```

### 5. Delegate to Review Agent for Each Repository

For each repository in the workspace, use the Task tool to launch the `review-workspace-repo-changes` agent:

```yaml
Task tool:
  subagent_type: review-workspace-repo-changes
  prompt: |
    Review changes for repository in workspace.

    Task Name: {task-name}
    Workspace Directory: workspace/{workspace-name}
    Repository Path: {org/repo-path}
    Repository Name: {repo-name}
    Repository Worktree Path: workspace/{workspace-name}/{repo-directory}
    Base Branch: {base-branch}

    Save review to: workspace/{workspace-name}/reviews/{timestamp}/{org}_{repo-name}.md
```

**Example**: For repository `github.com/sters/complex-ai-workspace`, the filename would be `github.com_sters_complex-ai-workspace.md` (slashes replaced with underscores).

**Important**: Launch review agents in parallel if there are multiple repositories to review efficiently. Pass the same `{timestamp}` value to all agents.

### 6. Collect Review Results

After all review agents complete, read each review document:

```bash
ls workspace/{workspace-name}/reviews/{timestamp}/*.md
```

For each review file, extract:
- Overall assessment
- Critical issues count
- Warnings count
- Suggestions count
- Key recommendations

### 7. Create Summary Report

Create a consolidated summary at `workspace/{workspace-name}/reviews/{timestamp}/SUMMARY.md`:

```markdown
# Workspace Review Summary

**Workspace**: {workspace-name}
**Review Date**: {timestamp}
**Repositories Reviewed**: {count}

## Overview

{Brief overview of the workspace task and what was reviewed}

## Summary by Repository

### {Repository 1 Name}

- **Review File**: [{org}_{repo-name}.md](./{org}_{repo-name}.md)
- **Overall Assessment**: {assessment}
- **Critical Issues**: {count}
- **Warnings**: {count}
- **Suggestions**: {count}
- **Key Points**: {1-2 sentence summary}

### {Repository 2 Name}

...

## Aggregate Statistics

- **Total Critical Issues**: {sum across all repos}
- **Total Warnings**: {sum across all repos}
- **Total Suggestions**: {sum across all repos}
- **Files Reviewed**: {sum across all repos}

## Top Priority Issues

{List the most critical issues across all repositories}

1. **{Repository}**: {Critical issue description}
2. **{Repository}**: {Critical issue description}
...

## Overall Recommendations

{Consolidated recommendations across all repositories}

1. {Recommendation 1}
2. {Recommendation 2}
...

## Next Steps

{Suggested actions based on the review findings}

- [ ] Address critical issues in {repository}
- [ ] Review and fix warnings
- [ ] Consider suggestions for code quality improvements
- [ ] Update tests as recommended
- [ ] Update documentation as needed

## Conclusion

{Final assessment of the workspace changes}
```

### 8. Present Summary to User

Display a concise summary to the user:

```
## Review Complete

Reviewed {count} repositories in workspace/{workspace-name}

**Results Summary**:
- Critical Issues: {total}
- Warnings: {total}
- Suggestions: {total}

**Reports Generated**:
- Summary: workspace/{workspace-name}/reviews/{timestamp}/SUMMARY.md
- Individual Reviews:
  - {org}_{repo1}.md
  - {org}_{repo2}.md
  ...

**Top Priorities**:
1. {Most critical issue}
2. {Second most critical issue}
...

**Recommendation**: {High-level recommendation about merge readiness}
```

## Example Usage

### Example 1: Review Current Workspace

```
User: Review the changes in my current workspace
Assistant: Let me review the workspace. First, I'll identify which workspace you're working in...
[Reads README.md, identifies repositories, launches review agents]
[After completion]
Review complete! I found 2 critical issues and 5 warnings across 3 repositories.
Summary: workspace/feature-user-auth-20260116/reviews/20260116-103045/SUMMARY.md
```

### Example 2: Review Specific Workspace

```
User: Review workspace/feature-login-fix-20260115
Assistant: I'll review the workspace/feature-login-fix-20260115 workspace...
[Identifies 2 repositories, launches agents in parallel]
[After completion]
Review complete! All changes look good with 0 critical issues and 3 suggestions.
```

## Tips

- **Parallel Execution**: Launch all repository review agents in parallel for faster execution
- **Error Handling**: If a repository review fails, continue with others and report which failed. Include a "Failed Reviews" section in the summary with the repository name and error message for debugging.
- **User Confirmation**: If unsure about base branches, ask the user before proceeding
- **Comprehensive Output**: Always generate both individual reviews and a summary report
- **Relative Paths**: Use relative paths in the summary to make markdown links work correctly
- **Filename Format**: Always replace slashes (`/`) in repository paths with underscores (`_`) when generating filenames

## Notes

- The skill delegates actual review work to the `review-workspace-repo-changes` agent
- Each repository is reviewed independently and in parallel
- Review results are timestamped to avoid overwriting previous reviews
- The summary provides a high-level view while individual reports contain detailed findings
