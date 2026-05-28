---
name: service-debugging-and-circuit-breaking
description: Use this skill for debugging microservices and implementing a circuit breaker to prevent infinite loops and excessive token usage.
---

# Service Debugging and Circuit Breaking Skill

> A combined skill for microservice debugging and circuit breaker functionality.

## Purpose

This skill serves two main functions: 
1. Debugging microservices by analyzing logs, checking service health, and verifying database connections.
2. Implementing a circuit breaker to detect and prevent inefficient operations in the Claude Code environment.

---

## Circuit Breaker Functionality

### Trigger Conditions

| Condition                | Threshold | Action          | Severity  |
|-------------------------|-----------|-----------------|-----------|
| Recursion Depth         | 15 calls  | Force Termination | CRITICAL  |
| Same Error Repeated     | 3 times   | Escalation      | HIGH      |
| Session Time            | 30 minutes| Warning          | MEDIUM    |
| Same File Edit Repeated | 5 times   | Halt            | HIGH      |
| Same Command Repeated    | 5 times   | Warning         | MEDIUM    |

### Action Flow

```
┌─────────────────────────────────────────────┐
│             Start Task                      │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│         Increment Counters (recursion/error/time) │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│              Check Thresholds               │
└─────────────────────────────────────────────┘
                    │
         ┌─────────┴─────────┐
         │                   │
    Normal Range         Exceeded Threshold
         │                   │
         ▼                   ▼
    Continue Task      ┌───────────────┐
                    │ Circuit Breaker │
                    │    Activated    │
                    └───────────────┘
                           │
                           ▼
                    ┌───────────────┐
                    │ User Notification │
                    │ + Confirmation Request │
                    └───────────────┘
```

### Detection Patterns

1. **Recursion Depth Exceeded**
   - **Condition**: Same task called more than 15 times.
   - **Action**: Notify user and request confirmation to continue.

2. **Same Error Repeated**
   - **Condition**: Same error message occurs 3 times.
   - **Action**: Escalate the issue to the user.

3. **Same File Edit Repeated**
   - **Condition**: Same file edited more than 5 times.
   - **Action**: Request user confirmation to continue.

4. **Session Time Exceeded**
   - **Condition**: Session lasts longer than 30 minutes.
   - **Action**: Warn the user about the long session.

---

## Debugging Microservices

### Quick Start

```bash
# Check service health
curl -s http://localhost:{port}/api/health | jq

# Check Docker logs (last 100 lines)
docker logs --tail 100 ms-{service}

# Check PM2 logs
pm2 logs {service} --lines 100
```

### Diagnostic Workflow

#### Phase 1: Service Status Check

```bash
SERVICE_PORT={port}
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" http://localhost:$SERVICE_PORT/api/health)
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -1)
BODY=$(echo "$HEALTH_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
  echo "✅ Health check OK"
  echo "$BODY" | jq
else
  echo "❌ Health check failed (HTTP $HTTP_CODE)"
fi
```

#### Phase 2: Log Collection

- **Docker Environment**:
```bash
docker logs --tail 200 ms-{service} 2>&1
docker logs ms-{service} 2>&1 | grep -i "error\|exception\|fail"
docker logs -f ms-{service}
```

- **PM2 Environment**:
```bash
pm2 status
pm2 logs {service} --lines 200
pm2 logs {service} --err --lines 100
```

#### Phase 3: Database Connection Check

- **PostgreSQL**:
```bash
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "SELECT 1"
```

#### Phase 4: Environment Variable Validation

```bash
REQUIRED_VARS=("DATABASE_URL" "NODE_ENV" "PORT")
for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var}" ]; then
    echo "❌ Missing: $var"
  else
    echo "✅ Set: $var"
  fi
done
```

---

## Output Format

### Diagnostic Result

```markdown
[SEMO] Skill: debug-service 호출 - ms-{service}

=== Service Diagnostic Report ===

## 1. Service Status
| Item       | Status | Details                  |
|------------|--------|--------------------------|
| Health Check | ✅ OK | HTTP 200, response time 45ms |
| Process    | ✅ Running | PID 12345              |
| Port       | ✅ Listening | :3000                  |

## 2. Database
| Item       | Status | Details                  |
|------------|--------|--------------------------|
| PostgreSQL | ✅ Connected | Active connections 5    |

## 3. Recent Error Logs
```
[2025-01-01 10:00:00] ERROR: Connection timeout
```

## 4. Recommended Actions
- ⚠️ DB connection timeout → Check connection pool size.
```

---

## Related Skills

- [health-check](../health-check/SKILL.md) - Development environment validation
- [review](../review/SKILL.md) - Code review

## References

- [Microservices Context](/.claude/memory/microservices.md) - Service list and context