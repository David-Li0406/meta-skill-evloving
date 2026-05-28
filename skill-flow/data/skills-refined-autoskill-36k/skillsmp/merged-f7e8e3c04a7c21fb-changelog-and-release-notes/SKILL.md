---
name: changelog-and-release-notes
description: Use this skill to generate user-friendly changelogs and release notes from git commit history for various audiences.
---

# Changelog and Release Notes Skill

## Overview

Transform technical git commits into polished, user-friendly changelogs and release notes that stakeholders can easily understand.

## When to Use

Use this skill when you need to:
- Prepare release notes for a new version.
- Create weekly/monthly product update summaries.
- Generate changelog entries for app stores or customer-facing notifications.
- Summarize development progress for product/marketing teams.

## Usage

```
/changelog-and-release-notes <args>
```

## Arguments

- `<args>`: Time period specification or commit range.
  - Relative: `last week`, `last month`, `last 2 weeks`
  - Since: `since 2024-01-01`, `since v1.0.0`
  - Range: `from 2024-01-01 to 2024-01-31`
  - Tags: `v1.0.0..v1.1.0`

## Workflow

### 1. Data Collection

Gather commits using `git log` for the specified period or range:
```bash
# Last week
git log --since="1 week ago" --pretty=format:"%h|%s|%b|%an|%ad" --date=short

# Between tags
git log v1.0.0..v1.1.0 --pretty=format:"%h|%s|%b|%an|%ad" --date=short
```

### 2. Analyze and Categorize Changes

Group commits into user-friendly categories:
| Category | Emoji | Keywords to detect |
|----------|-------|-------------------|
| New Features | 🚀 | feat, add, implement |
| Improvements | 💪 | improve, enhance, update |
| Bug Fixes | 🐛 | fix, resolve, repair |
| Security | 🔒 | security, vulnerability |
| Performance | ⚡ | perf, optimize |
| Breaking Changes | ⚠️ | breaking, BREAKING CHANGE |

### 3. Translate to User Language

Transform technical commit messages into user-friendly descriptions:
- "fix: resolve null ptr in auth handler" → "Fixed login issues for some users."
- "feat: implement websocket reconnection" → "App now automatically reconnects when connection drops."

### 4. Generate the Changelog

Create output in the following format:
```markdown
# 📋 Changelog

**Period:** [Start Date] → [End Date]

## 🚀 New Features
- **[Feature Name]** — [Brief description of what users can now do]

## 💪 Improvements
- **[Area]** — [What got better and why it matters]

## 🐛 Bug Fixes
- Fixed an issue where [user-facing problem description]

## 🔒 Security
- [Description without exposing vulnerability details]

## ⚡ Performance
- [Description of what is now faster/more efficient]

---

📊 **Stats:** [X] changes by [Y] contributors

🙏 **Contributors:** @name1, @name2, @name3
```

### 5. Handle Edge Cases

- **No commits found**: Inform the user that no changes were found for the period.
- **Too many commits (>100)**: Warn the user about the large volume and offer to summarize by category.
- **Technical-only changes**: Create a brief "Technical Improvements" section if all changes are internal.

## Writing Guidelines

1. Write from the user's perspective.
2. Emphasize benefits, not implementation details.
3. Use plain language and avoid technical jargon.
4. Keep entries concise (1-2 sentences max).
5. Frame fixes as improvements and celebrate significant features.

## Outputs

- Release notes and changelog entries grouped by change type, ready for distribution to stakeholders.

## Related Skills

- `/codebase-visualizer` - Diagrammatic summaries for releases.