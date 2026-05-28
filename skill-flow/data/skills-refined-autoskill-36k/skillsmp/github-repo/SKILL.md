---
name: github-repo
description: Get GitHub repository information including stars, forks, issues, languages, and metadata. Use when the user asks for repository details, GitHub stats, or repo information.
---

# Get GitHub Repository Information

Retrieve detailed information about a GitHub repository.

## Usage

```bash
npx tsx scripts/repo.ts <repository> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `repository` | Yes | Repository in format `owner/repo` or full GitHub URL |

### Options

| Option | Description |
|--------|-------------|
| `--token=TOKEN` | GitHub Personal Access Token (optional, overrides GITHUB_TOKEN env var) |
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

```
facebook/react
----------------
Description: A declarative, efficient, and flexible JavaScript library for building user interfaces.
Created: 2013-05-24
Updated: 2023-10-15
Pushed: 2023-10-15

Statistics:
  Stars: 213,456
  Forks: 45,678
  Open issues: 1,234
  Watchers: 7,890

Details:
  Language: TypeScript
  License: MIT
  Private: No
  Fork: No
  Default branch: main

Features:
  Issues: Enabled
  Projects: Enabled
  Wiki: Enabled
  Pages: Disabled
```

## Script Execution (Preferred)

```bash
npx tsx scripts/repo.ts <repository> [options]
```

Options:
- `--token=TOKEN` - GitHub Personal Access Token (optional, overrides GITHUB_TOKEN env var)
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the github-api plugin directory: `~/.claude/plugins/cache/github-api/`

## Repository API

```
GET https://api.github.com/repos/{owner}/{repo}
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `owner` | Yes | Repository owner (user or organization) |
| `repo` | Yes | Repository name |

### Examples

Get repository information:
```
https://api.github.com/repos/facebook/react
```

## Response Format

The response contains comprehensive repository metadata:

- **`id`** - Repository ID
- **`name`** - Repository name
- **`full_name`** - Owner/repo (e.g., "facebook/react")
- **`owner`** - Owner object (login, id, avatar_url, type, etc.)
- **`description`** - Repository description
- **`private`** - Whether the repository is private
- **`fork`** - Whether this is a fork
- **`created_at`** - Creation timestamp
- **`updated_at`** - Last update timestamp
- **`pushed_at`** - Last push timestamp
- **`homepage`** - Homepage URL
- **`size`** - Repository size in kilobytes
- **`stargazers_count`** - Number of stars
- **`watchers_count`** - Number of watchers
- **`language`** - Primary programming language
- **`languages_url`** - URL to get all languages
- **`has_issues`** - Whether issues are enabled
- **`has_projects`** - Whether projects are enabled
- **`has_wiki`** - Whether wiki is enabled
- **`has_pages`** - Whether GitHub Pages is enabled
- **`forks_count`** - Number of forks
- **`open_issues_count`** - Number of open issues
- **`license`** - License information
- **`topics`** - Repository topics
- **`default_branch`** - Default branch name

## URL Format Support

The script accepts various URL formats:
- `owner/repo` (simple format)
- `https://github.com/owner/repo`
- `git+https://github.com/owner/repo`
- `git@github.com:owner/repo`
- `ssh://git@github.com/owner/repo`

All formats are automatically parsed to extract owner and repo.

## Authentication

GitHub API rate limits:
- **Unauthenticated**: 60 requests/hour
- **Authenticated**: 5,000 requests/hour

To increase your rate limit, provide a GitHub Personal Access Token:

**Via environment variable:**
```bash
export GITHUB_TOKEN=your_token_here
npx tsx scripts/repo.ts facebook/react
```

**Via command-line option:**
```bash
npx tsx scripts/repo.ts facebook/react --token=your_token_here
```

Create a token at: https://github.com/settings/tokens

## Caching

Repository metadata is cached for 30 minutes. Repository information changes relatively infrequently, so this provides good freshness while improving performance.

Use the `--no-cache` flag to bypass the cache.

## Related

- Use `github-readme` to fetch the repository README
- Use `github-user` to get owner profile information
- Use `github-rate-limit` to check your remaining API quota

## Error Handling

**Repository not found**: Verify the owner and repository name are correct. Private repositories require authentication with appropriate access.

**Rate limit exceeded**: Use a Personal Access Token to increase your quota, or wait for the quota to reset (hourly).

**Authentication errors**: Ensure your token is valid and has the necessary permissions (for private repos).

## Use Cases

### Package Research
Get GitHub information for npm packages:
```bash
npx tsx scripts/repo.ts facebook/react
npx tsx scripts/repo.ts vercel/next.js
```

### Repository Stats
Check popularity and activity:
```bash
npx tsx scripts/repo.ts nodejs/node --token=$GITHUB_TOKEN
```

### License Information
Check repository license:
```bash
npx tsx scripts/repo.ts microsoft/typescript
```
