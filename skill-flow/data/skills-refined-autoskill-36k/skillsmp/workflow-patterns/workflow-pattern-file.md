---
name: workflow-pattern-file
description: "File processing workflow patterns (CSV, JSON, PDF, batch). Use when asking 'file processing', 'batch file', 'document workflow', or 'file automation'."
---

# File Processing Workflow Patterns

Patterns for automated file processing, transformation, and batch operations.

> **Skill Metadata**
> Category: `workflow-patterns`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`
> Related Skills: [`nodes-data-reference`](../nodes/nodes-data-reference.md), [`workflow-pattern-etl`](workflow-pattern-etl.md)
> Related Subagents: `pattern-expert` (file workflows)

## Quick Reference

File processing patterns:
- **Batch file processing** - Process multiple files
- **File transformation** - Convert formats
- **Document extraction** - PDF, DOCX to text
- **Archive management** - ZIP, unzip, organize

## Pattern 1: Batch CSV Processing

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

workflow = WorkflowBuilder()

# 1. List CSV files
workflow.add_node("FileListNode", "list_files", {
    "directory": "data/input",
    "pattern": "*.csv"
})

# 2. Process each file
workflow.add_node("MapNode", "process_files", {
    "input": "{{list_files.files}}",
    "workflow": "process_single_csv"
})

# 3. Merge results
workflow.add_node("MergeNode", "merge_results", {
    "inputs": "{{process_files.results}}",
    "strategy": "combine"
})

# 4. Write consolidated output
workflow.add_node("CSVWriterNode", "write_output", {
    "file_path": "data/output/consolidated.csv",
    "data": "{{merge_results.combined}}",
    "headers": ["id", "name", "value"]
})

workflow.add_connection("list_files", "process_files")
workflow.add_connection("process_files", "merge_results")
workflow.add_connection("merge_results", "write_output")

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Pattern 2: PDF Document Extraction

```python
workflow = WorkflowBuilder()

# 1. Read PDF document
workflow.add_node("DocumentProcessorNode", "extract_pdf", {
    "file_path": "{{input.pdf_path}}",
    "extract_metadata": True,
    "preserve_structure": True,
    "page_numbers": True
})

# 2. Extract tables
workflow.add_node("TransformNode", "extract_tables", {
    "input": "{{extract_pdf.content}}",
    "transformation": "extract_tables()"
})

# 3. Extract text
workflow.add_node("TransformNode", "extract_text", {
    "input": "{{extract_pdf.content}}",
    "transformation": "extract_text()"
})

# 4. Analyze with AI
workflow.add_node("LLMNode", "analyze_document", {
    "provider": "openai",
    "model": "gpt-4",
    "prompt": "Summarize this document: {{extract_text.text}}"
})

# 5. Save results
workflow.add_node("JSONWriterNode", "save_results", {
    "file_path": "output/{{input.pdf_name}}_analysis.json",
    "data": {
        "metadata": "{{extract_pdf.metadata}}",
        "tables": "{{extract_tables.tables}}",
        "summary": "{{analyze_document.response}}"
    },
    "indent": 2
})

workflow.add_connection("extract_pdf", "extract_tables")
workflow.add_connection("extract_pdf", "extract_text")
workflow.add_connection("extract_text", "analyze_document")
workflow.add_connection("analyze_document", "save_results")
```

## Pattern 3: File Format Conversion

```python
workflow = WorkflowBuilder()

# 1. Read source file
workflow.add_node("ConditionalNode", "detect_format", {
    "condition": "{{input.file_ext}}",
    "branches": {
        ".csv": "read_csv",
        ".json": "read_json",
        ".xlsx": "read_excel"
    }
})

# 2. Read different formats
workflow.add_node("CSVReaderNode", "read_csv", {
    "file_path": "{{input.file_path}}"
})

workflow.add_node("JSONReaderNode", "read_json", {
    "file_path": "{{input.file_path}}"
})

workflow.add_node("ExcelReaderNode", "read_excel", {
    "file_path": "{{input.file_path}}"
})

# 3. Normalize to common format
workflow.add_node("TransformNode", "normalize", {
    "input": "{{read_csv.data || read_json.data || read_excel.data}}",
    "transformation": "normalize_to_dict_list()"
})

# 4. Write in target format
workflow.add_node("ConditionalNode", "write_format", {
    "condition": "{{input.target_format}}",
    "branches": {
        "csv": "write_csv",
        "json": "write_json",
        "parquet": "write_parquet"
    }
})

workflow.add_connection("detect_format", "normalize")
workflow.add_connection("normalize", "write_format")
```

## Pattern 4: Watch Folder Automation

```python
workflow = WorkflowBuilder()

# 1. Watch directory for new files
workflow.add_node("FileWatchNode", "watch_folder", {
    "directory": "data/inbox",
    "pattern": "*.pdf",
    "event": "created"
})

# 2. Validate file
workflow.add_node("FileValidateNode", "validate", {
    "file_path": "{{watch_folder.file_path}}",
    "min_size": 1024,  # 1KB minimum
    "max_size": 10485760,  # 10MB maximum
    "extensions": [".pdf"]
})

# 3. Process document
workflow.add_node("DocumentProcessorNode", "process", {
    "file_path": "{{validate.file_path}}"
})

# 4. Move to processed folder
workflow.add_node("FileMoveNode", "move_file", {
    "source": "{{validate.file_path}}",
    "destination": "data/processed/{{watch_folder.filename}}"
})

# 5. On error, move to failed folder
workflow.add_node("FileMoveNode", "move_failed", {
    "source": "{{validate.file_path}}",
    "destination": "data/failed/{{watch_folder.filename}}"
})

workflow.add_connection("watch_folder", "validate")
workflow.add_connection("validate", "process")
workflow.add_connection("process", "move_file")
# Error handling connection
workflow.add_error_handler("process", "move_failed")
```

## Best Practices

1. **Error handling** - Move failed files to error folder
2. **File validation** - Check size, format, permissions
3. **Atomic operations** - Write to temp, then move
4. **Progress tracking** - Log processed files
5. **Cleanup** - Delete temp files
6. **Batch size** - Process in manageable chunks

## Common Pitfalls

- **No error handling** - Lost files on failures
- **Memory issues** - Loading large files entirely
- **Race conditions** - Multiple processors on same file
- **Missing validation** - Processing invalid files
- **No cleanup** - Accumulating temp files

## Related Skills

- **Data Nodes**: [`nodes-data-reference`](../nodes/nodes-data-reference.md)
- **ETL Patterns**: [`workflow-pattern-etl`](workflow-pattern-etl.md)

## Documentation

- **File Processing**: [`sdk-users/2-core-concepts/nodes/03-data-nodes.md`](../../../../sdk-users/2-core-concepts/nodes/03-data-nodes.md)

<!-- Trigger Keywords: file processing, batch file, document workflow, file automation, CSV processing, PDF extraction -->
