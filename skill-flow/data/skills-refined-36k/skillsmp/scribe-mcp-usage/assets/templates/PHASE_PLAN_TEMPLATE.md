{% extends "documents/base_document.md" %}
{% set doc_title = "Phase Plan" %}
{% set doc_icon = "⚙️" %}
{% set summary = metadata.summary | default("Break the architecture into reviewable execution phases tied to checklist items and measurable outcomes.") %}
{% set phases = metadata.phases or [] %}
{% set milestones = metadata.milestones or [] %}

{% block document_body %}
{% call section("Phase Overview", "phase_overview") %}
| Phase | Goal | Key Deliverables | Confidence (0-1) |
|-------|------|------------------|------------------|
{% if phases %}
  {% for phase in phases %}
| {{ phase.name | default("Phase " ~ loop.index0) }} | {{ phase.goal | default("State the objective for this phase.") }} | {{ (phase.deliverables or []) | join(", ") | default("List the tangible outputs.") }} | {{ "%.2f"|format(phase.confidence | default(0.7)) }} |
  {% endfor %}
{% else %}
| Phase 0 | Define real goals & constraints | Async bug fix, database schema, basic reliability | 0.90 |
| Phase 1 | Template Engine | Jinja2 integration, custom templates, enhanced rendering | 0.80 |
| Phase 2 | Sync & Change Tracking | Bidirectional sync, file watcher, git-level history | 0.75 |
{% endif %}
Update this table as the project evolves. Confidence values should change as knowledge increases.
{% endcall %}

{% if phases %}
  {% for phase in phases %}
    {% set anchor = phase.anchor or ("phase_" ~ loop.index0) %}
    {% call section("Phase " ~ loop.index0 ~ " — " ~ (phase.name | default("Name Me")), anchor) %}
**Objective:** {{ phase.goal | default("Summarise the measurable outcome.") }}

**Key Tasks:**
{{ bullet_list(phase.tasks, "List actionable tasks for this phase.") }}

**Deliverables:**
{{ bullet_list(phase.deliverables, "Describe the artifacts that will be produced.") }}

**Acceptance Criteria:**
{{ checklist(phase.acceptance, "Spell out the checks that prove the phase succeeded.") }}

**Dependencies:** {{ phase.dependencies | default("List upstream teams, systems, or sequencing constraints.") }}

**Notes:** {{ phase.notes | default("Capture risks, blockers, or decisions specific to this phase.") }}
    {% endcall %}
  {% endfor %}
{% else %}
{% call section("Phase 0 — Foundation Fixes & Database Enhancement", "phase_0") %}
**Objective:** Fix critical silent failures and establish a reliable storage foundation.

**Key Tasks:**
- [ ] Fix async/await bug in manager.py (add async_atomic_write function)
- [ ] Extend database schema with document_sections, custom_templates, document_changes tables
- [ ] Implement database migration system for new schema
- [ ] Add comprehensive error handling and validation to manage_docs operations
- [ ] Create post-write verification to eliminate silent failures
- [ ] Add structured logging for all document operations

**Deliverables:**
- Working manage_docs tool with 100% reliable file operations
- Enhanced SQLite database with document content mirroring
- Database migration system for backwards compatibility
- Comprehensive test coverage for document operations

**Acceptance Criteria:**
- [ ] All manage_docs operations succeed or raise appropriate errors (no silent failures)
- [ ] File content always matches expected result after operations
- [ ] Database properly mirrors document content after each operation
- [ ] All existing projects continue to work without manual intervention
- [ ] Test suite demonstrates 100% reliability of document operations

**Dependencies:** SQLite database access, Jinja2 library (for later phases)  
**Notes:** This phase fixes the critical bug that prevents document editing and establishes the foundation for all follow-up phases.
{% endcall %}

{% call section("Phase 1 — Jinja2 Template Engine & Custom Templates", "phase_1") %}
Reuse the structure above for each additional phase. Ensure tasks are actionable and tied to checklist entries.
{% endcall %}
{% endif %}

{% call section("Milestone Tracking", "milestone_tracking") %}
| Milestone | Target Date | Owner | Status | Evidence/Link |
|-----------|-------------|-------|--------|---------------|
{% if milestones %}
  {% for m in milestones %}
| {{ m.name | default("Milestone") }} | {{ m.target | default("YYYY-MM-DD") }} | {{ m.owner | default("Owner") }} | {{ m.status | default("⏳ Planned") }} | {{ m.evidence | default("Link to PROGRESS_LOG entry or commit") }} |
  {% endfor %}
{% else %}
| Phase 0 Complete | 2025-10-29 | DevTeam | 🚧 In Progress | PROGRESS_LOG.md entries |
| Phase 1 Complete | 2025-11-02 | DevTeam | ⏳ Planned | Phase 1 tasks |
| Phase 2 Complete | 2025-11-07 | DevTeam | ⏳ Planned | Phase 2 tasks |
{% endif %}
Update status and evidence as work progresses. Always link to PROGRESS_LOG entries or commits.
{% endcall %}

{% call section("Retro Notes & Adjustments", "retro_notes") %}
- Summarise lessons learned after each phase completes.  
- Document any scope changes or re-planning decisions here.
{% endcall %}
{% endblock %}
