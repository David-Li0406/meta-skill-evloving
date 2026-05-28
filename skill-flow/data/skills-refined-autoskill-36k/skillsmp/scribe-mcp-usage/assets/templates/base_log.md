{#-
  Base template for Scribe log documents (progress/doc/security/bug).
  Child templates should `{% extends "documents/base_log.md" %}` and override
  the `log_body` block to describe log-specific guidance.
-#}
{% set log_config = namespace(icon=None, title=None, timezone=None, maintained_by=None, summary=None) %}
{% block log_metadata %}{% endblock %}
{% set log_icon = log_config.icon | default(metadata.icon | default("📜", true), true) %}
{% set log_title = log_config.title | default(metadata.title | default("Project Log", true), true) %}
{% set log_timezone = log_config.timezone | default(metadata.timezone | default("UTC", true), true) %}
{% set maintained_by = log_config.maintained_by | default(metadata.maintained_by | default(metadata.maintainer | default(author | default("Scribe", true), true), true), true) %}
{% set log_summary = log_config.summary | default(metadata.summary | default(summary | default("Explain how to use this log and when to append entries.", true), true), true) %}

# {{ log_icon }} {{ log_title }} — {{ project_name or PROJECT_NAME }}
**Maintained By:** {{ maintained_by }}
**Timezone:** {{ log_timezone }}

> {{ log_summary }}

---

{% macro rotation_notice(meta=None) -%}
{%- set m = meta or metadata or {} -%}
{%- set rotation_id = m.get("rotation_id", m.get("ROTATION_ID", ROTATION_ID | default("unknown"))) -%}
{%- set rotation_timestamp = m.get("rotation_timestamp_utc", m.get("ROTATION_TIMESTAMP_UTC", ROTATION_TIMESTAMP_UTC | default("unknown"))) -%}
{%- set current_sequence = m.get("current_sequence", m.get("CURRENT_SEQUENCE", CURRENT_SEQUENCE | default("1"))) -%}
{%- set total_rotations = m.get("total_rotations", m.get("TOTAL_ROTATIONS", TOTAL_ROTATIONS | default("1"))) -%}
{%- set previous_path = m.get("previous_log_path", m.get("PREVIOUS_LOG_PATH")) -%}
{%- set previous_hash = m.get("previous_log_hash", m.get("PREVIOUS_LOG_HASH")) -%}
{%- set previous_entries = m.get("previous_log_entries", m.get("PREVIOUS_LOG_ENTRIES")) -%}
{%- set hash_chain_sequence = m.get("hash_chain_sequence", m.get("HASH_CHAIN_SEQUENCE")) -%}
{%- set hash_chain_previous = m.get("hash_chain_previous", m.get("HASH_CHAIN_PREVIOUS")) -%}
{%- set hash_chain_root = m.get("hash_chain_root", m.get("HASH_CHAIN_ROOT")) -%}

---

## 🔄 Log Rotation Information
**Rotation ID:** {{ rotation_id }}
**Rotation Timestamp:** {{ rotation_timestamp }}
**Current Sequence:** {{ current_sequence }}
**Total Rotations:** {{ total_rotations }}

{% if previous_path %}
### Previous Log Reference
- **Path:** {{ previous_path }}
- **Hash:** {{ previous_hash | default("unknown") }}
- **Entries:** {{ previous_entries | default("unknown") }}
{% endif %}

{% if hash_chain_sequence %}
### Hash Chain Information
- **Chain Sequence:** {{ hash_chain_sequence }}
- **Previous Hash:** {{ hash_chain_previous | default("unknown") }}
- **Root Hash:** {{ hash_chain_root | default("unknown") }}
{% endif %}

{% endmacro %}

{% block log_body %}
_Override `log_body` in child templates to describe log usage, entry format, and metadata expectations._
{% endblock %}
