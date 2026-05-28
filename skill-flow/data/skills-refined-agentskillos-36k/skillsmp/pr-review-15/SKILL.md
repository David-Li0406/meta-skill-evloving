---
name: pr-review
description: Review GitHub pull requests
---

# PR Review Skill

This skill helps you conduct comprehensive reviews of GitHub pull requests.

**Supporting files**:
- `scripts/summarize-pr.py` - Comprehensive PR summary script (uses GraphQL)
- `scripts/prepare-worktree.py` - Create git worktree for PR review

**Important**: All scripts use `uv` for automatic dependency management. Run them directly (e.g., `scripts/summarize-pr.py`). If `uv` is not available, fall back to `python scripts/summarize-pr.py` but you'll need to install dependencies manually.

## When to Use This Skill

Use this skill when the user asks you to review a GitHub pull request. The user will typically provide a PR URL or PR number.

## How to Review a PR

### Step 1: Generate PR Summary

Start by generating a comprehensive summary of the PR. This gives you the complete picture before diving deep:

```bash
scripts/summarize-pr.py <OWNER> <REPO> <PR_NUMBER>
```

**This script provides:**
- PR metadata (title, author, status, branch, stats)
- Description
- Files changed with additions/deletions
- **Discussion & Reviews** - Chronological timeline of all comments and reviews
- **Unresolved Review Comments** - Code review threads that need addressing (with diff context)

**Read and analyze this output carefully:**
- What problem is being solved?
- What's the current discussion context?
- What unresolved issues already exist?
- Who has reviewed and what are their concerns?

**IMPORTANT**: The unresolved comments are **known blockers**. Don't duplicate these in your review - focus on finding NEW issues.

### Step 2: Prepare Git Worktree and Review Notes

Create a clean worktree for reviewing the PR and initialize review tracking:

```bash
WORKTREE_PATH=$(scripts/prepare-worktree.py <repository_directory> <PR_NUMBER>)
cd "$WORKTREE_PATH"
```

**What this does:**
- Creates a new worktree in `<repository>/git-worktrees/<branch-name>`
- Creates a review notes directory in `<repository>/review-notes/<branch-name>`
- Generates a `README.md` template in the review notes directory for tracking progress
- Fetches and checks out the PR branch in the worktree
- If the worktree already exists, checks for uncommitted changes before recreating
- Returns the path to the worktree directory

**Benefits:**
- Main repository stays on its current branch
- Can review multiple PRs simultaneously in different worktrees
- Clean separation between review work and regular development
- Review notes are organized per-PR with a structured template
- Progress tracking with checkboxes for each review step

**Use the review notes file:**
- Open `<repository>/review-notes/<branch-name>/README.md`
- Fill in notes as you progress through each step
- Check off tasks as you complete them
- Document unresolved comments and new issues found
- Write your final recommendation

### Step 3: Gather Context

This is the critical step that goes beyond mechanical checking. Based on the PR type and files changed, use the **Task tool with subagent_type=Explore** to gather additional context:

**For code PRs:**
- **Related files**: Files that import/use the changed code (to understand integration)
- **Test files**: Are there tests? Do they cover the changes?
- **Documentation**: README, API docs, comments - are they updated?
- **Configuration**: Are there deployment/config implications?
- **Recent related PRs**: Is this part of a larger effort?

**For design/documentation PRs (SDPs, RFCs, etc.):**
- **Related design docs**: Other SDPs or architectural decisions
- **Architecture principles**: Does this align with standards?
- **Existing implementations**: What code might be affected?
- **Previous discussions**: GitHub issues, meeting notes, etc.

**How to gather context:**
- Use `gh pr view` to see linked issues
- **Use Task tool with subagent_type=Explore** to search for:
  - Related files (imports, callers, tests)
  - Architectural standards or guidelines
  - Existing similar implementations
  - Documentation that needs updating
- Read the files you discover to understand integration points

**Example context gathering:**
```bash
# Use the Task tool with subagent_type=Explore to find:
# - "Find all files that import X module"
# - "Find test files related to Y feature"
# - "Find architecture docs about Z pattern"
```

### Step 4: Analyze the PR

Now review the PR comprehensively:

