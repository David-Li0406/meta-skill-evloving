# GitHub MCP Tools Reference

This document lists the available GitHub MCP tools and their parameters. These tools provide comprehensive access to GitHub's functionality through the Model Context Protocol.

## Actions

### cancel_workflow_run
Cancel workflow run

**Parameters:**
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)
- `run_id`: The unique identifier of the workflow run (number, required)

### delete_workflow_run_logs
Delete workflow logs

**Parameters:**
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)
- `run_id`: The unique identifier of the workflow run (number, required)

### download_workflow_run_artifact
Download workflow artifact

**Parameters:**
- `artifact_id`: The unique identifier of the artifact (number, required)
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)

### get_job_logs
Get job logs

**Parameters:**
- `failed_only`: When true, gets logs for all failed jobs in run_id (boolean, optional)
- `job_id`: The unique identifier of the workflow job (required for single job logs) (number, optional)
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)
- `return_content`: Returns actual log content instead of URLs (boolean, optional)
- `run_id`: Workflow run ID (required when using failed_only) (number, optional)
- `tail_lines`: Number of lines to return from the end of the log (number, optional)

### get_workflow_run
Get workflow run

**Parameters:**
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)
- `run_id`: The unique identifier of the workflow run (number, required)

### get_workflow_run_logs
Get workflow run logs

**Parameters:**
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)
- `run_id`: The unique identifier of the workflow run (number, required)

### get_workflow_run_usage
Get workflow usage

**Parameters:**
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)
- `run_id`: The unique identifier of the workflow run (number, required)

### list_workflow_jobs
List workflow jobs

**Parameters:**
- `filter`: Filters jobs by their completed_at timestamp (string, optional)
- `owner`: Repository owner (string, required)
- `page`: Page number for pagination (min 1) (number, optional)
- `perPage`: Results per page for pagination (min 1, max 100) (number, optional)
- `repo`: Repository name (string, required)
- `run_id`: The unique identifier of the workflow run (number, required)

### list_workflow_run_artifacts
List workflow artifacts

**Parameters:**
- `owner`: Repository owner (string, required)
- `page`: Page number for pagination (min 1) (number, optional)
- `perPage`: Results per page for pagination (min 1, max 100) (number, optional)
- `repo`: Repository name (string, required)
- `run_id`: The unique identifier of the workflow run (number, required)

### list_workflow_runs
List workflow runs

**Parameters:**
- `actor`: Returns someone's workflow runs. Use the login for the user who created the workflow run. (string, optional)
- `branch`: Returns workflow runs associated with a branch. Use the name of the branch. (string, optional)
- `event`: Returns workflow runs for a specific event type (string, optional)
- `owner`: Repository owner (string, required)
- `page`: Page number for pagination (min 1) (number, optional)
- `perPage`: Results per page for pagination (min 1, max 100) (number, optional)
- `repo`: Repository name (string, required)
- `status`: Returns workflow runs with the check run status (string, optional)
- `workflow_id`: The workflow ID or workflow file name (string, required)

### list_workflows
List workflows

**Parameters:**
- `owner`: Repository owner (string, required)
- `page`: Page number for pagination (min 1) (number, optional)
- `perPage`: Results per page for pagination (min 1, max 100) (number, optional)
- `repo`: Repository name (string, required)

### rerun_failed_jobs
Rerun failed jobs

**Parameters:**
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)
- `run_id`: The unique identifier of the workflow run (number, required)

### rerun_workflow_run
Rerun workflow run

**Parameters:**
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)
- `run_id`: The unique identifier of the workflow run (number, required)

### run_workflow
Run workflow

**Parameters:**
- `inputs`: Inputs the workflow accepts (object, optional)
- `owner`: Repository owner (string, required)
- `ref`: The git reference for the workflow. The reference can be a branch or tag name. (string, required)
- `repo`: Repository name (string, required)
- `workflow_id`: The workflow ID (numeric) or workflow file name (e.g., main.yml, ci.yaml) (string, required)

## Discussions

### get_discussion
Get discussion

**Parameters:**
- `discussionNumber`: Discussion Number (number, required)
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)

### get_discussion_comments
Get discussion comments

**Parameters:**
- `after`: Cursor for pagination. Use the endCursor from the previous page's PageInfo for GraphQL APIs. (string, optional)
- `discussionNumber`: Discussion Number (number, required)
- `owner`: Repository owner (string, required)
- `perPage`: Results per page for pagination (min 1, max 100) (number, optional)
- `repo`: Repository name (string, required)

### list_discussion_categories
List discussion categories

**Parameters:**
- `owner`: Repository owner (string, required)
- `repo`: Repository name. If not provided, discussion categories will be queried at the organisation level. (string, optional)

### list_discussions
List discussions

**Parameters:**
- `after`: Cursor for pagination. Use the endCursor from the previous page's PageInfo for GraphQL APIs. (string, optional)
- `category`: Optional filter by discussion category ID. If provided, only discussions with this category are listed. (string, optional)
- `direction`: Order direction. (string, optional)
- `orderBy`: Order discussions by field. If provided, the 'direction' also needs to be provided. (string, optional)
- `owner`: Repository owner (string, required)
- `perPage`: Results per page for pagination (min 1, max 100) (number, optional)
- `repo`: Repository name. If not provided, discussions will be queried at the organisation level. (string, optional)

