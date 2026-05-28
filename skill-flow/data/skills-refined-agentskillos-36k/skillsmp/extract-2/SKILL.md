---
name: extract
description: Extract structured information (email, url, date, entity) from unstructured text with schema + anti-hallucination guardrails.
license: MIT OR Apache-2.0
compatibility: Native (CLI, llama.cpp), Browser (WebLLM), Edge (Deno HTTP LLM)
metadata:
  targets: ["email", "url", "date", "entity", "name"]
  version: "1.0.0"
  guardrails: ["json-schema", "anti-hallucination"]
allowed-tools: ""
---

# Skill: Extraction

## 1. Skill Name

`extract`

## 2. Description

Extract structured information from unstructured text or content. This skill transforms free-form text into validated, structured JSON output.

**Supported extraction targets:**
- `email` - Email addresses
- `url` - URLs and web links
- `date` - Dates in various formats
- `entity` - Named entities (people, organizations, locations)
- `name` - Person names (first name, last name, full name)

## 3. When the Agent Should Use This Skill

The agent MUST invoke this skill when:

1. The user explicitly requests extraction of structured data from text
2. The task requires identifying specific patterns (emails, URLs, dates) in content
3. The user provides unstructured text and asks for specific information types

The agent MUST NOT invoke this skill when:

1. The text is already structured (JSON, CSV, etc.)
2. The user asks for summarization or transformation (not extraction)
3. No specific extraction target is identifiable

## 4. Inputs

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | `string` | Yes | The unstructured text to extract from |
| `target` | `string` | Yes | What to extract: `email`, `url`, `date`, `entity`, or `name` |

### Input Validation Rules

- `text` must be non-empty
- `text` must be at least 1 character
- `target` must be one of the supported types
- Unknown targets cause immediate failure

## 5. Outputs

Output is always JSON with the following structure:

```json
{
  "<target>": <extracted_value>
}
```

### Output by Target Type

| Target | Output Type | Example |
|--------|-------------|---------|
| `email` | `string` or `string[]` | `{"email": "hello@agent.rs"}` |
| `url` | `string` or `string[]` | `{"url": "https://agent.rs"}` |
| `date` | `string` or `string[]` | `{"date": "2024-01-15"}` |
| `entity` | `object` | `{"entity": {"people": ["John"], "orgs": []}}` |
| `name` | `string` or `string[]` | `{"name": ["John Smith", "Jane Doe"]}` |

### Output Guarantees

- Output is always valid JSON
- Output always contains the requested target field
- Empty extractions return empty arrays, not null
- No free-form text in output

## 6. Failure Modes

This skill fails explicitly in these cases:

| Failure | Cause | Agent Behavior |
|---------|-------|----------------|
| `InvalidTarget` | Unknown extraction target | Fail immediately, do not retry |
| `EmptyInput` | Empty text provided | Fail immediately |
| `NoMatch` | No patterns found | Return empty array (not failure) |
| `MalformedOutput` | LLM returned non-JSON | Guardrail rejects, agent may retry |
| `SchemaViolation` | Output missing required fields | Guardrail rejects, agent may retry |

### Failure is First-Class

- All failures are explicit
- No silent empty results
- No hidden retries without policy
- Failures propagate to the host for handling

## 7. Guardrail Expectations

The Extraction skill enforces these guardrails:

### Structural Guardrails

1. **JSON Validity**: Output must parse as valid JSON
2. **Schema Conformance**: Output must contain the target field
3. **Type Correctness**: Field values must match expected types

### Semantic Guardrails

1. **No Hallucination**: Extracted values must appear in input text
2. **No Fabrication**: Cannot invent emails, URLs, or dates not present
3. **Plausibility**: Extracted patterns must match expected formats

### Guardrail Rejection Triggers

```
REJECT if:
  - Output is empty
  - Output is not valid JSON
  - Output missing target field
  - Extracted value not found in source text
  - Value format doesn't match target type
```

## 8. Host Execution Notes

### CLI Host

```bash
# Execution
agent extract --text "Contact: hello@agent.rs" --target "email"

# Success output (stdout)
{"email": "hello@agent.rs"}

# Failure output (stderr) + exit code 1
Error: InvalidTarget - unknown target 'phone'
```

### Browser Host

```javascript
// Execution
const result = await agent.invokeSkill('extract', {
  text: 'Contact: hello@agent.rs',
  target: 'email'
});

// Success
{ email: 'hello@agent.rs' }

// Failure - throws SkillError
SkillError: InvalidTarget - unknown target 'phone'
```

### Edge Host

```typescript
// HTTP Request
POST /skill/extract
Content-Type: application/json
{ "text": "Contact: hello@agent.rs", "target": "email" }

// Success Response (200)
{ "email": "hello@agent.rs" }

// Failure Response (400)
{ "error": "InvalidTarget", "message": "unknown target 'phone'" }
```

## 9. Examples

### Example 1: Email Extraction

**Input:**
```json
{
  "text": "For support, email us at support@agent.rs or sales@agent.rs",
  "target": "email"
}
```

**Output:**
```json
{
  "email": ["support@agent.rs", "sales@agent.rs"]
}
```

### Example 2: URL Extraction

**Input:**
```json
{
  "text": "Visit https://agent.rs or check https://github.com/hwclass/agent.rs",
  "target": "url"
}
```

**Output:**
```json
{
  "url": ["https://agent.rs", "https://github.com/hwclass/agent.rs"]
}
```

### Example 3: Date Extraction

**Input:**
```json
{
  "text": "The meeting is scheduled for January 15, 2024 at 3pm",
  "target": "date"
}
```

**Output:**
```json
{
  "date": "2024-01-15"
}
```

### Example 4: Entity Extraction

**Input:**
```json
{
  "text": "John Smith from Anthropic met with Sarah at Google headquarters",
  "target": "entity"
}
```

**Output:**
```json
{
  "entity": {
    "people": ["John Smith", "Sarah"],
    "organizations": ["Anthropic", "Google"],
    "locations": ["Google headquarters"]
  }
}
```

### Example 5: Name Extraction

**Input:**
```json
{
  "text": "The report was prepared by Dr. Jane Smith and reviewed by Michael Johnson.",
  "target": "name"
}
```

**Output:**
```json
{
  "name": ["Dr. Jane Smith", "Michael Johnson"]
}
```

### Example 6: No Match (Valid Result)

**Input:**
```json
{
  "text": "This text contains no email addresses",
  "target": "email"
}
```

**Output:**
```json
{
  "email": []
}
```

### Example 7: Guardrail Rejection

**Input:**
```json
{
  "text": "Contact us anytime",
  "target": "email"
}
```

**Invalid LLM Output (REJECTED):**
```json
{
  "email": "contact@example.com"
}
```

**Rejection Reason:** `contact@example.com` does not appear in source text - hallucination detected.

---

**Contract Version:** 1.0.0
**Last Updated:** 2024
