---
name: gemini-structured-output
description: Guide for using Structured Outputs with Gemini API to ensure type-safe JSON responses, including Zod integration.
---

# Gemini Structured Output

Structured Outputs ensure that the model generates responses that adhere to a specific JSON Schema. This is critical for building reliable applications where the model's output needs to be parsed programmatically.

## Key Concepts

- **Structured Output**: Forces the model to return JSON matching a schema.
- **Type Safety**: Use Zod to define schemas and validate implementation at runtime.
- **Single Source of Truth**: Use `zod-to-json-schema` to derive the Gemini API schema from your Zod definition (requires compatible SDK or manual conversion for legacy SDKs).

## Implementation Pattern

### 1. Define Zod Schema

Define your data structure using Zod. This serves as both your runtime validation and the source for the API schema.

```typescript
import { z } from "zod";

const RecipeSchema = z.object({
  recipeName: z.string(),
  ingredients: z.array(z.string()),
  instructions: z.array(z.string()),
});
```

### 2. Configure Gemini Request

Pass the schema to the model's generation config.

**For `@google/genai` (New SDK):**

```typescript
import { zodToJsonSchema } from "zod-to-json-schema";

const response = await client.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: "How to make cookies?",
  config: {
    responseMimeType: "application/json",
    responseJsonSchema: zodToJsonSchema(RecipeSchema), // Direct Zod support
  },
});
```

**For `@google/generative-ai` (Legacy SDK - Current Project):**

You must manually construct the `ResponseSchema` or convert the Zod schema to the specific format expected by this SDK (`SchemaType`).

```typescript
import { SchemaType } from "@google/generative-ai";

const responseSchema = {
  type: SchemaType.OBJECT,
  properties: {
    recipeName: { type: SchemaType.STRING },
    ingredients: { 
      type: SchemaType.ARRAY, 
      items: { type: SchemaType.STRING } 
    },
    // ...
  },
  required: ["recipeName", "ingredients"],
};

const model = client.getGenerativeModel({
  model: "gemini-3-flash-preview",
  generationConfig: {
    responseMimeType: "application/json",
    responseSchema: responseSchema,
  },
});
```

### 3. Parse and Validate

Always validate the output, even with Structured Outputs.

```typescript
const json = JSON.parse(response.text());
const data = RecipeSchema.parse(json); // Runtime check
```

## Best Practices

1.  **Use Enums**: For fields with limited options (e.g., `sentiment: "positive" | "negative"`), use `z.enum()` or schema enums strictly.
2.  **Descriptions**: Add `.describe()` to Zod fields. These descriptions are passed to the model and dramatically improve accuracy.
3.  **Nullable**: Explicitly handle optional fields.
4.  **Runtime Validation**: Trust but verify. Always parse the result with Zod.

## References

- [Gemini API Docs: Structured Outputs](https://ai.google.dev/gemini-api/docs/structured-output)
