---
name: code-review-and-unresolved-comments
description: Use this skill when reviewing code or pull requests (PRs) and listing unresolved review comments.
---

# Code Review and Unresolved Comments

## 📋 Pre-Execution Checklist (Required)

### Should you use this skill?
- [ ] Are you reviewing a PR?
- [ ] Are you checking code quality?
- [ ] Are you reading someone else's code?
- [ ] Are you performing a final check before merging?

### Prerequisites
- [ ] Do you understand the purpose of the PR?
- [ ] Are you aware of the scope of changes?
- [ ] Have you reviewed related specifications or tickets?

### Prohibited Actions Check
- [ ] Are you avoiding personal attacks in comments?
- [ ] Are you not denying without basis?
- [ ] Are you not pointing out style preferences only?
- [ ] Are you not overlooking blocking issues?

---

## Triggers

- During PR reviews
- When checking code quality
- While reading others' code
- For final checks before merging

---

## 🚨 Ground Rules

**Prioritize readability. The time spent writing is less than the time spent reading.**

---

## Review Order

1. **Blocking**: Security, crashes
2. **Simple**: Typos, imports
3. **Complex**: Logic, design

---

## Checkpoints

### Design
- Is there a single responsibility?
- Is there no duplication (DRY)?
- Is the level of abstraction appropriate?

### Security
- Is there input validation?
- Are authorization checks present?
- Is sensitive information not leaked?

### Readability
- Are names clear?
- Is it not overly complex?
- Are comments appropriate?

---

## 🚫 Summary of Prohibited Actions

- Personal attacks in comments
- Denials without basis
- Style preference-only comments
- Overlooking blocking issues

---

## Unresolved PR Comments

To list unresolved review comments for a specified PR, follow these steps:

1. **Retrieve PR Number and Repository Information**

   Execute:
   ```bash
   gh pr view --json number,url -q '{number: .number, url: .url}'
   ```
   - If `pr_number` is specified: `gh pr view <pr_number>`
   - If `pr_number` is not specified: `gh pr view` to get the current branch's PR.

   From the retrieved JSON:
   - PR Number: `.number`
   - Owner: Split `.url` by `/` and take the 4th element
   - Repo: Split `.url` by `/` and take the 5th element

   If the PR number cannot be retrieved (command fails), exit with an error.

2. **Execute GraphQL Query**

   Write the following bash script to a temporary file and execute it:

   ```bash
   cat > /tmp/fetch_pr_comments.sh << 'SCRIPT_EOF'
   #!/bin/bash
   owner="owner_from_step_1"
   repo="repo_from_step_1"
   pr_number="pr_number_from_step_1"

   cursor=""
   all_results="[]"

   while true; do
     if [ -z "$cursor" ]; then
       result=$(gh api graphql -F pr="$pr_number" -f query="
         query(\$pr: Int!) {
           repository(owner: \"$owner\", name: \"$repo\") {
             pullRequest(number: \$pr) {
               reviewThreads(first: 100) {
                 pageInfo { hasNextPage endCursor }
                 nodes {
                   isResolved
                   isOutdated
                   line
                   path
                   comments(first: 1) {
                     nodes {
                       databaseId
                       body
                       author { login }
                     }
                   }
                 }
               }
             }
           }
         }")
     else
       result=$(gh api graphql -F pr="$pr_number" -F cursor="$cursor" -f query="
         query(\$pr: Int!, \$cursor: String) {
           repository(owner: \"$owner\", name: \"$repo\") {
             pullRequest(number: \$pr) {
               reviewThreads(first: 100, after: \$cursor) {
                 pageInfo { hasNextPage endCursor }
                 nodes {
                   isResolved
                   isOutdated
                   line
                   path
                   comments(first: 1) {
                     nodes {
                       databaseId
                       body
                       author { login }
                     }
                   }
                 }
               }
             }
           }
         }")
     fi

     threads=$(echo "$result" | jq -r '.data.repository.pullRequest.reviewThreads.nodes')
     all_results=$(echo "$all_results" | jq ". + $threads")

     has_next=$(echo "$result" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.hasNextPage')
     if [ "$has_next" != "true" ]; then
       break
     fi
     cursor=$(echo "$result" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo.endCursor')
   done

   echo "$all_results"
   SCRIPT_EOF

   bash /tmp/fetch_pr_comments.sh
   ```

   **Reason**: To avoid syntax errors in complex scripts with loops when using the Bash tool.

3. **Process Results**

   Process `all_results` obtained in step 2:
   - Extract unresolved comments using `jq 'map(select(.isResolved == false)) | sort_by(.path // "", .line // 0)'`
   - For each thread, retrieve the first comment from `.comments.nodes[0]`
   - Summarize the comment body:
     * If within 100 characters: display as is
     * If over 100 characters: summarize the main points to about 50-80 characters, including specific suggestions or questions
     * If it contains code examples: summarize as "Suggesting a fix for ~"

## Output Format

```
PR #{pr_number} の未解決コメント: {total}件

---

{path}:{line}
著者: {author.login} | Outdated: {isOutdated}
要約: {summarized comment body}
→ https://github.com/{owner}/{repo}/pull/{pr_number}#discussion_r{databaseId}

---

(Repeat)
```

## Error Handling

- If `gh` CLI is unavailable: "エラー: gh CLI がインストールされていないか、認証されていません。'gh auth login' を実行してください"
- If `pr_number` is unspecified and no PR exists for the current branch: "エラー: 現在のブランチにPRが見つかりません。PR番号を指定してください"
- If PR is not found: "エラー: PR #{pr_number} が見つかりません"
- If there are no unresolved comments: "エラー: PR #{pr_number} のコメントはすべて解決済みです"
- If there is a GraphQL API error: "エラー: " followed by the error message in Japanese

## Notes

- If the path is null, display as "全般的なコメント"
- If the line number is null, omit the line number
- All output should be in Japanese