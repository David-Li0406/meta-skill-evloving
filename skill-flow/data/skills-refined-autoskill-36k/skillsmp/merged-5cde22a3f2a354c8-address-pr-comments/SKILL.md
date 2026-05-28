---
name: address-pr-comments
description: Use this skill to efficiently address PR review comments by making code changes, posting replies, and resolving threads. It auto-detects the PR from the current branch or accepts a PR number/URL as input.
---

# Address PR Comments

## Overview

This skill streamlines the process of addressing PR review comments. It allows you to:
- Auto-detect the PR from the current branch or accept a PR number/URL as an argument.
- Fetch unresolved review threads and comments.
- Make necessary code changes and post replies to acknowledge feedback.
- Resolve threads after addressing comments.

## Workflow

1. **Verify Environment**
   - Ensure you are on a feature branch and have a GitHub remote:
     ```bash
     git remote -v
     git status
     git rev-parse --abbrev-ref HEAD
     ```
   - **STOP if:**
     - No remote exists → "This skill requires a GitHub remote. Please add one with `git remote add origin <url>` first."
     - On main/master → "Please switch to the PR's branch first."
     - Uncommitted changes → "Please commit or stash your changes first."

2. **Identify the PR**
   - If the user provides a PR number or URL, use it.
   - Otherwise, detect from the current branch:
     ```bash
     gh pr view --json number,url,headRefName,baseRefName
     ```
   - If no PR is found, ask the user to specify one.
   - Validate that the PR is open.

3. **Fetch Unresolved Review Threads and Comments**
   - Use GraphQL to fetch unresolved review threads:
     ```bash
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
   - Loop until all threads are fetched and filter to only unresolved threads.

4. **Display Unresolved Threads**
   - Show a numbered list with:
     - File path and line number
     - First 2-3 lines of the comment body
     - Author
   - If no unresolved threads, report success and exit.

5. **Process Comments**
   - For each comment, present it to the user and ask for the action to take:
     - Make code changes
     - Post a reply
     - Discuss first
     - Skip this comment
   - Execute the chosen action:
     - **Code changes**: Implement the changes and optionally post a reply.
     - **Reply**: Draft and post a response using:
       ```bash
       gh pr comment <number> --body "<reply>"
       ```
     - **Discussion**: Explore the codebase if needed.

6. **Post Replies and Resolve Threads**
   - After addressing a comment, post a concise reply acknowledging the change.
   - Resolve the thread using GraphQL mutation:
     ```bash
     gh api graphql -f query='
       mutation($threadId: ID!) {
         resolveReviewThread(input: {threadId: $threadId}) {
           thread { isResolved }
         }
       }
     ' -f threadId="$THREAD_ID"
     ```

7. **Commit and Push Changes**
   - After making code changes:
     ```bash
     git add .
     git commit -m "<summary of changes addressing review feedback>"
     git push
     ```

8. **Report Completion**
   - Summarize what was done:
     - Number of comments addressed
     - Code changes made
     - Replies posted
     - Any comments skipped or left unresolved

## Guidelines

- Keep replies concise and professional.
- Make requested code changes accurately and with user approval.
- Track progress through comments and report on completion.

## Error Handling

- If `gh` CLI is not installed, show installation instructions.
- If not authenticated, prompt `gh auth login`.
- Handle API rate limiting and other common errors gracefully.

## Examples

### Basic usage (auto-detect PR)
```
/address-pr-comments
```

### Specify PR by number
```
/address-pr-comments 38
```

### Specify PR by URL
```
/address-pr-comments https://github.com/owner/repo/pull/38
```