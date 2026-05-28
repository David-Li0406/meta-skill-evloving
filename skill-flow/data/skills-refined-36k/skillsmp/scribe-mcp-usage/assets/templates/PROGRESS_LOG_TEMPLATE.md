{% extends "documents/base_log.md" %}
{% from "documents/base_log.md" import rotation_notice with context %}

{% block log_metadata %}
{% set log_config.title = "Progress Log" %}
{% set log_config.icon = "📜" %}
{% set log_config.summary = "Generated automatically. Use `append_entry` (or scripts/scribe.py) to append new entries. Never edit past lines by hand." %}
{% endblock %}

{% block log_body %}
{% set rotation_raw = metadata.get("is_rotation", metadata.get("IS_ROTATION", is_rotation | default("false"))) %}
{% set rotation_active = rotation_raw in [True, "true", "True", 1, "1", "yes", "YES"] %}
{% if rotation_active %}
{{ rotation_notice(metadata) }}
{% endif %}

## Entry Format
```
[EMOJI] [YYYY-MM-DD HH:MM:SS UTC] [Agent: <name>] [Project: {{ project_name or PROJECT_NAME }}] Message text | key=value; key2=value2
```

**Tips:**
- Always include `meta` fields tying work back to the checklist/phase (e.g., `phase=1` or `checklist_id=phase0-task2`).
- Keep confidence in a `confidence=` meta key if helpful.
- Use `--dry-run` first when unsure what will be written.

---

## Reminders
- Append after every meaningful change (code, docs, decisions).
- Mention updated docs explicitly (e.g., `docs=architecture,phase_plan`).
- Rotate the log (`rotate_log`) when it nears 200 entries.
- All rotations are cryptographically verified and auditable.

---

## Entries will populate below
{% endblock %}
