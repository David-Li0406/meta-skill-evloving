# Command Patterns

Detailed patterns derived from official Anthropic slash commands.

## Pattern 1: Simple Git Workflow

For single git operations with context awareness.

**Source:** Anthropic's `commit.md`

**Structure:**
```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.

You have the capability to call multiple tools in a single response. Stage and create the commit using a single message. Do not use any other tools or do anything else. Do not send any other text or messages besides these tool calls.
```

**Key elements:**
- Granular `allowed-tools` with wildcards
- Context injection via `!`bash commands``
- Clear task instruction
- Explicit constraint on tool usage
- Multi-tool efficiency instruction

## Pattern 2: Complete Git Workflow

For multi-step git operations (commit → push → PR).

**Source:** Anthropic's `commit-push-pr.md`

**Structure:**
```markdown
---
allowed-tools: Bash(git checkout --branch:*), Bash(git add:*), Bash(git status:*), Bash(git push:*), Bash(git commit:*), Bash(gh pr create:*)
description: Commit, push, and open a PR
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`

## Your task

Based on the above changes:
1. Create a new branch if on main
2. Create a single commit with an appropriate message
3. Push the branch to origin
4. Create a pull request using `gh pr create`
5. You have the capability to call multiple tools in a single response. You MUST do all of the above in a single message. Do not use any other tools or do anything else. Do not send any other text or messages besides these tool calls.
```

**Key elements:**
- Expanded tool permissions for full workflow
- Numbered steps for clarity
- Conditional logic ("if on main")
- MUST emphasis for critical requirements

## Pattern 3: Multi-Agent Orchestration

For complex tasks requiring parallel agent work.

**Source:** Anthropic's `dedupe.md`

**Structure:**
```markdown
---
allowed-tools: Bash(gh issue view:*), Bash(gh search:*), Bash(gh issue list:*), Bash(gh api:*), Bash(gh issue comment:*)
description: Find duplicate GitHub issues
---

Find up to 3 likely duplicate issues for a given GitHub issue.

To do this, follow these steps precisely:

1. Use an agent to check if the Github issue (a) is closed, (b) does not need to be deduped (eg. because it is broad product feedback without a specific solution, or positive feedback), or (c) already has a duplicates comment that you made earlier. If so, do not proceed.
2. Use an agent to view a Github issue, and ask the agent to return a summary of the issue
3. Then, launch 5 parallel agents to search Github for duplicates of this issue, using diverse keywords and search approaches, using the summary from #1
4. Next, feed the results from #1 and #2 into another agent, so that it can filter out false positives, that are likely not actually duplicates of the original issue. If there are no duplicates remaining, do not proceed.
5. Finally, comment back on the issue with a list of up to three duplicate issues (or zero, if there are no likely duplicates)

Notes (be sure to tell this to your agents, too):

