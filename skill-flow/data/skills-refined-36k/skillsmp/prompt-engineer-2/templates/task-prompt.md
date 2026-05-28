# Task Prompt Template

## Purpose

Template for creating task-specific prompts that accomplish a single, focused objective.

---

## Complete Template

```xml
<task>
{{TASK_DESCRIPTION}}
</task>

<context>
## Relevant Background
{{BACKGROUND_INFO}}

## Input Details
{{INPUT_DESCRIPTION}}

## Expected Output
{{OUTPUT_DESCRIPTION}}
</context>

<instructions>
Complete this task by following these steps:

1. {{STEP_1}}
2. {{STEP_2}}
3. {{STEP_3}}
4. {{STEP_4}}
</instructions>

<format>
Structure your response as follows:

{{OUTPUT_STRUCTURE}}
</format>

<example>
<input>
{{EXAMPLE_INPUT}}
</input>
<output>
{{EXAMPLE_OUTPUT}}
</output>
</example>

<constraints>
- {{CONSTRAINT_1}}
- {{CONSTRAINT_2}}
- {{CONSTRAINT_3}}
</constraints>
```

---

## Task Type Templates

### Analysis Task

```xml
<task>
Analyze {{SUBJECT}} to identify {{OBJECTIVE}}.
</task>

<context>
Focus on: {{FOCUS_AREAS}}
Ignore: {{OUT_OF_SCOPE}}
</context>

<instructions>
1. Review the provided {{INPUT_TYPE}}
2. Identify key patterns related to {{OBJECTIVE}}
3. Document findings with evidence
4. Summarize conclusions
</instructions>

<format>
## Analysis: {{SUBJECT}}

### Key Findings
1. [Finding with evidence]
2. [Finding with evidence]

### Patterns Identified
- [Pattern description]

### Conclusion
[Summary of analysis]

### Evidence
- [Source references]
</format>

<constraints>
- Base findings only on provided input
- Include specific references for each finding
- Do not speculate beyond evidence
</constraints>
```

### Transformation Task

```xml
<task>
Transform {{INPUT_TYPE}} into {{OUTPUT_TYPE}}.
</task>

<context>
Input format: {{INPUT_FORMAT}}
Output format: {{OUTPUT_FORMAT}}
</context>

<instructions>
1. Parse the input {{INPUT_TYPE}}
2. Apply transformation rules:
   - {{RULE_1}}
   - {{RULE_2}}
3. Validate output matches {{OUTPUT_FORMAT}}
4. Return transformed result
</instructions>

<format>
{{OUTPUT_STRUCTURE}}
</format>

<example>
<input>
{{EXAMPLE_INPUT}}
</input>
<output>
{{EXAMPLE_OUTPUT}}
</output>
</example>

<constraints>
- Preserve all original information unless explicitly excluded
- Follow format exactly
- Handle edge cases gracefully
</constraints>
```

### Generation Task

```xml
<task>
Generate {{OUTPUT_TYPE}} based on {{REQUIREMENTS}}.
</task>

<context>
Purpose: {{PURPOSE}}
Audience: {{AUDIENCE}}
Tone: {{TONE}}
</context>

<instructions>
1. Review requirements
2. Plan structure
3. Generate content
4. Validate against requirements
</instructions>

<format>
{{EXPECTED_STRUCTURE}}
</format>

<examples>
<example type="good">
{{GOOD_EXAMPLE}}
</example>
<example type="avoid">
{{ANTI_PATTERN}}
</example>
</examples>

<constraints>
- Length: {{LENGTH_REQUIREMENT}}
- Style: {{STYLE_REQUIREMENTS}}
- Must include: {{REQUIRED_ELEMENTS}}
- Must avoid: {{FORBIDDEN_ELEMENTS}}
</constraints>
```

### Extraction Task

```xml
<task>
Extract {{TARGET_INFO}} from {{SOURCE}}.
</task>

<context>
Source type: {{SOURCE_TYPE}}
Target format: {{TARGET_FORMAT}}
</context>

<instructions>
1. Scan {{SOURCE}} for {{TARGET_INFO}}
2. Validate each extracted item
3. Format according to specification
4. Return complete extraction
</instructions>

<format>
{
  "extracted": [
    {
      "item": "{{ITEM}}",
      "source_location": "{{LOCATION}}",
      "confidence": "HIGH|MEDIUM|LOW"
    }
  ],
  "total_found": {{COUNT}},
  "notes": "{{ANY_ISSUES}}"
}
</format>

<constraints>
- Only extract explicitly present information
- Mark confidence level for each item
- Note any ambiguous cases
</constraints>
```

### Comparison Task

```xml
<task>
Compare {{ITEM_A}} and {{ITEM_B}} on {{CRITERIA}}.
</task>

<context>
Purpose: {{COMPARISON_PURPOSE}}
Key factors: {{IMPORTANT_FACTORS}}
</context>

<instructions>
1. Analyze {{ITEM_A}} on each criterion
2. Analyze {{ITEM_B}} on each criterion
3. Compare side-by-side
4. Provide recommendation
</instructions>

<format>
## Comparison: {{ITEM_A}} vs {{ITEM_B}}

| Criterion | {{ITEM_A}} | {{ITEM_B}} | Winner |
|-----------|------------|------------|--------|
| {{C1}} | [score/notes] | [score/notes] | A/B/Tie |

### Recommendation
[Based on comparison, which is better for {{PURPOSE}}]

### Trade-offs
- If choosing A: [considerations]
- If choosing B: [considerations]
</format>

<constraints>
- Evaluate objectively on stated criteria
- Acknowledge trade-offs
- Provide clear recommendation with reasoning
</constraints>
```

---

## Minimal Task Prompt

For simple, straightforward tasks:

```xml
<task>{{TASK}}</task>
<input>{{INPUT}}</input>
<format>{{FORMAT}}</format>
<constraints>{{KEY_CONSTRAINT}}</constraints>
```

---

## Version

**Version**: 1.0.0
