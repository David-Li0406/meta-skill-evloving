---
name: refine-implementation
description: Review my code, check for issues, clean up implementation, refine before commit. Use when implementation is done and you want fresh-eyes review, code quality check, or to catch issues before committing.
disable-model-invocation: true
---

# Refine Implementation

Multi-pass quality review of recent implementation. Ensures code adheres to CLAUDE.md, skills, and project conventions before committing.

## Philosophy

You cannot objectively assess code you just wrote. This command provides fresh perspectives through specialized agents that review for different concerns. Multiple passes continue until the code meets quality standards.

## Process

### 1. Gather Context

**Implementation context** (run in parallel):

- `git diff` (or `git diff --cached` if staged) to see changes
- `git status` to understand scope
- `git log --oneline main..HEAD` to see commit history on this branch
- `gh pr view --json title,body` to get PR description (if exists)
- Read any relevant CLAUDE.md files in the changed directories

**Intent reconstruction** (if no conversation context):

If this is a fresh conversation on an existing branch, spawn a `code-explorer` agent:

> Analyze this branch to understand what was intentionally built. Review the PR description/title, commit messages, and actual code changes. Summarize: What features/capabilities were intentionally implemented? What problem was being solved?

Pass this context summary to all review agents.

### 2. Select and Launch Review Agents

Choose agents from the table below based on the nature of the changes. Launch selected agents in parallel. All agents use the `code-refiner` subagent type.

#### Required Agents

These agents run on every refinement pass:

| Agent             | Focus                                   | Behavior                                                                                                                                                                                                                                                                    |
| ----------------- | --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Dead Code**     | Find and remove unused code             | Delete unreferenced functions, variables, imports, and files. Remove commented-out code. If something is unused, delete it completely—no `_unused` prefixes or keeping "just in case".                                                                                      |
| **Code Elegance** | Improve maintainability and readability | Extract functions where naming would clarify intent. Reduce nesting depth. Improve variable/method names. Make code more beautiful and self-documenting. Remove unnecessary complexity without over-abstracting—three similar lines is better than a premature abstraction. |
| **Conventions**   | Match existing codebase patterns        | Check consistency with project style. Follow established patterns for similar code. Ensure new code looks like it belongs.                                                                                                                                                  |
| **Adherence**     | CLAUDE.md compliance                    | Check adherence to CLAUDE.md instructions. Verify skills/agents that should have been used were used. Flag deviations from documented patterns.                                                                                                                             |

#### Optional Agents

Select these based on what the changes involve:

| Agent             | When to Use                                                               | Focus                                                                                                                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Architecture**  | New domain models, significant new functionality, architectural additions | Identify anti-patterns (anemic domain model, god objects, feature envy). Suggest patterns that fit (strategy, decorator, repository). Review domain modeling and layer boundaries. **Escalate rather than fix**—frame as "Consider whether..." |
| **Test Coverage** | New functionality, bug fixes, refactors touching business logic           | Verify tests exist for new code paths. Check edge cases are covered. Identify untested branches. Flag missing test files for new classes.                                                                                      |
| **Documentation** | New public APIs, changed CLI interfaces, new configuration options        | Check README/CHANGELOG updates needed. Verify inline documentation for public interfaces. Ensure CLAUDE.md reflects new patterns or commands.                                                                                  |
| **Prompt Review** | Changes to Claude skills, CLAUDE.md files, agent prompts                  | Apply the `writing-claude-prompts` skill. Check for clarity, specificity, and actionability. Review instruction structure and examples.                                                                                        |

### 3. Review Agent Reports

After agents complete:

1. Review what each agent changed and their reasoning
2. For any major deletions or reverts, verify the reasoning is sound
3. **If reasoning seems wrong or missing context, resume the agent** to discuss before accepting
4. Reject or revert changes that undo intentional design decisions without strong justification

### 4. Handle Escalations

If any agent reported escalations:

1. Present each escalation to the user with the agent's reasoning
2. **Use AskUserQuestion**: "Was this intentionally requested, or should we reconsider?"
3. For confirmed removals, make the change
4. For intentional features, note them to avoid re-flagging in subsequent passes

### 5. Reconcile Changes

After reviewing and discussing with agents as needed:

1. Keep non-conflicting improvements
2. For conflicts, choose the better approach
3. Revert any changes that were rejected after discussion
4. Show the user what changed

### 6. Check for Another Pass

**Use AskUserQuestion** to ask about next steps:

- **Another pass** → Return to step 2
- **Review changes** → Show `git diff` and wait for feedback
- **Ready to commit** → Launch `committer` agent

### 7. Final Review (Optional)

If user wants to review:

- Show the full diff of all refinements
- Allow them to revert specific changes: `git checkout HEAD -- path/to/file`
- Proceed to commit when satisfied

## When to Stop Iterating

Stop after:

- No agents find issues to fix
- User indicates satisfaction
- 3 passes maximum (diminishing returns)

## Key Principles

- **No commits until user approves** - Changes stay uncommitted for review
- **Multiple perspectives** - Different agents catch different issues
- **Iterative improvement** - One pass rarely catches everything
- **User control** - Always show changes, never auto-commit
