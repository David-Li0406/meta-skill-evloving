---
name: gemini-pdf-analyzer
description: Analyzes PDFs and images using Gemini 2.5 Flash via OpenRouter. Use when asked to extract info, ask questions about, or analyze large PDFs or images agentically.
---

# Gemini PDF Analyzer

Analyze PDFs and images using Google's Gemini 3 Flash model via OpenRouter API.

## Usage

Run the analyzer script with a prompt and one or more PDF/image files:

```bash
bun run .agents/skills/gemini-pdf-analyzer/scripts/analyze.ts "Your question here" path/to/file1.pdf path/to/file2.png
```

## Environment

Requires `OPENROUTER_API_KEY` environment variable.

## Capabilities

- Extract text and tables from PDFs
- Answer questions about document content
- Analyze images and diagrams
- Compare multiple documents
- Process large PDFs by sending them directly to Gemini's vision capabilities

## Examples

**Ask about a PDF:**
```bash
bun run .agents/skills/gemini-pdf-analyzer/scripts/analyze.ts "What are the main findings in this report?" report.pdf
```

**Analyze multiple files:**
```bash
bun run .agents/skills/gemini-pdf-analyzer/scripts/analyze.ts "Compare these two documents" doc1.pdf doc2.pdf
```

**Extract structured data:**
```bash
bun run .agents/skills/gemini-pdf-analyzer/scripts/analyze.ts "Extract all tables as JSON" data.pdf
```

## Agentic Workflow

For complex multi-page PDFs, use iteratively:
1. First ask for a summary/overview
2. Then drill down into specific sections
3. Extract structured data as needed
