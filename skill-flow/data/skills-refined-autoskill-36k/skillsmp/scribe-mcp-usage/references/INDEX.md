# Skill Index (How to Search Fast)

Use `read_file(mode="search")` against skill reference docs. Default `search_mode` is `regex`.

Common searches:
```python
# Doc registration (create/register/auto-register)
read_file(path="references/Scribe_Usage.md", mode="search", query=r"register_doc|register_existing|auto-registration|DOC_NOT_FOUND", context_lines=2)

# manage_docs actions and required params
read_file(path="references/Scribe_Usage.md", mode="search", query=r"### `manage_docs`|#### `create_doc`|#### `apply_patch`|#### `status_update`", context_lines=2)

# doc_name vs doc_category semantics
read_file(path="references/Scribe_Usage.md", mode="search", query=r"doc_name|doc_category", context_lines=2)

# read_file scope rules
read_file(path="references/Scribe_Usage.md", mode="search", query=r"allow_outside_repo|denylist|\\.codex/skills|\\.claude/skills", context_lines=2)

# tight search within a single top-level section (generated section pack)
read_file(path="references/sections/INDEX.md", mode="search", query=r"Document Editing|Documentation Management|read_file|manage_docs", context_lines=1)
```
