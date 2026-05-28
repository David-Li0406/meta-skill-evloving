---
name: agrag-llm-judge
description: Run headless AgRAG prompts in a shared thread and produce an LLM-as-judge evaluation report. Use for evaluating retrieval quality, grounding, graph paths, and tool usage of the agrag agent in headless mode, especially when you need a consistent context window via --thread-id.
---

# AgRAG LLM Judge

## Overview
Run a short evaluation session against the AgRAG agent in headless mode, capture a transcript, then judge the responses with a structured rubric.

## Workflow

### 1) Choose session inputs
- Pick a thread id and 5-10 prompts.
- Use `references/query-templates.md` for prompts.
- Include at least one negative query.
- Do not run the synthetic generator; use the existing DB state.

### 2) Run headless prompts in a shared thread
Use a single thread id for all prompts so the context stays consistent.

Single prompt:
```bash
poetry run agrag -p "<prompt>" --thread-id <id> --output-format json
```

Batch helper:
```bash
./.codex/skills/agrag-llm-judge/scripts/run_headless_batch.sh <id> prompts.txt out.jsonl
```

### 3) Optional tool audit
Re-run a subset with stream-json to inspect tool calls and results:
```bash
poetry run agrag -p "<prompt>" --thread-id <id> --output-format stream-json
```
Look for missing `tool_result` events or repeated tool calls.

### 4) Detect issues + propose fixes
Run the diagnostics script to identify issues and recommended fixes:
```bash
python .codex/skills/agrag-llm-judge/scripts/diagnose_headless_output.py <output_file>
```
If issues are detected, summarize them and propose fixes, then **wait for user confirmation** before applying any changes.

### 5) Build the transcript
Create a simple Q/A transcript from the outputs:
- User prompt
- Assistant response
- Any cited evidence snippets
- Any graph paths

### 6) LLM-as-judge evaluation
Score each response and summarize issues with fixes.

## Rubric (1-10 each)
- Accuracy: statements match retrieved evidence.
- Relevance: answers the asked entity type and question.
- Groundedness: evidence cites entity IDs; avoid tool-only citations unless no IDs exist.
- Graph path validity: only uses relationship labels returned by `graph_traverse`.
- Tool efficiency: minimal calls, no redundant searches.

## Common failure modes + fixes
- Wrong entity type in results: use "Ranked Results" with entity type tags.
- Invented relationship labels: ensure `graph_traverse` outputs relationship types and only cite those.
- Evidence cites tool names not IDs: format tool outputs with explicit `Entity ID` lines and cite them.

## Resources
- `references/query-templates.md`
- `scripts/run_headless_batch.sh`
- `scripts/diagnose_headless_output.py`
