---
name: github-user
description: Get GitHub user profile information including repos, followers, and activity. Use when the user asks for GitHub user details, profile information, or developer stats.
---

# Get GitHub User Profile

Retrieve detailed information about a GitHub user or organization.

## Usage

```bash
npx tsx scripts/user.ts <username> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `username` | Yes | GitHub username |

### Options

| Option | Description |
|--------|-------------|
| `--token=TOKEN` | GitHub Personal Access Token (optional, overrides GITHUB_TOKEN env var) |
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

```
torvalds (Linus Torvalds)
--------------------------
Bio: Creator of Linux
Location: Portland, OR
Company: Linux Foundation

Account:
  Type: User
  Created: 2010-08-19
  Updated: 2023-10-01
  Hireable: Yes

Statistics:
  Public repos: 12
  Public gists: 5
  Followers: 156,789
  Following: 0

Links:
  Profile: https://github.com/torvalds
  Blog: https://lkml.org/
  Avatar: https://avatars.githubusercontent.com/u/102402?v=4
```

## Script Execution (Preferred)

```bash
npx tsx scripts/user.ts <username> [options]
```

Options:
- `--token=TOKEN` - GitHub Personal Access Token (optional, overrides GITHUB_TOKEN env var)
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the github-api plugin directory: `~/.claude/plugins/cache/github-api/`

## User API

```
GET https://api.github.com/users/{username}
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `username` | Yes | GitHub username |

### Examples

Get user information:
```
https://api.github.com/users/torvalds
```

## Response Format

The response contains comprehensive user profile metadata:

- **`login`** - Username
- **`id`** - User ID
- **`node_id`** - Node ID
- **`avatar_url`** - Avatar image URL
- **`gravatar_id`** - Gravatar ID
- **`url`** - API URL for the user
- **`html_url`** - GitHub profile URL
- **`type`** - User type ("User" or "Organization")
- **`site_admin`** - Whether the user is a GitHub admin
- **`name`** - Display name
- **`company`** - Company
- **`blog`** - Blog/website URL
- **`location`** - Location
- **`email`** - Email address
- **`hireable`** - Whether seeking employment
- **`bio`** - Profile bio
- **`public_repos`** - Number of public repositories
- **`public_gists`** - Number of public gists
- **`followers`** - Number of followers
- **`following`** - Number of following
- **`created_at`** - Account creation timestamp
- **`updated_at`** - Last profile update timestamp

## Authentication

User profile data access:
- **Public profiles**: No authentication required for basic information
- **Private information**: Authentication may be required for email addresses and other private details
- **Rate limits**: Higher limits with authentication (5,000/hr vs 60/hr)

Provide a GitHub Personal Access Token:

**Via environment variable:**
```bash
export GITHUB_TOKEN=your_token_here
npx tsx scripts/user.ts username
```

**Via command-line option:**
```bash
npx tsx scripts/user.ts username --token=your_token_here
```

## Caching

User profiles are cached for 1 hour. Profile information changes relatively infrequently, so this provides good freshness while improving performance.

Use the `--no-cache` flag to bypass the cache.

## Related

- Use `github-repo` to get detailed repository information
- Use `github-readme` to fetch repository documentation
- Use `github-rate-limit` to check your remaining API quota

## Error Handling

**User not found**: Verify the username is correct. Usernames are case-insensitive but must be exact otherwise.

**Organization vs User**: The API returns the same data structure for both users and organizations. Check the `type` field.

**Rate limit exceeded**: Use a Personal Access Token for higher rate limits, or wait for the quota to reset (hourly).

## Use Cases

### Developer Research
Get information about package maintainers:
```bash
npx tsx scripts/user.ts zce
npx tsx scripts/user.ts sindresorhus
```

### Company Profiles
Check organization profiles:
```bash
npx tsx scripts/user.ts facebook
npx tsx scripts/user.ts microsoft
```

### Follower Analysis
Check follower counts and activity:
```bash
npx tsx scripts/user.ts gaearon
```

## Notes

- Email addresses are only returned if visible on the user's profile
- Private information requires authentication with appropriate scopes
- Organization profiles have similar structure but different data fields
- Avatar URLs can be used directly in HTML `<img>` tags
