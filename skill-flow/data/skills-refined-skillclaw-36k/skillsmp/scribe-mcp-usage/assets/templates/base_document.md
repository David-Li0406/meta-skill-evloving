{#-
  Base template for all Scribe documentation assets.
  Child templates should `{% extends "documents/base_document.md" %}`
  and override the `document_body` block. Common helpers are provided
  to keep authoring consistent across architecture/phase/checklist docs.
-#}
{% set doc_title = doc_title | default(metadata.title | default("Project Document")) %}
{% set doc_icon = doc_icon | default(metadata.icon | default("📄")) %}
{% set doc_status = doc_status | default(metadata.status | default(status | default("Active"))) %}
{% set doc_version = doc_version | default(metadata.version | default("Draft v0.1")) %}
{% set doc_author = metadata.author | default(author | default("Scribe")) %}
{% set doc_last_updated = metadata.last_updated | default(date_utc) %}
{% set doc_summary = metadata.summary | default(summary | default("Summarise why this document exists and what decisions it captures.")) %}

# {{ doc_icon }} {{ doc_title }} — {{ project_name or PROJECT_NAME }}
**Author:** {{ doc_author }}
**Version:** {{ doc_version }}
**Status:** {{ doc_status }}
**Last Updated:** {{ doc_last_updated }}

> {{ doc_summary }}

---

{%- macro section(title, anchor, description="") -%}
## {{ title }}
<!-- ID: {{ anchor }} -->
{%- if description %}
{{ description }}
{%- endif %}

{{ caller() }}

---
{%- endmacro %}

{%- macro bullet_list(items, placeholder="Add bullet points here.") -%}
{%- set seq = [] -%}
{%- if items is iterable and (items is not string) %}
    {%- set seq = items %}
{%- elif items %}
    {%- set seq = [items] %}
{%- endif %}
{%- if seq %}
{%- for item in seq %}
- {{ item }}
{%- endfor %}
{%- else %}
- {{ placeholder }}
{%- endif %}
{%- endmacro %}

{%- macro checklist(items, placeholder="Document actionable checklist items.") -%}
{%- set seq = [] -%}
{%- if items is iterable and (items is not string) %}
    {%- set seq = items %}
{%- elif items %}
    {%- set seq = [items] %}
{%- endif %}
{%- if seq %}
{%- for item in seq %}
- [ ] {{ item.label | default(item) }}{% if item.proof %} (proof: {{ item.proof }}){% endif %}
{%- endfor %}
{%- else %}
- [ ] {{ placeholder }}
{%- endif %}
{%- endmacro %}

{%- macro table(headers, rows, placeholder="Populate this table with structured data.") -%}
{%- if rows %}
| {{ headers | join(' | ') }} |
|{%- for _ in headers %} --- |{%- endfor %}
{%- for row in rows %}
| {{ row | join(' | ') }} |
{%- endfor %}
{%- else %}
{{ placeholder }}
{%- endif %}
{%- endmacro %}

{% block document_body %}
_Override `document_body` in child templates to provide document-specific content._
{% endblock %}
