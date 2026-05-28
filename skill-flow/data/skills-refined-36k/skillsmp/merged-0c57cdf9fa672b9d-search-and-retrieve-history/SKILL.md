---
name: search-and-retrieve-history
description: Use this skill to search, filter, and retrieve indexed Claude/Codex history, whether using the memex or automem CLI. Ideal for indexing history, running various types of searches, and producing structured JSON output for RAG.
---

# Search and Retrieve History

This skill allows you to index local history and retrieve results in a structured, LLM-friendly way.

## Indexing

- Build or update the index (incremental):
  - `index` (use `memex` or `automem` command)
- Full rebuild (clears index):
  - `reindex` (use `memex` or `automem` command)
- Embeddings are on by default.
- Disable embeddings:
  - `index --no-embeddings` (use `memex` or `automem` command)
- Backfill embeddings only:
  - `embed` (use `memex` or `automem` command)
- Common flags:
  - `--source <path>` for Claude logs
  - `--include-agents` to include agent transcripts
  - `--codex/--no-codex` to include or skip Codex logs
  - `--root <path>` to change data root (default: `~/.memex` or `~/.automem`)

## Search (LLM default JSON)

Run a search; output is JSON lines by default.

```
search "query" --limit 20
```

Each JSON line includes:
- `doc_id`, `ts` (ISO), `session_id`, `project`, `role`, `source_path`
- `text` (full record text)
- `snippet` (trimmed single-line summary)
- `matches` (offsets + before/after context)
- `score` (ranked score)

### Mode decision table

| Need | Command |
| --- | --- |
| Exact terms | `search "exact term"` |
| Fuzzy concepts | `search "concept" --semantic` |
| Mixed | `search "term concept" --hybrid` |

### Filters

- `--project <name>`
- `--role <user|assistant|tool_use|tool_result>`
- `--tool <tool_name>`
- `--session <session_id>` (search inside a transcript)
- `--source claude|codex`
- `--since <iso|unix>` / `--until <iso|unix>`
- `--limit <n>`
- `--min-score <float>`

### Grouping / dedupe

- `--top-n-per-session <n>` (top n per session)
- `--unique-session` (same as top-k per session = 1)
- `--sort score|ts` (default score)

### Output shape

- JSONL default (one JSON per line)
- `--json-array` for a single JSON array
- `--fields score,ts,doc_id,session_id,snippet` to reduce output
- `-v/--verbose` for human output

### Narrowing Tips

1) Start with exact terms (quoted) before hybrid if results are noisy.
2) Use `--unique-session` to collapse PR-link spam fast.
3) Use `--min-score` to prune low-signal hits.
4) Use `--sort ts` for a timeline view.
5) For a specific session, prefer `search "<term>" --session <id> --sort ts --limit 50` to jump to outcomes.

## Fetch Full Context

- One record:
  - `show <doc_id>` (use `memex` or `automem` command)
- Full transcript:
  - `session <session_id>` (use `memex` or `automem` command)

Both commands return JSON by default.

## Human Output

Use `-v/--verbose` for human-readable output:

- `search "query" -v`
- `show <doc_id> -v`
- `session <session_id> -v`

## Sharing Sessions

Share a session transcript via agentexport (requires `brew install nicosuave/tap/agentexport`):

```
share <session_id>
share <session_id> --title "Bug fix session"
```

Returns an encrypted share URL.

## Recommended LLM Flow

1) `search "query" --limit 20`
2) Pick hits using `matches` or `snippet`
3) `show <doc_id>` or `session <session_id>`
4) Refine with `--session`, `--role`, or time filters
5) Share relevant sessions with `share <session_id>`