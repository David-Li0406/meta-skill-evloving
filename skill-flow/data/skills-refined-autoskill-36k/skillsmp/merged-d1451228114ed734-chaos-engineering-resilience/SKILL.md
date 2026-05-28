---
name: chaos-engineering-resilience
description: Use this skill for chaos engineering and resilience testing, including fault injection, load testing, and system recovery validation in distributed systems.
---

# Chaos Engineering & Resilience Testing

## Purpose

Guide the use of chaos engineering principles, controlled failure injection, load/stress testing, resilience validation, and disaster recovery testing.

## Activation

Use this skill when:
- Testing system resilience
- Performing chaos experiments
- Conducting load/stress testing
- Validating disaster recovery
- Testing circuit breakers

## Quick Start

```bash
# Run chaos experiment
aqe chaos run --experiment network-latency --target api-service

# Load test
aqe chaos load --scenario peak-traffic --duration 30m

# Stress test to breaking point
aqe chaos stress --endpoint /api/users --max-users 10000

# Test circuit breaker
aqe chaos circuit-breaker --service payment-service
```

## Chaos Experiment Structure

### Steps for Chaos Engineering
1. DEFINE steady state (normal metrics: error rate, latency, throughput)
2. HYPOTHESIZE system continues in steady state during failure
3. INJECT real-world failures (network, instance, disk, CPU)
4. OBSERVE and measure deviation from steady state
5. FIX weaknesses discovered, document runbooks, repeat

### Quick Chaos Steps
- Start small: Dev → Staging → 1% prod → gradual rollout
- Define clear rollback triggers (e.g., error_rate > 5%)
- Measure blast radius, never exceed planned scope
- Document findings → runbooks → improved resilience

### Critical Success Factors
- Controlled experiments with automatic rollback
- Steady state must be measurable
- Start in non-production, graduate to production

## Chaos Experiments

### 1. Fault Injection

```typescript
await chaosEngineer.injectFault({
  target: 'api-service',
  fault: {
    type: 'latency',
    parameters: {
      delay: '500ms',
      jitter: '100ms',
      percentage: 50
    }
  },
  duration: '5m',
  monitoring: {
    metrics: ['response_time', 'error_rate', 'throughput'],
    alerts: true
  },
  rollback: {
    automatic: true,
    trigger: 'error_rate > 10%'
  }
});
```

### 2. Load Testing

```typescript
await loadTester.execute({
  scenario: 'peak-traffic',
  profile: {
    rampUp: '5m',
    steadyState: '30m',
    rampDown: '5m'
  },
  users: {
    initial: 100,
    target: 5000,
    pattern: 'linear'
  },
  assertions: {
    p95_latency: '<500ms',
    error_rate: '<1%',
    throughput: '>1000rps'
  }
});
```

### 3. Stress Testing

```typescript
await loadTester.stressTest({
  endpoint: '/api/checkout',
  strategy: 'step-increase',
  steps: [100, 500, 1000, 2000, 5000],
  stepDuration: '5m',
  findBreakingPoint: true,
  monitoring: {
    resourceUtilization: true,
    databaseConnections: true,
    memoryUsage: true
  }
});
```

### 4. Resilience Validation

```typescript
await resilienceTester.validate({
  scenarios: [
    'database-failover',
    'cache-failure',
    'external-service-timeout',
    'pod-termination'
  ],
  expectations: {
    gracefulDegradation: true,
    automaticRecovery: true,
    dataIntegrity: true,
    recoveryTime: '<30s'
  }
});
```

## Failure Types to Inject
| Category | Failures | Tools |
|----------|----------|-------|
| **Network** | Latency, packet loss, partition | tc, toxiproxy |
| **Infrastructure** | Instance kill, disk failure, CPU | Chaos Monkey |
| **Application** | Exceptions, slow responses, leaks | Gremlin, LitmusChaos |
| **Dependencies** | Service outage, timeout | WireMock |

## Safety Controls

```yaml
safety:
  blast_radius:
    max_affected_pods: 1
    max_affected_percentage: 10

  abort_conditions:
    - error_rate > 50%
    - p99_latency > 10s
    - service_unavailable

  excluded_environments:
    - production-critical

  required_approvals:
    production: 2
    staging: 0
```

## Coordination

**Primary Agents**: qe-chaos-engineer, qe-load-tester, qe-resilience-tester  
**Coordinator**: qe-chaos-coordinator  

## Remember

**Break things on purpose to prevent unplanned outages.** Find weaknesses before users do. Define steady state, inject failures, measure impact, fix weaknesses, create runbooks. Start small, increase blast radius gradually.

**With Agents:** `qe-chaos-engineer` automates chaos experiments with blast radius control, automatic rollback, and comprehensive resilience validation. Generates runbooks from experiment results.