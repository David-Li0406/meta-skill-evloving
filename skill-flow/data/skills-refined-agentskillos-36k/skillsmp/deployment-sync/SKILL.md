---
name: deployment-sync
description: Verify deployment documentation is in sync with configuration files. Use when checking documentation consistency, verifying ports match, auditing deployment config, or when user asks "check docs", "sync documentation", "verify deployment", or "audit config".
allowed-tools: Read, Grep, Glob
user-invocable: true
---

# Deployment Documentation Sync

This skill verifies that deployment documentation stays in sync with actual configuration files.

## Files to Cross-Reference

| Source of Truth | Documentation |
|-----------------|---------------|
| `docker-compose.yml` | `DOCUMENTATION/DEPLOYMENT.md` |
| `Jenkinsfile` | `DOCUMENTATION/DEPLOYMENT.md` |
| `.env.example` | `DOCUMENTATION/DEPLOYMENT.md` |

## Verification Steps

### 1. Port Configuration

Extract ports from each source and compare:

**From docker-compose.yml:**
```bash
# Look for "ports:" sections
grep -A1 "ports:" docker-compose.yml
```

**From Jenkinsfile:**
```bash
# Look for PORT variables
grep "_PORT = " Jenkinsfile
```

**From DOCUMENTATION/DEPLOYMENT.md:**
- Check "Port Configuration" tables
- Verify Production and Development ports match

### 2. Container Names

**From docker-compose.yml:**
```bash
grep "container_name:" docker-compose.yml
```

**From Jenkinsfile:**
```bash
grep "_CONTAINER = " Jenkinsfile
```

**From DOCUMENTATION/DEPLOYMENT.md:**
- Check "Container Reference" tables

### 3. Environment Variables

**From .env.example:**
```bash
grep "^[A-Z].*=" .env.example | cut -d= -f1
```

**From DOCUMENTATION/DEPLOYMENT.md:**
- Check "Environment Variables" sections
- Verify all variables are documented

### 4. Service Health Endpoints

**From Jenkinsfile:**
```bash
grep "curl.*health" Jenkinsfile
```

**From DOCUMENTATION/DEPLOYMENT.md:**
- Check "Infrastructure Endpoints" table
- Check "Quick Reference - Health Checks" section

## Report Format

Generate a report listing:

1. **Ports** - Any mismatches between files
2. **Containers** - Missing or extra container names
3. **Environment Variables** - Undocumented variables
4. **Health Endpoints** - Missing health check documentation

## Example Output

```
## Deployment Sync Report

### Ports
✅ Backend: 8000 (consistent across all files)
✅ Telegram MCP: 8081 (consistent)
⚠️ GitHub MCP: 8083 in Jenkinsfile, missing from docker-compose.yml

### Containers
✅ All 7 containers documented

### Environment Variables
⚠️ NEW_VAR in .env.example not documented in DEPLOYMENT.md

### Health Endpoints
✅ All endpoints documented
```

## Common Issues

| Issue | Fix |
|-------|-----|
| Port mismatch | Update DEPLOYMENT.md to match Jenkinsfile |
| Missing container | Add to Container Reference table |
| Undocumented env var | Add to Environment Variables section |
| Missing health endpoint | Add to Infrastructure Endpoints table |

## Automation

For automated checking, look for patterns:

```python
# Ports should match this pattern in each file:
# docker-compose.yml: "- 808X:808X"
# Jenkinsfile: "_PORT = '808X'"
# DEPLOYMENT.md: "| Service | 808X | 808X |"
```

## After Fixing

When documentation is updated:
1. Update the Changelog table in DEPLOYMENT.md
2. Commit with message: "docs: sync deployment documentation"
