---
name: grep-app
description: "Grep.app MCP for searching public GitHub code with literal/regex patterns. Use for real-world usage examples and API syntax. Load the mcporter skill to execute calls."
---

# Grep.app MCP

Use Grep.app to search real code in public GitHub repos. Not keyword search; use literal code patterns.

## When to use

- Real usage patterns, syntax, or config examples
- Regex search across many repos
- OSS only (no private repos)

## Quick start

```bash
searchGitHub query="useState(" language='["TypeScript","TSX"]'
searchGitHub query="(?s)useEffect\\(\\(\\) => {.*removeEventListener" useRegexp=true language='["TSX"]'
```

## Notes

- Filter with `repo`, `path`, `language` for precision.
- Use `useRegexp=true` for regex; prefix `(?s)` to match across lines.
- Public GitHub only; check licenses before reuse.

## Query templates

See `assets/query-templates.json`.

## Reference

See `reference.md`.
