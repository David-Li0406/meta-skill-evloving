# GitHub CLI Commands Reference

## PR Operations

```bash
# List PRs
gh pr list
gh pr list --author <username>
gh pr list --label "needs-review"

# View PR details
gh pr view <number>
gh pr view <number> --json title,body,author,baseRefName,headRefName,commits,files

# View diff
gh pr diff <number>
gh pr diff <number> -- <filepath>

# List changed files
gh pr view <number> --json files --jq '.files[].path'

# View commit history
gh pr view <number> --json commits --jq '.commits[] | "\(.oid[:7]) \(.messageHeadline)"'

# Check CI status
gh pr checks <number>
gh pr checks <number> --watch

# View failed CI logs
gh run view <run-id> --log-failed

# Checkout PR branch
gh pr checkout <number>
```

## View Existing Reviews

```bash
gh api repos/{owner}/{repo}/pulls/<number>/comments --jq '.[] | {path, line, body}'
gh pr view <number> --json reviews --jq '.reviews[] | {author: .author.login, state: .state, body}'
```

## Tips

- Combine `--json` with `--jq` to extract specific information
- Use `gh pr checkout` for local review, `gh pr diff` for terminal review
- For large PRs, review file by file with `gh pr diff -- <file>`
