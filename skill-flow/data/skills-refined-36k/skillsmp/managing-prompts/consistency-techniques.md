# Consistency Techniques

Advanced patterns for ensuring consistent outputs through prefilling, Structured Outputs, and format enforcement.

## Prefilling Claude's Response

Prefilling allows you to guide Claude's response format by providing the initial text it should continue from. This bypasses preambles and enforces specific structures.

### Basic Prefilling Pattern

**What is prefilling:**
- Include text in the Assistant message before the user input
- Claude continues from where the prefill ends
- Powerful for skipping preambles and enforcing formats

**Implementation:**
```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "What is your favorite color?"},
        {"role": "assistant", "content": "I don't have personal preferences, but if I had to choose, I'd pick"}
    ]
)
```

**Critical constraint:** No trailing whitespace in prefill text. A prefill like "As an AI, " (with space at end) will error.

### Use Cases: When to Prefill

**1. Force JSON Output**
```python
messages = [
    {"role": "user", "content": "Analyze this data: {{DATA}}"},
    {"role": "assistant", "content": "```json\n{\"analysis\": ["}
]
# Claude continues from the JSON structure
```

**2. Skip Preambles**
```python
messages = [
    {"role": "user", "content": "Generate code to sort an array"},
    {"role": "assistant", "content": "```python\n"}
]
# Claude jumps straight to code without explanation
```

**3. Role-Play Character Consistency**
```python
messages = [
    {"role": "user", "content": "Tell me a joke"},
    {"role": "assistant", "content": "[COMEDIAN_PERSONA]"}
]
# Reinforces role even in extended conversations
```

**4. Format Enforcement**
```python
messages = [
    {"role": "user", "content": "Translate: {{TEXT}}"},
    {"role": "assistant", "content": "<spanish>"}
]
# Enforces XML format from first token
```

### Prefilling in Prompts

If using Claude Console or integrated APIs without explicit message control:

```xml
<instructions>
Your task is to analyze the customer feedback below.

Output in exactly this format, starting your response with the opening bracket:

```json
{
  "sentiment": "positive|negative|neutral",
  "topics": [],
  "action_required": boolean
}
```

Begin your response with: ```json
</instructions>
```

### Prefilling Limitations

**Does NOT work with:**
- Extended thinking mode (prefilling incompatible with thinking)
- When you need Claude's internal reasoning first
- Tasks requiring uncertainty acknowledgment (override not ideal)

**Alternative for these cases:**
Use Structured Outputs (see below) for strict JSON schemas instead of prefilling for safety-critical applications.

---

## Structured Outputs (API-Enforced Format Compliance)

Structured Outputs is an API feature that GUARANTEES Claude's response matches your JSON schema. Unlike prompt-based techniques (prefilling, examples), the API enforces structure automatically with 100% compliance.

### What It Is

**Structured Outputs API:**
- Dedicated `response_format` parameter for JSON schema enforcement
- API-level validation ensures exact compliance
- Automatic retry/correction if output doesn't match schema
- No post-processing needed - guaranteed valid JSON

**Key difference from other techniques:**
- Prefilling/examples: Best-effort format guidance (high success but not guaranteed)
- Structured Outputs: API-enforced guarantee (100% compliance or error)

### When to Use Structured Outputs vs Prefilling

**Use Structured Outputs (API) when:**
- Format compliance is critical (no tolerance for deviations)
- Output feeds directly into downstream systems (APIs, databases, code execution)
- JSON parsing errors would break your application
- You need 100% reliability without post-processing validation
- Handling sensitive data where format errors could cause issues

**Use Prefilling when:**
- Flexibility needed (structured but not rigid format)
- Non-JSON formats required (XML, custom markup, prose)
- Creative tasks where exact structure matters less
- Extended thinking needed (incompatible with Structured Outputs)
- Rapid iteration without schema definition overhead

**Avoid Structured Outputs when:**
- Output should be conversational or unstructured text
- Format flexibility is a feature, not a constraint
- Using extended thinking (cannot combine both)

### Implementation: Dedicated Structured Outputs API

**Basic implementation:**
```python
import anthropic

client = anthropic.Anthropic(api_key="...")

response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Analyze this customer feedback and return structured insights: {{FEEDBACK}}"
    }],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "feedback_analysis",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "sentiment": {
                        "type": "string",
                        "enum": ["positive", "negative", "neutral", "mixed"]
                    },
                    "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    },
                    "key_issues": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "action_required": {"type": "boolean"}
                },
                "required": ["sentiment", "confidence", "key_issues", "action_required"],
                "additionalProperties": False
            }
        }
    },
    betas=["structured-outputs-2025-02-19"]
)

# Response is guaranteed to match schema
data = response.content[0].text
import json
result = json.loads(data)  # Will never fail - guaranteed valid
```

