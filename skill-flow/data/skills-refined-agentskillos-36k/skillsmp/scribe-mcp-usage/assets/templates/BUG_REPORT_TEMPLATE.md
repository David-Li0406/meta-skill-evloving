{% extends "documents/base_document.md" %}
{% set doc_title = metadata.title | default("Bug Report") %}
{% set doc_icon = metadata.icon | default("🐞") %}
{% set doc_status = metadata.status | default("Investigating") %}
{% set doc_version = metadata.version | default("v0.1") %}
{% set doc_summary = metadata.summary | default("Document the discovery, analysis, and remediation plan for the reported defect.") %}

{% block document_body %}
{% call section("Bug Overview", "bug_overview") %}
{% set slug = metadata.get("slug", "bug_" + (timestamp | replace(" ", "_"))) %}
**Bug ID:** {{ slug }}

**Reported By:** {{ metadata.get("reporter", agent_id | default("Unknown Reporter")) }}

**Date Reported:** {{ metadata.get("reported_at", timestamp) }}

**Severity:** {{ metadata.get("severity", "medium") | upper }}

**Status:** {{ metadata.get("status", "INVESTIGATING") | upper }}

**Component:** {{ metadata.get("component", "[Component or subsystem]") }}

**Environment:** {{ metadata.get("environment", "[local/staging/production]") }}

**Customer Impact:** {{ metadata.get("customer_impact", "[Describe impact or 'None']") }}
{% endcall %}

{% call section("Description", "description") %}
### Summary
{{ metadata.get("summary_long", "[Brief description of the bug]") }}

### Expected Behaviour
{{ metadata.get("expected_behavior", "[What should happen]") }}

### Actual Behaviour
{{ metadata.get("actual_behavior", "[What actually happens]") }}

### Steps to Reproduce
{{ checklist(metadata.get("reproduction_steps"), "List reproducible steps for engineers/QA.") }}
{% endcall %}

{% call section("Investigation", "investigation") %}
**Root Cause Analysis:**
{{ metadata.get("root_cause", "[Describe suspected or confirmed root cause]") }}

**Affected Areas:**
{{ bullet_list(metadata.get("affected_areas"), "List impacted services, components, or files.") }}

**Related Issues:**
{{ bullet_list(metadata.get("related_issues"), "Link to related bugs, tickets, or documentation.") }}
{% endcall %}

{% call section("Resolution Plan", "resolution_plan") %}
### Immediate Actions
{{ checklist(metadata.get("immediate_actions"), "Track urgent steps needed to mitigate the issue.") }}

### Long-Term Fixes
{{ checklist(metadata.get("long_term_fixes"), "Outline long-term remedial work or refactors.") }}

### Testing Strategy
{{ checklist(metadata.get("testing_strategy"), "Define validation steps for the fix (unit, integration, regression).") }}
{% endcall %}

{% call section("Timeline & Ownership", "timeline") %}
| Phase | Owner | Target Date | Notes |
| --- | --- | --- | --- |
| Investigation | {{ metadata.get("owners", {}).get("investigation", "[Name]") }} | {{ metadata.get("timeline", {}).get("investigation", "[Date]") }} | {{ metadata.get("notes", {}).get("investigation", "[Details]") }} |
| Fix Development | {{ metadata.get("owners", {}).get("fix", "[Name]") }} | {{ metadata.get("timeline", {}).get("fix", "[Date]") }} | {{ metadata.get("notes", {}).get("fix", "[Details]") }} |
| Testing | {{ metadata.get("owners", {}).get("testing", "[Name]") }} | {{ metadata.get("timeline", {}).get("testing", "[Date]") }} | {{ metadata.get("notes", {}).get("testing", "[Details]") }} |
| Deployment | {{ metadata.get("owners", {}).get("deployment", "[Name]") }} | {{ metadata.get("timeline", {}).get("deployment", "[Date]") }} | {{ metadata.get("notes", {}).get("deployment", "[Details]") }} |
{% endcall %}

{% call section("Appendix", "appendix") %}
- **Logs & Evidence:** {{ metadata.get("logs", "[Link to relevant logs, traces, screenshots]") }}
- **Fix References:** {{ metadata.get("fix_references", "[Git commits, PRs, or documentation]") }}
- **Open Questions:** {{ metadata.get("open_questions", "[List unresolved unknowns or next investigations]") }}
{% endcall %}
{% endblock %}
