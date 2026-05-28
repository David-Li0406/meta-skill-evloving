---
name: log-entity-actions
description: Security pattern for implementing security logging and audit trails. Use when designing logging systems for security events, implementing non-repudiation, creating audit trails, or addressing security monitoring and incident response needs. Addresses "Entity repudiates action request" problem.
---

# Log Entity Actions Security Pattern

Records entity actions to create an audit trail, enabling accountability, non-repudiation, incident investigation, and security monitoring.

## Problem Addressed

**Entity repudiates action request**: An entity denies having performed an action, or there's no way to determine what actions occurred, who performed them, or when.

## Core Components

| Role | Type | Responsibility |
|------|------|----------------|
| **Entity** | Entity | Performs actions that should be logged |
| **System** | Entity | Processes entity requests |
| **Logger** | Entity | Records actions to log store |
| **Log Store** | Storage | Persists log entries |
| **Log Monitor** | Entity | Analyzes logs for anomalies |

### Data Elements

- **action**: The operation performed
- **principal**: Identity of entity performing action
- **timestamp**: When action occurred
- **outcome**: Success/failure status
- **context**: Additional relevant information

## What to Log

### Security-Relevant Events
- Authentication attempts (success and failure)
- Authorization decisions (grants and denials)
- Access to sensitive data
- Administrative operations
- Security configuration changes
- Session events (creation, termination)

### Per-Event Information
- **Who**: Principal/user identifier
- **What**: Action performed
- **When**: Timestamp (synchronized, preferably UTC)
- **Where**: Source (IP, location, system)
- **Outcome**: Success, failure, error
- **Context**: Relevant parameters (without sensitive data)

## What NOT to Log

**Never log:**
- Passwords or credentials
- Session tokens
- Encryption keys
- Full credit card numbers
- Personal data beyond necessity
- Sensitive business data

## Security Considerations

### Log Integrity
- Protect logs from tampering
- Detect unauthorized modifications
- Consider append-only storage
- Sign or hash log entries

### Log Confidentiality
- Logs may contain sensitive information
- Restrict access to authorized personnel
- Encrypt logs at rest and in transit

### Log Availability
- Ensure logging system resilience
- Handle logging failures gracefully
- Don't let logging failures stop business operations
- Alert on logging system issues

### Centralized Logging
- Aggregate logs from multiple sources
- Enables correlation and analysis
- Protects against local log tampering
- Use secure transmission to central store

### Log Retention
- Define retention periods
- Meet compliance requirements
- Secure deletion when expired
- Archive for long-term storage if needed

### Time Synchronization
- Use NTP for consistent timestamps
- Critical for correlating events across systems
- Include timezone information (prefer UTC)

## Logging Flow

```
Entity → [action] → System
System → [log(action, principal, timestamp, outcome)] → Logger
Logger → [store] → Log Store
Log Monitor → [analyze] → Log Store
Log Monitor → [alert] → Security Team (if anomaly)
```

## Implementation Guidelines

### Log Format
- Use structured format (JSON, key-value)
- Consistent schema across systems
- Include correlation IDs for request tracing

### Log Levels
- ERROR: Security failures requiring attention
- WARN: Suspicious but not definitively malicious
- INFO: Normal security events
- DEBUG: Detailed troubleshooting (not in production)

### Performance
- Asynchronous logging to avoid blocking
- Buffer and batch writes
- Monitor logging overhead

### Monitoring and Alerting
- Real-time analysis for critical events
- Threshold-based alerts (e.g., failed logins)
- Pattern detection for attack identification

## Common Security Events to Log

| Event | Log Level | Details to Include |
|-------|-----------|-------------------|
| Login success | INFO | principal, source IP, timestamp |
| Login failure | WARN | attempted user, source IP, failure reason |
| Authorization denied | WARN | principal, action, resource |
| Admin action | INFO | principal, action, target, parameters |
| Security config change | INFO | principal, what changed, old/new values |
| Session timeout | INFO | principal, session duration |

## Implementation Checklist

- [ ] All authentication events logged
- [ ] All authorization denials logged
- [ ] Sensitive operations logged
- [ ] No credentials in logs
- [ ] Timestamps synchronized (NTP)
- [ ] Logs protected from tampering
- [ ] Log access restricted
- [ ] Retention policy defined
- [ ] Monitoring/alerting configured
- [ ] Secure transmission to central store

## Related Patterns

- Authentication (events to log)
- Authorisation (events to log)
- Data validation (events to log)

## References

- Source: https://securitypatterns.distrinet-research.be/patterns/02_02_001__log_entity_actions/
- OWASP Logging Cheat Sheet
- OWASP Security Logging Vocabulary