**Required beta header:** `"structured-outputs-2025-02-19"`

### JSON Schema Requirements

**Must be valid JSON Schema Draft 7:**
- `type`: Define data types (object, array, string, number, boolean, null)
- `properties`: Define object fields and their schemas
- `required`: List required fields (all fields should typically be required)
- `additionalProperties`: Set to `False` to prevent extra fields
- `enum`: Restrict string values to specific options
- `minimum`/`maximum`: Constrain numeric ranges
- `items`: Define array element schemas

**Strict mode (`strict: True`):**
- Enforces exact schema compliance
- No additional properties allowed
- All required fields must be present
- Type mismatches cause automatic correction

**Example with complex schema:**
```python
response_format={
    "type": "json_schema",
    "json_schema": {
        "name": "entity_extraction",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {
                                "type": "string",
                                "enum": ["PERSON", "ORG", "LOCATION", "DATE", "PRODUCT"]
                            },
                            "confidence": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 1
                            },
                            "context": {"type": "string"}
                        },
                        "required": ["name", "type", "confidence", "context"],
                        "additionalProperties": False
                    }
                },
                "metadata": {
                    "type": "object",
                    "properties": {
                        "source": {"type": "string"},
                        "processed_at": {"type": "string"}
                    },
                    "required": ["source", "processed_at"],
                    "additionalProperties": False
                }
            },
            "required": ["entities", "metadata"],
            "additionalProperties": False
        }
    }
}
```

### Alternative: Tools-Based Structured Outputs

You can also enforce structure using the tools API (older approach, still valid):

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Extract entities from: {{TEXT}}"
    }],
    tools=[{
        "name": "extract_entities",
        "description": "Extract named entities from text",
        "input_schema": {
            "type": "object",
            "properties": {
                "entities": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string"},
                            "confidence": {"type": "number"}
                        },
                        "required": ["name", "type"]
                    }
                }
            },
            "required": ["entities"]
        }
    }],
    tool_choice={"type": "tool", "name": "extract_entities"}
)

# Extract result from tool use
tool_use = response.content[0]
result = tool_use.input  # Validated against schema
```

**Difference:**
- `response_format`: Direct JSON response, simpler extraction
- `tools`: Wrapped in tool use block, requires tool_choice forcing

### Comparison: Structured Outputs vs Prefilling

| Aspect | Structured Outputs (API) | Prefilling (Prompt) |
|--------|-------------------------|---------------------|
| **Format guarantee** | 100% compliance | Best-effort (95-99% typical) |
| **Supported formats** | JSON only | Any format (XML, CSV, custom) |
| **Implementation** | `response_format` API parameter | Prompt technique |
| **Error handling** | Automatic retry/correction | Manual post-processing needed |
| **Validation** | API-level (before response) | Client-side (after response) |
| **Use case** | Strict downstream integration | Flexible creative tasks |
| **Cost** | Standard pricing | Standard pricing |
| **Extended thinking** | Incompatible | Compatible |
| **Complexity** | Requires schema definition | Simple prompt modification |
| **Flexibility** | Rigid (must match schema) | Flexible (approximate match ok) |

### Decision Flow: When to Use Which

```
Need format compliance?
├─ YES → Is output JSON?
│        ├─ YES → Downstream system requires exact structure?
│        │        ├─ YES → Use Structured Outputs API
│        │        │        (100% guarantee, no post-processing)
│        │        └─ NO → Can you handle minor variations?
│        │                 ├─ YES → Use prefilling + examples
│        │                 │        (more flexible, easier iteration)
│        │                 └─ NO → Use Structured Outputs API
│        │
│        └─ NO (XML, CSV, custom) → Use prefilling
│                                    (Structured Outputs only supports JSON)
│
└─ NO → Use basic format specification or no format enforcement
```

### Error Handling and Validation

**Structured Outputs API:**
```python
try:
    response = client.beta.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "..."}],
        response_format={"type": "json_schema", "json_schema": {...}},
        betas=["structured-outputs-2025-02-19"]
    )

    # Guaranteed valid JSON matching schema
    data = json.loads(response.content[0].text)

except anthropic.BadRequestError as e:
    # Schema validation error (malformed schema, not response issue)
    print(f"Schema error: {e}")

