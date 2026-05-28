# Structured Data with Skillet Schema

## When to use

- To get predictable, type-safe JSON output from an LLM instead of plain text.
- For converting natural language user input into a structured format for forms or API calls.
- When you need to define a strict data contract for the model's response.
- To power generative UI by populating components with structured data.

## Core concepts

- **Skillet**: A Zod-like, LLM-optimized schema language used to define the structure of the desired JSON output.
- **Schema**: A definition of the shape of data, composed of types like `s.string()`, `s.number()`, `s.object()`, and `s.array()`.
- **Type Inference**: The ability to create a static TypeScript type directly from a Skillet schema using `s.Infer<T>`.
- **Structured Hooks**: React hooks like `useStructuredChat` and `useStructuredCompletion` that accept a `schema` option to enforce structured JSON output.

## Rules & constraints

- **MUST**: Provide a `schema` property to `useStructuredChat` or `useStructuredCompletion` to receive structured output.
- **MUST**: Use descriptive text for every field in a schema (e.g., `s.string('The user's full name')`) to give the model necessary context.
- **SHOULD**: Use `s.anyOf` with `s.literal` discriminators to handle distinct output shapes, such as a success case and an error case.
- **SHOULD**: Use the `streaming` keyword (e.g., `s.streaming.array()`) within schemas when expecting large or partial data to improve UI responsiveness.

## Key Learning Points

### Point 1: Defining a Skillet Schema

Use the `s` object to compose a schema that matches your desired output. This provides a clear contract for the LLM.

```ts
import { s } from '@hashbrownai/core'

const userSchema = s.object('A user profile', {
  name: s.string("The user's full name"),
  age: s.number("The user's age in years"),
  isActive: s.boolean('Whether the user account is active'),
})
```

### Point 2: Getting Structured Output

Pass your schema to `useStructuredCompletion` (for single-turn requests) or `useStructuredChat` (for multi-turn conversations). The hook's return value will be a parsed object matching the schema.

```tsx
import { useStructuredCompletion } from '@hashbrownai/react'

const { output } = useStructuredCompletion({
  model: 'gpt-4',
  system: 'Extract user details from the input.',
  input: 'My name is Alex, I am 30 years old, and my account is active.',
  schema: userSchema,
})

// `output` will be { name: 'Alex', age: 30, isActive: true }
```

### Point 3: Handling Success and Error States

For robust interactions, define separate schemas for success and error conditions and combine them with `s.anyOf`. Use `s.literal('Expense')` as a `type` field to easily discriminate between the two outcomes in your code.

```ts
const successSchema = s.object('Parsed expense', {
  type: s.literal('Expense'),
  amount: s.number('The expense amount'),
  // ... other fields
})

const errorSchema = s.object('Unable to parse', {
  type: s.literal('ParseError'),
  message: s.string('Human-readable error message'),
})

const expenseResultSchema = s.anyOf([successSchema, errorSchema])
```

### Point 4: Inferring TypeScript Types

Ensure full type safety by inferring a TypeScript type directly from your schema. This connects your AI logic and your application code seamlessly.

```ts
import { s } from '@hashbrownai/core'

const mySchema = s.object('Schema', { id: s.string('ID') })

// Create a TypeScript type from the schema
type MyType = s.Infer<typeof mySchema>

// const data: MyType = { id: '123' }; // This is valid
```

## Pitfalls

- **Overly Complex Schemas**: Very deep or ambiguous schemas can confuse the model and lead to unreliable output.
- **Vague Descriptions**: Failing to provide clear, descriptive text for schema fields often results in poor quality or incorrect data from the model.
- **Ignoring Errors**: When using an `s.anyOf` schema for success/error states, failing to check for and handle the error case in your UI logic.

## Source map

- `/concept/schema.md` — Introduction to the Skillet schema language and its methods.
- `/concept/structured-output.md` — How to use schemas with `useStructuredChat` and `useStructuredCompletion`.
- `/recipes/natural-language-to-structured-data.md` — A practical example of replacing a form with a single input using structured data.
