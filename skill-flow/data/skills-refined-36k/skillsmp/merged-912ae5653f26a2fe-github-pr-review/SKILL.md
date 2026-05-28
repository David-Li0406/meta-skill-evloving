---
name: github-pr-review
description: Use this skill for conducting comprehensive code reviews of GitHub Pull Requests, automating data collection, and providing structured feedback.
---

# GitHub PR Review Skill

Conduct thorough code reviews for GitHub Pull Requests using the `gh` CLI and automated tooling. This skill helps in fetching PR metadata, analyzing code against industry-standard criteria, and optionally adding inline comments.

## Key Concepts

### Comment Types

GitHub PRs have **two different types of comments**:

1. **PR-level comments** - General discussion on the PR (shown via `gh pr view --comments`)
2. **Inline code review comments** - Comments attached to specific lines of code (requires API)

**Important**: `gh pr view --comments` does NOT show inline code review comments!

## Purpose

This skill performs code reviews by:

1. **Automating data collection** - Fetching all PR-related information (metadata, diff, comments, commits, issues).
2. **Organizing review workspace** - Creating a structured directory with all artifacts.
3. **Applying systematic criteria** - Reviewing against a comprehensive quality checklist.
4. **Facilitating inline feedback** - Optionally adding comments directly to PR code.
5. **Ensuring completeness** - Checking functionality, security, testing, and maintainability.

## When to Use

Activate this skill when:
- A GitHub PR URL is provided with a review request.
- Receiving "review this PR" or "code review" requests.
- Checking PR quality before merging.
- Providing systematic feedback on proposed changes.

## Review Process Workflow

**IMPORTANT**: This skill uses a **two-stage approval process**. Nothing is posted to GitHub until explicit approval with `/send` or `/send-decline`.

### Step 1: Fetch PR Data

Use `fetch_pr_data.py` to automatically collect all PR information:

```bash
python scripts/fetch_pr_data.py <pr_url> [--output-dir <dir>] [--no-clone]
```

**Actions performed:**
- Parse PR URL to extract owner, repo, and PR number.
- Create directory structure: `<output-dir>/PRs/<repo-name>/<PR-NUMBER>/`.
- Fetch PR metadata (title, author, state, branches, labels).
- Download PR diff and commit history.
- Retrieve all PR comments and reviews.
- Extract ticket references (JIRA, GitHub issues).
- Optionally clone source branch and generate git diff.

### Step 2: Analyze PR Data

After fetching, analyze collected data against review criteria:

1. Read `SUMMARY.txt` - High-level overview.
2. Review `metadata.json` - PR context, labels, assignees.
3. Examine `diff.patch` - Code changes.
4. Check `comments.json` - Existing feedback.
5. Review `commits.json` - Commit quality and messages.
6. Check `related_issues.json` - Linked tickets/issues.
7. Apply review criteria - Evaluate against a comprehensive checklist.

### Step 3: Generate Review Files

After analysis, use `generate_review_files.py` to create structured review documents:

```bash
python scripts/generate_review_files.py <pr_review_dir> --findings <findings_json> [--metadata <metadata_json>]
```

Creates three files in `pr_review_dir/pr/`:
1. **`pr/review.md`** - Detailed internal review.
2. **`pr/human.md`** - Clean review for posting.
3. **`pr/inline.md`** - Proposed inline comments with code snippets.

### Step 4: Review and Edit Files

**Use `/show` to open the review directory in VS Code.**

Actions available:
- Read `pr/review.md` - Detailed analysis.
- Edit `pr/human.md` - Modify before posting.
- Review `pr/inline.md` - Check proposed comments.

### Step 5: Approve and Post

Post the review when ready:

**Option A: Approve the PR**
```
/send
```

**Option B: Request Changes**
```
/send-decline
```

### Step 6: Apply Review Criteria

Reference `references/review_criteria.md` for a comprehensive checklist. Review against these categories:

| Category | Key Questions |
|----------|--------------|
| Functionality | Does code solve the problem? Bugs? Edge cases? |
| Readability | Clear code? Meaningful names? DRY? |
| Style | Follows linter rules? Consistent with codebase? |
| Performance | Efficient algorithms? Scalable? |
| Security | Vulnerabilities addressed? Secrets protected? |
| Testing | Tests exist? Cover happy paths and edge cases? |
| PR Quality | Focused scope? Clean commits? Clear description? |

## Reference Documentation

This skill includes comprehensive reference guides:

| Reference | Purpose |
|-----------|---------|
| `references/review_criteria.md` | Complete checklist covering functionality, security, testing, and more. |
| `references/gh_cli_guide.md` | Quick reference for GitHub CLI commands. |
| `references/scenarios.md` | Detailed workflows for common review scenarios. |
| `references/troubleshooting.md` | Common issues and solutions. |

## Scripts Reference

### `scripts/fetch_pr_data.py`

Automated PR data fetching and organization.

```bash
python scripts/fetch_pr_data.py <pr_url> [options]
```

### `scripts/generate_review_files.py`

Generate structured review files from analysis findings.

```bash
python scripts/generate_review_files.py <pr_review_dir> --findings <findings_json> [--metadata <metadata_json>]
```

### `scripts/add_inline_comment.py`

Add inline code review comments to specific lines in PR.

```bash
python scripts/add_inline_comment.py <owner> <repo> <pr_number> <commit_id> <file_path> <line> "<comment>" [options]
```

## Best Practices

### Communication
- Frame feedback as suggestions, not criticism.
- Explain why an issue matters, not just what is wrong.
- Acknowledge excellent practices.

### Review Efficiency
- Use scripts to automate data fetching and comment posting.
- Reference `review_criteria.md` as a checklist.

## Quick Reference Commands

```bash
# Fetch PR data
python scripts/fetch_pr_data.py https://github.com/owner/repo/pull/123

# Add inline comment
python scripts/add_inline_comment.py owner repo 123 latest "src/app.py" 42 "Comment"

# View PR in browser
gh pr view 123 --repo owner/repo --web

# Check PR status
gh pr checks 123 --repo owner/repo
```

## Tips for Effective Reviews

1. Start with context: Read PR description, linked issues, commit messages.
2. Understand intent: Identify the problem being solved.
3. Check tests first: Verify tests demonstrate the fix/feature.

**For troubleshooting:** Read `references/troubleshooting.md`.

## Resources

- **Review Criteria**: `references/review_criteria.md`
- **gh CLI Guide**: `references/gh_cli_guide.md`
- **Scenarios**: `references/scenarios.md`
- **Troubleshooting**: `references/troubleshooting.md`
- **GitHub PR Review Docs**: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests