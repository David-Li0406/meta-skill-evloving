---
name: permanent-rebuilder
description: "Rebuild and maintain an Obsidian vault's permanent knowledge base for work knowledge and learning notes. Use when asked to reorganize permanent, design hub/leaf/MOC structure, standardize frontmatter (especially required summary), define tag taxonomy, generate a safe restructure plan (dry-run), and apply non-destructive moves/renames while preserving links."
---

# Permanent Note Rebuilder

Use this skill to help a user restructure and continuously maintain the `permanent/` folder as a durable knowledge base.

## Operating Principles

- Prefer minimal folders and strong metadata.
- Require a decisive `summary` in every permanent note.
- Treat **Hub** notes as long-form, navigational documents; treat **Leaf** notes as reusable units.
- Avoid destructive operations. Default to planning and dry-runs.

## Target Folder Layout

Adopt this layout under `permanent/`:

- `permanent/00_inbox/` — promoted candidates awaiting normalization
- `permanent/10_hub/` — long-form syntheses, study notes, indexes
- `permanent/20_leaf/` — reusable notes (how-to, principles, decisions, glossary)
- `permanent/90_meta/` — rules, templates, tag dictionary

If the vault already uses a different structure, map existing folders into these four buckets rather than inventing many new categories.

## Required Metadata

For every note in `permanent/`, enforce:

- `summary`: 1–2 lines describing what the note provides
- `created`: YYYY-MM-DD

Recommended:

- `updated`: YYYY-MM-DD
- `status`: seed | draft | evergreen | deprecated
- `tags`: role-based tags (see references)
- `related`: list of wiki links

## Workflow (Plan → Apply → Maintain)

1. **Scan** the current `permanent/` and produce a report.
   - Use `scripts/scan_permanent_notes.py`.
2. **Design** the taxonomy and templates.
   - Read `references/tag-taxonomy.md` and `references/note-templates.md`.
3. **Build** a restructure plan (moves + metadata fixes), but do not apply it yet.
   - Use `scripts/build_restructure_plan.py`.
4. **Apply** the plan safely.
   - Prefer a staged approach: move files first, then add/normalize metadata, then update MOCs.
   - Use `scripts/apply_restructure_plan.py` with `--dry-run` first.
5. **Maintain** continuously.
   - New notes land in `00_inbox/` with minimal metadata.
   - Periodically convert inbox items into hub/leaf and update MOCs.

## Link & Rename Safety

- Prefer moving files without renaming first.
- If renaming, do it after moves, and update wiki links.
- Keep note titles stable; use `aliases` rather than frequent renames.

## Bundled Resources

- Templates: `assets/templates/*.md`
- References: `references/*.md`
- Scripts: `scripts/*.ps1`
