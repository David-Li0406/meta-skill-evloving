---
name: directoryreader-patterns
description: "DirectoryReader node patterns for file discovery. Use when asking 'directory reader', 'file discovery', 'read directories', 'scan folders', or 'file patterns'."
---

# Directoryreader Patterns

Directoryreader Patterns guide with patterns, examples, and best practices.

> **Skill Metadata**
> Category: `advanced`
> Priority: `HIGH`
> SDK Version: `0.9.25+`

## Quick Reference

- **Primary Use**: Directoryreader Patterns
- **Category**: advanced
- **Priority**: HIGH
- **Trigger Keywords**: directory reader, file discovery, read directories, scan folders

## Core Pattern

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Directoryreader Patterns implementation
workflow = WorkflowBuilder()

# See source documentation for specific node types and parameters
# Reference: sdk-users/2-core-concepts/cheatsheet/directoryreader-patterns.md

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```


## Common Use Cases

- **File Discovery & Processing**: Recursively scan directories with glob patterns, filter by extension/size/date, process matching files
- **Data Pipeline Ingestion**: Batch process CSV/JSON/XML files from input directories, handle incremental updates
- **Document Processing**: Scan document folders, extract text/metadata, feed to LLM agents for analysis
- **Log File Analysis**: Monitor log directories, process new files, extract patterns, aggregate metrics
- **Media File Management**: Scan media folders, read metadata (EXIF, ID3), organize/transcode based on properties

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

- 💡 **Use Glob Patterns**: Specify patterns like `**/*.csv` or `logs/**/*.log` for flexible file matching
- 💡 **Filter by Metadata**: Use file_size_min/max, modified_after/before to process only relevant files
- 💡 **Handle Large Directories**: Enable pagination with max_files to avoid memory issues in folders with 1000s of files
- 💡 **Combine with PythonCodeNode**: Read directory list, then process each file conditionally based on content
- 💡 **Recursive vs Flat**: Set recursive=True for deep scans, False for single-level directory listing

## Keywords for Auto-Trigger

<!-- Trigger Keywords: directory reader, file discovery, read directories, scan folders -->
