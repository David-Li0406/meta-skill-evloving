{% extends "documents/base_document.md" %}
{% set doc_title = "Acceptance Checklist" %}
{% set doc_icon = "✅" %}
{% set doc_version = metadata.version | default("v0.1") %}
{% set doc_status = metadata.status | default("Draft") %}
{% set summary = metadata.summary | default("Mirror the Phase Plan here. Every task should map to a checkbox with proof (commit, log entry, screenshot, etc.).") %}
{% set sections = metadata.sections or [] %}

{% block document_body %}
{% if sections %}
  {% for section_block in sections %}
    {% set checklist_items = section_block["items"] if "items" in section_block else [] %}
    {% call section(section_block.title, section_block.anchor or ("section_" ~ loop.index0)) %}
{{ checklist(checklist_items, "Add verification tasks for " ~ section_block.title ~ ".") }}
    {% endcall %}
  {% endfor %}
{% else %}
{% call section("Documentation Hygiene", "documentation_hygiene") %}
- [x] Architecture guide updated after each code or plan change (proof: ARCHITECTURE_GUIDE.md with comprehensive Document Management 2.0 design).
- [x] Phase plan reflects current scope (proof: PHASE_PLAN.md with 3 detailed implementation phases).
- [x] Checklist cross-referenced in progress logs (proof: All bootstrap tasks logged with checklist references).
{% endcall %}

{% call section("Phase 0 — Foundation Fixes & Database Enhancement", "phase_0") %}
- [ ] Fix async/await bug in manager.py by adding async_atomic_write function (proof: commit showing files.py and manager.py changes).
- [ ] Extend database schema with document_sections, custom_templates, document_changes tables (proof: migration script and updated models.py).
- [ ] Implement database migration system for backwards compatibility (proof: migration tests and existing project compatibility).
- [ ] Add comprehensive error handling and validation to manage_docs operations (proof: enhanced error messages in logs).
- [ ] Create post-write verification to eliminate silent failures (proof: test suite showing 100% operation success).
- [ ] Add structured logging for all document operations (proof: JSON log entries with operation context).
{% endcall %}

{% call section("Phase 1 — Jinja2 Template Engine & Custom Templates", "phase_1") %}
- [ ] Integrate Jinja2 template engine with security sandboxing (proof: Jinja2 environment setup with security constraints).
- [ ] Replace simple {{'{{variable}}'}} substitution with Jinja2 rendering (proof: template rendering tests passing).
- [ ] Implement template inheritance and block system (proof: template tests with inheritance scenarios).
- [ ] Create custom template discovery system (.scribe/templates/) (proof: custom template loading and usage).
- [ ] Add JSON-based custom variable definitions (proof: variable resolution tests).
- [ ] Implement template validation and error reporting (proof: template error handling tests).
{% endcall %}

{% call section("Phase 2 — Bidirectional Sync & Change Tracking", "phase_2") %}
- [ ] Implement file system watcher for manual edit detection (proof: watcher tests detecting file changes).
- [ ] Create bidirectional sync manager with conflict resolution (proof: sync tests with conflict scenarios).
- [ ] Add git-level change tracking with commit messages (proof: change history logs with git-style messages).
- [ ] Implement change diff visualization and history (proof: diff display in change logs).
- [ ] Create conflict resolution system with manual override (proof: conflict resolution tests).
- [ ] Add file system integrity verification (proof: integrity check tests).
- [ ] Implement database change logging and rollback (proof: database rollback tests).
- [ ] Add performance monitoring and metrics collection (proof: performance metrics in logs).
{% endcall %}
{% endif %}

{% call section("Final Verification", "final_verification") %}
- [ ] All checklist items checked with proofs attached.  
- [ ] Stakeholder sign-off recorded (name + date).  
- [ ] Retro completed and lessons learned documented.
{% endcall %}
{% endblock %}
