---
name: agent-ops-git-story
description: Use this skill to generate narrative summaries from git history for onboarding, retrospectives, changelogs, and exploration, with optional LLM enhancements.
---

# Git Story Skill

Generate human-readable narratives from git commit history. Useful for:
- **Onboarding** — Help new team members understand project evolution.
- **Retrospectives** — Create sprint/milestone summaries.
- **Changelogs** — Generate release notes from commits.
- **Exploration** — Understand "what happened here?" for any period.

## Requirements

- **Git**: Must be installed locally and available on PATH.
- **LLM**: Optional — enhanced narratives when available, templated output without.

## Data Extraction

**Works with or without `aoc` CLI installed.** Story generation uses raw `git log` commands by default.

### Git Commands (Default)

| Operation | Command |
|-----------|---------|
| Recent commits | `git log --oneline -N` |
| Date range | `git log --since="YYYY-MM-DD" --until="YYYY-MM-DD"` |
| By author | `git log --author="name"` |
| Detailed | `git log --stat --since="YYYY-MM-DD"` |
| JSON-like | `git log --format="%H|%an|%ad|%s" --date=short` |

### CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, enhanced commands are available:

| Command | Description |
|---------|-------------|
| `aoc git story` | Generate narrative from commits. |
| `aoc git stats` | Quick repository statistics. |
| `aoc git info` | Basic repository information. |

### Story Command Options (CLI)

```bash
aoc git story [OPTIONS]

Options:
  --since DATE         Include commits after this date (YYYY-MM-DD).
  --until DATE         Include commits before this date (YYYY-MM-DD).
  --last N             Last N commits only.
  --author NAME        Filter by author name or email.
  --group [date|author|type]  Grouping strategy (default: date).
  --format [narrative|changelog|bullets|json]  Output format.
  --output FILE        Write to file (default: stdout).
  --merges             Include merge commits.
  --repo PATH          Repository path (default: current directory).
  --title TEXT         Custom story title.
```

### Examples

```bash
# Last 30 days of activity
aoc git story --since 2026-01-01

# Generate changelog format
aoc git story --last 50 --format changelog

# Filter by author, group by type
aoc git story --author "John Doe" --group author
```