---
name: remote-troubleshoot
description: Structured remote server troubleshooting workflow that follows investigation-only practices until user approval. Use when Claude needs to diagnose issues on remote SSH-accessible servers including k8s clusters, bare metal, and containerized services. Covers service/port access problems, configuration issues, service startup failures, and performance/resource issues. Emphasizes creating helper scripts on remote server, obtaining user approval before fixes, script-based repairs, and generating comprehensive analysis reports.
---

# Remote Server Troubleshooting

## Overview

Provides a structured workflow for troubleshooting issues on remote servers with emphasis on:
- Investigation-only approach until user approval
- Creating reusable helper scripts on remote server
- Script-based fixes for reproducibility
- Comprehensive analysis and resolution reports

## Investigation Workflow

### Phase 0: Information Gathering

Before starting any investigation, gather:

1. **Remote Server Access**
   - Server address/IP
   - SSH method (sshpass, keys, etc.) and credentials
   - Remote user

2. **Problem Description**
   - What is the exact issue?
   - When did it start?
   - What service/component is affected?

3. **Context**
   - Environment (k8s, bare metal, containerized)
   - Relevant config file locations
   - Recent changes

### Phase 1: Initial Verification (Read-Only)

**CRITICAL: Do NOT make any changes without user approval**

Validate the reported issue actually exists:
```bash
sshpass -p<password> ssh -o StrictHostKeyChecking=no user@host "echo 'OK'"
ssh user@host "ss -tlnp | grep :<port>"
ssh user@host "systemctl status <service>"
ssh user@host "kubectl get pods -n <namespace>"
```

If issue cannot be reproduced, inform user and ask clarification.

### Phase 2: Create Investigation Environment

```bash
ssh user@host "mkdir -p ~/troubleshoot-$(date +%Y%m%d)"
```

### Phase 3: Deploy Helper Scripts

Generate and upload investigation scripts. Use `scripts/generate_helper.sh`.

Common scenarios: service status, ports, config inspection, logs.

**Always execute investigation scripts, never modify actions.**

### Phase 4: Execute Investigation

Run helper scripts. Document:
- Current state (what IS happening)
- Expected state (what SHOULD happen)
- Differences (the gap)

### Phase 5: Analysis and Root Cause

Synthesize findings to identify root cause. Consider multiple hypotheses if unclear.

### Phase 6: Propose Solution

Present to user:
1. Root Cause Summary
2. Proposed Fix (step-by-step)
3. Risk Assessment
4. Rollback Plan

**WAIT for user approval before proceeding to repair.**

## Repair Workflow

### Phase 7: Create Fix Script

Script the fix procedure. Fix script MUST:
1. Create backups before modifying
2. Apply changes in safe steps
3. Verify after each step
4. Report results clearly

### Phase 8: Apply Fix

```bash
cat fix-script.sh | ssh user@host "bash -s"
```

### Phase 9: Verification

Confirm fix resolved the issue:
- Re-run initial validation
- Check service/operation
- Monitor logs

### Phase 10: Generate Report

Use `assets/report-template.md` to create analysis report.

## Scenarios and Patterns

See [references/patterns.md](references/patterns.md) for:
- K8s troubleshooting patterns
- Network/port issues
- Service failures
- Configuration mismatches

## Quick Reference

```bash
# Service
systemctl status <service>
systemctl is-active <service>

# Port
ss -tlnp | grep :<port>

# Process
ps aux | grep <name>

# Logs
journalctl -u <service> -n 50 --no-pager
tail -f /var/log/<service>.log

# K8s
kubectl get pods -n <namespace>
kubectl describe pod <name> -n <namespace>
kubectl logs <pod> -n <namespace>
```

## Resources

### scripts/
- `generate_helper.sh` - Generate investigation helper scripts
- `generate_fix.sh` - Generate fix script templates

### references/
- [patterns.md](references/patterns.md) - Common investigation patterns
- [report_guide.md](references/report_guide.md) - Report structure guide

### assets/
- [report-template.md](assets/report-template.md) - Markdown report template
