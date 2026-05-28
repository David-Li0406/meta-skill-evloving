---
name: observability-and-troubleshooting
description: Use this skill when you need to add or improve observability through logs, metrics, traces, and alerts, as well as troubleshoot production or performance issues.
---

# Observability and Troubleshooting Skill

## Core Principle

**Measure what matters, alert on what's actionable.**

Effective observability is about collecting the right data to understand system health, debug issues quickly, and make informed decisions. Focus on actionable alerts rather than every fluctuation.

---

## When to Use

Use this skill when:
- Setting up monitoring for new applications or services
- Debugging production issues or incidents
- Performing performance optimization
- Defining SLAs, SLOs, and error budgets
- Responding to incidents
- Establishing alerting strategies
- Implementing distributed tracing
- Creating dashboards for system observability
- Analyzing system performance and reliability
- Planning capacity and scaling decisions
- Diagnosing incidents or instrumenting critical paths

---

## The Three Pillars of Observability

Modern observability is built on three complementary pillars:

```
┌─────────────────────────────────────────────┐
│           OBSERVABILITY                      │
├─────────────┬──────────────┬────────────────┤
│   METRICS   │     LOGS     │    TRACES      │
├─────────────┼──────────────┼────────────────┤
│ What is     │ What         │ Where is       │
│ happening?  │ happened?    │ the problem?   │
│             │              │                │
│ Time-series │ Event        │ Request flow   │
│ data        │ records      │ through system │
│             │              │                │
│ Aggregated  │ Detailed     │ Distributed    │
│ numbers     │ context      │ context        │
└─────────────┴──────────────┴────────────────┘
```

### 1. Metrics: What is Happening?

**Time-series numerical data aggregated over time.**

**Examples:**
- Request rate (requests per second)
- Error rate (percentage)
- Response time (milliseconds, percentiles)
- CPU usage (percentage)
- Memory usage (bytes)
- Queue depth (items)

**Characteristics:**
- Cheap to collect and store
- Efficient for alerting
- Good for dashboards and trends
- Limited context (numbers only)

**When to Use:**
- Real-time monitoring
- Alerting on thresholds
- Capacity planning
- Performance trending

---

### 2. Logs: What Happened?

**Timestamped event records with contextual information.**

**Examples:**
```json
{
  "timestamp": "2025-01-10T14:32:15Z",
  "level": "ERROR",
  "service": "payment-service",
  "trace_id": "abc123",
  "user_id": "user_456",
  "message": "Payment processing failed",
  "error": "Gateway timeout",
  "amount": 99.99,
  "currency": "USD"
}
```

**Characteristics:**
- Rich contextual information
- Event-by-event detail
- Expensive to store at scale
- Powerful for debugging

**When to Use:**
- Debugging specific issues
- Audit trails
- Understanding event sequences
- Post-mortem analysis

---

### 3. Traces: Where is the Problem?

**Request flow tracking across distributed systems.**

```
User Request → API Gateway → Auth Service → User Service → Database
                    ↓
              Payment Service → Payment Gateway
                    ↓
              Email Service → Email Provider
```

**Example Trace:**
```
Trace ID: abc123
Total Duration: 450ms

Span 1: API Gateway        [0-450ms]   ████████████████████
Span 2: Auth Service       [10-30ms]   ██
Span 3: User Service       [35-100ms]  ██████
Span 4: Database Query     [40-95ms]   █████
Span 5: Payment Service    [105-400ms] ████████████████  ← SLOW!
Span 6: Payment Gateway    [120-390ms] ███████████████
Span 7: Email Service      [405-440ms] ███
```

**Characteristics:**
- Shows request path through services
- Identifies bottlenecks visually
- Requires instrumentation
- Can be expensive at scale

**When to Use:**
- Debugging latency issues
- Understanding microservice interactions
- Optimizing distributed systems
- Identifying performance bottlenecks

---

## The Four Golden Signals

**Google's SRE framework for monitoring any system.**

### 1. Latency

**How long does it take to service a request?**

**Key Metrics:**
- Median response time (p50)
- 95th percentile (p95)
- 99th percentile (p99)
- 99.9th percentile (p999)

### 2. Traffic

**How much demand is being placed on the system?**

**Key Metrics:**
- Requests per second (RPS)
- Transactions per second (TPS)
- Concurrent users
- Data throughput (bytes/sec)

### 3. Errors

**What is the rate of failing requests?**

**Key Metrics:**
- Error rate (percentage)
- HTTP 5xx errors
- HTTP 4xx errors (client errors)
- Exception rate
- Failed transactions

### 4. Saturation

**How full is the service?**

**Key Metrics:**
- CPU utilization (%)
- Memory utilization (%)
- Disk I/O usage
- Network bandwidth
- Connection pool usage
- Queue depth

---

## Alerting Strategy

### Alert Fatigue: The Silent Killer

**Bad Alerting:**
```
3:00 AM: Disk usage 71% ⚠️
3:15 AM: Memory usage 82% ⚠️
3:30 AM: CPU spike to 90% for 10 seconds ⚠️
3:45 AM: Database connection pool 70% full ⚠️
4:00 AM: Disk usage 72% ⚠️
```

**Good Alerting:**
```
3:00 AM: [CRITICAL] Error rate 15% for 10 minutes - users affected!
```

---

## SLIs, SLOs, and SLAs

### Service Level Indicator (SLI)

**A metric that measures service quality.**

### Service Level Objective (SLO)

**Target value or range for an SLI.**

### Service Level Agreement (SLA)

**Contract with users about service levels, often with consequences.**

---

## Monitoring Best Practices

### 1. Instrument Early

**Add monitoring from day one, not after issues arise.**

### 2. Use Structured Logging

**Structured logging (JSON) is easier to parse, query, and alert on.**

### 3. Include Trace IDs Everywhere

**Connect metrics, logs, and traces using trace ID for effective debugging.**

---

## Quick Reference

### Metrics to Monitor Checklist

**Application:**
- [ ] Request rate (requests/sec)
- [ ] Error rate (%)
- [ ] Response time (p50, p95, p99)

**Infrastructure:**
- [ ] CPU usage (%)
- [ ] Memory usage (%)
- [ ] Disk usage (%)

**Dependencies:**
- [ ] Database query time
- [ ] External API response time

**Business:**
- [ ] User signups
- [ ] Successful transactions

---

**Remember:** Good monitoring is invisible when everything works, but invaluable when things break. Instrument early, alert sparingly, and always connect metrics to user impact. Measure what matters, not just what's easy to measure.