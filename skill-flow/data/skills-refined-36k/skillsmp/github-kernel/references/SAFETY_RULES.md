# Safety Rules & Guidelines

## Core Principles

1. **Do No Harm**: Never perform destructive actions without checking context and, if necessary, asking for confirmation.
2. **Least Privilege**: Do not change repository settings or secrets unless that is the explicit task.
3. **Transparency**: Always log or report what actions were taken.

## Operation Categories

### 🟢 Safe (Auto-Run Allowed)

- **Reading Data**: `issue_read`, `get_file_contents`, `search_code`.
- **Non-Disruptive Writing**: `add_issue_comment` (if helpful), `create_branch`.
- **Drafting**: `create_pull_request` (as draft).

### 🟡 Sensitive (Careful Execution)

- **State Changes**: `issue_write` (closing issues), `update_pull_request` (changing base/status).
- **Code Modification**: `push_files`, `create_or_update_file`.
- **Reviewing**: `pull_request_review_write` (APPROVE/REQUEST_CHANGES).
  - _Rule_: Verify context before approving.

### 🔴 Destructive (User Confirmation Required)

- **Deletion**: `delete_file`, deleting branches (unless temporary task branches).
- **Force Pushes**: `git push --force`.
- **Repo Administration**: Changing visibility, deleting repos, adding collaborators.
- **Merging**: `merge_pull_request` to `main`/`master` (unless heavily tested/verified).

## Confirmation Protocol

If an action falls into the 🔴 **Destructive** category, you MUST:

1. Pause execution.
2. Present a clear summary of the intended action and its consequences.
3. Ask the user: "Do you want to proceed with [ACTION]?"
4. Only proceed upon explicit "Yes" or equivalent.

## Protected Branches

- Never push directly to `main`, `master`, `production`, or `release/*`.
- Always use a feature branch and a Pull Request.
