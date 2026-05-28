# Error Categorization

Classifying errors for effective triage and resolution.

## Error Taxonomy

### By Layer

```
┌─────────────────────────────────────────┐
│              Presentation               │
│  (UI errors, validation, formatting)    │
├─────────────────────────────────────────┤
│               Application               │
│  (Business logic, workflows, rules)     │
├─────────────────────────────────────────┤
│                Service                  │
│  (API calls, integrations, messaging)   │
├─────────────────────────────────────────┤
│                  Data                   │
│  (Database, cache, storage)             │
├─────────────────────────────────────────┤
│              Infrastructure             │
│  (Network, compute, memory)             │
└─────────────────────────────────────────┘
```

### By Type

| Category | Examples | Typical Cause |
|----------|----------|---------------|
| Validation | Invalid input, format errors | Bad user input |
| Authentication | 401, token expired | Invalid credentials |
| Authorization | 403, permission denied | Access control |
| Not Found | 404, missing resource | Bad reference |
| Conflict | 409, duplicate, version | Concurrent modification |
| Server Error | 500, unhandled exception | Bug in code |
| Timeout | 504, gateway timeout | Performance issue |
| Rate Limit | 429, too many requests | Traffic spike |

### By Severity

```markdown
## Severity Levels

### SEV-1: Critical
- System completely down
- Data loss or corruption
- Security breach
- All users affected

### SEV-2: High
- Major feature broken
- Significant user impact
- Data integrity at risk
- Many users affected

### SEV-3: Medium
- Feature degraded
- Workaround exists
- Some users affected
- Performance impacted

### SEV-4: Low
- Minor inconvenience
- Cosmetic issues
- Edge cases
- Few users affected
```

## Categorization Framework

### Decision Tree

```markdown
## Error Categorization Flow

1. Is the system responding?
   - No → SEV-1 (System Down)
   - Yes → Continue

2. Are users blocked from core actions?
   - Yes → SEV-2 (Major Feature)
   - No → Continue

3. Is functionality degraded?
   - Yes → SEV-3 (Degraded)
   - No → SEV-4 (Minor)

4. Is data affected?
   - Corruption → Escalate one level
   - Loss → Escalate two levels
```

### Error Fingerprinting

```python
def categorize_error(error):
    """Categorize error by fingerprint."""

    fingerprint = {
        'type': type(error).__name__,
        'message_pattern': extract_pattern(str(error)),
        'stack_top': get_top_frame(error),
        'module': get_module(error)
    }

    # Match against known patterns
    if 'ECONNREFUSED' in str(error):
        return Category.INFRASTRUCTURE
    if 'ValidationError' in fingerprint['type']:
        return Category.VALIDATION
    if '401' in str(error) or 'Unauthorized' in str(error):
        return Category.AUTHENTICATION

    return Category.UNKNOWN
```

## Triage Matrix

### Response Time by Category

| Category | Severity | Response Time | Escalation |
|----------|----------|---------------|------------|
| Security | SEV-1 | Immediate | Security team |
| System Down | SEV-1 | < 15 min | All hands |
| Data Issues | SEV-1/2 | < 30 min | Data team |
| Core Feature | SEV-2 | < 1 hour | Feature team |
| Performance | SEV-2/3 | < 4 hours | Platform team |
| Integration | SEV-3 | < 8 hours | Integration owner |
| Minor Bug | SEV-4 | Next sprint | Product backlog |

### Owner Assignment

```markdown
## Error Ownership

### By Error Pattern
| Pattern | Primary Owner | Backup |
|---------|--------------|--------|
| Database | DBA | Backend |
| API 5xx | Backend | Platform |
| Auth | Security | Backend |
| UI | Frontend | Design |
| Performance | Platform | Backend |
| Third-party | Integration | Backend |

### Escalation Path
1. Primary owner
2. Team lead
3. Engineering manager
4. CTO (SEV-1 only)
```

## Error Tracking

### Grouping Strategy

```markdown
## Error Grouping Rules

### By Fingerprint
Group errors with same:
- Exception type
- Top stack frame
- Error message pattern

### By Impact
Group errors affecting:
- Same user cohort
- Same feature
- Same time window

### Example Groups
| Group ID | Count | Sample | Status |
|----------|-------|--------|--------|
| ERR-001 | 1,234 | NullPointer in getUser | Investigating |
| ERR-002 | 567 | Connection timeout | Known issue |
| ERR-003 | 89 | Validation failed | By design |
```

### Status Workflow

```
┌──────────┐     ┌────────────┐     ┌──────────┐
│   New    │────>│Investigating│────>│ Resolved │
└──────────┘     └─────┬──────┘     └──────────┘
                       │
                       │ If expected
                       ▼
                 ┌───────────┐
                 │  Ignored  │
                 └───────────┘
```

## Error Metrics

### Key Metrics

```markdown
## Error Metrics Dashboard

### Volume
- Error count per minute
- Error rate (errors / requests)
- Unique error types

### Impact
- Users affected
- Requests failed
- Revenue impact

### Response
- Time to detect (TTD)
- Time to resolve (TTR)
- Time to root cause (TTRC)
```

### SLO Integration

```yaml
# Error rate SLOs
slos:
  - name: error_rate
    target: 99.9%
    metric: 1 - (5xx_errors / total_requests)
    window: 30d

  - name: critical_error_rate
    target: 99.99%
    metric: 1 - (critical_errors / total_requests)
    window: 30d
```

## Automated Categorization

### ML-Based Categorization

```python
# Example: Error classification model
class ErrorClassifier:
    def __init__(self):
        self.model = load_model('error_classifier')

    def categorize(self, error):
        features = self.extract_features(error)
        prediction = self.model.predict(features)
        return {
            'category': prediction.category,
            'confidence': prediction.confidence,
            'suggested_owner': prediction.owner
        }

    def extract_features(self, error):
        return {
            'message_tokens': tokenize(error.message),
            'stack_frames': parse_stack(error.stack),
            'error_type': error.type,
            'service': error.service
        }
```

### Rule-Based Categorization

```yaml
# Error categorization rules
rules:
  - name: database_connection
    patterns:
      - "ECONNREFUSED.*5432"
      - "Connection refused.*postgres"
    category: infrastructure
    severity: high
    owner: dba

  - name: authentication
    patterns:
      - "401"
      - "JWT.*expired"
      - "Invalid token"
    category: authentication
    severity: medium
    owner: security

  - name: validation
    patterns:
      - "ValidationError"
      - "Invalid.*format"
    category: validation
    severity: low
    owner: backend
```
