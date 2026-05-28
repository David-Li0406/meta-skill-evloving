---
name: repo-spy
description: Check Anthropic repos and web sources for updates
version: 3.0.0
allowed-tools: Bash(uv run *)
---

Monitor GitHub repositories and official web sources for updates, releases, and breaking changes.

## Workflow

1. Run: `uv run .claude/skills/repo-spy/scripts/run.py [owner]`
2. Report summary to user
3. Highlight action items, breaking changes, and new blog posts

## Usage

```bash
# Scan all owners
uv run .claude/skills/repo-spy/scripts/run.py

# Scan specific owner
uv run .claude/skills/repo-spy/scripts/run.py anthropics

# List available owners
uv run .claude/skills/repo-spy/scripts/run.py --list-owners

# Web sources only (blog posts, release notes)
uv run .claude/skills/repo-spy/scripts/run.py --web-only

# Report only (skip git fetch, use cached data)
uv run .claude/skills/repo-spy/scripts/run.py --report

# JSON output to stdout
uv run .claude/skills/repo-spy/scripts/run.py --json
```

## Configuration

Each owner can have an optional `repos/{owner}/config.yaml`:

```yaml
# Repository priorities (HIGH, MEDIUM, LOW)
priorities:
  important-repo: HIGH
  less-important: LOW

# Web sources to monitor
web_sources:
  blog: "https://example.com/news"
  docs_changelog: "https://docs.example.com/changelog"

# Paths to monitor for hook/plugin changes
hook_paths:
  some-repo:
    - "src/hooks/"
    - "CHANGELOG.md"
```

## Output

Reports saved to `.data/repo-spy/{owner}/`:

- `latest.json` - Machine-readable
- `latest.md` - Human-readable
- `history/{YYYYMMDD}.*` - Archived

## Report to User

After running, summarize:

- Total repos scanned and commits (30d)
- Breaking changes and hook alerts
- Recent blog posts (titles + links)
- Action items requiring attention
