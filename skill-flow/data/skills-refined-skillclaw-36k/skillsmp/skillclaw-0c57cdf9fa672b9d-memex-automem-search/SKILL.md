---
name: memex-automem-search
description: Use this skill when you want to index and retrieve Claude/Codex history in a structured, LLM-friendly way, utilizing either the memex or automem CLI.
---

# Skill body

## Indexing

- Build or update the index (incremental):
  - `memex index` or `./target/debug/automem index`
- Continuous index (memex only):
  - `memex index-service enable --continuous`
- Full rebuild (clears index):
  - `memex reindex` or `./target/debug/automem reindex`
- Embeddings are on by default.
- Disable embeddings:
  - `memex index --no-embeddings` or `./target/debug/automem index --no-embeddings`
- Backfill embeddings only:
  - `memex embed` or `./target/debug/automem embed`
- Common flags:
  - `--source <path>` for Claude logs
  - `--include-agents` to include agent transcripts
  - `--codex/--no-codex` to include or skip Codex logs
  - `--root <path>` to change data root (default: `~/.memex` or `~/.automem`)

## Search (LLM default JSON)

Run a search; output is JSON lines by default.

```
memex search "query" --limit 20
```
or
```
./target/debug/automem search "query" --limit 20
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

### Narrow first (fastest reducers)

1) Global search with `--limit`
2) Reduce with `--project` and `--since/--until`
3) Optionally `--top-n-per-session` or `--unique-session`
4) `./target/debug/automem session <id>` for full context (automem only)

### Practical narrowing tips

- Start with exact terms (quoted) before hybrid if results are noisy.
- Use `--unique-session` to collect unique results per session.