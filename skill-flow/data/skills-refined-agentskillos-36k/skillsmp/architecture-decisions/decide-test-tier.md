---
name: decide-test-tier
description: "Choose test tier (unit, integration, e2e) based on scope and dependencies. Use when asking 'test tier', 'unit vs integration', 'test type', 'which test', 'test strategy', or 'test level'."
---

# Decision: Test Tier Selection

Decision: Test Tier Selection guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `cross-cutting`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Decision: Test Tier Selection
- **Category**: cross-cutting
- **Priority**: MEDIUM
- **Trigger Keywords**: test tier, unit vs integration, test type, which test, test strategy

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Decide Test Tier implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/decide-test-tier.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Decide-Test-Tier Core Functionality**: Primary operations and common patterns
- **Integration Patterns**: Connect with other nodes, workflows, external systems
- **Error Handling**: Robust error handling with retries, fallbacks, and logging
- **Performance**: Optimization techniques, caching, batch operations, async execution
- **Production Use**: Enterprise-grade patterns with monitoring, security, and reliability

## Related Patterns

- **For fundamentals**: See [`workflow-quickstart`](#)
- **For connections**: See [`connection-patterns`](#)
- **For parameters**: See [`param-passing-quick`](#)

## When to Escalate to Subagent

Use specialized subagents when:
- Complex implementation needed
- Production deployment required
- Deep analysis necessary
- Enterprise patterns needed

## Documentation References

### Primary Sources
- [`sdk-users/3-development/testing/test-organization-policy.md`](../../../sdk-users/3-development/testing/test-organization-policy.md)

## Quick Tips

- 💡 **Tip 1**: Always follow Decision: Test Tier Selection best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: test tier, unit vs integration, test type, which test, test strategy -->
