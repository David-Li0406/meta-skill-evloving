---
name: create-source-destination
description: Use this skill when creating a new walkerOS source or destination, following an example-driven workflow that includes research, examples, mapping, implementation, testing, and documentation.
---

# Create a New Source or Destination

## Prerequisites

Before starting, read these skills:

- [understanding-flow](../understanding-flow/SKILL.md) - How sources and destinations fit in architecture
- [understanding-sources](../understanding-sources/SKILL.md) - Source interface
- [understanding-destinations](../understanding-destinations/SKILL.md) - Destination interface
- [understanding-transformers](../understanding-transformers/SKILL.md) - Transformer chaining from sources to destinations
- [understanding-mapping](../understanding-mapping/SKILL.md) - Event transformation
- [testing-strategy](../testing-strategy/SKILL.md) - How to test
- [writing-documentation](../writing-documentation/SKILL.md) - Documentation standards (for Phase 7)

## Source and Destination Types

### Source Types

| Type   | Platform | Input                   | Example                             |
| ------ | -------- | ----------------------- | ----------------------------------- |
| Web    | Browser  | DOM events, dataLayer   | `browser`, `dataLayer`              |
| Server | Node.js  | HTTP requests, webhooks | `gcp`, `express`, `lambda`, `fetch` |

### Destination Templates

| Complexity | Template     | When to Use                         |
| ---------- | ------------ | ----------------------------------- |
| Simple     | `plausible/` | Single SDK call, minimal config     |
| Complex    | `gtag/`      | Multiple services, sub-destinations |
| Server     | `gcp/`       | Server-side, batching, SDK init     |

## Process Overview

```
1. Research     → Understand input/output formats, find SDKs
2. Examples     → Create input/output examples in dev entry FIRST
3. Mapping      → Define input/output transformation
4. Scaffold     → Copy template and configure
5. Implement    → Build using examples as test fixtures
6. Test         → Verify against example variations
7. Document     → Write README
```

---

## Phase 1: Research

**Goal:** Understand the input/output formats and vendor APIs before writing any code.

### 1.1 Identify Input/Output Sources

- **What triggers events?** - HTTP POST, webhook, DOM mutation, dataLayer push
- **What data is received?** - Request body, headers, query params
- **Authentication?** - API keys, signatures, tokens

### 1.2 Find Official Resources

```bash
# Search npm for official types
npm search @[platform]
npm info @types/[platform]

# Check for official SDK
npm search [platform]-sdk
```

### 1.3 Document Input/Output Schema

Capture real examples of incoming data and expected outputs:

| Field        | Type   | Required | Description            |
| ------------ | ------ | -------- | ---------------------- |
| `event`      | string | Yes      | Event type from source |
| `properties` | object | No       | Event data             |
| `userId`     | string | No       | User identifier        |
| `timestamp`  | number | No       | Event time             |

### Gate: Research Complete

Before proceeding, confirm:

- [ ] Input trigger identified (HTTP, webhook, DOM, dataLayer)
- [ ] Input schema documented (required/optional fields)
- [ ] Fields mapped to walkerOS event structure

---

## Phase 2: Create Input/Output Examples (BEFORE Implementation)

**Goal:** Define realistic input/output data in `dev` entry FIRST.

### 2.1 Scaffold Directory Structure

```bash
mkdir -p packages/[type]/[name]/src/{examples,schemas,types}
```

### 2.2 Create Input Examples

**Real examples of what the source will receive:**

`src/examples/inputs.ts`:

```typescript
// Examples of incoming data this source will receive.
export const pageViewInput = {
  event: 'page_view',
  properties: {
    page_title: 'Home Page',
    page_path: '/home',
    referrer: 'https://google.com',
  },
  userId: 'user-123',
  timestamp: 1700000000000,
};

// Additional examples...
```

### 2.3 Create Expected Output Examples

**walkerOS events that should result from inputs:**

`src/examples/outputs.ts`:

```typescript
// Expected walkerOS events from inputs.
export const pageViewEvent = {
  event: 'page view',
  data: {
    title: 'Home Page',
    path: '/home',
    referrer: 'https://google.com',
  },
  user: { id: 'user-123' },
};

// Additional expected outputs...
```

### Gate: Examples Valid

- [ ] All example files compile (`npm run build`)
- [ ] Can trace: input → expected output for each example

---

## Phase 3: Define Mapping

**Goal:** Document transformation from input format to walkerOS events and vendor format.

### 3.1 Create Mapping Configuration

