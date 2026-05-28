---
name: convex-component-authoring
description: Use this skill when you need to create, structure, and publish self-contained Convex components with proper isolation, exports, and dependency management.
---

# Skill body

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: [Convex Components Documentation](https://docs.convex.dev/components)
- Component Authoring: [Component Authoring Guide](https://docs.convex.dev/components/authoring)
- For broader context: [LLMs Overview](https://docs.convex.dev/llms.txt)

## What Are Convex Components?

Convex components are self-contained packages that include:
- Database tables (isolated from the main app)
- Functions (queries, mutations, actions)
- TypeScript types and validators
- Optional frontend hooks

## Component Structure

```
my-convex-component/
├── package.json
├── tsconfig.json
├── README.md
├── src/
│   ├── index.ts           # Main exports
│   ├── component.ts       # Component definition
│   ├── schema.ts          # Component schema
│   └── functions/
│       ├── queries.ts
│       ├── mutations.ts
│       └── actions.ts
└── convex.config.ts       # Component configuration
```

## Creating a Component

### 1. Component Configuration

```typescript
// convex.config.ts
import { defineComponent } from "convex/server";

export default defineComponent("myComponent");
```

### 2. Component Schema

```typescript
// src/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // Tables are isolated to this component
  items: defineTable({
    name: v.string(),
    data: v.any(),
    createdAt: v.number(),
  }).index("by_name", ["name"]),
  
  config: defineTable({
    key: v.string(),
    value: v.any(),
  }).index("by_key", ["key"]),
});
```

### 3. Component Definition

```typescript
// src/component.ts
import { defineComponent } from "convex/server";
import schema from "./schema";
import * as queries from "./functions/queries";
import * as mutations from "./functions/mutations";

const component = defineComponent("myComponent", {
  schema,
  functions: {
    ...queries,
    ...mutations,
  },
});

export default component;
```

### 4. Component Functions

```typescript
// src/functions/queries.ts
// Define your query functions here
```

```typescript
// src/functions/mutations.ts
// Define your mutation functions here
```