---
name: generate-prd-entry
description: Generate a single PRD JSON entry from a plain-English feature idea and append it to ralph/prd.json. Use when asked to convert feature ideas into this project's PRD schema, produce a JSON object with id/title/priority/description/acceptanceCriteria/passes, and update the PRD file.
---

# Generate Prd Entry

## Overview

Turn a feature idea into a single PRD JSON object matching the project's schema, then append it to `ralph/prd.json` while keeping the file valid JSON.

## Workflow

1. Read the feature idea and extract the core problem, goal, and expected behavior.
2. Open `ralph/prd.json` and determine its structure (single object vs array). Append the new entry in a way that preserves valid JSON.
3. Emit only the JSON object in the response and ensure the file update matches it.

## Output Requirements

Return a single JSON object that matches:

```json
{
  "id": "<lowercase_dash_id>",
  "title": "<short descriptive title>",
  "priority": <integer 1-99>,
  "description": "<summarized problem and goal>",
  "acceptanceCriteria": [
    "<criterion 1>",
    "<criterion 2>"
  ],
  "passes": false
}
```

Constraints:
- Use a concise lowercase `id` with words separated by dashes.
- Pick `priority` 1-99 based on urgency implied in the idea.
- Summarize goals/behavior in `description` (one sentence is usually enough).
- Provide 2-4 objective, testable acceptance criteria.
- Set `passes` to `false`.
- Do not wrap the object in an array; emit only the object text.
- Update `ralph/prd.json` by appending this object in the existing structure (array or other) and keep JSON valid.

## Quality Checklist

Before responding:
- Confirm the JSON object is valid and fields match the schema.
- Ensure acceptance criteria are measurable and not vague.
- Keep text concise and ASCII-only.
