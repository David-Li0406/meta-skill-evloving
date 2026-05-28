---
name: error-missing-build
description: "Fix 'missing .build()' and wrong execution pattern errors in Kailash workflows. Use when encountering 'AttributeError: WorkflowBuilder has no attribute execute', 'execute() missing arguments', 'workflow.execute(runtime)' errors, or asking about correct execution pattern."
---

# Error: Missing .build() Call

Fix the most common Kailash SDK error - forgetting to call `.build()` before executing workflows or using the wrong execution pattern.

> **Skill Metadata**
> Category: `cross-cutting` (error-resolution)
> Priority: `CRITICAL` (Most common SDK error)
> SDK Version: `0.9.0+`
> Related Skills: [`workflow-quickstart`](../../01-core-sdk/workflow-quickstart.md), [`runtime-execution`](../../01-core-sdk/runtime-execution.md)
> Related Subagents: `pattern-expert` (complex debugging)

## The Error

### Common Error Messages
```
AttributeError: 'WorkflowBuilder' object has no attribute 'execute'
TypeError: execute() got an unexpected keyword argument 'runtime'
TypeError: execute() takes 1 positional argument but 2 were given
```

### Root Cause
The workflow is not a built artifact yet - it's still in builder mode. Workflows must be built before execution.

## Quick Fix

### ❌ **WRONG** - Missing .build()
```python
workflow = WorkflowBuilder()
workflow.add_node("CSVReaderNode", "reader", {"file_path": "data.csv"})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow)  # ❌ ERROR!
```

### ✅ **CORRECT** - Always Call .build()
```python
workflow = WorkflowBuilder()
workflow.add_node("CSVReaderNode", "reader", {"file_path": "data.csv"})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())  # ✅ CORRECT
```

## Common Variations of This Error

### Variation 1: Backwards Execution
```python
# ❌ WRONG - workflow doesn't have execute() method
workflow.execute(runtime)  # ERROR!

# ✅ CORRECT - runtime executes workflow
runtime.execute(workflow.build())
```

### Variation 2: Extra Runtime Parameter
```python
# ❌ WRONG - passing runtime twice
runtime.execute(workflow.build(), runtime)  # ERROR!

# ✅ CORRECT - runtime already knows it's the runtime
runtime.execute(workflow.build())
```

### Variation 3: Missing .build() with Parameters
```python
# ❌ WRONG - parameters without .build()
runtime.execute(workflow, parameters={"node": {"param": "value"}})  # ERROR!

# ✅ CORRECT - .build() before parameters
runtime.execute(workflow.build(), parameters={"node": {"param": "value"}})
```

### Variation 4: Storing Workflow Without .build()
```python
# ❌ WRONG - storing unbuild workflow
my_workflow = workflow  # Still a WorkflowBuilder instance
runtime.execute(my_workflow)  # ERROR!

# ✅ CORRECT - build and store
my_workflow = workflow.build()  # Now a Workflow instance
runtime.execute(my_workflow)
```

## Why .build() is Required

### WorkflowBuilder vs Workflow

| WorkflowBuilder | Workflow (after .build()) |
|-----------------|---------------------------|
| Construction phase | Ready for execution |
| Mutable (can add nodes) | Immutable (finalized) |
| No .execute() method | Executable by runtime |
| Validation not yet run | Fully validated |
| Graph not finalized | DAG compiled |

### What .build() Does
1. **Validates** the workflow structure
2. **Compiles** the directed acyclic graph (DAG)
3. **Checks** for cycles (non-cyclic workflows)
4. **Verifies** all connections are valid
5. **Finalizes** the workflow for execution

## Complete Example

### The Wrong Way (All Common Mistakes)
```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

workflow = WorkflowBuilder()
workflow.add_node("CSVReaderNode", "reader", {"file_path": "data.csv"})
workflow.add_node("PythonCodeNode", "processor", {"code": "result = len(data)"})
workflow.add_connection("reader", "data", "processor", "data")

# ❌ All these are WRONG:
runtime = LocalRuntime()
results = runtime.execute(workflow)  # Missing .build()
results = workflow.execute(runtime)  # Wrong direction
results = runtime.execute(workflow.build(), runtime)  # Extra parameter
results = workflow.run()  # No .run() method
```

### The Right Way
```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

workflow = WorkflowBuilder()
workflow.add_node("CSVReaderNode", "reader", {"file_path": "data.csv"})
workflow.add_node("PythonCodeNode", "processor", {"code": "result = len(data)"})
workflow.add_connection("reader", "data", "processor", "data")

# ✅ CORRECT execution pattern
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
#                                            ^^^^^^^^ CRITICAL
```

## Related Patterns

- **Workflow creation**: [`workflow-quickstart`](../../01-core-sdk/workflow-quickstart.md)
- **Runtime options**: [`runtime-execution`](../../01-core-sdk/runtime-execution.md)
- **Other common errors**: [`common-mistakes-catalog`](../../06-cheatsheets/common-mistakes-catalog.md)
- **Parameter errors**: [`error-parameter-validation`](error-parameter-validation.md)
- **Connection errors**: [`error-connection-params`](error-connection-params.md)

## When to Escalate to Subagent

Use `pattern-expert` subagent when:
- Error persists after applying this fix
- Complex workflow with multiple execution patterns
- Need to debug advanced parameter passing
- Dealing with cyclic workflow execution issues

## Documentation References

### Primary Sources
- **Common Mistakes**: [`sdk-users/2-core-concepts/validation/common-mistakes.md` (lines 136-151)](../../../../sdk-users/2-core-concepts/validation/common-mistakes.md#L136-L151)
- **Pattern Expert**: [`.claude/agents/pattern-expert.md` (lines 257-264)](../../../agents/pattern-expert.md#L257-L264)
- **Essential Pattern**: [`CLAUDE.md` (lines 139-141)](../../../../CLAUDE.md#L139-L141)

### Related Documentation
- **Critical Rules**: [`sdk-users/2-core-concepts/validation/critical-rules.md`](../../../../sdk-users/2-core-concepts/validation/critical-rules.md)
- **Workflow Creation Guide**: [`sdk-users/3-development/02-workflows-creation.md`](../../../../sdk-users/3-development/02-workflows-creation.md)

## Quick Diagnostic

Run this mental checklist when you see execution errors:

- [ ] Did I call `.build()` on the workflow?
- [ ] Is the pattern `runtime.execute(workflow.build())`?
- [ ] Am I NOT calling `workflow.execute()`?
- [ ] Am I NOT passing `runtime` as a parameter?
- [ ] Did I assign the built workflow to a variable if reusing?

## Prevention Tips

- 💡 **Muscle memory**: Always type `workflow.build()` together
- 💡 **Code review**: Search for `.execute(workflow)` in your code - should never appear
- 💡 **IDE snippets**: Create a snippet for `runtime.execute(workflow.build())`
- 💡 **Remember the rule**: **Runtime executes workflow**, not the other way around
- 💡 **Think "compile"**: `.build()` is like compiling - do it before running

## Version Notes

- **v0.9.0+**: `.build()` became mandatory (previously optional in some cases)
- **v0.8.0+**: WorkflowBuilder clearly separated from Workflow class
- **All versions**: This pattern has always been the recommended approach

<!-- Trigger Keywords: missing .build, AttributeError: WorkflowBuilder, execute error, workflow.execute(runtime), runtime.execute without build, forgot to build, build() missing, execution pattern error, workflow execution error, cannot execute workflow -->
