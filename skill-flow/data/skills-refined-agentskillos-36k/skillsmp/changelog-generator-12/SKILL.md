---
name: changelog-generator
description: Generate user-friendly changelogs from git commits for releases
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: release
---

# Changelog Generator

Transform technical git commits into polished, user-friendly changelogs that customers understand.

## When to Use

- Preparing release notes for a new version
- Creating weekly/monthly product update summaries
- Writing changelog entries for app stores
- Generating customer-facing update notifications
- Maintaining a public changelog page

## How to Use

### Basic Usage

```
Create a changelog from commits since last release
```

```
Generate changelog for commits from the past week
```

```
Create release notes for version 2.5.0
```

### With Date Range

```
Create changelog for commits between March 1 and March 15
```

### With Tag Range

```
Generate changelog for commits between v1.0.0 and v2.0.0
```

## Process

### 1. Gather Commits

```bash
# Since last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# Between tags
git log v1.0.0..v2.0.0 --oneline

# By date range
git log --after="2025-01-01" --before="2025-01-15" --oneline
```

### 2. Categorize Changes

| Category | Commit Prefixes | Emoji |
|----------|-----------------|-------|
| New Features | feat, add | ✨ |
| Improvements | improve, enhance, update | 🔧 |
| Bug Fixes | fix, resolve, patch | 🐛 |
| Breaking Changes | breaking, !: | 💥 |
| Security | security, vuln | 🔒 |
| Performance | perf, optimize | ⚡ |

### 3. Translate to User Language

| Technical Commit | User-Friendly |
|------------------|---------------|
| "fix: resolve null ptr in auth handler" | "Fixed login issues for some users" |
| "feat: implement websocket reconnection" | "App now automatically reconnects when connection drops" |
| "perf: optimize query with index" | "Dashboard loads 2x faster" |

### 4. Filter Noise

Exclude from changelog:
- refactor: (internal code changes)
- test: (test updates)
- chore: (maintenance)
- ci: (pipeline changes)
- docs: (unless user-facing)

## Output Format

```markdown
# Release Notes - v2.5.0

**Release Date**: January 15, 2025

## ✨ New Features

- **Team Workspaces**: Create separate workspaces for different 
  projects. Invite team members and keep everything organized.

- **Keyboard Shortcuts**: Press `?` to see all shortcuts. 
  Navigate faster without touching your mouse.

## 🔧 Improvements

- **Faster Sync**: Files now sync 2x faster across devices
- **Better Search**: Search now includes file contents

## 🐛 Bug Fixes

- Fixed issue where large images wouldn't upload
- Resolved timezone confusion in scheduled posts
- Corrected notification badge count

## 💥 Breaking Changes

- API v1 endpoints deprecated (use v2)
- Minimum Node.js version is now 18

---

[Full Changelog](./CHANGELOG.md) | [Upgrade Guide](./docs/upgrade.md)
```

## Tips

- Run from git repository root
- Review output before publishing
- Keep descriptions under 2 lines
- Lead with user benefit, not technical detail
- Use consistent formatting across releases