## Issues

### add_issue_comment
Add comment to issue

**Parameters:**
- `body`: Comment content (string, required)
- `issue_number`: Issue number to comment on (number, required)
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)

### assign_copilot_to_issue
Assign Copilot to issue

**Parameters:**
- `issueNumber`: Issue number (number, required)
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)

### get_label
Get a specific label from a repository

**Parameters:**
- `name`: Label name. (string, required)
- `owner`: Repository owner (username or organization name) (string, required)
- `repo`: Repository name (string, required)

### issue_read
Get issue details

**Parameters:**
- `issue_number`: The number of the issue (number, required)
- `method`: The read operation to perform on a single issue. Options are:
  - `get` - Get details of a specific issue.
  - `get_comments` - Get issue comments.
  - `get_sub_issues` - Get sub-issues of the issue.
  - `get_labels` - Get labels assigned to the issue. (string, required)
- `owner`: The owner of the repository (string, required)
- `page`: Page number for pagination (min 1) (number, optional)
- `perPage`: Results per page for pagination (min 1, max 100) (number, optional)
- `repo`: The name of the repository (string, required)

### issue_write
Create or update issue

**Parameters:**
- `assignees`: Usernames to assign to this issue (string[], optional)
- `body`: Issue body content (string, optional)
- `duplicate_of`: Issue number that this issue is a duplicate of. Only used when state_reason is 'duplicate'. (number, optional)
- `issue_number`: Issue number to update (number, optional)
- `labels`: Labels to apply to this issue (string[], optional)
- `method`: Write operation to perform on a single issue. Options are:
  - `create` - creates a new issue.
  - `update` - updates an existing issue. (string, required)
- `milestone`: Milestone number (number, optional)
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)
- `state`: New state (string, optional)
- `state_reason`: Reason for the state change. Ignored unless state is changed. (string, optional)
- `title`: Issue title (string, optional)
- `type`: Type of this issue. Only use if the repository has issue types configured. Use list_issue_types tool to get valid type values for the organization. If the repository doesn't support issue types, omit this parameter. (string, optional)

### list_issue_types
List available issue types

**Parameters:**
- `owner`: The organization owner of the repository (string, required)

### list_issues
List issues

**Parameters:**
- `after`: Cursor for pagination. Use the endCursor from the previous page's PageInfo for GraphQL APIs. (string, optional)
- `direction`: Order direction. If provided, the 'orderBy' also needs to be provided. (string, optional)
- `labels`: Filter by labels (string[], optional)
- `orderBy`: Order issues by field. If provided, the 'direction' also needs to be provided. (string, optional)
- `owner`: Repository owner (string, required)
- `perPage`: Results per page for pagination (min 1, max 100) (number, optional)
- `repo`: Repository name (string, required)
- `since`: Filter by date (ISO 8601 timestamp) (string, optional)
- `state`: Filter by state, by default both open and closed issues are returned when not provided (string, optional)

### search_issues
Search issues

**Parameters:**
- `order`: Sort order (string, optional)
- `owner`: Optional repository owner. If provided with repo, only issues for this repository are listed. (string, optional)
- `page`: Page number for pagination (min 1) (number, optional)
- `perPage`: Results per page for pagination (min 1, max 100) (number, optional)
- `query`: Search query using GitHub issues search syntax (string, required)
- `repo`: Optional repository name. If provided with owner, only issues for this repository are listed. (string, optional)
- `sort`: Sort field by number of matches of categories, defaults to best match (string, optional)

### sub_issue_write
Change sub-issue

**Parameters:**
- `after_id`: The ID of the sub-issue to be prioritized after (either after_id OR before_id should be specified) (number, optional)
- `before_id`: The ID of the sub-issue to be prioritized before (either after_id OR before_id should be specified) (number, optional)
- `issue_number`: The number of the parent issue (number, required)
- `method`: The action to perform on a single sub-issue Options are:
  - `add` - add a sub-issue to a parent issue in a GitHub repository.
  - `remove` - remove a sub-issue from a parent issue in a GitHub repository.
  - `reprioritize` - change the order of sub-issues within a parent issue in a GitHub repository. Use either 'after_id' or 'before_id' to specify the new position. (string, required)
- `owner`: Repository owner (string, required)
- `replace_parent`: When true, replaces the sub-issue's current parent issue. Use with 'add' method only. (boolean, optional)
- `repo`: Repository name (string, required)
- `sub_issue_id`: The ID of the sub-issue to add. ID is not the same as issue number (number, required)

## Pull Requests

### add_comment_to_pending_review
Add review comment to the requester's latest pending pull request review

