---
name: pr-fix
description: Address PR review comments efficiently. Auto-detects PR from current branch, fetches unresolved threads, applies fixes, posts threaded replies, and resolves threads. Use when responding to review feedback.
---

# PR Fix

## Overview

Streamline the workflow for addressing PR review comments. This skill:
- Auto-detects the PR from the current branch (or accepts PR number/URL as argument)
- Fetches all unresolved review threads
- Guides through fixing each issue
- Posts reply comments properly threaded to the original review comment
- Resolves threads after addressing feedback

## Workflow

1. **Identify the PR**
   - If the user provides a PR number or URL, use it.
   - Otherwise, detect from the current branch:
     ```sh
     gh pr view --json number,url,headRefName,baseRefName
     ```
   - If no PR is found, ask the user to specify one.

2. **Extract repository info**
   - Parse owner and repo from the PR URL or use:
     ```sh
     gh repo view --json owner,name --jq '{owner: .owner.login, repo: .name}'
     ```

3. **Fetch unresolved review threads**
   - Use GraphQL with pagination to get all review threads:
     ```sh
     gh api graphql -f query='
       query($owner: String!, $repo: String!, $pr: Int!, $after: String) {
         repository(owner: $owner, name: $repo) {
           pullRequest(number: $pr) {
             reviewThreads(first: 50, after: $after) {
               nodes {
                 id
                 isResolved
                 path
                 line
                 comments(first: 10) {
                   nodes {
                     id
                     databaseId
                     body
                     author { login }
                   }
                 }
               }
               pageInfo {
                 hasNextPage
                 endCursor
               }
             }
           }
         }
       }
     ' -f owner="$OWNER" -f repo="$REPO" -F pr="$PR_NUMBER"
     ```
   - Loop until `hasNextPage` is false and merge `nodes` from each page:
     ```sh
     after=""
     has_next="true"
     nodes_file="$(mktemp)"
     : > "$nodes_file"
     while [ "$has_next" = "true" ]; do
       args=(-f owner="$OWNER" -f repo="$REPO" -F pr="$PR_NUMBER")
       if [ -n "$after" ]; then
         args+=(-F after="$after")
       fi
       resp="$(gh api graphql -f query='
         query($owner: String!, $repo: String!, $pr: Int!, $after: String) {
           repository(owner: $owner, name: $repo) {
             pullRequest(number: $pr) {
               reviewThreads(first: 50, after: $after) {
                 nodes {
                   id
                   isResolved
                   path
                   line
                   comments(first: 10) {
                     nodes {
                       id
                       databaseId
                       body
                       author { login }
                     }
                   }
                 }
                 pageInfo {
                   hasNextPage
                   endCursor
                 }
               }
             }
           }
         }
       ' "${args[@]}")"
       printf '%s' "$resp" | jq -c '.data.repository.pullRequest.reviewThreads.nodes[]' >> "$nodes_file"
       has_next="$(printf '%s' "$resp" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.hasNextPage')"
       after="$(printf '%s' "$resp" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.endCursor')"
     done
     threads="$(jq -s '.' "$nodes_file")"
     ```
   - Filter to only unresolved threads (`isResolved: false`).
   - Extract priority badges (P1/P2/P3) from comment body if present.

4. **Display unresolved threads**
   - Show a numbered list with:
     - File path and line number
     - Priority badge (if any)
     - First 2-3 lines of the comment body
     - Author
   - If no unresolved threads, report success and exit.

5. **Ask user for approach**
   - Options:
     - Address all sequentially (recommended)
     - Select specific threads by number
     - Dry run (show what would be done without executing)

6. **For each selected thread**:
   a. **Show full context**
      - Display the complete comment
      - Read the relevant file and show surrounding code

   b. **Implement the fix**
      - Apply code changes as needed
      - If no code change is needed (acknowledgment only), note this

   c. **Post reply comment**
      - Use REST API to reply to the top-level comment:
        ```sh
        gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies \
          -f body="<reply message>"
        ```
      - Reply templates:
        - Code fix: "Fixed: <brief description of what was changed>"
        - Acknowledgment: "Acknowledged. <brief response>"
        - Won't fix: "Won't fix: <reason>"

   d. **Resolve the thread**
      - Use GraphQL mutation:
        ```sh
        gh api graphql -f query='
          mutation($threadId: ID!) {
            resolveReviewThread(input: {threadId: $threadId}) {
              thread { isResolved }
            }
          }
        ' -f threadId="$THREAD_ID"
        ```

   e. **Move to next thread**

7. **Report completion**
   - Number of threads addressed
   - Number of threads remaining (if any)
   - Suggest next steps:
     - Commit changes if there are uncommitted modifications
     - Push and request re-review if appropriate

## Dry Run Mode

When dry run is selected:
- List all unresolved threads with full details
- For each thread, describe what action would be taken
- Do NOT make any API calls to post replies or resolve threads
- Do NOT modify any files

## Reply Comment Guidelines

- Keep replies concise (1-2 sentences)
- Focus on what was done, not why the reviewer was right
- For code changes: reference the specific fix (e.g., "Added null check before accessing property")
- For acknowledgments: be brief (e.g., "Good catch, updated.")
- For won't fix: explain the reasoning clearly

## Edge Cases

- **Comment requires no code change**: Post acknowledgment reply and resolve
- **New reviews added during session**: Re-fetch threads before processing next item
- **API rate limiting**: Pause and retry with backoff
- **Thread already resolved**: Skip and move to next
- **Multiple comments in thread**: Reply to the first (top-level) comment only

## Integration with Other Skills

After completing all fixes:
- If there are uncommitted changes, suggest using `/ship` or manual commit
- If user wants re-review, suggest commenting `@codex review` on the PR

## Error Handling

- If `gh` CLI is not installed, show installation instructions
- If not authenticated, prompt `gh auth login`
- If GraphQL query fails, show the error and suggest manual URL
- If reply fails, show the error but continue with resolve attempt

## Examples

### Basic usage (auto-detect PR)
```
/pr-fix
```

### Specify PR by number
```
/pr-fix 38
```

### Specify PR by URL
```
/pr-fix https://github.com/owner/repo/pull/38
```

### Dry run
```
/pr-fix --dry-run
```
