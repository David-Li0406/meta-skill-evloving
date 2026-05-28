---
name: production-patterns
description: "Production workflow patterns and best practices. Use when asking 'production patterns', 'production workflows', 'production best practices', 'deployment patterns', or 'production guide'."
---

# Production Patterns

Production Patterns for production-ready workflows.

> **Skill Metadata**
> Category: `quick-reference`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Production Patterns
- **Category**: quick-reference
- **Priority**: HIGH
- **Trigger Keywords**: production patterns, production workflows, production best practices

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Production Patterns implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/production-patterns.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Enterprise Deployment Patterns**: Production-ready workflows with health checks, circuit breakers, retry logic, monitoring
- **High Availability Design**: Multi-instance deployments, load balancing, failover strategies, state persistence
- **Performance Optimization**: Connection pooling, caching strategies, batch operations, async execution patterns
- **Security Implementation**: Authentication, authorization, secrets management, input validation, audit logging
- **Operational Excellence**: Structured logging, metrics collection, alerting, error tracking, performance monitoring

## Related Patterns

- **For fundamentals**: See [`workflow-quickstart`](#)
- **For patterns**: See [`workflow-patterns-library`](#)
- **For parameters**: See [`param-passing-quick`](#)

## When to Escalate to Subagent

Use specialized subagents when:
- **pattern-expert**: Complex patterns, multi-node workflows
- **sdk-navigator**: Error resolution, parameter issues
- **testing-specialist**: Comprehensive testing strategies

## Documentation References

### Primary Sources
- [`sdk-users/2-core-concepts/cheatsheet/`](../../../sdk-users/2-core-concepts/cheatsheet/)

## Quick Tips

- 💡 **Use AsyncLocalRuntime for Docker**: WorkflowAPI defaults to AsyncLocalRuntime - 10-100x faster, no thread hanging issues
- 💡 **Implement Health Checks**: Add HealthCheckNode with database/API connectivity checks for load balancer monitoring
- 💡 **Enable Circuit Breakers**: Protect external dependencies with circuit breaker pattern to prevent cascade failures
- 💡 **Configure Retry Policies**: Set max_retries, exponential_backoff, jitter for transient failures
- 💡 **Monitor with Metrics**: Use TransactionMetricsNode to track latency, throughput, error rates in production

## Keywords for Auto-Trigger

<!-- Trigger Keywords: production patterns, production workflows, production best practices -->
