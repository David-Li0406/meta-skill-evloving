# Catalog Design Patterns

The **Catalog** is the most critical part of a `json-render` implementation. A well-designed catalog ensures AI reliability and developer sanity.

## 🏗 Schema Structure
Use **Zod** for schema definition. `json-render` uses these schemas to:
1. Validate the AI output at runtime.
2. Provide type safety in your React components.
3. Generate the "prompt context" for the AI model.

### Recommended Pattern: Atomic Components
Avoid monolithic "Dashboard" components. Instead, provide small, reusable blocks.

```typescript
const components = {
  Badge: {
    schema: z.object({
      label: z.string(),
      variant: z.enum(['success', 'error', 'warning', 'info']),
    }),
  },
  Grid: {
    schema: z.object({
      columns: z.number().min(1).max(12),
      gap: z.number().optional(),
    }),
  }
};
```

## 📝 Descriptive Prompting
The `description` field in each component is sent to the AI. Be specific about **when** and **how** to use the component.

**Bad Description**: "A card for data."
**Good Description**: "Use this card to display a single metric with a trend indicator. Ideal for financial summaries or user statistics."

## 🔗 Nested Components
`json-render` supports children via the `children` prop pattern.

```typescript
const Container = {
  schema: z.object({
    title: z.string(),
    children: z.array(z.any()), // AI can nest any catalog component here
  })
};
```

## 🛠 Catalog Validation Script
In 2026, we automate catalog integrity. You can use a script to verify that all components in your catalog have corresponding React implementations.

```bash
# Example check
bun x json-render-cli validate ./src/catalog.ts
```

*Updated: January 22, 2026 - 17:40*
