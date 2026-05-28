---
name: error-analysis-and-resolution
description: Use this skill when you need to systematically analyze and resolve errors in distributed systems, from development to production incidents.
---

# Skill body

## Context

This tool provides systematic error analysis and resolution capabilities for modern applications. You will analyze errors across the full application lifecycle—from local development to production incidents—using industry-standard observability tools, structured logging, distributed tracing, and advanced debugging techniques. Your goal is to identify root causes, implement fixes, establish preventive measures, and build robust error handling that improves system reliability.

## Requirements

Analyze and resolve errors in: `$ARGUMENTS`

The analysis scope may include specific error messages, stack traces, log files, failing services, or general error patterns. Adapt your approach based on the provided context.

## Error Detection and Classification

### Error Taxonomy

Classify errors into these categories to inform your debugging strategy:

**By Severity:**
- **Critical**: System down, data loss, security breach, complete service unavailability
- **High**: Major feature broken, significant user impact, data corruption risk
- **Medium**: Partial feature degradation, workarounds available, performance issues
- **Low**: Minor bugs, cosmetic issues, edge cases with minimal impact

**By Type:**
- **Runtime Errors**: Exceptions, crashes, segmentation faults, null pointer dereferences
- **Logic Errors**: Incorrect behavior, wrong calculations, invalid state transitions
- **Integration Errors**: API failures, network timeouts, external service issues
- **Performance Errors**: Memory leaks, CPU spikes, slow queries, resource exhaustion
- **Configuration Errors**: Missing environment variables, invalid settings, version mismatches
- **Security Errors**: Authentication failures, authorization violations, injection attempts

**By Observability:**
- **Deterministic**: Consistently reproducible with known inputs
- **Intermittent**: Occurs sporadically, often timing or race condition related
- **Environmental**: Only happens in specific environments or configurations
- **Load-dependent**: Appears under specific load conditions