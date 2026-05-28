# Deployment Checklist: [Service] [Version]

## Summary

| Field       | Value              |
| ----------- | ------------------ |
| Service     | [service name]     |
| Environment | [target env]       |
| Version     | [version/tag]      |
| Deployer    | [name]             |
| Date        | [YYYY-MM-DD HH:MM] |

## Changes Included

### Features

- [ ] [Feature description] — [PR/commit link]

### Bug Fixes

- [ ] [Fix description] — [PR/commit link]

### Migrations

| Migration        | Type       | Reversible | Tested |
| ---------------- | ---------- | ---------- | ------ |
| [migration name] | [add/modify/delete] | [yes/no] | [yes/no] |

### Configuration Changes

- [ ] [Config change description]

### Dependency Updates

| Dependency | From    | To      | Breaking |
| ---------- | ------- | ------- | -------- |
| [package]  | [old]   | [new]   | [yes/no] |

## Pre-flight Checklist

### Code Readiness

- [ ] All tests passing in CI
- [ ] Code reviewed and approved
- [ ] Merged to release branch
- [ ] Version/tag created

### Environment Readiness

- [ ] Target environment available
- [ ] Required resources provisioned
- [ ] Configuration/secrets updated
- [ ] Feature flags configured

### Observability

- [ ] Dashboards ready
- [ ] Alerts configured
- [ ] Log queries prepared
- [ ] Tracing enabled

### Communication

- [ ] Stakeholders notified
- [ ] On-call aware
- [ ] Runbook available
- [ ] Rollback plan reviewed

## Deployment Strategy

### Rollout Type

[Rolling Update / Blue-Green / Canary]

### Rollout Steps

1. [ ] [Step 1 with verification gate]
2. [ ] [Step 2 with verification gate]
3. [ ] [Step 3 with verification gate]

### Traffic Progression (Canary)

| Stage | Traffic | Duration | Verification          |
| ----- | ------- | -------- | --------------------- |
| 1     | 10%     | 10 min   | [what to check]       |
| 2     | 50%     | 15 min   | [what to check]       |
| 3     | 100%    | —        | Full verification     |

## Deployment Commands

```bash
# [Command description]
[actual command]

# [Command description]
[actual command]
```

## Verification Checklist

### Immediate (0-5 minutes)

- [ ] Pods/instances healthy
- [ ] No error spikes in logs
- [ ] Health checks passing
- [ ] Basic smoke test passing

### Short-term (5-30 minutes)

- [ ] Metrics within normal range
- [ ] Key features functional
- [ ] No elevated error rates
- [ ] Response times acceptable

### Extended (30 min - 2 hours)

- [ ] Performance stable
- [ ] No memory leaks
- [ ] No degradation over time
- [ ] User reports (if applicable)

## Rollback

### Trigger Conditions

Initiate rollback if ANY of these occur:

- [ ] Error rate exceeds [threshold]%
- [ ] P99 latency exceeds [threshold]ms
- [ ] [Critical feature] unavailable
- [ ] Migration failure
- [ ] [Other condition]

### Rollback Plan

```bash
# [Rollback command description]
[actual rollback command]

# [Verification command]
[actual command]
```

### Rollback Verification

- [ ] Previous version running
- [ ] Health checks passing
- [ ] Error rates normalized
- [ ] Functionality restored

### Post-Rollback Communication

- [ ] Team notified
- [ ] Incident created (if applicable)
- [ ] Stakeholders updated

## Notes

[Additional context, known issues, special considerations]
