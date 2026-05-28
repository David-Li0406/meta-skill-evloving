---
name: incident-response-runbook
description: Use this skill when responding to outages, investigating errors, or running post-incident reviews for various integrations.
---

# Incident Response Runbook

## Overview
Rapid incident response procedures for various service outages.

## Prerequisites
- Access to the service dashboard and status page
- kubectl access to production cluster
- Prometheus/Grafana access
- Communication channels (Slack, PagerDuty)

## Severity Levels

| Level | Definition | Response Time | Examples |
|-------|------------|---------------|----------|
| P1 | Complete outage | < 15 min | API unreachable |
| P2 | Degraded service | < 1 hour | High latency, partial failures |
| P3 | Minor impact | < 4 hours | Webhook delays, non-critical errors |
| P4 | No user impact | Next business day | Monitoring gaps |

## Quick Triage

```bash
# 1. Check service status
curl -s https://status.yourservice.com | jq

# 2. Check our integration health
curl -s https://api.yourapp.com/health | jq '.services.yourservice'

# 3. Check error rate (last 5 min)
curl -s localhost:9090/api/v1/query?query=rate(yourservice_errors_total[5m])

# 4. Recent error logs
kubectl logs -l app=yourservice-integration --since=5m | grep -i error | tail -20
```

## Decision Tree

```
Is the API returning errors?
├─ YES: Is the service status page showing an incident?
│   ├─ YES → Wait for the service to resolve. Enable fallback.
│   └─ NO → Our integration issue. Check credentials, config.
└─ NO: Is our service healthy?
    ├─ YES → Likely resolved or intermittent. Monitor.
    └─ NO → Our infrastructure issue. Check pods, memory, network.
```

## Immediate Actions by Error Type

### 401/403 - Authentication
```bash
# Verify API key is set
kubectl get secret yourservice-secrets -o jsonpath='{.data.api-key}' | base64 -d

# Check if key was rotated
# → Verify in the service dashboard

# Remediation: Update secret and restart pods
kubectl create secret generic yourservice-secrets --from-literal=api-key=NEW_KEY --dry-run=client -o yaml | kubectl apply -f -
kubectl rollout restart deployment/yourservice-integration
```

### 429 - Rate Limit
```bash
# Check rate limit headers
curl -v https://api.yourservice.com 2>&1 | grep
```