- Use `gh` to interact with Github, rather than web fetch
- Do not use other tools, beyond `gh` (eg. don't use other MCP servers, file edit, etc.)
- Make a todo list first
- For your comment, follow the following format precisely (assuming for this example that you found 3 suspected duplicates):

---

Found 3 possible duplicate issues:

1. <link to issue>
2. <link to issue>
3. <link to issue>

This issue will be automatically closed as a duplicate in 3 days.

- If your issue is a duplicate, please close it and 👍 the existing issue instead
- To prevent auto-closure, add a comment or 👎 this comment

🤖 Generated with [Claude Code](https://claude.ai/code)

---
```

**Key elements:**
- Sequential agent orchestration (steps 1-2)
- Parallel agent execution (step 3: "launch 5 parallel agents")
- Result aggregation (step 4: "feed results into another agent")
- Early exit conditions ("If so, do not proceed")
- Notes section for agents with tool constraints
- Exact output format template

## Pattern 4: Triage Workflow

For processing multiple items with criteria-based decisions.

**Source:** Anthropic's `oncall-triage.md`

**Structure:**
```markdown
---
allowed-tools: Bash(gh issue list:*), Bash(gh issue view:*), Bash(gh issue edit:*), TodoWrite
description: Triage GitHub issues and label critical ones for oncall
---

You're an oncall triage assistant for GitHub issues. Your task is to identify critical issues that require immediate oncall attention and apply the "oncall" label.

Repository: anthropics/claude-code

Task overview:

1. First, get all open bugs updated in the last 3 days with at least 50 engagements:
   ```bash
   gh issue list --repo anthropics/claude-code --state open --label bug --limit 1000 --json number,title,updatedAt,comments,reactions | jq -r '.[] | select((.updatedAt >= (now - 259200 | strftime("%Y-%m-%dT%H:%M:%SZ"))) and ((.comments | length) + ([.reactions[].content] | length) >= 50)) | "\(.number)"'
   ```

2. Save the list of issue numbers and create a TODO list with ALL of them. This ensures you process every single one.

3. For each issue in your TODO list:
   - Use `gh issue view <number> --repo anthropics/claude-code --json title,body,labels,comments` to get full details
   - Read and understand the full issue content and comments to determine actual user impact
   - Evaluate: Is this truly blocking users from using Claude Code?
     - Consider: "crash", "stuck", "frozen", "hang", "unresponsive", "cannot use", "blocked", "broken"
     - Does it prevent core functionality? Can users work around it?
   - Be conservative - only flag issues that truly prevent users from getting work done

4. For issues that are truly blocking and don't already have the "oncall" label:
   - Use `gh issue edit <number> --repo anthropics/claude-code --add-label "oncall"`
   - Mark the issue as complete in your TODO list

5. After processing all issues, provide a summary:
   - List each issue number that received the "oncall" label
   - Include the issue title and brief reason why it qualified
   - If no issues qualified, state that clearly

Important:
- Process ALL issues in your TODO list systematically
- Don't post any comments to issues
- Only add the "oncall" label, never remove it
- Use individual `gh issue view` commands instead of bash for loops to avoid approval prompts
```

**Key elements:**
- Role assignment ("You're an oncall triage assistant")
- Concrete bash command with complex jq filtering
- TodoWrite tool for systematic processing
- Decision criteria with specific keywords
- Conservative guidance ("Be conservative")
- Summary requirements
- Important constraints section

## Pattern 5: Cleanup Workflow

For maintenance operations with clear commands.

**Source:** Anthropic's `clean_gone.md`

**Structure:**
```markdown
---
description: Cleans up all git branches marked as [gone] (branches that have been deleted on the remote but still exist locally), including removing associated worktrees.
---

## Your Task

You need to execute the following bash commands to clean up stale local branches that have been deleted from the remote repository.

## Commands to Execute

1. **First, list branches to identify any with [gone] status**
   Execute this command:
   ```bash
   git branch -v
   ```
   
   Note: Branches with a '+' prefix have associated worktrees and must have their worktrees removed before deletion.

2. **Next, identify worktrees that need to be removed for [gone] branches**
   Execute this command:
   ```bash
   git worktree list
   ```

3. **Finally, remove worktrees and delete [gone] branches**
   Execute this command:
   ```bash
   # Process all [gone] branches, removing '+' prefix if present
   git branch -v | grep '\[gone\]' | sed 's/^[+* ]//' | awk '{print $1}' | while read branch; do
     echo "Processing branch: $branch"
     # Find and remove worktree if it exists
     worktree=$(git worktree list | grep "\\[$branch\\]" | awk '{print $1}')
     if [ ! -z "$worktree" ] && [ "$worktree" != "$(git rev-parse --show-toplevel)" ]; then
       echo "  Removing worktree: $worktree"
       git worktree remove --force "$worktree"
     fi
     # Delete the branch
     echo "  Deleting branch: $branch"
     git branch -D "$branch"
   done
   ```

## Expected Behavior

After executing these commands, you will:

- See a list of all local branches with their status
- Identify and remove any worktrees associated with [gone] branches
- Delete all branches marked as [gone]
- Provide feedback on which worktrees and branches were removed

If no branches are marked as [gone], report that no cleanup was needed.
```

**Key elements:**
- Comprehensive description in frontmatter
- Step-by-step command execution
- Detailed bash scripts with comments
- Notes explaining edge cases
- Expected behavior section
- Graceful handling of "nothing to do"

## Pattern 6: Comprehensive Review

For multi-aspect analysis with optional focus areas.

**Source:** Anthropic's `review-pr.md`

**Structure:**
```markdown
---
description: "Comprehensive PR review using specialized agents"
argument-hint: "[review-aspects]"
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Task"]
---

# Comprehensive PR Review

Run a comprehensive pull request review using multiple specialized agents, each focusing on a different aspect of code quality.

**Review Aspects (optional):** "$ARGUMENTS"

## Review Workflow:

1. **Determine Review Scope**
   - Check git status to identify changed files
   - Parse arguments to see if user requested specific review aspects
   - Default: Run all applicable reviews

2. **Available Review Aspects:**

   - **comments** - Analyze code comment accuracy and maintainability
   - **tests** - Review test coverage quality and completeness
   - **errors** - Check error handling for silent failures
   - **types** - Analyze type design and invariants (if new types added)
   - **code** - General code review for project guidelines
   - **simplify** - Simplify code for clarity and maintainability
   - **all** - Run all applicable reviews (default)

3. **Identify Changed Files**
   - Run `git diff --name-only` to see modified files
   - Check if PR already exists: `gh pr view`
   - Identify file types and what reviews apply

[... detailed workflow continues ...]

## Usage Examples:

**Full review (default):**
/pr-review-toolkit:review-pr

**Specific aspects:**
/pr-review-toolkit:review-pr tests errors
/pr-review-toolkit:review-pr comments
/pr-review-toolkit:review-pr simplify

**Parallel review:**
/pr-review-toolkit:review-pr all parallel

## Tips:

- **Run early**: Before creating PR, not after
- **Focus on changes**: Agents analyze git diff by default
- **Address critical first**: Fix high-priority issues before lower priority
- **Re-run after fixes**: Verify issues are resolved
```

**Key elements:**
- Quoted description in frontmatter
- Optional arguments with `$ARGUMENTS`
- Workflow phases with clear numbering
- Available options as bullet list
- Usage examples showing different invocations
- Tips section for best practices
- Integration guidance

## Common Elements Across Patterns

1. **Frontmatter always includes:**
   - `description` (required for discoverability)
   - `allowed-tools` (for commands needing bash/tools)

2. **Context section for git commands:**
   ```markdown
   ## Context
   - Current git status: !`git status`
   - Current branch: !`git branch --show-current`
   ```

3. **Clear task section:**
   ```markdown
   ## Your task
   [Instructions...]
   ```

4. **Explicit constraints:**
   ```markdown
   Do not use any other tools or do anything else.
   Do not send any other text or messages besides these tool calls.
   ```

5. **Notes for subagents:**
   ```markdown
   Notes (be sure to tell this to your agents, too):
   - [constraint 1]
   - [constraint 2]
   ```
