# GitHub CLI Command Reference

Complete reference for GitHub CLI (`gh`) commands used in PR review workflows.

## Pull Request Operations

**View PR details:**
```bash
gh pr view <pr-number>
gh pr view <pr-number> --json title,body,author,state,merged,baseRefName,headRefName
```

**List PRs:**
```bash
gh pr list
gh pr list --state all
gh pr list --author @me
gh pr list --label "bug"
```

**Get PR diff:**
```bash
gh pr diff <pr-number>
gh pr diff <pr-number> --patch
```

**Get PR files:**
```bash
gh pr view <pr-number> --json files --jq '.files[].path'
```

**Create PR comment:**
```bash
gh pr comment <pr-number> --body "Review comment"
```

**Get PR checks/status:**
```bash
gh pr checks <pr-number>
gh pr checks <pr-number> --watch
```

## Issue Operations

**View issue:**
```bash
gh issue view <issue-number>
gh issue view <issue-number> --json title,body,state,labels
```

**List issues:**
```bash
gh issue list
gh issue list --state all
gh issue list --label "bug"
```

**Link PR to issue:**
```bash
gh pr create --body "Fixes #123"
# Or manually: gh issue comment <issue-number> --body "Related PR: #456"
```

## Repository Operations

**Get repository info:**
```bash
gh repo view
gh repo view --json name,description,url,defaultBranchRef
```

**List branches:**
```bash
gh api repos/:owner/:repo/branches
```

**Get file contents:**
```bash
gh api repos/:owner/:repo/contents/path/to/file
```

## Advanced: Using `gh api` for GraphQL/REST

**GraphQL query:**
```bash
gh api graphql -f query='
  query($owner: String!, $repo: String!, $pr: Int!) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $pr) {
        title
        body
        author { login }
        state
        files(first: 100) {
          nodes {
            path
            additions
            deletions
          }
        }
      }
    }
  }' -f owner=OWNER -f repo=REPO -f pr=PR_NUMBER
```

**REST API:**
```bash
gh api repos/:owner/:repo/pulls/:pr_number
gh api repos/:owner/:repo/pulls/:pr_number/files
```

## Error Handling

- **Not authenticated:** Run `gh auth login`
- **Not in repo context:** Use `--repo owner/repo` flag or `cd` into repository
- **PR not found:** Verify PR number and repository
- **Rate limiting:** GitHub CLI respects rate limits; wait and retry

## Best Practices

1. **Use JSON output** for programmatic parsing: `--json` flag with `--jq` for filtering
2. **Specify repository** when not in git context: `--repo owner/repo`
3. **Combine commands** for complex operations using shell pipes
4. **Cache results** when possible to avoid rate limiting
5. **Handle errors** gracefully; check exit codes

## References

- GitHub CLI Manual: [cli.github.com/manual](https://cli.github.com/manual)
- GitHub CLI API: [cli.github.com/manual/gh_api](https://cli.github.com/manual/gh_api)
- GitHub GraphQL API: [docs.github.com/en/graphql](https://docs.github.com/en/graphql)
- GitHub REST API: [docs.github.com/en/rest](https://docs.github.com/en/rest)
