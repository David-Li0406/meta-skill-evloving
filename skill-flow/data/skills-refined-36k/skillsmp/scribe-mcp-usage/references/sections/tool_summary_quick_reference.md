## Tool Summary Quick Reference

| Tool | Purpose | Required Params | Project Context |
|------|---------|----------------|-----------------|
| `set_project` | Initialize project | `name` | No |
| `get_project` | Get current context | None | Yes |
| `list_projects` | Browse projects | None | No |
| `append_entry` | **PRIMARY** logging | `message` or `items` | Yes |
| `read_recent` | Recent entries | None | Yes |
| `query_entries` | Search logs | None | Yes |
| `manage_docs` | Documentation | `action`, `doc_name` | Yes |
| `generate_doc_templates` | Create templates | `project_name` | No |
| `rotate_log` | Archive logs | None | Yes |
| `verify_rotation_integrity` | Verify archive | `archive_path` | No |
| `get_rotation_history` | Rotation history | None | Yes |
| `delete_project` | Remove project | `name`, `confirm` | No |
