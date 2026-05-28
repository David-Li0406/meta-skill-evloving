# MCP Tool Map

Use this map to find the correct MCP tool for a desired capability.

## Issues

| Capability        | MCP Tool                         |
| :---------------- | :------------------------------- |
| **Read Issue**    | `issue_read`                     |
| **Create Issue**  | `issue_write` (method: `create`) |
| **Update Issue**  | `issue_write` (method: `update`) |
| **Comment**       | `add_issue_comment`              |
| **Search**        | `search_issues`                  |
| **Sub-issues**    | `sub_issue_write`                |
| **Start Copilot** | `assign_copilot_to_issue`        |
| **List Types**    | `list_issue_types`               |

## Pull Requests

| Capability         | MCP Tool                        |
| :----------------- | :------------------------------ |
| **List PRs**       | `list_pull_requests`            |
| **Read PR**        | `pull_request_read`             |
| **Create PR**      | `create_pull_request`           |
| **Update PR**      | `update_pull_request`           |
| **Update Branch**  | `update_pull_request_branch`    |
| **Review**         | `pull_request_review_write`     |
| **Comments**       | `add_comment_to_pending_review` |
| **Complete Merge** | `merge_pull_request`            |
| **Copilot Review** | `request_copilot_review`        |

## Repository Data

| Capability        | MCP Tool            |
| :---------------- | :------------------ |
| **List Branches** | `list_branches`     |
| **Get Commit**    | `get_commit`        |
| **Get File**      | `get_file_contents` |
| **Search Code**   | `search_code`       |
| **Commits**       | `list_commits`      |
| **Tags**          | `list_tags`         |

## File Operations

| Capability      | MCP Tool                |
| :-------------- | :---------------------- |
| **Create/Edit** | `create_or_update_file` |
| **Push Files**  | `push_files` (batch)    |
| **Delete**      | `delete_file`           |
