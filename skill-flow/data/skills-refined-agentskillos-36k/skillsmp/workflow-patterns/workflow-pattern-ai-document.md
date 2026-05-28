---
name: workflow-pattern-ai-document
description: "AI document processing patterns (OCR, extraction, analysis). Use when asking 'AI document', 'document AI', 'OCR workflow', or 'intelligent document processing'."
---

# AI Document Processing Patterns

AI-powered document analysis, extraction, and classification workflows.

> **Skill Metadata**
> Category: `workflow-patterns`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`
> Related Skills: [`workflow-pattern-rag`](workflow-pattern-rag.md), [`nodes-ai-reference`](../nodes/nodes-ai-reference.md)

## Pattern: Invoice Processing with AI

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

workflow = WorkflowBuilder()

# 1. Read document
workflow.add_node("DocumentProcessorNode", "read_invoice", {
    "file_path": "{{input.invoice_path}}"
})

# 2. OCR extraction
workflow.add_node("LLMNode", "extract_fields", {
    "provider": "openai",
    "model": "gpt-4-vision",
    "prompt": "Extract: invoice_number, date, amount, vendor from this invoice",
    "image": "{{read_invoice.content}}"
})

# 3. Validate extracted data
workflow.add_node("DataValidationNode", "validate", {
    "input": "{{extract_fields.data}}",
    "schema": {
        "invoice_number": "string",
        "date": "date",
        "amount": "decimal",
        "vendor": "string"
    }
})

# 4. Store in database
workflow.add_node("DatabaseExecuteNode", "store", {
    "query": "INSERT INTO invoices (number, date, amount, vendor) VALUES (?, ?, ?, ?)",
    "parameters": "{{validate.valid_data}}"
})

workflow.add_connection("read_invoice", "extract_fields")
workflow.add_connection("extract_fields", "validate")
workflow.add_connection("validate", "store")

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Documentation

- **AI Patterns**: [`sdk-users/7-advanced-topics/workflows/ai-patterns.md`](../../../../sdk-users/7-advanced-topics/workflows/ai-patterns.md)

<!-- Trigger Keywords: AI document, document AI, OCR workflow, intelligent document processing, invoice extraction -->
