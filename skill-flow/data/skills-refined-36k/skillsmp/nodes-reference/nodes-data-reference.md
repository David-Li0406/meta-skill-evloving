---
name: nodes-data-reference
description: "Data nodes reference (CSV, JSON, Excel, XML). Use when asking 'CSV node', 'JSON node', 'Excel', 'data nodes', 'file reader', or 'data I/O'."
---

# Data Nodes Reference

Complete reference for file I/O and data processing nodes.

> **Skill Metadata**
> Category: `nodes`
> Priority: `HIGH`
> SDK Version: `0.9.25+`
> Related Skills: [`nodes-database-reference`](nodes-database-reference.md), [`nodes-quick-index`](nodes-quick-index.md)
> Related Subagents: `pattern-expert` (data workflows)

## Quick Reference

```python
from kailash.nodes.data import (
    CSVReaderNode, CSVWriterNode,
    JSONReaderNode, JSONWriterNode,
    TextReaderNode, ExcelReaderNode,
    DocumentProcessorNode  # ⭐ Multi-format support
)
```

## CSV Nodes

### CSVReaderNode
```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()
workflow.add_node("CSVReaderNode", "reader", {
    "file_path": "data/users.csv",
    "delimiter": ",",
    "encoding": "utf-8"
})
```

### CSVWriterNode
```python
workflow.add_node("CSVWriterNode", "writer", {
    "file_path": "output/results.csv",
    "data": [],  # From previous node
    "headers": ["id", "name", "email"]
})
```

## JSON Nodes

### JSONReaderNode
```python
workflow.add_node("JSONReaderNode", "json_reader", {
    "file_path": "config/settings.json",
    "encoding": "utf-8"
})
```

### JSONWriterNode
```python
workflow.add_node("JSONWriterNode", "json_writer", {
    "file_path": "output/data.json",
    "data": {},  # From previous node
    "indent": 2
})
```

## Document Processing

### DocumentProcessorNode ⭐
```python
# Multi-format document processing (PDF, DOCX, MD, HTML, RTF, TXT)
workflow.add_node("DocumentProcessorNode", "doc_processor", {
    "file_path": "documents/report.pdf",
    "extract_metadata": True,
    "preserve_structure": True,
    "page_numbers": True
})
```

**Supported Formats**: PDF, DOCX, Markdown, HTML, RTF, TXT

## Text Nodes

### TextReaderNode
```python
workflow.add_node("TextReaderNode", "text_reader", {
    "file_path": "data/content.txt",
    "encoding": "utf-8"
})
```

## Excel Nodes

### ExcelReaderNode
```python
workflow.add_node("ExcelReaderNode", "excel_reader", {
    "file_path": "data/sales.xlsx",
    "sheet_name": "Q4_2024"
})
```

## Related Skills

- **Database Nodes**: [`nodes-database-reference`](nodes-database-reference.md)
- **Transform Nodes**: [`nodes-transform-reference`](nodes-transform-reference.md)
- **Node Index**: [`nodes-quick-index`](nodes-quick-index.md)

## Documentation

- **Data Nodes**: [`sdk-users/2-core-concepts/nodes/03-data-nodes.md`](../../../../sdk-users/2-core-concepts/nodes/03-data-nodes.md)

<!-- Trigger Keywords: CSV node, JSON node, Excel, data nodes, file reader, data I/O, CSVReaderNode, JSONReaderNode -->
