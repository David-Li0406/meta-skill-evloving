# Advanced Structured Output with Gemini (2026)

Controlled outputs are the foundation of agentic workflows. By forcing the model to adhere to a JSON Schema, we eliminate non-deterministic parsing and enable seamless integration with traditional software systems.

## 1. The Schema Definition (Pydantic & JSON Schema)

While the SDK provides a `Type` helper, complex nested schemas are best defined using standard JSON Schema objects or Pydantic models (for Python).

### TypeScript Example (Nested Objects & Arrays)
```typescript
const analysisSchema = {
  type: "object",
  properties: {
    overall_sentiment: { type: "string", enum: ["positive", "neutral", "negative"] },
    key_points: {
      type: "array",
      items: {
        type: "object",
        properties: {
          topic: { type: "string" },
          impact_score: { type: "number", minimum: 0, maximum: 10 },
          evidence: { type: "string" }
        },
        required: ["topic", "impact_score"]
      }
    },
    metadata: {
      type: "object",
      properties: {
        processing_version: { type: "string" },
        confidence_threshold: { type: "number" }
      }
    }
  },
  required: ["overall_sentiment", "key_points"]
};
```

## 2. Configuration Best Practices

To ensure the highest adherence to your schema:

1.  **Set MIME Type**: Always set `responseMimeType: "application/json"`.
2.  **Model Choice**: Use `gemini-3-flash` for high-volume extraction or `gemini-3-pro` for complex reasoning over schemas.
3.  **Strict Mode (2026)**: In late 2025, Google introduced "Strict Mode" for schemas, ensuring 100% adherence but requiring all properties to be defined as `required` or having default values.

## 3. Handling Output Length

Structured output often requires more tokens due to JSON overhead. 
- **Optimization**: Use short key names (e.g., `sent` instead of `sentiment`) if token count is a bottleneck.
- **Max Tokens**: Increase `maxOutputTokens` when generating large arrays.

## 4. Validating the Response

Always use a runtime validator like **Zod** (TypeScript) or **Pydantic** (Python) to parse the model's response. This provides a secondary layer of type safety.

```typescript
import { z } from 'zod';

const AnalysisZod = z.object({
  overall_sentiment: z.enum(["positive", "neutral", "negative"]),
  key_points: z.array(z.object({
    topic: z.string(),
    impact_score: z.number()
  }))
});

const rawResponse = JSON.parse(result.response.text());
const validatedData = AnalysisZod.parse(rawResponse);
```

## 5. Common Pitfalls

- **Hallucinating Enums**: The model might try to use a value not in your `enum` list if the prompt is ambiguous. Be explicit in the system instructions.
- **Schema Complexity**: Extremely deep nesting (>5 levels) can degrade model performance. Flatten schemas where possible.
- **Empty Arrays**: Ensure the model knows how to handle cases where no data is found (e.g., return `[]` rather than a string saying "none").

---
*Updated: January 22, 2026 - 17:15*
