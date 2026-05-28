{% extends "documents/base_log.md" %}
{% from "documents/base_log.md" import rotation_notice with context %}

{% block log_metadata %}
{% set log_config.title = "Bug Log" %}
{% set log_config.icon = "🐞" %}
{% set log_config.summary = 'Track bug discoveries, investigations, and resolutions. Use `log_type="bugs"` (or `--log bugs`).' %}
{% endblock %}

{% block log_body %}
{% set rotation_raw = metadata.get("is_rotation", metadata.get("IS_ROTATION", is_rotation | default("false"))) %}
{% set rotation_active = rotation_raw in [True, "true", "True", 1, "1", "yes", "YES"] %}
{% if rotation_active %}
{{ rotation_notice(metadata) }}
{% endif %}

## Entry Format
```
[EMOJI] [YYYY-MM-DD HH:MM:SS UTC] [Agent: <name>] [Project: {{ project_name or PROJECT_NAME }}] Message text | severity=<severity>; component=<component>; status=<status>; [additional metadata]
```

**Required Metadata Fields:**
- `severity`: critical/high/medium/low/minimal
- `component`: Component or module where bug exists
- `status`: open/investigating/in_progress/fixed/verified/closed/wont_fix

**Optional Metadata Fields:**
- `bug_id`: Ticket number or identifier
- `environment`: production/staging/development/local
- `reproduction_steps`: Brief summary of repro steps
- `test_case`: Test case ID that should cover this bug
- `fix_commit`: Commit hash for the fix
- `reviewer`: Code reviewer
- `confidence`: Confidence in root cause analysis (0-1)
- `impact`: Business impact (critical/high/medium/low/minimal)
- `customer_impacted`: true/false
- `regression`: true/false
- `estimated_effort`: XS/S/M/L/XL
- `related_issues`: Comma-separated list of linked tickets

---

## Severity Classification Guide
- **Critical**: System down, data loss, security vulnerability, or production outage.
- **High**: Major feature broken or significant customer impact; workaround limited.
- **Medium**: Feature partially broken; minor impact; workaround available.
- **Low**: Minor UI issues, edge cases, documentation errors.
- **Minimal**: Cosmetic issues, typos, non-functional improvements.

---

## Component Categories
- **Backend**: Server-side code, APIs, databases.
- **Frontend**: UI and client-side logic.
- **Infrastructure**: Deployment, CI/CD, monitoring, configuration.
- **Tests**: Test suites or infrastructure.
- **Documentation**: READMEs, API docs, guides.
- **Performance**: Latency/throughput regressions.
- **Security**: Security-related bugs and vulnerabilities.
- **Data**: Migration, seeding, or validation errors.

---

## Status Flow Guide
1. **open** → Initial discovery and logging  
2. **investigating** → Root cause analysis  
3. **in_progress** → Fix under development  
4. **fixed** → Fix implemented, ready for testing  
5. **verified** → Fix tested and confirmed  
6. **closed** → Issue resolved and documented  
7. **wont_fix** → Issue accepted as-is (include justification)

---

## Entries will populate below
{% endblock %}
