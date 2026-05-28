# Extraction Skill

The Extraction skill extracts structured information from unstructured text. It is the first built-in skill in agent.rs and demonstrates the skills architecture.

## Quick Start

### CLI

```bash
agent extract \
  --text "Contact us at hello@agent.rs" \
  --target "email"
```

Output:
```json
{
  "email": "hello@agent.rs"
}
```

### Browser

```javascript
const result = await agent.invokeSkill('extract', {
  text: 'Contact us at hello@agent.rs',
  target: 'email'
});
console.log(result); // { email: 'hello@agent.rs' }
```

### Edge (Deno)

```typescript
const response = await fetch('/skill/extract', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Contact us at hello@agent.rs',
    target: 'email'
  })
});
const result = await response.json();
```

## Supported Targets

| Target | Description | Example Output |
|--------|-------------|----------------|
| `email` | Email addresses | `{"email": ["user@example.com"]}` |
| `url` | URLs and links | `{"url": ["https://example.com"]}` |
| `date` | Dates (ISO format) | `{"date": "2024-01-15"}` |
| `entity` | Named entities | `{"entity": {"people": [], "organizations": [], "locations": []}}` |
| `name` | Person names | `{"name": ["John Smith", "Jane Doe"]}` |

## Guardrails

This skill enforces strict guardrails:

1. **No Hallucination**: Extracted values must exist in the source text
2. **Schema Validation**: Output must match the expected JSON structure
3. **Type Correctness**: Values must match the target type format

### Failure Examples

```bash
# Invalid target - fails immediately
agent extract --text "hello" --target "phone"
# Error: InvalidTarget - unknown target 'phone'

# Hallucination detected - guardrail rejects
# Input: "Contact us anytime"
# LLM Output: {"email": "contact@example.com"}
# Error: HallucinationDetected - 'contact@example.com' not found in source
```

## Contract

The full skill contract is defined in [SKILL.md](./SKILL.md).

The JSON schema is defined in [schema.json](./schema.json).

## Design Principles

- **Pure**: No I/O, no side effects, deterministic where possible
- **Host-Agnostic**: Same logic runs in CLI, browser, and edge
- **Guarded**: All outputs validated before returning
- **Explicit**: Failures are first-class, never silent
