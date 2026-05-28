---
name: env-variables
description: "Manage environment variables for workflows, API keys, and configuration. Use when asking 'environment variables', 'env vars', 'config', 'API keys', 'secrets', 'environment config', or 'env management'."
---

# Environment Variables Configuration

Environment Variables Configuration guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `patterns`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Environment Variables Configuration
- **Category**: patterns
- **Priority**: HIGH
- **Trigger Keywords**: environment variables, env vars, config, API keys, secrets, environment config

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Env Variables implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/env-variables.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **Env-Variables Core Functionality**: Primary operations and common patterns
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
- [`sdk-users/2-core-concepts/cheatsheet/016-environment-variables.md`](../../../sdk-users/2-core-concepts/cheatsheet/016-environment-variables.md)

## Quick Tips

- 💡 **Tip 1**: Always follow Environment Variables Configuration best practices
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference documentation for details

## Keywords for Auto-Trigger

<!-- Trigger Keywords: environment variables, env vars, config, API keys, secrets, environment config -->
