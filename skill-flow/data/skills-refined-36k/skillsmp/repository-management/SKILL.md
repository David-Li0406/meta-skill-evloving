---
name: repository-management
description: Standards for repository hygiene, security, and public documentation.
---

# Repository Management Best Practices

## Security & Hygiene
- **CRITICAL**: Never commit `.env` files or any file containing secrets/API keys.
- **Agent Sharing**: You **SHOULD** commit the `.agent/` folder (workflows, skills, rules) so that the team shares the same capabilities.
- **Rule Sharing**: `PROJECT_RULES.md` is now the shared source of truth and **SHOULD** be committed.
- **Gitignore Audit**: Verify that `.env` and `.claude/` (personal config) are in `.gitignore`.
- **Shell Syntax**: Use `&&` to chain commands in Bash.
- **Pre-Commit Scan**: Never run `git add .` without first running `git status` to check for untracked sensitive files.
  - **Explicit Block**: If you see files named `mcp.json` (especially in `.agent/`), `credentials.json`, `service_account.json`, or anything containing `token` or `secret`, **STOP**. Do not commit them. Add them to `.gitignore` immediately.
  - **Secret Scrubbing**: If you accidentally catch a secret in a commit history, you MUST rewrite the history (e.g., `git filter-branch` or `git rebase -i`) to remove it before pushing. Pushing a secret will block the push and require manual intervention.
- **Repository Sweep (Sub-Agent)**: You can spawn a sub-agent to perform a thorough security sweep:
  - `claude -p "Perform a deep security audit of the repository. Check all files (even ignored ones) for potential secrets and report findings." --agent "qa-bot"`

## Tool Hygiene
- **No Hammering**: If a tool call (like `mcp_list_resources` or `run_command`) fails, **DO NOT** retry the exact same call within the same step. Analyze the error message first. If a resource or command is not found, assume it is unavailable and ask the user or try an alternative approach.
- **Agent Folder Location**: The `claude` CLI strictly requires agents to be in `.claude/agents/`. **NEVER** try to place them in `.agent/agents/` or create new directories for them. Use the existing location.


## GitHub Operations
- **CLI Usage**: For PRs, Issues, and Releases, prefer using the GitHub CLI.
- **Skill Check**: Read `view_file .agent/skills/github-cli/SKILL.md` for specific commands and shortcuts.

## Public Documentation (README)
- **Mirroring Standards**: If `PROJECT_RULES.md` is ignored, ensure all development standards (styling, hooks, state management) are summarized in the public `README.md`.
- **Setup Clarity**: Always provide a "Getting Started" section that includes environment variable requirements.
- **Tech Stack Transparency**: Clearly list the technologies used (Expo, Supabase, NativeWind) to assist other developers or for your own future reference.

## Conventional Commits
- Use the format: `type(scope): description`.
- Common types: `feat`, `fix`, `chore`, `docs`, `refactor`, `style`, `test`.

## Workflow Stewardship
- **STRICT ADHERENCE**: Always follow the exact step-by-step instructions in `.agent/workflows/[workflow].md`. Never merge or shuffle steps between different workflows.
- **Checkpoint vs Completion**: When saving, explicitly verify if the work is a "Checkpoint" (partial work) or "Feature Complete". **NEVER** close the GitHub Issue for a Checkpoint save. Only close when the feature-set in the PRD is 100% finished.
- **State Restoration**: If you accidentally delete or move a specification file, DO NOT guess its content or restore a DIFFERENT file. Use your history or `git checkout` to restore the exact state.
- **REMOTE SYNCHRONIZATION**: Never consider a task "saved" or "done" until changes have been pushed to the remote repository (`origin`). Local commits alone create state drift that confuses both the user and the agent. The `@[/save]` workflow MUST always end with a successful `git push`.
