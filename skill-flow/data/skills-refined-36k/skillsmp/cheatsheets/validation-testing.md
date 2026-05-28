---
name: validation-testing
description: "Validation and testing patterns for production workflows. Use when asking 'validation', 'testing patterns', 'workflow validation', 'production testing', or 'test strategies'."
---

# Validation Testing

Validation Testing guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `production`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Validation Testing
- **Category**: production
- **Priority**: HIGH
- **Trigger Keywords**: validation, testing patterns, workflow validation, production testing

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Validation Testing implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/validation-testing.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **3-Tier Testing Strategy**: Unit tests (node logic), Integration tests (multi-node flows), End-to-end (full workflows)
- **Real Infrastructure Testing**: NO MOCKING policy - test against actual databases, APIs, LLMs for production confidence
- **Cyclic Workflow Testing**: Validate cycle limits, state persistence, termination conditions, memory leaks
- **Error Scenario Testing**: Test retry logic, fallback paths, compensation actions, timeout handling
- **Performance Testing**: Load testing, stress testing, benchmark key workflows under production-like conditions

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

- 💡 **Tip 1**: Follow best practices from documentation
- 💡 **Tip 2**: Test patterns incrementally
- 💡 **Tip 3**: Reference examples for complex cases

## Keywords for Auto-Trigger

<!-- Trigger Keywords: validation, testing patterns, workflow validation, production testing -->
