# Troubleshooting

`DOC_NOT_FOUND` in `manage_docs`:
- Meaning: `doc_name` is not registered and could not be auto-registered.
- Fix: standard docs → `generate_doc_templates`; custom docs → `create_doc`.

`read_file denied` / scope violations:
- Meaning: denylist hit, or outside allowlist without override.
- Fix: `.claude/skills` and `.codex/skills` are always allowed; otherwise pass `allow_outside_repo=true` (denylist still enforced).
