{% extends "documents/base_log.md" %}
{% from "documents/base_log.md" import rotation_notice with context %}

{% block log_metadata %}
{% set log_config.title = "Security Log" %}
{% set log_config.icon = "🔒" %}
{% set log_config.summary = 'Track security events, vulnerabilities, and decisions. Use `log_type="security"` (or `--log security`).' %}
{% endblock %}

{% block log_body %}
{% set rotation_raw = metadata.get("is_rotation", metadata.get("IS_ROTATION", is_rotation | default("false"))) %}
{% set rotation_active = rotation_raw in [True, "true", "True", 1, "1", "yes", "YES"] %}
{% if rotation_active %}
{{ rotation_notice(metadata) }}
{% endif %}

## Entry Format
```
[EMOJI] [YYYY-MM-DD HH:MM:SS UTC] [Agent: <name>] [Project: {{ project_name or PROJECT_NAME }}] Message text | severity=<severity>; area=<area>; impact=<impact>; [additional metadata]
```

**Required Metadata Fields:**
- `severity`: critical/high/medium/low/informational
- `area`: authentication, data_storage, network, code_injection, infrastructure, configuration
- `impact`: Business impact level (critical/high/medium/low/minimal)

**Optional Metadata Fields:**
- `cve_id`: CVE identifier (if applicable)
- `cvss_score`: CVSS score (0-10)
- `component`: Component or module affected
- `mitigation_status`: open/in_progress/mitigated/accepted_risk
- `mitigation_date`: Date mitigation was implemented
- `reviewer`: Security reviewer
- `test_coverage`: covered/partial/uncovered
- `compliance_framework`: SOC2, GDPR, HIPAA, PCI_DSS, etc.
- `remediation_priority`: P0/P1/P2/P3

---

## Severity Classification Guide
- **Critical**: Immediate threat to production data or systems; requires immediate action.
- **High**: Significant security risk; address within 24 hours.
- **Medium**: Moderate risk; fix within a week.
- **Low**: Minor issue; schedule for next release cycle.
- **Informational**: Observations, best practices, or low-risk improvements.

---

## Security Areas
- **Authentication**: Login, authorization, identity management.
- **Data Storage**: Encryption, database security, data handling.
- **Network**: API security, segmentation, firewall rules.
- **Code Injection**: XSS, SQL injection, command injection.
- **Infrastructure**: Servers, containers, secrets management.
- **Configuration**: Settings, permissions, access controls.

---

## Entries will populate below
{% endblock %}