except json.JSONDecodeError:
    # Should never happen with Structured Outputs
    # If it does, it's an API bug - report to Anthropic
    pass
```

**With prefilling (manual validation needed):**
```python
response = client.messages.create(...)

try:
    data = json.loads(response.content[0].text)

    # Manual validation required
    if "required_field" not in data:
        # Handle missing field
        pass

    if not isinstance(data.get("count"), int):
        # Handle type mismatch
        pass

except json.JSONDecodeError:
    # Format didn't match expectation - common with prefilling
    # Retry with more explicit instructions or examples
    pass
```

### Pricing and Performance

**Cost:**
- Both Structured Outputs and prefilling have standard pricing
- No additional cost for schema enforcement
- Slight overhead for schema definition (development time)

**Performance:**
- Structured Outputs: Minimal latency impact (API-level validation is fast)
- Prefilling: No latency impact
- Both: Similar token usage (schema definition adds ~50-200 tokens)

### Template-Based Structured Output

```xml
<instructions>
Extract customer feedback and structure it in this exact format:

{
  "customer_id": "string",
  "sentiment": "positive|negative|neutral",
  "categories": ["array of issue categories"],
  "priority": "low|medium|high|critical",
  "resolution_status": "open|in_progress|resolved",
  "action_items": [
    {
      "action": "string",
      "owner": "string",
      "deadline": "YYYY-MM-DD or null"
    }
  ]
}

All fields are required. Do not add extra fields. Use null for missing data, not empty strings.
</instructions>

<feedback>
{{CUSTOMER_FEEDBACK}}
</feedback>
```

### Combining Structured Outputs with Other Techniques

**Structured Outputs + Examples:**
```xml
<instructions>
Extract feedback and output in JSON. Here's an example of the expected format:
</instructions>

<examples>
<example>
<input>
"I loved the new dashboard but the export feature doesn't work on Firefox"
</input>
<output>
{
  "sentiment": "mixed",
  "positive_feedback": ["dashboard redesign"],
  "issues": [{"category": "bug", "description": "export broken on Firefox", "browser": "Firefox"}],
  "priority": "high"
}
</output>
</example>
</examples>

<feedback>
{{NEW_FEEDBACK}}
</feedback>
```

**Structured Outputs + Prefilling (via tool use):**

When using tools-based structured outputs, Claude naturally prefills tool calls, combining both approaches:

```python
# Claude will output tool use with prefilled structure,
# allowing you to guide the format while maintaining schema compliance
messages = [
    {"role": "user", "content": "Extract info from: {{TEXT}}"},
    {"role": "assistant", "content": "[Initial context or format guidance]"}
]
# Then provide tool with structured schema
```

---

## Format Specification Patterns

### XML Format Enforcement

**Simple XML structure:**
```xml
<instructions>
Analyze the report and output in this XML format:

<analysis>
  <executive_summary>[Summary paragraph]</executive_summary>
  <key_findings>
    <finding priority="1|2|3">
      <description>[Finding text]</description>
      <evidence>[Supporting evidence]</evidence>
    </finding>
  </key_findings>
  <recommendations>
    <recommendation priority="1|2|3">[Action text]</recommendation>
  </recommendations>
</analysis>

Do not deviate from this structure. Do not include any text outside the XML tags.
</instructions>
```

**XML with namespaces (for domain-specific):**
```xml
<instructions>
Structure output as healthcare data:

<medical:patient_assessment xmlns:medical="http://healthcare.example.com/medical">
  <medical:patient_id>[ID]</medical:patient_id>
  <medical:assessments>
    <medical:assessment date="YYYY-MM-DD">
      <medical:vital_signs>
        <medical:blood_pressure>[mmHg]</medical:blood_pressure>
        <medical:heart_rate>[bpm]</medical:heart_rate>
      </medical:vital_signs>
    </medical:assessment>
  </medical:assessments>
</medical:patient_assessment>
</instructions>
```

### CSV Format Enforcement

```xml
<instructions>
Output results as valid CSV with headers:

header1,header2,header3,header4
value1,value2,value3,value4
...

Rules:
- Quoted fields containing commas or newlines: "field content"
- No trailing whitespace
- Consistent ordering of columns
- Escape quotes as ""

Process:
1. Output the header row first
2. Output data rows in consistent order
3. Validate CSV formatting
</instructions>
```

### Markdown Format

```xml
<instructions>
Format output as markdown:

# Main Heading

## Section 1
Description with `inline code` where needed.

### Subsection
- Bullet 1
- Bullet 2

