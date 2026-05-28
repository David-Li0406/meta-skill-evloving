# Report Structure Guide

## Report Components

1. **Summary** - Brief overview of issue and resolution status
2. **Problem Description** - What was reported
3. **Investigation** - Steps taken and findings
4. **Root Cause** - Analysis of why the issue occurred
5. **Solution** - What was fixed and how
6. **Verification** - How the fix was confirmed
7. **Scripts Created** - List of helper/fix scripts
8. **Notes** - Any additional information

## Section Details

### Summary
- Server address
- Date/time
- Issue type
- Resolution status (Resolved/Open)

### Problem Description
- What user reported
- Expected behavior
- Actual behavior

### Investigation
- Steps taken (numbered)
- Commands executed
- Output/findings from each step

### Root Cause
- Direct cause
- Contributing factors
- Why it wasn't caught earlier

### Solution
- changes made (before/after if applicable)
- Script used
- Backup location

### Verification
- Test results
- Metrics before/after
- Logs showing success

## Example Report Structure

```markdown
# [Issue Title]

| Field | Value |
|-------|-------|
| Server | 10.0.0.1 |
| Date | 2025-01-22 |
| Status | Resolved |

## Problem Description
User reported nginx 443 port not accessible.

## Investigation
1. Verified port not listening
2. Checked systemd status
3. Inspected nginx config
4. Reviewed logs

...

## Solution
[Description of changes]

## Verification
[Results of tests]

## Scripts
- `investigate_nginx.sh` - Investigation helper
- `fix_nginx.sh` - Fix script

## Notes
[Any follow-up actions needed]
```