`src/examples/mapping.ts`:

```typescript
// Default mapping: input format → walkerOS events.
export const eventNameMap: Record<string, string> = {
  page_view: 'page view',
  purchase: 'order complete',
  button_click: 'button click',
};

// Data field mapping
export const defaultMapping = {
  page: {
    view: {
      data: {
        map: {
          title: 'properties.page_title',
          path: 'properties.page_path',
          referrer: 'properties.referrer',
        },
      },
    },
  },
  // Additional mappings...
};
```

### Gate: Mapping Verified

- [ ] Mapping covers main input types
- [ ] Each mapping rule traces correctly to expected output

---

## Phase 4: Scaffold

**Template sources/destinations:**

```bash
cp -r packages/[type]/[template] packages/[type]/[name]
cd packages/[type]/[name]

# Update package.json: name, description, repository.directory
```

**Directory structure:**

```
packages/[type]/[name]/
├── src/
│   ├── index.ts           # Main export
│   ├── index.test.ts      # Tests against examples
│   ├── dev.ts             # Exports schemas and examples
│   ├── examples/
│   │   ├── index.ts       # Re-exports
│   │   ├── inputs.ts      # Incoming data examples
│   │   ├── outputs.ts     # Expected walkerOS events
│   │   ├── requests.ts    # HTTP request examples (if applicable)
│   │   └── mapping.ts     # Transformation config
│   ├── schemas/
│   │   └── index.ts       # Zod schemas for input validation
│   └── types/
│       └── index.ts       # Config, Input interfaces
├── package.json
├── tsconfig.json
├── tsup.config.ts
├── jest.config.mjs
└── README.md
```

---

## Phase 5: Implement

**Now write code to transform inputs to expected outputs.**

### 5.1 Define Types

`src/types/index.ts`:

```typescript
export interface Config {
  mapping?: WalkerOS.Mapping;
  eventNameMap?: Record<string, string>;
}

export interface Input {
  event: string;
  properties?: Record<string, unknown>;
  userId?: string;
  timestamp?: number;
}

// Additional types...
```

### 5.2 Implement Source/Destination (Context Pattern)

```typescript
export const sourceOrDestination: SourceOrDestination.Init<Types> = async (context) => {
  const { config = {}, env } = context;

  // Validate and apply default settings using Zod schema
  const settings = SettingsSchema.parse(config.settings || {});

  // Push handler - receives incoming data and forwards to collector.
  const push: Types['push'] = async (request) => {
    // Transform to walkerOS event format
    const eventData = transformInput(request.body, settings);

    // Forward to collector via env.push
    await envPush(eventData);
  };

  return {
    type: 'my-source-or-destination',
    config: fullConfig,
    push,
  };
};
```

### Gate: Implementation Compiles

- [ ] `npm run build` passes
- [ ] `npm run lint` passes

---

## Phase 6: Test Against Examples

**Verify implementation produces expected outputs.**

### 6.1 Test Helper Pattern

Create a helper to build source/destination context for tests:

```typescript
function createSourceOrDestinationContext(
  config: Partial<SourceOrDestination.Config<Types>> = {},
  env: Partial<Types['env']> = {},
): SourceOrDestination.Context<Types> {
  return {
    config,
    env: env as Types['env'],
    logger: env.logger || createMockLogger(),
    id: 'test-my-source-or-destination',
    collector: {} as Collector.Instance,
  };
}
```

### Gate: Tests Pass

- [ ] `npm run test` passes
- [ ] Tests verify against example outputs (not hardcoded values)

---

## Phase 7: Document

Follow the [writing-documentation](../writing-documentation/SKILL.md) skill for:

- README structure and templates
- Example validation against `apps/quickstart/`
- Quality checklist before publishing

Key requirements for source/destination documentation:

- [ ] Input/output format table documenting expected fields
- [ ] Event name mapping table (source/destination format → walkerOS format)
- [ ] Configuration options table
- [ ] Working code example with imports
- [ ] Installation instructions

---

## Reference Files

| What            | Where                               |
| --------------- | ----------------------------------- |
| Web template    | `packages/web/sources/dataLayer/`   |
| Server template | `packages/server/sources/fetch/`    |
| Destination types| `packages/web/core/src/types/destination.ts` |

## Related

- [understanding-sources skill](../understanding-sources/SKILL.md)
- [understanding-destinations skill](../understanding-destinations/SKILL.md)
- [← Back to Hub](../../AGENT.md)