# Log Analysis Workflow

## Purpose

Analyze Cloud Run production logs using gcloud CLI to verify system health and diagnose issues.

---

## Prerequisites

- gcloud CLI authenticated
- Correct project configured (`gcloud config set project gcp-transcribe-test`)
- Cloud Run service deployed (`nikita-api`)

---

## Quick Reference

```bash
# Set correct project
gcloud config set project gcp-transcribe-test

# Basic log view
gcloud run services logs read nikita-api --region us-central1 --limit 100

# With timestamp filter
gcloud run services logs read nikita-api --region us-central1 --limit 100 --format='table(timestamp,textPayload)'
```

---

## Phase 1: Recent Activity Check

### 1.1 Get Last 100 Logs

```bash
gcloud run services logs read nikita-api \
  --region us-central1 \
  --limit 100 \
  --format='value(timestamp,textPayload)'
```

### 1.2 Filter for Errors

```bash
gcloud run services logs read nikita-api \
  --region us-central1 \
  --limit 200 \
  2>&1 | grep -i -E "(error|exception|traceback|failed)"
```

### 1.3 Filter for Warnings

```bash
gcloud run services logs read nikita-api \
  --region us-central1 \
  --limit 200 \
  2>&1 | grep -i -E "(warn|warning)"
```

---

## Phase 2: Request Flow Analysis

### 2.1 Webhook Requests

```bash
gcloud run services logs read nikita-api \
  --region us-central1 \
  --limit 100 \
  2>&1 | grep -i "webhook\|telegram"
```

### 2.2 LLM Timing

Look for timing logs from the agent:

```bash
gcloud run services logs read nikita-api \
  --region us-central1 \
  --limit 100 \
  2>&1 | grep -i "TIMING\|LLM-DEBUG\|PROMPT-DEBUG"
```

**Expected patterns:**
- `[TIMING] _create_nikita_agent START`
- `[TIMING] Tools imported: X.XXs`
- `[LLM-DEBUG] generate_response called`
- `[PROMPT-DEBUG] Personalized prompt generated: X chars, Xms`

### 2.3 Memory Operations

```bash
gcloud run services logs read nikita-api \
  --region us-central1 \
  --limit 100 \
  2>&1 | grep -i "MEMORY\|neo4j\|graphiti"
```

---

## Phase 3: Error Investigation

### 3.1 Get Stack Traces

```bash
gcloud run services logs read nikita-api \
  --region us-central1 \
  --limit 500 \
  2>&1 | grep -A 20 "Traceback"
```

### 3.2 Common Error Patterns

| Pattern | Meaning | Likely Cause |
|---------|---------|--------------|
| `OpenAIError` | OpenAI API issue | Quota, key, rate limit |
| `Neo4jError` | Graph DB issue | Credentials, connection |
| `AttributeError: 'NoneType'` | Null reference | Missing data |
| `IntegrityError` | DB constraint | Duplicate, FK violation |
| `TimeoutError` | Operation timeout | Cold start, slow LLM |

### 3.3 Specific Error Search

```bash
# OpenAI issues
gcloud run services logs read nikita-api \
  --region us-central1 --limit 200 \
  2>&1 | grep -i "openai\|embeddings\|quota"

# Database issues
gcloud run services logs read nikita-api \
  --region us-central1 --limit 200 \
  2>&1 | grep -i "supabase\|postgres\|sql"

# Authentication issues
gcloud run services logs read nikita-api \
  --region us-central1 --limit 200 \
  2>&1 | grep -i "auth\|jwt\|token\|otp"
```

---

## Phase 4: Performance Analysis

### 4.1 Cold Start Detection

```bash
gcloud run services logs read nikita-api \
  --region us-central1 \
  --limit 100 \
  2>&1 | grep -i "cold\|startup\|init"
```

### 4.2 Request Duration

Look for FastAPI request timing:

```bash
gcloud run services logs read nikita-api \
  --region us-central1 \
  --limit 100 \
  2>&1 | grep -E "[0-9]+ms\|[0-9]+s\|duration"
```

### 4.3 Memory Usage

```bash
gcloud run services logs read nikita-api \
  --region us-central1 \
  --limit 100 \
  2>&1 | grep -i "memory\|heap\|oom"
```

---

## Phase 5: Specific User Investigation

### 5.1 Filter by User ID

```bash
USER_ID="your-user-uuid-here"
gcloud run services logs read nikita-api \
  --region us-central1 \
  --limit 200 \
  2>&1 | grep -i "$USER_ID"
```

### 5.2 Filter by Telegram ID

```bash
TELEGRAM_ID="123456789"
gcloud run services logs read nikita-api \
  --region us-central1 \
  --limit 200 \
  2>&1 | grep -i "$TELEGRAM_ID"
```

---

## Phase 6: Time-Based Analysis

### 6.1 Last Hour

```bash
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="nikita-api"' \
  --limit 100 \
  --freshness=1h \
  --project gcp-transcribe-test \
  --format='table(timestamp,textPayload)'
```

### 6.2 Specific Time Range

```bash
gcloud logging read \
  'resource.type="cloud_run_revision" AND resource.labels.service_name="nikita-api" AND timestamp>="2025-12-21T12:00:00Z" AND timestamp<="2025-12-21T13:00:00Z"' \
  --limit 500 \
  --project gcp-transcribe-test
```

---

## Phase 7: Service Health

### 7.1 Check Deployment Status

```bash
gcloud run services describe nikita-api \
  --region us-central1 \
  --format='table(status.url,status.conditions[0].status,status.conditions[0].message)'
```

### 7.2 Current Revision

```bash
gcloud run services describe nikita-api \
  --region us-central1 \
  --format='value(status.latestReadyRevisionName)'
```

### 7.3 Recent Deployments

```bash
gcloud run revisions list \
  --service nikita-api \
  --region us-central1 \
  --limit 5
```

---

## Log Severity Guide

| Severity | Meaning | Action |
|----------|---------|--------|
| DEFAULT | Info logs | Monitor patterns |
| WARNING | Potential issue | Investigate if recurring |
| ERROR | Failure occurred | Fix required |
| CRITICAL | System impact | Immediate fix |

---

## Common Failure Patterns

### Pattern 1: OpenAI Quota

```
OpenAIError: Rate limit exceeded
```
**Fix:** Wait, or upgrade API plan

### Pattern 2: Neo4j Connection

```
Neo4jError: Unable to connect
```
**Fix:** Check NEO4J_URI env var, verify credentials

### Pattern 3: Cold Start Timeout

```
Request timeout after 60s
```
**Fix:** Increase timeout, optimize startup

### Pattern 4: Memory Pressure

```
Container killed due to memory
```
**Fix:** Increase memory limit, optimize usage

---

## Report Template

```markdown
## Log Analysis Report

**Service**: nikita-api
**Region**: us-central1
**Period**: [timestamp range]

### Error Summary

| Error Type | Count | Severity |
|------------|-------|----------|
| OpenAI errors | X | HIGH/LOW |
| DB errors | X | HIGH/LOW |
| Auth errors | X | HIGH/LOW |

### Performance Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Avg response time | Xms | ✅/⚠️ |
| Error rate | X% | ✅/⚠️ |
| Cold starts | X | ✅/⚠️ |

### Key Events

1. [timestamp] - [event description]
2. [timestamp] - [event description]

### Recommendations

- [Action items]
```

---

## Checklist

- [ ] No unhandled exceptions
- [ ] No 500 errors
- [ ] LLM timing acceptable (<5s)
- [ ] Memory operations working
- [ ] No quota errors
- [ ] No auth failures
- [ ] Performance acceptable
