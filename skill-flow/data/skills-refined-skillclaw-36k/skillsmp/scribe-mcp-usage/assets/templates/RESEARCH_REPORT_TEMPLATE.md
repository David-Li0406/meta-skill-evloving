{% extends "documents/base_document.md" %}
{% set doc_title = metadata.title | default("Research Report") %}
{% set doc_icon = metadata.icon | default("🔬") %}
{% set doc_status = metadata.status | default("In Progress") %}
{% set doc_version = metadata.version | default("v0.1") %}
{% set doc_summary = metadata.summary | default("Capture the investigation scope, key findings, analysis, and recommendations for upcoming work.") %}

{% block document_body %}
{% call section("Executive Summary", "executive_summary", "High-level overview of the research effort and conclusions.") %}
**Primary Objective:** {{ metadata.get("objective", "[Describe the primary research goal]") }}

**Key Takeaways:**
{{ bullet_list(metadata.get("key_takeaways"), "[List critical conclusions or risks].") }}
{% endcall %}

{% call section("Research Scope", "research_scope") %}
**Research Lead:** {{ metadata.get("researcher", agent_name | default(agent_id | default("Scribe Researcher"))) }}

**Investigation Window:** {{ metadata.get("window", "[YYYY-MM-DD — YYYY-MM-DD]") }}

**Focus Areas:**
{{ checklist(metadata.get("focus_areas"), "Identify the focus areas explored during research.") }}

**Dependencies & Constraints:**
{{ bullet_list(metadata.get("constraints"), "Document assumptions, dependencies, or limitations that shaped the research.") }}
{% endcall %}

{% call section("Findings", "findings", "Detail each major finding with evidence and confidence levels.") %}
### Finding 1
- **Summary:** {{ metadata.get("finding_1", {}).get("summary", "[Describe the finding]") }}
- **Evidence:** {{ metadata.get("finding_1", {}).get("evidence", "[Link to logs, code references, or experiments]") }}
- **Confidence:** {{ metadata.get("finding_1", {}).get("confidence", "Medium") }}

### Finding 2
- **Summary:** {{ metadata.get("finding_2", {}).get("summary", "[Describe the finding]") }}
- **Evidence:** {{ metadata.get("finding_2", {}).get("evidence", "[Link to supporting material]") }}
- **Confidence:** {{ metadata.get("finding_2", {}).get("confidence", "Medium") }}

### Additional Notes
{{ bullet_list(metadata.get("additional_notes"), "Capture supporting observations or open follow-ups.") }}
{% endcall %}

{% call section("Technical Analysis", "technical_analysis") %}
**Code Patterns Identified:**
{{ bullet_list(metadata.get("code_patterns"), "List relevant code paths, abstractions, or anti-patterns uncovered.") }}

**System Interactions:**
{{ bullet_list(metadata.get("system_interactions"), "Summarise dependencies across services, databases, or external APIs.") }}

**Risk Assessment:**
{{ checklist(metadata.get("risks"), "Document technical or product risks discovered and mitigation ideas.") }}
{% endcall %}

{% call section("Recommendations", "recommendations", "Translate research into recommended actions.") %}
### Immediate Next Steps
{{ checklist(metadata.get("next_steps"), "List concrete follow-up tasks for the team.") }}

### Long-Term Opportunities
{{ bullet_list(metadata.get("long_term_opportunities"), "Highlight strategic improvements informed by the research.") }}
{% endcall %}

{% call section("Appendix", "appendix") %}
- **References:** {{ metadata.get("references", "[Link to diagrams, ADRs, whitepapers, or related documents]") }}
- **Attachments:** {{ metadata.get("attachments", "[List supporting artifacts or datasets]") }}
{% endcall %}
{% endblock %}
