---
name: tidb-doc-finder
description: "TiDB-specific documentation lookup guided by this repo's llms.txt hub: read llms.txt, pick the best linked source (tidb-dev-guide llms-full.txt, TiDB user guide llms.txt, or Uber Go style guide), fetch it, then search within it to answer with precise references. Use when asked to find docs, research, or provide doc-grounded answers about TiDB development or usage."
---

# tidb-doc-finder

Use `llms.txt` in the current repo as the single source of truth for "where to look".

## Workflow

1. **Read the hub**
   - Open `llms.txt` and extract the doc endpoints (URLs).
   - Do not hardcode URLs elsewhere; `llms.txt` is authoritative.

2. **If MCP `tidb-doc-ext` is available, prefer it**
   - Use the MCP to fetch documentation content.
   - Only request markdown sources; do not fetch HTML or URLs without a file extension.
   - If MCP is available, use it instead of the local fetch/cache scripts; otherwise fall back to the scripts below.

3. **Select the best source**
   - **TiDB dev / contribution / architecture** -> TiDB Developer Guide (`llms-full.txt`)
   - **TiDB SQL behavior / user-facing features / releases** -> TiDB User Guide (`llms.txt`)
   - **Go style / idioms** -> Uber Go Style Guide (`style.md`)

4. **Fetch to a local cache file (recommended)**
   - Use `tidb-doc-finder/scripts/fetch.sh` to download and cache the selected source.
   - Keep the cache so subsequent searches are fast and can be done offline.

5. **Search within the fetched file**
   - Use `tidb-doc-finder/scripts/search.sh <cached_file> <query>` to:
     - find the most relevant sections,
     - show a small excerpt,
     - and capture headings/anchors if present.

6. **Answer with doc-grounded output**
   - Provide a direct answer.
   - Include the source URL from `llms.txt` and the matched heading/section name.
   - If the doc does not contain the answer, say so and propose the next-best source (still chosen from `llms.txt`).

## Commands

- Fetch: `bash tidb-doc-finder/scripts/fetch.sh <url>`
- Search: `bash tidb-doc-finder/scripts/search.sh <cached_file> <query>`

## References

- Query patterns: `tidb-doc-finder/references/query-patterns.md`