1. **Does it solve the stated problem?**
   - Compare the changes to the PR description
   - Check if the solution is complete

2. **Are unresolved comments blocking?**
   - Review the unresolved threads from Step 1's summary
   - Determine severity and impact

3. **What NEW issues exist?**
   - Things not already flagged in unresolved threads (from Step 1)
   - Consider: correctness, design, testing, documentation, edge cases

4. **Context and design concerns**
   - Does it fit the broader architecture?
   - Are there cross-cutting concerns (security, performance, etc.)?
   - Is the approach consistent with similar code?

**Review criteria by PR type:**

For **code PRs**:
- Correctness and logic
- Test coverage
- Error handling
- Performance implications
- Security concerns
- Documentation completeness
- Code style and conventions

For **design/documentation PRs**:
- Completeness of requirements
- Clarity of problem statement
- Well-defined use cases
- Consistency in terminology
- Alignment with architecture principles
- Missing sections or incomplete information
- Feasibility of implementation

### Step 5: Complete Review Notes and Provide Recommendation

As you work through the review, systematically fill in the review notes at `<repository>/review-notes/<branch-name>/README.md`:

1. **Step 1 - PR Summary Analysis**
   - Check off each task as you review the summary output
   - Document key observations in the Notes section
   - List unresolved comments under "Unresolved Comments (from PR)"

2. **Step 3 - Context Gathering**
   - Note what related files/tests/docs you examined
   - Document architectural concerns or patterns found
   - Check off tasks as you complete them

3. **Step 4 - Code Review**
   - Work through the changed files systematically
   - Check off review tasks as you complete them
   - Document new issues found under "New Issues Found" with `file:line` references

4. **Step 5 - Final Recommendation**
   - Select the appropriate status (Approve/Request Changes/Comment)
   - Write a clear summary of your findings
   - List specific, actionable items for the author
   - **Focus on NEW issues**, not duplicating unresolved comments

**Review notes structure:**
- **Unresolved Comments**: Issues already flagged in the PR discussion
- **New Issues Found**: Problems you discovered during review
- **Final Recommendation**: Your verdict and next steps
- Use `file:line` references for all code-specific feedback

## Output Format

Your review output should be written in the review notes file at `<repository>/review-notes/<branch-name>/README.md`.

The template provides sections for:
- PR Summary Analysis with checkboxes
- Context Gathering notes
- Code Review progress tracking
- Unresolved Comments (from existing PR discussion)
- New Issues Found (your discoveries)
- Final Recommendation with status and action items

Use code references in the format `file_path:line_number` when pointing to specific locations.

## Important Notes

- **Always start with summarize-pr.py** - This gives you the complete PR context upfront
- **Always use prepare-worktree.py** - Never checkout PRs in the main repository
- **Always use the review notes file** - Document your progress systematically in `review-notes/<branch-name>/README.md`
- **Always use the `gh` CLI tool** via Bash, never try to construct GitHub URLs manually
- **Prefer running scripts with uv** - The scripts have uv-style dependency declarations and will auto-install dependencies. Fall back to `python` only if `uv` is unavailable.
- **Don't duplicate unresolved threads** - They're already documented, focus on NEW issues
- **Use Task tool with subagent_type=Explore** for context gathering - this is where you add value
- **Be thorough but constructive** - provide specific, actionable feedback
- **Prioritize findings** by severity and impact
- **Check off tasks** in the review notes as you complete each step

## Example Workflow

```bash
# Step 1: Generate comprehensive PR summary
scripts/summarize-pr.py <OWNER> <REPO> <PR_NUMBER>

# Read and analyze the output:
# - What's the PR about?
# - What's the discussion history?
# - What unresolved issues exist?

# Step 2: Prepare git worktree
WORKTREE_PATH=$(scripts/prepare-worktree.py /path/to/repo <PR_NUMBER>)
cd "$WORKTREE_PATH"

# Step 3: Gather context using Task tool
# Use Task tool with subagent_type=Explore to find:
# - Related architecture docs
# - Similar implementations
# - Test coverage
# - Integration points

# Step 4: Analyze the PR
# - Read changed files
# - Check for issues not in unresolved threads
# - Verify alignment with context found

# Step 5: Provide structured review
# Follow the 5-section format above
```
