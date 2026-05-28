## Update v2.1.1

- `apply_patch` now supports **structured mode** with compiler-generated unified diffs.
- Unified diffs are **compiler output only** (do not hand-craft).
- Optional `patch_source_hash` enforces stale-source protection for patches.
- Reminders teach: scaffold with `replace_section`, then prefer structured/line edits.
- New lifecycle actions: `normalize_headers`, `generate_toc`, `create_doc`, `validate_crosslinks`.
- Structural actions validate `doc_name` against the project registry; unknown docs fail with `DOC_NOT_FOUND`.
- `normalize_headers` now supports ATX headers with or without a space plus Setext (`====` / `----`), skipping fenced code blocks.
- `generate_toc` uses GitHub-style anchors (NFKD normalization, ASCII folding, emoji removal, punctuation collapse, de-dup suffixes).
- `create_doc` preserves multiline body content in metadata (`body`, `snippet`, `content`).
- `read_file` adds repo-scoped scan/chunk/page/search modes with provenance logging for every read (optional `allow_outside_repo` for approved external reads).
- `read_file` **Phase 5 enhancements**: Full signature extraction (types, defaults, return types), line ranges for all functions/classes/methods, method display under classes, structure filtering (`structure_filter` for regex-based class/function search), and structure pagination (`structure_page`, `structure_page_size`) for browsing large classes with 50+ methods.
- `scribe_doctor` provides environment readiness diagnostics (repo root, config, plugin status, vector readiness).
- `manage_docs` adds semantic search via `action="search"` with `search_mode="semantic"` and doc/log separation.
- Semantic search supports `project_slug`, `project_slugs`, `project_slug_prefix`, `doc_type`, `file_path`, `time_start/time_end`.
- Per-type defaults: `vector_search_doc_k` / `vector_search_log_k` (overrides via `doc_k` / `log_k`).
- Vector indexing uses registry-managed docs only; log/rotated-log files are excluded from doc indexing.
- `scripts/reindex_vector.py` supports `--rebuild` for clean index rebuilds, `--safe` for low-thread fallback, and `--wait-for-drain` to block until embeddings are written.
