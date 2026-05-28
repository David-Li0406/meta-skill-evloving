# Structured Output Patterns

## XML Tags

XML tags help organize complex prompts and outputs. Models handle nested tags well.

**Basic structure**:
```xml
<instructions>
Analyze the document and extract key information.
</instructions>

<document>
[content here]
</document>

<output_format>
Return findings in this structure:
<findings>
  <item priority="high|medium|low">description</item>
</findings>
</output_format>
```

**Benefits**:
- Clear separation of prompt sections
- Unambiguous content boundaries
- Easy to parse programmatically
- Models naturally close opened tags

**Common tag patterns**:
```xml
<context>Background information</context>
<task>What to do</task>
<constraints>Limitations and requirements</constraints>
<examples>Input/output pairs</examples>
<input>User-provided content</input>
<output>Expected response format</output>
```

**Nesting for complex structures**:
```xml
<analysis>
  <section name="overview">
    <summary>Brief description</summary>
    <confidence>high|medium|low</confidence>
  </section>
  <section name="details">
    <finding id="1">First finding</finding>
    <finding id="2">Second finding</finding>
  </section>
</analysis>
```

---

## JSON Output

Request JSON when you need programmatic parsing.

**Strict schema specification**:
```
Respond with valid JSON matching this schema:

{
  "summary": "string (1-2 sentences)",
  "items": [
    {
      "name": "string",
      "score": "number (1-10)",
      "issues": ["string"]
    }
  ],
  "recommendation": "string"
}

Return ONLY the JSON, no additional text.
```

**With TypeScript types**:
```
Return JSON matching this TypeScript type:

type Response = {
  status: "success" | "error";
  data: {
    id: string;
    values: number[];
    metadata: Record<string, string>;
  } | null;
  errors?: string[];
}
```

**Tips for reliable JSON**:
- Say "Return ONLY valid JSON" to prevent markdown wrapping
- Provide complete schema with types
- Use examples for complex structures
- Specify whether null/empty values are acceptable

---

## Markdown Output

For human-readable structured output.

**Template pattern**:
```
Format your response using this template:

# [Title]

## Summary
[2-3 sentence overview]

## Key Points
- **Point 1**: [explanation]
- **Point 2**: [explanation]
- **Point 3**: [explanation]

## Details

### [Subtopic 1]
[Content]

### [Subtopic 2]
[Content]

## Conclusion
[Final thoughts and recommendations]
```

**Table output**:
```
Present the comparison as a markdown table:

| Feature | Option A | Option B | Winner |
|---------|----------|----------|--------|
| [name]  | [value]  | [value]  | A/B    |

Include at least 5 comparison points.
```

---

## Code Output

For generating or analyzing code.

**Specify language and format**:
```
Write a Python function that [description].

Requirements:
- Include type hints
- Add docstring with examples
- Handle edge cases: [list them]

Return only the code block, no explanation.
```

**With test cases**:
```
Generate the function and test cases:

```python
# Implementation
def function_name(...):
    ...

# Tests
def test_function_name():
    assert function_name(...) == ...
    assert function_name(...) == ...
```
```

---

## Mixed Formats

Combine formats for complex outputs.

**Analysis with code**:
```xml
<analysis>
  <summary>Brief description of findings</summary>
  <issues>
    <issue severity="high">
      <description>What's wrong</description>
      <location>file:line</location>
      <fix>
        ```python
        # corrected code
        ```
      </fix>
    </issue>
  </issues>
</analysis>
```

**Report with data**:
```
Provide your analysis in this format:

## Executive Summary
[Narrative summary]

## Data
```json
{
  "metrics": {...},
  "trends": [...]
}
```

## Recommendations
[Bulleted list]
```

---

## Handling Ambiguity

When output might vary, provide explicit guidance.

**Optional fields**:
```
{
  "required_field": "always include",
  "optional_field": "include only if applicable, otherwise omit key"
}
```

**Variable length**:
```
Return 3-5 items. Include more only if genuinely distinct.
```

**Uncertainty**:
```
If information is unavailable or uncertain:
- Use null for missing values
- Add "confidence": "low" when inferring
- Explain uncertainty in a separate "notes" field
```
