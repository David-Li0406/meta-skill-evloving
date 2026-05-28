# Example: Debug Test Failure

Scenario: A test passed yesterday but fails today. Compare the logs to find what changed.

## Step 1: Quick Diff

```bash
log-analyzer diff passing.log failing.log
```

## Step 2: Focus on Key Areas

If the diff is large, narrow down:

```bash
# Focus on errors
log-analyzer diff passing.log failing.log -l ERROR

# Focus on specific component
log-analyzer diff passing.log failing.log -C core-universal

# Exclude noisy debug logs
log-analyzer diff passing.log failing.log --exclude-level DEBUG
```

## Step 3: Analyze Results

Look for:
- **Configuration changes**: SDK version, browser version, test settings
- **Error status changes**: Requests that succeed in one but fail in another
- **Missing operations**: Events present in passing but absent in failing
- **Timing differences**: Operations taking significantly longer

## Step 4: Deep Dive

For specific differences:
```bash
# Get full JSON objects for comparison
log-analyzer diff passing.log failing.log -f -t "specificEventName"

# JSON output for further processing
log-analyzer diff passing.log failing.log -F json -c > diff.json
```

## Common Findings

| Pattern | Likely Cause |
|---------|--------------|
| Different SDK version | SDK regression or behavior change |
| Different browser version | Browser compatibility issue |
| Request timeout in failing | Backend service issue |
| Missing event in failing | Race condition or timing issue |
| Different configuration | Environment/setup difference |
