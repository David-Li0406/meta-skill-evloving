---
name: llm-parse-resume
description: Extract structured fields using LLM (via Ollama). Converts raw resume text into a standardized JSON structure with fields for contact info, skills, experience, and education.
---

# LLM Parse Resume

## Overview

This skill utilizes a large language model (via Ollama) to parse unstructured resume text into a structured JSON schema. It is more robust than regex-based parsers for varying layouts.

## Prerequisites

*   Ollama running locally.
*   `requests` library.

## Usage

### Parser Script

**Syntax:**

```bash
python3 .agent/skills/llm-parse-resume/scripts/parse_resume.py <resume.txt> [--model model_name]
```

**Output:**
JSON object adhering to the schema.

**Example:**

```bash
python3 .agent/skills/llm-parse-resume/scripts/parse_resume.py raw_resume.txt > resume.json
```
