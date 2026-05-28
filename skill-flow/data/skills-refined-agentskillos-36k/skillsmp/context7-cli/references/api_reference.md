# Context7 CLI Reference

This skill uses the local `agent-skills` CLI with the `c7` subcommand.

## Location

- Source: `cmd/agent-skills/main.go`
- Binary (optional): `go build -o bin/agent-skills ./cmd/agent-skills`
- Remote install (only if missing):

```bash
if ! command -v agent-skills >/dev/null 2>&1; then
  go install github.com/strantalis/agent-skills/cmd/agent-skills@latest
fi
```

## Commands

### `c7 search`

Search Context7 libraries and return results.

```bash
go run ./cmd/agent-skills c7 search --library-name react --query "useEffect cleanup"
```

Flags:
- `--library-name` (required)
- `--query` (required)
- `--format` (`json` default, or `jsonl`, `text`)
- `--limit` (0 = no limit)

Text format output is tab-separated: `<id>\t<name>\t<description>`

### `c7 context`

Fetch context for a specific library.

```bash
go run ./cmd/agent-skills c7 context --library-id /facebook/react --query "useEffect cleanup"
```

If you only have a name, you may use `--library-name`. This resolves the first search result.

```bash
go run ./cmd/agent-skills c7 context --library-name react --query "useEffect cleanup"
```

Flags:
- `--library-id` (preferred)
- `--library-name` (fallback)
- `--query` (required)
- `--format` (`text` default, or `json`, `jsonl`)
- `--select` (`error` default, or `first`, `interactive`)

## Global `c7` flags

- `--api-key` (or env `CONTEXT7_API_KEY`)
- `--base-url` (default `https://context7.com`)
- `--timeout` (default `30s`)
- `--retries` (default `2`)
- `--cache-dir` (enable disk cache when set)
- `--cache-ttl` (default `24h`)

## Notes

- For deterministic runs, prefer `--library-id` and `--format json`.
- For quick reading, use `--format text`.
