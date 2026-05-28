# Runbook: [Service/Operation Name]

## Overview

- **Service**: [Service name]
- **Owner**: [Team/person]
- **Last Updated**: [Date]
- **Criticality**: [P1-P4]

## Service Information

### Architecture

[Brief architecture description with component diagram if applicable]

### Dependencies

| Dependency | Type     | Criticality | Failure Impact       |
| ---------- | -------- | ----------- | -------------------- |
| PostgreSQL | Database | Critical    | Full outage          |
| Redis      | Cache    | High        | Degraded performance |

### Endpoints

| Endpoint | Purpose   | Health Check |
| -------- | --------- | ------------ |
| /health  | Liveness  | Yes          |
| /ready   | Readiness | Yes          |

### Key Metrics

| Metric              | Normal Range | Alert Threshold |
| ------------------- | ------------ | --------------- |
| Request latency p99 | < 200ms      | > 500ms         |
| Error rate          | < 0.1%       | > 1%            |

## Procedures

### Deployment

#### Prerequisites

- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

#### Steps

1. [Step with command]
   ```bash
   [command]
   ```

2. [Step with command]
   ```bash
   [command]
   ```

#### Verification

- [ ] [Verification step]
- [ ] [Verification step]

#### Rollback

[Link to rollback procedure or inline steps]

### Scaling

#### Scale Up

```bash
[commands]
```

#### Scale Down

```bash
[commands]
```

#### Auto-scaling Configuration

[Current auto-scaling settings and how to modify]

### Restart/Recovery

#### Graceful Restart

```bash
[commands]
```

#### Force Restart

```bash
[commands]
```

#### Full Recovery from Failure

1. [Step]
2. [Step]

### Maintenance

#### Database Maintenance

[Procedures for DB maintenance windows]

#### Cache Flush

```bash
[commands]
```

#### Log Rotation

[Log management procedures]

## Troubleshooting

### Common Issues

#### [Issue 1: Description]

**Symptoms**: [What you'll see]

**Diagnosis**:

```bash
[diagnostic commands]
```

**Resolution**:

1. [Step]
2. [Step]

#### [Issue 2: Description]

**Symptoms**: [What you'll see]

**Diagnosis**:

```bash
[diagnostic commands]
```

**Resolution**:

1. [Step]
2. [Step]

### Logs

```bash
# View logs
[log commands]

# Common log queries
[query examples]
```

### Useful Commands

```bash
# [Description]
[command]

# [Description]
[command]
```

## Escalation

| Level | Contact       | When to Escalate       |
| ----- | ------------- | ---------------------- |
| L1    | On-call       | Initial response       |
| L2    | Service owner | Unresolved after 30min |
| L3    | Platform team | Infrastructure issues  |

## References

- [Link to architecture docs]
- [Link to monitoring dashboard]
- [Link to related runbooks]
