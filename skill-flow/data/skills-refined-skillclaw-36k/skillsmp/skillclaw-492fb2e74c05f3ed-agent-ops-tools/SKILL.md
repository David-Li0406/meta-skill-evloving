---
name: agent-ops-tools
description: Use this skill to detect available development tools at session start, saving the results to `.agent/tools.json` and warning about any missing required tools. It works with or without the `aoc` CLI installed.
---

# Tool Detection Skill

Discover available development tools and save to `.agent/tools.json` for use by other skills.

**Works with or without `aoc` CLI installed.** If `aoc` is not available, use the pure skill procedure below.

## CLI Integration (when aoc is installed)

This skill wraps the `aoc tools` CLI commands:

| Command | Purpose |
|---------|---------|
| `aoc tools scan` | Detect all available tools |
| `aoc tools show <tool>` | Show details for specific tool |
| `aoc tools export` | Export to JSON file |

## When to Invoke

### Automatic Invocation

The skill runs automatically during:

1. **Session start** — detect tools before any work begins
2. **Constitution creation** — populate available build/test commands
3. **Baseline capture** — verify required tools exist

### Manual Invocation

```
/tools-detect
/tools-check <tool-name>
/tools-require <tool-list>
```

## Procedure (with aoc CLI)

### 1. Detect Available Tools

```bash
# Run tool detection
aoc tools scan --json > .agent/tools.json
```

### 2. Display Summary

```
🔧 Tool Detection Results

| Category | Tool | Version | Status |
|----------|------|---------|--------|
| Version Control | git | 2.43.0 | ✅ Available |
| Version Control | gh | 2.40.0 | ✅ Available |
| Node.js | node | 20.10.0 | ✅ Available |
| Node.js | npm | 10.2.3 | ✅ Available |
| Node.js | pnpm | ❌ | Not found |
| Python | python | 3.12.0 | ✅ Available |
| Python | uv | 0.4.0 | ✅ Available |
| Python | pip | 23.3.1 | ✅ Available |
| Container | docker | 24.0.7 | ✅ Available |
| Container | kubectl | ❌ | Not found |

Detected: 8/14 common tools
```

### 3. Check Required Tools

If the project has requirements (from constitution or package files):

```
⚠️ Missing Required Tools

Based on project configuration:
- `pyproject.toml` requires: python, uv
- `package.json` requires: node, npm
- `Dockerfile` requires: docker

Missing:
- ❌ kubectl (referenced in k8s/ manifests)

Action: Install missing tools or remove references.
```

### 4. Save to tools.json

```json
{
  "tools": [
    {
      "name": "Git",
      "command": "git",
      "available": true,
      "category": "Version Control"
    },
    ...
  ]
}
```