# Runbook

This file is an example placeholder referenced by the Skill Creator skill.

## Incident Basics

- **Severity levels**: [SEV-1/2/3 definitions]
- **Primary on-call**: [Team/contact]
- **Escalation**: [When/how to page additional responders]

## Quick Triage Checklist

1. Identify symptoms: errors, latency, timeouts, data issues
2. Determine scope: single tenant/user vs. global
3. Check recent changes: deploys, config, feature flags
4. Verify dependencies: DB, cache, queue, third-party APIs

## Common Signals

- **Logs**: where to look, key queries
- **Metrics**: dashboards, SLOs, error rate, p95/p99
- **Tracing**: service maps, span attributes

## Immediate Mitigations

- Roll back / disable feature flag
- Reduce load: rate limiting, circuit breakers
- Increase capacity: scale services, workers
- Degrade gracefully: disable non-critical features

## Deep Dive

- How to reproduce (if possible)
- How to identify the failing component
- How to validate data integrity

## Post-Incident

- Timeline and root cause
- Customer impact summary
- Action items: prevention, detection, documentation
