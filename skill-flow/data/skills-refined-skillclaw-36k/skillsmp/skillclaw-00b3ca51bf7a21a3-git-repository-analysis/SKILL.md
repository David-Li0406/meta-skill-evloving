---
name: git-repository-analysis
description: Use this skill to analyze a git repository for insights such as contributor statistics, commit patterns, branch health, and change analysis, generating actionable reports.
---

# Git Analysis Skill

Generate repository insights and health reports from git history.

## Commands

All analysis uses standard `git` commands. No external dependencies required.

### Quick Stats

```bash
# Total commits
git rev-list --count HEAD

# Contributors count
git shortlog -sn --all | wc -l

# First and last commit dates
git log --reverse --format=%ci | head -1
git log -1 --format=%ci

# Files in repository
git ls-files | wc -l

# Lines of code (approximate)
git ls-files | xargs wc -l 2>/dev/null | tail -1
```

### Contributor Analysis

```bash
# Commits per author
git shortlog -sn --all

# Commits per author (last 30 days)
git shortlog -sn --since="30 days ago"

# Most active files by author
git log --author="Name" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20
```

### Commit Patterns

```bash
# Commits by day of week
git log --format=%ad --date=format:%A | sort | uniq -c | sort -rn

# Commits by hour
git log --format=%ad --date=format:%H | sort | uniq -c | sort -n

# Commits per month (last year)
git log --since="1 year ago" --format=%ad --date=format:%Y | sort | uniq -c

# Average commits per day (last 30 days)
# commits / 30
```

### Branch Health

```bash
# List all branches with last commit date
git for-each-ref --sort=-committerdate refs/heads/ --format='%(committerdate:short) %(refname:short)'

# Stale branches (no commits in 90 days)
git for-each-ref --sort=committerdate refs/heads/ --format='%(committerdate:iso) %(refname:short)' | while read date branch; do
  if [[ $(date -d "$date" +%s) -lt $(date -d "90 days ago" +%s) ]]; then
    echo "STALE: $branch (last: $date)"
  fi
done

# Merged branches (candidates for deletion)
git branch --merged main | grep -v main

# Branches ahead/behind main
git for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads
```

### Large Files Detection

```bash
# Find large files in history
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  sed -n 's/^blob //p' | \
  sort -rnk2 | \
  head -20

# Current large files
git ls-files | xargs ls -la 2>/dev/null | sort -rnk5 | head -20
```

### Change Analysis

```bash
# Files most frequently changed
git log --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20
```