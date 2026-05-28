## Quick Start (High Level)

Scribe tools follow a simple flow:

1. **Pick or create a project** with `set_project(...)` so the tool knows where to read/write.
2. **Use the tool for the job**:
   - `append_entry` for logging actions/results.
   - `manage_docs` for structured doc edits (sections, patches, ranges).
   - `read_recent` and `query_entries` for log retrieval/search.
3. **Check outputs** for `ok`, `error`, and any `parameter_healing` notes.

If you skip step 1, most tools will error because no active project context exists.

---
