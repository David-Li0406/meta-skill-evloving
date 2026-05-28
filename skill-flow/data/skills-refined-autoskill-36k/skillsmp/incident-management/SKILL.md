---
name: Incident Management
description: This skill should be used when the user asks to "handle incident", "create postmortem", "incident response", "on-call", "service outage", "incident escalation", "root cause analysis", "blameless postmortem", "incident severity", or needs help with incident management processes and procedures.
version: 1.0.0
---

# Incident Management

Comprehensive guidance for incident response, on-call procedures, and postmortem analysis.

## Incident Severity Levels

| Level | Description | Response Time | Examples |
|-------|-------------|---------------|----------|
| SEV1 | Critical outage | < 15 min | Full service down, data breach |
| SEV2 | Major impact | < 30 min | Partial outage, degraded performance |
| SEV3 | Minor impact | < 2 hours | Non-critical feature broken |
| SEV4 | Low impact | Next business day | Minor bug, cosmetic issue |

## Incident Response Process

### 1. Detection & Alert

```yaml
# PagerDuty alert example
alerts:
  - name: High Error Rate
    condition: error_rate > 5%
    duration: 5m
    severity: SEV2
    notify:
      - on-call-primary
      - on-call-secondary
```

### 2. Triage

- Assess impact and severity
- Assign incident commander
- Create communication channel
- Start incident timeline

### 3. Mitigation

```bash
# Common mitigation commands
kubectl rollout undo deployment/myapp
kubectl scale deployment/myapp --replicas=10
kubectl cordon node-with-issues
```

### 4. Resolution

- Verify service restored
- Monitor for recurrence
- Update status page
- Notify stakeholders

### 5. Postmortem

Schedule within 48 hours of resolution.

## Postmortem Template

```markdown
# Incident Postmortem: [Title]

**Date**: YYYY-MM-DD
**Duration**: X hours Y minutes
**Severity**: SEV-X
**Author**: Name

## Summary
Brief description of what happened.

## Impact
- X users affected
- Y% error rate
- $Z revenue impact

## Timeline (UTC)
| Time | Event |
|------|-------|
| 10:00 | Alert triggered |
| 10:05 | On-call acknowledged |
| 10:15 | Root cause identified |
| 10:30 | Mitigation applied |
| 10:45 | Service restored |

## Root Cause
Technical explanation of what caused the incident.

## Contributing Factors
- Factor 1
- Factor 2

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Add monitoring | @engineer | 2024-02-01 | Open |

## Lessons Learned
What went well? What could be improved?
```

## On-Call Best Practices

### Rotation Structure

- Primary on-call: First responder
- Secondary on-call: Backup if primary unavailable
- Escalation path: Team lead → SRE → Management

### On-Call Checklist

- [ ] Laptop and charger accessible
- [ ] VPN configured and tested
- [ ] Access to monitoring dashboards
- [ ] Runbooks bookmarked
- [ ] Escalation contacts available

## Communication Templates

### Status Page Update

```
[Investigating] We are investigating reports of elevated error rates.

[Identified] The issue has been identified as a database connectivity problem.

[Monitoring] A fix has been deployed. We are monitoring the situation.

[Resolved] The incident has been resolved. All services are operating normally.
```

## Additional Resources

### Reference Files
- **`references/runbook-templates.md`** - Service runbook templates
- **`references/communication-templates.md`** - Incident communication

### Example Files
- **`examples/postmortem-example.md`** - Complete postmortem example
