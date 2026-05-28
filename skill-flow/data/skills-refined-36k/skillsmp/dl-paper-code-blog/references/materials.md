# Materials Bundle Map

Use this map whenever you open a new blog workspace. Every directory under the project root is deterministic and already populated by the collection scripts, so you only need to consume the pieces that matter for writing.

## Root Files

- `materials_manifest.json` &rarr; single source of truth for metadata. It records the absolute paths of the PDF and repo that were scraped, useful counts (pages rendered, figures detected), and the slug under `out_dir`. Parse this first to learn the venue, release date, and where figures live without opening large binaries.
- `article_scaffold.md` &rarr; blank outline you will overwrite with your own notes. Keep one version with TODO bullets for planning and another finalized version once filled (see `assets/article_scaffold_template.md` for the baseline copy).
- `<slug>_blog.md` or `blog.md` &rarr; the polished article you will produce. Match the slug shown in the manifest.
- `.lsky_upload_cache.json` &rarr; cache of figure uploads. Keys are SHA256 hashes of the source file, values store `{ "url": ..., "path": ... }`. Update this file whenever you upload new media so you never push duplicates.

Optional extras:
- `salad_blog_assets/images/` &rarr; when a downstream platform needs local PNG copies (e.g., for slides or newsletters), mirror the figures referenced in the article here and keep the naming stable (`fig1.png`, `fig2.png`, ...).
- `sources/` &rarr; storage for any ad‑hoc TSV/CSV data the user drops in. Treat it as read-only context; do not assume it exists.

## `paper/` Directory

Structured PDF derivatives live here. The filenames are stable across projects.

| File | Purpose | Usage Tips |
| --- | --- | --- |
| `paper_text.txt` | Raw text of the PDF in reading order. | `rg` or an editor is the fastest way to find section headings, tables, and figure references without scrolling the PDF. |
| `pages/` | 150 dpi PNG renders per page. | Quick visual confirmation of layouts. Use when you need to screenshot text tables instead of cropped figures. |
| `figures/` | 220 dpi crops of detected figures/tables with captions in `figures_manifest.json`. | Primary source for the blog’s inline figures. Each entry includes `kind`, `number`, and caption text—perfect for writing `【图X：...】` callouts. |
| `front_matter/page1_header.png` | Hero image of the first page. | Always embed once near the top to ground the article visually. |
| `bibliography.md/json` | Structured citations. | Copy the canonical citation for the “参考文献” section and note any supporting refs pulled from the code repo/README. |
| `manifest.json`, `pages_manifest.json`, `figures_manifest.json`, `paper_meta.json` | Machine-readable stats. | When you need counts (pages processed, DPI, figure list) or quick access to DOI/ISSN, pull from these instead of re-scraping the PDF. |

## `code/` Directory

Everything inside is generated from the project repository commit listed in `materials_manifest.json`.

- `repo_context.md` &rarr; curated tree plus README excerpts. Use this to explain which scripts reproduce training/inference, how configs are organized, and any gotchas (data downloads, environment setup).
- `repo_manifest.json` &rarr; metadata about the snapshot (git commit, number of files scanned). Helpful when you need to mention commit hashes or confirm whether certain folders were omitted during collection.

## Other Helpful Locations

- `blog_materials*/.lsky_upload_cache.json` (from previous runs) show how figure URLs were logged—reuse the same format.
- `paper/figures_manifest.json` contains caption text you can quote verbatim when naming figures.

> **Workflow reminder:** always skim `materials_manifest.json` first, then open `paper_text.txt` and `repo_context.md` in splits. Keep the template (`assets/article_scaffold_template.md`) nearby for copy/paste when bootstrapping a new workspace.

## Journal Metrics (local)

Journal impact factor (JCR) and CAS partitions can be looked up from a local DB generated from your Excel tables:

- `references/journal_metrics_2025.sqlite3` (inside the skill folder)
- Query helper: `scripts/query_journal_metrics.py --journal "<venue>"`
