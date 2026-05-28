# Root Cause Analysis Checklist

Use this checklist after fixing a bug to ensure you've found the true root cause and prevented recurrence.

## Verify the Fix

### Symptom is Gone
```
□ Original error no longer occurs
□ Tested with same reproduction steps
□ Tested in same environment as bug report
□ Tested by original reporter (if possible)
```

### No Regressions
```
□ Related functionality still works
□ Tests pass
□ No new errors in logs
□ Performance not degraded
```

## The 5 Whys

Ask "why" until you reach the fundamental cause.

### Example:
```
Bug: Users can't log in

Why 1: Login API returns 500 error
Why 2: Database query times out
Why 3: Query is doing full table scan
Why 4: Index was dropped
Why 5: Migration script had bug

Root cause: Migration script deleted production index
Fix: Restore index + fix migration + add index verification
```

### Template:
```
Bug: _________________

Why 1: _________________
Why 2: _________________
Why 3: _________________
Why 4: _________________
Why 5: _________________

Root cause: _________________
```

## Cause Categories

Check which category the root cause falls into:

### Code Issues
```
□ Logic error
□ Missing error handling
□ Race condition
□ Resource leak (memory, connections)
□ Incorrect algorithm
□ Missing validation
```

### Configuration Issues
```
□ Wrong environment variable
□ Missing configuration
□ Configuration mismatch between environments
□ Expired credentials/certificates
□ Resource limits too low
```

### Data Issues
```
□ Corrupt data in database
□ Missing data
□ Data type mismatch
□ Encoding issues
□ Data migration problem
```

### Infrastructure Issues
```
□ Resource exhaustion (disk, memory, CPU)
□ Network connectivity
□ Service dependency failure
□ Load balancer misconfiguration
□ DNS issues
```

### Process Issues
```
□ Missing test coverage
□ Incomplete code review
□ Deployment process gap
□ Missing monitoring
□ Documentation gap
```

## Prevention Measures

### Technical Prevention
```
□ Test added to catch this specific case?
□ Validation added to prevent bad input?
□ Error handling improved?
□ Logging added for faster detection?
□ Monitoring/alerting added?
□ Type checking added (TypeScript, MyPy)?
```

### Process Prevention
```
□ Checklist updated?
□ Documentation updated?
□ Code review guidelines updated?
□ Deployment process improved?
□ On-call runbook updated?
```

### Similar Issues
```
□ Could this bug exist elsewhere in the codebase?
□ Are there similar patterns that should be fixed?
□ Should we do a broader audit?
```

## Documentation

### What to Record
```
□ Bug description
□ Root cause identified
□ Fix applied
□ How it was detected
□ Time to detect
□ Time to resolve
□ Impact (users affected, duration)
□ Prevention measures added
```

### Where to Record
```
□ Ticket/issue updated
□ Post-mortem document (if significant)
□ Runbook updated (if operational issue)
□ Knowledge base article (if common pattern)
```

## Post-Mortem Questions

For significant bugs, answer:

### Timeline
```
□ When was the bug introduced?
□ When was it deployed?
□ When did it start affecting users?
□ When was it detected?
□ When was it fixed?
□ When was fix deployed?
```

### Detection
```
□ How was it detected? (User report, monitoring, etc.)
□ Why wasn't it caught earlier?
□ What would have caught it sooner?
```

### Resolution
```
□ How was it diagnosed?
□ How was it fixed?
□ Was there a quicker fix available?
□ Was rollback considered? Why/why not?
```

### Impact
```
□ How many users affected?
□ What was user experience during outage?
□ Any data loss or corruption?
□ Financial impact?
□ Reputation impact?
```

## Red Flags: Is It Really Fixed?

Be suspicious if:

```
⚠️ Fix is a workaround, not addressing root cause
⚠️ You don't understand WHY the fix works
⚠️ Fix requires manual intervention regularly
⚠️ Fix depends on specific timing or ordering
⚠️ Similar bugs have occurred before
⚠️ You can't explain the bug to someone else
⚠️ No test proves the fix works
```

## Quick Verification

At minimum:

1. **What was the root cause?** (One sentence)
2. **Why did it happen?** (Contributing factors)
3. **What's the fix?** (What changed)
4. **How do we prevent recurrence?** (Test, validation, monitoring)
5. **Is it documented?** (For future reference)

---

**Remember:** A bug fixed without understanding the root cause will likely come back. Take the time to understand why.
