---
name: workbench-github
description: Use this skill when creating pull requests from work items or wiring GitHub-specific actions with the Workbench CLI.
---

# Skill body

## Key settings

- `.workbench/config.json`: Set `github.owner`, `github.repository`, `github.host`, and `git.defaultBaseBranch`.
- Ensure GitHub authentication is configured (using a token or `gh auth login`).

## Commands

### Create a PR from a work item:
```bash
workbench github pr create TASK-0001 --fill
```

### Create a draft PR targeting a base branch:
```bash
workbench github pr create TASK-0001 --draft --base main --fill
```

## Output

- The PR URL is printed to stdout or returned in JSON format.
- The work item front matter is updated with the PR link.

## Guardrails

- Prefer using `workbench github pr create`; the command `workbench pr create` is deprecated.
- Use the `--fill` option to include the work item summary and acceptance criteria in the PR body.