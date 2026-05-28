---
name: observability-review
description: Evaluate logging coverage, error tracking, debugging capabilities, and monitoring patterns. Use when investigating production issues becomes difficult, after incidents, or when expanding monitoring coverage.
---

# Observability Review

Assess the ability to understand, debug, and monitor the application in production.

## Scope

### 1. Logging Coverage (per AGENTS.md)
- Structured logs with context (user id, request id)
- Sensitive data redacted before logging
- Appropriate log levels (error, warn, info, debug)
- Server actions logging mutations
- No excessive logging impacting performance

### 2. Error Tracking (Sentry)
- Sentry configured per AGENTS.md
- Performance traces for slow APIs
- Breadcrumb data for client errors
- Error boundaries on critical routes
- Source maps uploaded for stack traces
- User context attached to errors

### 3. Analytics (PostHog)
- Event tracking via `lib/posthog/client.ts` (client) and `lib/posthog/server.ts` (server)
- Feature flags with UPPERCASE_WITH_UNDERSCORE naming
- Custom properties in enums/const objects when reused
- No API key hallucination (use `.env` values)
- Key user actions tracked

### 4. Activity System (per CLAUDE.md)
- Activity logging via `lib/activity/events/`
- Domain-specific handlers (tasks, projects, clients, etc.)
- Overview cache (`activity_overview_cache`) maintained
- Audit trail for compliance

### 5. Health Monitoring
- API endpoint health checks
- Database connection monitoring
- External service health (Supabase, Resend)
- Queue processing status (Supabase Queues)

### 6. Debugging Capabilities
- Can reproduce issues from error reports?
- Request tracing from client to database?
- State inspection available?
- Time-based correlation possible?

### 7. Alerting Readiness
- Critical errors trigger notifications?
- Performance degradation detectable?
- Failed background jobs visible?
- Security events flagged?

## Observability Gaps Analysis

For each area, identify:
- What we CAN see today
- What we CANNOT see
- Impact of blind spots
- Recommended additions

## Output Format

```
[PILLAR: LOGGING|ERRORS|METRICS|TRACES|ANALYTICS]
[PRIORITY: CRITICAL|HIGH|MEDIUM|LOW]
Area: What's being assessed
Current State: What exists
Gap: What's missing
Impact: How this affects debugging/monitoring
Recommendation: What to add
Effort: LOW|MEDIUM|HIGH
```

## Actions

1. Inventory current logging statements
2. Review Sentry configuration and coverage
3. Audit PostHog event tracking
4. Check activity logging completeness
5. Identify production debugging pain points

## Observability Patterns (from AGENTS.md)

```typescript
// Structured logging with context
console.log(JSON.stringify({
  level: 'info',
  action: 'task_created',
  userId: user.id,
  taskId: task.id,
  timestamp: new Date().toISOString()
}))

// Activity event logging
import { logTaskCreated } from '@/lib/activity/events/tasks'
await logTaskCreated(taskId, userId)

// PostHog server-side tracking
import { posthogServer } from '@/lib/posthog/server'
posthogServer.capture({
  distinctId: userId,
  event: 'task_completed',
  properties: { taskId, projectId }
})
```

## Key Questions

1. **When a user reports a bug**: Can we find their session and see what happened?
2. **When an API is slow**: Can we identify the bottleneck?
3. **When data looks wrong**: Can we trace how it got that way?
4. **When a deploy breaks something**: Can we correlate timing with errors?
5. **When we need usage patterns**: Can we answer product questions?

## Post-Review

Generate:
- Observability coverage map
- Blind spot inventory
- Recommended instrumentation additions
- Alerting rule suggestions
- Dashboard recommendations for Sentry/PostHog