**Parameters:**
- `body`: The text of the review comment (string, required)
- `line`: The line of the blob in the pull request diff that the comment applies to. For multi-line comments, the last line of the range (number, optional)
- `owner`: Repository owner (string, required)
- `path`: The relative path to the file that necessitates a comment (string, required)
- `pullNumber`: Pull request number (number, required)
- `repo`: Repository name (string, required)
- `side`: The side of the diff to comment on. LEFT indicates the previous state, RIGHT indicates the new state (string, optional)
- `startLine`: For multi-line comments, the first line of the range that the comment applies to (number, optional)
- `startSide`: For multi-line comments, the starting side of the diff that the comment applies to. LEFT indicates the previous state, RIGHT indicates the new state (string, optional)
- `subjectType`: The level at which the comment is targeted (string, required)

### create_pull_request
Open new pull request

**Parameters:**
- `base`: Branch to merge into (string, required)
- `body`: PR description (string, optional)
- `draft`: Create as draft PR (boolean, optional)
- `head`: Branch containing changes (string, required)
- `maintainer_can_modify`: Allow maintainer edits (boolean, optional)
- `owner`: Repository owner (string, required)
- `repo`: Repository name (string, required)
- `title`: PR title (string, required)

### list_pull_requests
List pull requests

**Parameters:**
- `base`: Filter by base branch (string, optional)
- `direction`: Sort direction (string, optional)
- `head`: Filter by head user/org and branch (string, optional)
- `owner`: Repository owner (string, required)
- `page`: Page number for pagination (min 1) (number, optional)
- `perPage`: Results per page for pagination (min 1, max 100) (number, optional)
- `repo`: Repository name (string, required)
- `sort`: Sort by (string, optional)
- `state`: Filter by state (string, optional)

### merge_pull_request
Merge pull request

**Parameters:**
- `commit_message`: Extra detail for merge commit (string, optional)
- `commit_title`: Title for merge commit (string, optional)
- `merge_method`: Merge method (string, optional)
- `owner`: Repository owner (string, required)
- `pullNumber`: Pull request number (number, required)
- `repo`: Repository name (string, required)

### pull_request_read
Get details for a single pull request

**Parameters:**
- `method`: Action to specify what pull request data needs to be retrieved from GitHub. Possible options:
  - `get` - Get details of a specific pull request.
  - `get_diff` - Get the diff of a pull request.
  - `get_status` - Get status of a head commit in a pull request. This reflects status of builds and checks.
  - `get_files` - Get the list of files changed in a pull request. Use with pagination parameters to control the number of results returned.
  - `get_review_comments` - Get the review comments on a pull request. They are comments made on a portion of the unified diff during a pull request review. Use with pagination parameters to control the number of results returned.
  - `get_reviews` - Get the reviews on a pull request. When asked for review comments, use get_review_comments method.
  - `get_comments` - Get comments on a pull request. Use this if user doesn't specifically want review comments. Use with pagination parameters to control the number of results returned. (string, required)
- `owner`: Repository owner (string, required)
- `page`: Page number for pagination (min 1) (number, optional)
- `perPage`: Results per page for pagination (min 1, max 100) (number, optional)
- `pullNumber`: Pull request number (number, required)
- `repo`: Repository name (string, required)

### pull_request_review_write
Write operations (create, submit, delete) on pull request reviews

**Parameters:**
- `body`: Review comment text (string, optional)
- `commitID`: SHA of commit to review (string, optional)
- `event`: Review action to perform. (string, optional)
- `method`: The write operation to perform on pull request review. (string, required)
- `owner`: Repository owner (string, required)
- `pullNumber`: Pull request number (number, required)
- `repo`: Repository name (string, required)

### request_copilot_review
Request Copilot review

**Parameters:**
- `owner`: Repository owner (string, required)
- `pullNumber`: Pull request number (number, required)
- `repo`: Repository name (string, required)

### search_pull_requests
Search pull requests

**Parameters:**
- `order`: Sort order (string, optional)
- `owner`: Optional repository owner. If provided with repo, only pull requests for this repository are listed. (string, optional)
- `page`: Page number for pagination (min 1) (number, optional)
- `perPage`: Results per page for pagination (min 1, max 100) (number, optional)
- `query`: Search query using GitHub pull request search syntax (string, required)
- `repo`: Optional repository name. If provided with owner, only pull requests for this repository are listed. (string, optional)
- `sort`: Sort field by number of matches of categories, defaults to best match (string, optional)

### update_pull_request
Edit pull request

**Parameters:**
- `base`: New base branch name (string, optional)
- `body`: New description (string, optional)
- `draft`: Mark pull request as draft (true) or ready for review (false) (boolean, optional)
- `maintainer_can_modify`: Allow maintainer edits (boolean, optional)
- `owner`: Repository owner (string, required)
- `pullNumber`: Pull request number to update (number, required)
- `repo`: Repository name (string, required)
- `reviewers`: GitHub usernames to request reviews from (string[], optional)
- `state`: New state (string, optional)
- `title`: New title (string, optional)

### update_pull_request_branch
Update pull request branch

**Parameters:**
- `expectedHeadSha`: The expected SHA of the pull request's HEAD ref (string, optional)
- `owner`: Repository owner (string, required)
- `pullNumber`: Pull request number (number, required)
- `repo`: Repository name (string, required)
