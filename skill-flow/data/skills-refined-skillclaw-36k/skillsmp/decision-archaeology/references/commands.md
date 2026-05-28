# Commands Reference

## Git History

```bash
# Find who changed a line
git blame <file>
git blame -L <start>,<end> <file>
git blame -L :<function_name> <file>

# View file history
git log --oneline <file>
git log --oneline -p <file>
git log --follow <file>

# Search commits by message
git log --oneline --grep="keyword"

# Search commits by code change
git log -S "code_snippet" --oneline
git log -G "regex_pattern" --oneline

# View commit details
git show <commit>
git show <commit> --stat

# Compare changes
git diff <commit1>..<commit2> -- <file>
```

## GitHub PRs

```bash
# Search PRs by commit
gh pr list --search "<commit-sha>" --state all

# Search PRs by keyword
gh pr list --search "keyword" --state all
gh pr view <number>
gh pr view <number> --json body,comments,reviews
gh pr view <number> --comments
```

## GitHub Issues

```bash
# Search issues
gh issue list --search "keyword" --state all
gh issue view <number>
gh issue view <number> --comments

# Find issue references in commit
git show <commit> --format="%B" --no-patch
# Look for: #123, fixes #123, closes #123
```