## Section 2
Additional content.

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
```

---

## Advanced Consistency Patterns

### Multi-Format Output with Fallback

```xml
<instructions>
Output primary format as JSON. If JSON encoding fails, fallback to XML.

Primary (JSON):
```json
{
  "status": "success|error",
  "data": {...},
  "timestamp": "ISO8601"
}
```

Fallback (XML):
```xml
<response>
  <status>success|error</status>
  <data>...</data>
  <timestamp>ISO8601</timestamp>
</response>
```

Try JSON first. If you encounter any issues with JSON formatting, switch to XML instead.
</instructions>
```

### Conditional Formatting

```xml
<instructions>
Format output based on content type:

IF type=summary:
  Output as single paragraph, max 500 chars

IF type=detailed:
  Output as structured sections with markdown headers

IF type=technical:
  Output as code blocks with language specifiers

IF type=list:
  Output as numbered list with clear hierarchy

For this request: type={{TYPE}}
</instructions>
```

### Format Validation

```xml
<instructions>
Before finalizing, validate your output:

1. Check format: {{REQUIRED_FORMAT}} ✓
2. Check fields: All required fields present ✓
3. Check types: All values match specified types ✓
4. Check constraints: All constraints met ✓
5. Check encoding: No special character issues ✓

If any validation fails, fix the output before responding.
</instructions>
```

---

## Combining Consistency Techniques

### Full Stack Example: High-Consistency Extraction

```xml
<role>
You are a data extraction specialist. Accuracy and consistency are critical.
</role>

<instructions>
Extract information from customer reviews using all consistency techniques:

1. Format Specification (JSON):
```json
{
  "review_id": "string",
  "sentiment": "positive|negative|neutral|mixed",
  "rating": 1|2|3|4|5,
  "topics": ["array of topic tags"],
  "extracted_quotes": ["array of direct quotes"],
  "summary": "string (max 200 chars)"
}
```

2. Examples (3 diverse cases):
- Positive review with feature requests
- Negative review with bugs
- Neutral/mixed review with trade-offs

3. Prefill guidance:
Start response with: ```json\n{

4. Validation before output:
- All fields present (use null if missing)
- Topics match predefined list
- Quotes are exact matches
- Summary under 200 chars
</instructions>

<examples>
<example>
<input>
"Absolutely love the new dashboard! So intuitive. Would be great if we could export to PDF though."
</input>
<output>
{
  "review_id": "review_001",
  "sentiment": "positive",
  "rating": 5,
  "topics": ["UI/UX", "feature_request"],
  "extracted_quotes": [
    "Absolutely love the new dashboard",
    "So intuitive",
    "export to PDF"
  ],
  "summary": "User loves dashboard design but wants PDF export capability"
}
</output>
</example>

<example>
<input>
"The app keeps crashing when I try to upload files. Been like this for weeks. Not good."
</input>
<output>
{
  "review_id": "review_002",
  "sentiment": "negative",
  "rating": 1,
  "topics": ["bug", "file_handling", "stability"],
  "extracted_quotes": [
    "app keeps crashing",
    "when I try to upload files",
    "Been like this for weeks"
  ],
  "summary": "Critical bug: app crashes during file upload for extended period"
}
</output>
</example>
</examples>

<feedback>
{{CUSTOMER_REVIEW}}
</feedback>
```

---

## Performance and Trade-offs

### Consistency vs Flexibility

**Strict Consistency (Prefilling + Structured + Format Spec):**
- Pro: Guaranteed format compliance
- Pro: Easier parsing
- Con: Less flexibility for edge cases
- Con: May reduce output quality slightly
- Best for: Production automation, API integration

**Loose Consistency (Examples + Format Guidance):**
- Pro: Better output quality
- Pro: Handles edge cases better
- Con: Requires parsing/normalization
- Con: Occasional format deviations
- Best for: Human-readable reports, creative tasks

### Token Cost Analysis

**Prefilling cost:** Minimal (just the prefix tokens)

**Structured Outputs cost:** Slight increase for schema definition

**Format Specification cost:** Highest (explicit format definitions use tokens)

**Optimization:** Combine techniques strategically, not all at once.

---

## Quick Reference Decision Tree

```
Need consistent format?
├─ Must be 100% valid JSON/schema?
│  └─ Use Structured Outputs
├─ Skip preamble/intro?
│  └─ Use Prefilling
├─ Need specific markup/XML?
│  └─ Use Format Specification
├─ Multiple similar tasks?
│  └─ Use Examples (3-5 diverse cases)
└─ All of above?
   └─ Layer techniques: Format spec + examples + prefill/structured
```

