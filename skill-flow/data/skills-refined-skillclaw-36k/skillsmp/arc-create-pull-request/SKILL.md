---
name: arc-create-pull-request
description: Create a pull request following project PR guidelines and template. Use this when asked to draft or create a PR.
---

# Skill: Create Pull Request (Project Workflow)

<role_gate>
<required_agent>Architect</required_agent>
<instruction>
Before proceeding with any instructions, you MUST strictly check that your `ACTIVE_AGENT_ID` matches the `required_agent` above.

Match Case:

- Proceed normally.

Mismatch Case:

- You MUST read the file `.github/agents/{required_agent}.agent.md`.
- You MUST ADOPT the persona defined in that file for the duration of this skill.
- Proceed with the skill acting as the {required_agent}.

</instruction>
</role_gate>

## Purpose

Provide a repeatable, guideline-compliant process to draft or create a Pull Request for this repository.

## When to Use

- The user asks to create a PR, draft a PR description, or prepare PR content.

## When Not to Use

- If no changes exist between the current branch and base branch.
- If the user only wants a high-level explanation without PR creation.

## Inputs and Assumptions

- Workspace is a git repository.
- Base branch is typically `main` unless otherwise specified.
- Follow:
  - `knowledge/guidelines/pr-creation-guidelines.md`
  - `knowledge/templates/issues/pull_request.md`

## Procedure

1. **Load PR standards**
   - Read `knowledge/guidelines/pr-creation-guidelines.md`.
   - Read `knowledge/templates/issues/pull_request.md`.

2. **Check repository state**
   - Run `git status`.
   - Identify base branch (default `main`). If unclear, run `git branch -a`.

3. **Verify actual code changes**
   - Run `git diff <base_branch>...HEAD --stat`.
   - For each significant changed file, run:
     - `git diff <base_branch>...HEAD -- <file>`
   - If no changes, stop and report.

4. **Draft PR title & description**
   - Title: clear and concise.
   - Description must follow the template sections:
     - Context (Why)
     - Changes (What) + Impact Scope
     - Verification (Proof)
     - Risks
     - Self-Check
   - Include issue link if known (e.g., `Fixes #123`).

5. **Create PR**
   - Preferred: use GitHub MCP create PR tool if available.
   - Alternative: use `gh pr create --title "<Title>" --body "<Description>"`.
   - If automation fails, provide title/body for manual creation.

## Outputs

- A PR title and description aligned with project guidelines.
- A created PR link if successfully created.

## Error Handling / Edge Cases

- **No changes**: report and stop.
- **Missing base branch**: ask the user to confirm.
- **Template mismatch**: report and align with `knowledge/templates/issues/pull_request.md`.

## Final Check

- [ ] Title is clear and concise.
- [ ] Description follows the required structure.
- [ ] Changes are verified from actual diffs.
- [ ] Verification steps cover impact scope.
- [ ] Risks are documented.
