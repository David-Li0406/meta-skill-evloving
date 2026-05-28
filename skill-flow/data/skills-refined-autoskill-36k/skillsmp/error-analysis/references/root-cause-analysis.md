# Root Cause Analysis

Techniques for finding the true cause of errors.

## RCA Framework

### The 5 Whys

```markdown
## 5 Whys Analysis

**Problem:** Users getting 500 errors on checkout

**Why 1:** Payment service returning errors
→ Payment service receiving invalid data

**Why 2:** Why is data invalid?
→ User's card number has spaces

**Why 3:** Why are spaces not handled?
→ Input validation doesn't strip whitespace

**Why 4:** Why doesn't validation strip whitespace?
→ Validation copied from old system

**Why 5:** Why wasn't this caught in testing?
→ Test data used pre-formatted card numbers

**Root Cause:** Test data doesn't represent real user input
**Fix:** Update validation AND test data
```

### Fishbone Diagram (Ishikawa)

```markdown
## Fishbone Analysis: Slow API Response

                    People              Process
                      │                    │
          Inexperienced dev   No code review
                      │                    │
                      └────────┬───────────┘
                               │
    ┌──────────────────────────┴──────────────────────────┐
    │                   SLOW API RESPONSE                  │
    └──────────────────────────┬──────────────────────────┘
                               │
                      ┌────────┴───────────┐
                      │                    │
              Missing index       No caching
                      │                    │
                 Technology            Methods

### Contributing Factors
- **People:** Developer unfamiliar with performance
- **Process:** No performance testing in CI
- **Technology:** Database missing index
- **Methods:** No caching strategy
```

### Timeline Analysis

```markdown
## Timeline Analysis

### Pre-Incident
- 09:00 - Deploy v2.3.4 to production
- 09:30 - Traffic ramp-up begins
- 10:00 - Normal traffic levels

### Incident
- 10:15 - First error alert
- 10:17 - Error rate at 5%
- 10:20 - Error rate at 15%
- 10:25 - On-call paged

### Response
- 10:27 - Investigation started
- 10:35 - Root cause identified
- 10:40 - Rollback initiated
- 10:45 - Rollback complete
- 10:50 - Error rate normalized

### Key Finding
Error started 75 minutes after deploy, triggered by
traffic pattern that only occurs at 10:15 (batch job).
```

## Investigation Techniques

### Binary Search (Git Bisect)

```bash
# Find commit that introduced bug
git bisect start
git bisect bad HEAD
git bisect good v2.3.0

# Git will checkout commits for testing
# After each test:
git bisect good  # if working
git bisect bad   # if broken

# Find result
git bisect log
```

### Log Correlation

```markdown
## Correlating Multiple Services

### Request Flow
1. API Gateway (req-123)
2. Auth Service (auth-456)
3. User Service (user-789)
4. Database

### Cross-Service Query
```bash
# Find request in all services
for log in gateway.log auth.log user.log; do
  grep "correlation_id=abc-123" $log
done
```

### Timeline Reconstruction
```
10:15:00.100 gateway  req-123 Received POST /checkout
10:15:00.150 auth     auth-456 Token validated
10:15:00.200 user     user-789 Fetching user profile
10:15:02.500 user     user-789 ERROR: Query timeout
10:15:02.501 gateway  req-123 502 Bad Gateway
```
```

### Differential Analysis

```markdown
## What Changed?

### Code Changes
```bash
git diff v2.3.3..v2.3.4 -- src/services/
```

### Config Changes
```bash
diff production.env.bak production.env
```

### Infrastructure Changes
- Check recent deployments
- Check infrastructure changes
- Check dependency updates

### Data Changes
- New data patterns
- Volume changes
- Migration effects
```

## Common Root Causes

### Category: Code Issues

| Symptom | Root Cause | Evidence |
|---------|------------|----------|
| Null pointer | Missing validation | Stack trace points to access |
| Infinite loop | Bad termination condition | CPU spike, no error |
| Memory leak | Unbounded cache | Gradual memory increase |
| Race condition | Missing synchronization | Intermittent failures |

### Category: Configuration

| Symptom | Root Cause | Evidence |
|---------|------------|----------|
| Connection refused | Wrong host/port | Config diff shows change |
| Auth failed | Wrong credentials | Credential rotation timeline |
| Timeout | Too short timeout | Works with longer timeout |
| 404 errors | Wrong path | URL config changed |

### Category: Infrastructure

| Symptom | Root Cause | Evidence |
|---------|------------|----------|
| Slow queries | Missing index | EXPLAIN shows full scan |
| Connection timeout | Network issue | Ping/traceroute failures |
| Out of memory | Under-provisioned | Metrics show OOM |
| Disk full | Log accumulation | df shows full disk |

### Category: External

| Symptom | Root Cause | Evidence |
|---------|------------|----------|
| 429 errors | Rate limiting | X-RateLimit headers |
| Intermittent failures | Third-party issues | Status page shows incident |
| Changed response | API version change | Response schema differs |
| Slow responses | Provider degradation | Provider metrics |

## RCA Documentation

### Template

```markdown
# Root Cause Analysis: [Incident Title]

## Summary
Brief description of what happened.

## Impact
- Duration: X hours
- Users affected: Y
- Revenue impact: $Z

## Timeline
[Detailed timeline with timestamps]

## Root Cause
[Clear explanation of the actual root cause]

## Contributing Factors
1. [Factor 1]
2. [Factor 2]
3. [Factor 3]

## Resolution
[What was done to fix it]

## Action Items

### Prevent
- [ ] [Action to prevent recurrence]

### Detect
- [ ] [Action to detect faster]

### Respond
- [ ] [Action to respond faster]

## Lessons Learned
1. What worked well
2. What could be improved
3. Unexpected findings
```

### Action Item Categories

```markdown
## Action Item Types

### Prevention (Stop it from happening)
- Add validation
- Add tests
- Fix code
- Update process

### Detection (Find it faster)
- Add monitoring
- Add alerting
- Improve logging
- Add health checks

### Response (Fix it faster)
- Update runbooks
- Improve rollback process
- Add feature flags
- Cross-train team
```
