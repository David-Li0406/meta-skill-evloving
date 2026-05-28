# Pre-Debug Checklist

Gather this information BEFORE diving into debugging. It will save you time.

## The Bug Report

### What is happening?
```
□ Exact error message (copy/paste, not paraphrase)
□ Screenshot or screen recording
□ Observed behavior vs expected behavior
□ Impact (who/what is affected)
```

### When does it happen?
```
□ Consistent or intermittent?
□ Specific time of day?
□ Under specific load?
□ After specific actions?
□ First noticed when? (date/time)
```

### Where does it happen?
```
□ Which environment? (dev/staging/prod)
□ Which browser/client?
□ Which user(s)?
□ Which URL/endpoint?
□ Geographic location (if relevant)
```

## Context Gathering

### Recent Changes
```bash
# What changed recently?
git log --oneline -20

# What files changed?
git diff HEAD~5 --stat

# Any recent deployments?
# Check deployment logs/history
```

### Environment State
```bash
# Version information
node --version
python --version
docker version

# Running services
docker ps
systemctl status service_name

# Resource usage
df -h
free -m
top -bn1 | head -5
```

### Logs Available
```
□ Application logs - where are they?
□ Web server logs (nginx, Apache)
□ Database logs
□ System logs (journald, syslog)
□ Cloud provider logs (CloudWatch, Stackdriver)
```

## Reproduction Steps

### Minimal Reproduction Path
```
1. Starting state: _________________
2. Action 1: _________________
3. Action 2: _________________
4. ...
5. Error occurs: _________________
```

### Variables to Document
```
□ User account used
□ Data/input that triggers bug
□ Browser/client version
□ Network conditions
□ Authentication state
□ Feature flags enabled
```

### Test Variations
```
□ Does it happen for all users?
□ Does it happen with different data?
□ Does it happen in different browsers?
□ Does it happen without extensions?
□ Does it happen in incognito mode?
```

## Tools Ready

### Have open/ready:
```
□ Code editor with project loaded
□ Terminal with correct directory
□ Browser DevTools
□ Database client
□ Log viewer (tail -f, CloudWatch, etc.)
□ API client (curl, Postman, etc.)
```

### Access verified:
```
□ Can access production/staging logs?
□ Can access database (read-only)?
□ Can deploy to staging?
□ Know how to rollback if needed?
```

## Communication

### Stakeholders Informed
```
□ Acknowledge the bug report
□ Set expectations for timeline
□ Identify if others need to be looped in
□ Know escalation path if critical
```

### Status Updates Planned
```
□ Who to update and how often?
□ Where to document findings?
□ When to escalate?
```

## Quick Version

If you need to start fast, at minimum get:

1. **Exact error message**
2. **Steps to reproduce**
3. **When did it start?**
4. **What changed?**
5. **Who is affected?**

---

**Remember:** 10 minutes gathering context can save hours of debugging in the wrong direction.
