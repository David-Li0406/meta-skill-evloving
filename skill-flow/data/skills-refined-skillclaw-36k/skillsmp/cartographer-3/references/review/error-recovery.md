# Review Error Recovery Protocol

This reference defines error handling and recovery procedures for `/navigator:review`.

## Agent Failures

When review agents fail after 3 attempts:

### 1. Partial Results Handling

```
⚠️ Agent failures during review

Completed:
- Pattern Enforcer: ✅ 5 violations
- Architecture Auditor: ✅ 2 violations

Failed:
- Anti-Pattern Detector: ❌ (3 attempts)
- Convention Checker: ❌ (timeout)

Options:
1. Continue with partial results
2. Retry failed agents only
3. Skip agent review, do manual review
4. Abort review
```

### 2. Continue with Partial Results

When continuing with partial results:
- Generate report with available data
- Mark missing sections as "Not Available"
- Add warning to review summary

```markdown
### Multi-Agent Review Results

| Agent | Findings | Severity |
|-------|----------|----------|
| Pattern Enforcer | 5 violations | error |
| Architecture Auditor | 2 violations | warning |
| Anti-Pattern Detector | ⚠️ Not Available | - |
| Convention Checker | ⚠️ Not Available | - |

**Note:** 2 agents failed. Results may be incomplete.
```

### 3. Preserve Partial State

Write `.claude/review-partial.json`:

```json
{
  "spec_file": "{spec}",
  "timestamp": "{ISO-8601}",
  "completed_agents": ["pattern-enforcer", "architecture-auditor"],
  "failed_agents": [
    {"name": "anti-pattern-detector", "error": "{error}", "attempts": 3},
    {"name": "convention-checker", "error": "timeout", "attempts": 3}
  ],
  "partial_results": {
    "pattern_violations": [...],
    "architecture_violations": [...]
  }
}
```

## Validation Command Failures

When validation commands fail:

### 1. Classify Failure Type

| Type | Example | Action |
|------|---------|--------|
| Build error | `npm run build` fails | Report errors, suggest fixes |
| Test failure | `npm test` has failures | List failing tests with reasons |
| Lint error | `npm run lint` has issues | List lint violations |
| Timeout | Command exceeds limit | Report timeout, suggest async |
| Not found | Command doesn't exist | Warn, skip that validation |

### 2. Continue Despite Failures

```
⚠️ Validation command failed: npm run build

Exit code: 1
Error output:
  {first 500 chars of stderr}

Impact: Build validation marked as failed
Continuing with remaining validations...
```

### 3. Summary Handling

- Failed validations appear in Validation section with ❌
- Don't block entire review for validation failures
- User can still see other review findings

```markdown
### Validation Status

| Check | Status | Details |
|-------|--------|---------|
| Type check | ✅ | Passed |
| Tests | ❌ | 3 failures |
| Lint | ⚠️ | 5 warnings |
| Build | ❌ | TypeScript errors |
```

## Error Reference Table

| Error | Action | Recovery |
|-------|--------|----------|
| No atlas | Block with message | Run /cartographer:chart |
| No spec | Error with path | User provides correct path |
| No changes | Note implementation may be missing | Check if on correct branch |
| Validation fails | Report failures | User fixes or accepts |
| Agent timeout | Retry once, then skip | Continue with partial |
| Parse error | Report parse issue | Check agent output manually |
| Git error | Report git issue | Check git state |

## Retry Strategy

### Agent Retries

```
Attempt 1: Normal invocation
Attempt 2: Same invocation (transient failure)
Attempt 3: Simplified context (reduce input size)
After 3: Mark as failed, continue without
```

### Validation Retries

```
Attempt 1: Normal execution
Timeout: Double timeout, retry once
Failure: No retry, report failure
```

## Recovery Options

### For Blocked Reviews

If review cannot complete:

```
❌ Review blocked

Reason: {reason}

Options:
1. Fix the issue and re-run /navigator:review {spec}
2. Run with --no-agents for lightweight review
3. Skip review and proceed (not recommended)
```

### For Partial Reviews

If review completes with gaps:

```
⚠️ Review completed with limitations

Missing data:
- Anti-pattern scan (agent failed)
- Build validation (command not found)

The review is still useful but may miss some issues.
Consider:
1. Accept partial review
2. Run missing checks manually
3. Re-run full review after fixing agent issues
```

## Logging

All errors should be logged with:

| Field | Description |
|-------|-------------|
| `timestamp` | When error occurred |
| `component` | Agent or command that failed |
| `error_type` | Classification of error |
| `error_message` | Full error text |
| `recovery_action` | What action was taken |
| `impact` | What was affected |
