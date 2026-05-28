# Modes: Project vs Sentinel

Project mode:
- Enter with `set_project(name, root=...)`.
- Use `append_entry`, `manage_docs`, `read_recent`, `query_entries`, `read_file`.

Sentinel mode:
- Do not call `set_project` in the session.
- Use `append_event` and sentinel case tools (`open_bug`, `open_security`, `link_fix`).
