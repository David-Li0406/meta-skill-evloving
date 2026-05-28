---
name: github-scout
description: Search GitHub repositories (public and private) for code patterns, implementations, and examples. Use when you need to find how others implement a feature, search for code patterns across repos, or find known issues and solutions.
---

# GitHub Scout

GitHub librarian to search across repositories for relevant code, implementations, and examples.

**Role**: GitHub code searcher
**Purpose**: Find code patterns, implementations, and examples from GitHub
**Current year**: 2026 (use for assessing repo activity)

## Tool Requirements

**Required tools**: Execute (gh CLI)

**Degradation strategy** (if gh unavailable):
```
gh CLI not available. Please execute manually:

1. Code search:
   gh search code "[pattern]" --language [lang] --json repository,path -L 10

2. Repo quality check:
   gh api repos/{owner}/{repo} --jq '{stars: .stargazers_count, pushed: .pushed_at}'

3. Fetch file content:
   gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d

4. Search issues:
   gh search issues "[query]" --repo [owner/repo] --json title,url -L 5
```

## Capabilities

- Search all public GitHub code
- Access private repos the user has authenticated with via `gh`
- Fetch file contents from any accessible repo
- Search issues/discussions for known problems
- Check repo quality signals

## Search Commands

### Code Search
```bash
# General code search
gh search code "[pattern]" --language [lang] --json repository,path,textMatches -L 10

# Scoped to specific repos/orgs
gh search code "[pattern]" --owner [org] --json repository,path -L 10
gh search code "[pattern]" --repo [owner/repo] --json path,textMatches -L 10

# Filter by path
gh search code "[pattern]" path:src/ --json repository,path -L 10
gh search code "[pattern]" path:examples/ --json repository,path -L 10
```

### Fetch File Contents
```bash
# Get file content (base64 encoded)
gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | tr -d '\n' | base64 -d

# Get specific ref/branch
gh api "repos/{owner}/{repo}/contents/{path}?ref={branch}" --jq '.content' | tr -d '\n' | base64 -d
```

### Search Issues/Discussions
```bash
# Find known issues
gh search issues "[query]" --repo [owner/repo] --json title,url,state,body -L 5

# Search across repos
gh search issues "[query]" --language [lang] --json title,url,repository -L 10
```

## Source Quality Assessment

### Quality Signals
```bash
# Quick repo quality check
gh api repos/{owner}/{repo} --jq '{
  stars: .stargazers_count,
  forks: .forks_count,
  fork: .fork,
  archived: .archived,
  pushed: .pushed_at,
  license: .license.spdx_id
}'
```

### Quality Tiers

**Tier 1 - Authoritative** (high confidence):
- Official library repos (org matches package name)
- Stars >= 5000
- Active in last 6 months
- Maintained by known orgs (facebook, google, vercel, microsoft)

**Tier 2 - Established** (good confidence):
- Stars >= 1000
- Active in last 6 months
- Has license, has CI
- Production code (not demos)

**Tier 3 - Reference** (use with context):
- Stars >= 100
- Active in last year
- Clear purpose/documentation

**Tier 4 - Examples Only** (validate before using):
- Tutorial repos, bootcamp projects
- Low stars but relevant code
- Forks (check if they add value)

### Red Flags
- Archived repos (may be outdated)
- No commits in >2 years
- Fork with no additional commits
- No license (legal concerns)
- Single file repos

## Output Format

```markdown
## GitHub Search Results: [Query]

### Authoritative Sources
- **[owner/repo]** (Tier 1)
  - Path: `path/to/file.ts`
  - [Why relevant]
  ```[lang]
  // Key code snippet
  ```

### Quality Examples
- **[owner/repo]** (Tier 2)
  - Path: `path/to/file.ts`
  - [What it demonstrates]

### Additional References
- **[owner/repo]** (Tier 3) - [brief note]

### Related Issues/Discussions
- [Issue title](url) - [relevance]
  - Status: open/closed
  - [Key insight or solution]

### Source Quality Summary
| Repo | Stars | Last Push | Tier | Notes |
|------|-------|-----------|------|-------|
| owner/repo | N | date | 1-4 | ... |

### Search Queries Used
- `gh search code "..."` -> N results
```

## Rules

- Always check source quality before citing
- Include stars/tier in output for context
- Prefer official repos over third-party examples
- Fetch actual file contents when snippets are important
- Note when using lower-tier sources
- Check issue tracker for known problems
- Respect rate limits - batch quality checks
- Private repos: only search if user context suggests relevance
- Cross-reference multiple sources when possible

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo"
  exit 1
fi

ls "$REPO_ROOT/.factory/skills/github-scout/SKILL.md"
# Expected: file exists, exit code 0

# Check gh CLI availability
gh --version 2>/dev/null || echo "gh CLI not available"
````
