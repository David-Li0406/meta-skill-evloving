{% extends "documents/base_log.md" %}
{% from "documents/base_log.md" import rotation_notice with context %}

{% block log_metadata %}
{% set log_config.title = "Documentation Update Log" %}
{% set log_config.icon = "📋" %}
{% set log_config.summary = 'Track every structured documentation change. Use `log_type="doc_updates"` (or `--log doc_updates`).' %}
{% endblock %}

{% block log_body %}
{% set rotation_raw = metadata.get("is_rotation", metadata.get("IS_ROTATION", is_rotation | default("false"))) %}
{% set rotation_active = rotation_raw in [True, "true", "True", 1, "1", "yes", "YES"] %}
{% if rotation_active %}
{{ rotation_notice(metadata) }}
{% endif %}

## Entry Format
```
[EMOJI] [YYYY-MM-DD HH:MM:SS UTC] [Agent: <name>] [Project: {{ project_name or PROJECT_NAME }}] Message text | doc=<doc_name>; section=<section_id>; action=<action_type>; [additional metadata]
```

**Required Metadata Fields:**
- `doc`: Document name (e.g., "architecture", "phase_plan", "checklist")
- `section`: Section ID being modified (e.g., "directory_structure", "phase_overview")
- `action`: Action type (`replace_section`, `append`, `status_update`, etc.)

**Optional Metadata Fields:**
- `file_path`: Full path to the Markdown file
- `changes_count`: Number of lines changed
- `review_status`: pending/approved/rejected
- `reviewer`: Reviewer name
- `jira_ticket`: Associated ticket number
- `confidence`: Confidence level for the change (0-1)
- `context`: Additional context about the change

---

## Tips for Documentation Updates
- Always specify which document section you're updating via `section=`.
- Include `action=` to indicate the type of modification.
- Reference checklist items or phases when applicable.
- Use `--dry-run` first when making structural changes.
- All documentation changes are automatically tracked and versioned.

---

## Entries will populate below
{% endblock %}
