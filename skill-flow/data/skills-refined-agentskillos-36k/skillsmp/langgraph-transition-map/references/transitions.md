# LangGraph State Transition Map

This document defines the valid state transitions for the RoleSense agentic workflows.

## State Schema

The global state includes:
*   `resume_text`: Initial parsed text
*   `tailored_content`: Generated bullet points
*   `matches`: Keyword matches
*   `score`: Current match score

## Transitions

### Parser Workflow

1.  **START** -> `detect_format`
2.  `detect_format` ->
    *   If PDF: `extract_pdf`
    *   If DOCX: `extract_docx`
    *   If TXT: `read_text`
3.  `extract_*` -> `llm_parse`
4.  `llm_parse` -> `validate_schema`
5.  `validate_schema` ->
    *   If Valid: **END**
    *   If Invalid: `retry_parse` or **FAIL**

### Main Pipeline

1.  **START** -> `ParserAgent`
2.  `ParserAgent` -> `ScorerAgent`
3.  `ScorerAgent` ->
    *   If Score < Threshold: `TailorAgent`
    *   If Score >= Threshold: `ExporterAgent`
4.  `TailorAgent` -> `ScorerAgent` (Re-score)
5.  `ExporterAgent` -> **END**
