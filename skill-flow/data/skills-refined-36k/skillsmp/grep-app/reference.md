# Grep.app MCP Reference

## Server setup

- Base URL: `https://mcp.grep.app`
- Recommended MCP name: `grep`
- Public GitHub repos only

## Tool catalog

### searchGitHub
Search literal code patterns in public GitHub repos.

Key params: `query`, `matchCase`, `matchWholeWords`, `useRegexp`, `repo`, `path`, `language`.

Notes:
- Use literal code strings (e.g., `useState(`).
- For regex, set `useRegexp=true`; prefix `(?s)` to match across lines.
