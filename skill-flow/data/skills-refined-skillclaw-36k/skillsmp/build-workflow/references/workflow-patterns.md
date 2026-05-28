# Temporal Workflow Patterns

## Core Architecture

All workflows in this codebase follow a consistent pattern:

```
packages/temporal/use-cases/<workflow-name>/
├── workflow.ts           # Main workflow with withWorkflowTracking()
├── types.ts              # TypeScript input/output types
├── activities/
│   └── index.ts          # All activity implementations
└── README.md             # Documentation
```

## Determinism Rules (Critical)

Temporal workflows must be deterministic. **Workflow files cannot import modules that touch database, filesystem, or network directly.**

### Primitives Architecture

Primitives with both workflow utilities AND activities expose separate entry points:

```
primitives/<name>/
├── workflow.ts   → Workflow-safe exports (signals, queries, types)
├── index.ts      → Activity exports (may import @repo/database)
└── types.ts      → Shared types
```

### Workflow Import Rules

In workflow files:

```typescript
// ✅ CORRECT - type-only import for activities
import type * as activities from "./activities/index";

// ✅ CORRECT - workflow subpath for primitive utilities
import { waitForApprovalSignal } from "@temporal/primitives/human/workflow";

// ❌ WRONG - barrel export pulls in database code
import { waitForApprovalSignal } from "@temporal/primitives/human";

// ❌ WRONG - direct import of activity code in workflow
import { requestApproval } from "@temporal/primitives/human";
```

### What Can Be Imported in Workflows

| Safe to Import | Not Safe |
|----------------|----------|
| `@temporalio/workflow` | `@repo/database` |
| Type-only imports (`import type`) | Filesystem (`fs`, `path`) |
| Primitive `/workflow` subpaths | Network (`fetch`, `axios`) |
| Pure functions, constants | Activity implementations |

### Generator Note

If the workflow generator needs primitive workflow utilities (like `waitForApprovalSignal`), it must use the `/workflow` subpath, not the barrel export.

## The `withWorkflowTracking` Wrapper

Every workflow MUST use this wrapper for automatic database synchronization:

```typescript
import { proxyActivities } from "@temporalio/workflow";
import { withWorkflowTracking } from "@shared/workflows/workflowWrapper";
import type * as myActivities from "./activities/index";
import type { MyWorkflowInput, MyWorkflowOutput } from "./types";

const { myActivity } = proxyActivities<typeof myActivities>({
  startToCloseTimeout: "5 minutes",
  retry: {
    initialInterval: "1s",
    maximumInterval: "10s",
    backoffCoefficient: 2,
    maximumAttempts: 3,
  },
});

export async function myWorkflow(input: MyWorkflowInput): Promise<MyWorkflowOutput> {
  return await withWorkflowTracking(input.workflowId, async () => {
    // Workflow logic here
    const result = await myActivity(input.data);

    return {
      result: processedResult,
      metadata: { /* optional tracking data */ }
    };
  });
}
```

**What `withWorkflowTracking` does:**
- On success: updates DB status to "completed" with result and metadata
- On failure: updates DB status to "failed" with error message
- Uses the `updateWorkflowStatus` activity internally

## Activity Patterns

### Activity File Structure

Each activity is a separate async function in its own file:

```typescript
// activities/fetchData.ts
import type { FetchDataInput, FetchDataOutput } from "../types";

export async function fetchData(input: FetchDataInput): Promise<FetchDataOutput> {
  // Implementation
  return { data: result };
}
```

All activities exported from `activities/index.ts`:
```typescript
export * from "./fetchData.js";
export * from "./processData.js";
export * from "./generateReport.js";
```

### Activity Timeouts

Standard timeout configuration:
```typescript
const activities = proxyActivities<typeof myActivities>({
  startToCloseTimeout: "5 minutes",   // Adjust based on expected duration
  retry: {
    initialInterval: "1s",
    maximumInterval: "10s",
    backoffCoefficient: 2,
    maximumAttempts: 3,
  },
});
```

Common timeout ranges:
- Simple operations: 2-5 minutes
- AI generation: 5-10 minutes
- Complex processing: 10-15 minutes

## Primitive Activities

The codebase provides reusable primitives (import from `@temporal/primitives`):

### HTTP
```typescript
import { httpFetch } from "@temporal/primitives";

const result = await httpFetch({
  url: "https://api.example.com",
  method: "GET",
  headers: { "Authorization": "Bearer token" },
  timeout: 30000,
  retries: 3
});
// Returns: { status, headers, body }
```

### AI
```typescript
import { aiGenerateText, aiGenerateObject } from "@temporal/primitives";

// Text generation
const text = await aiGenerateText({
  prompt: "Summarize this content",
  systemPrompt: "You are helpful",
  model: "gemini-3-flash-preview"
});

// Structured generation
const obj = await aiGenerateObject({
  prompt: "Extract entities",
  schema: { type: "object", properties: { ... } }
});
```

### Data Transformation
```typescript
import { transform, validate } from "@temporal/primitives";

// JSONata transformation
const transformed = await transform({
  data: inputData,
  expression: "{ items: data[status='active'] }"
});

// JSON Schema validation
const validated = await validate({
  data: inputData,
  schema: { type: "object", required: ["email"] }
});
```

### Human Approval
```typescript
import { requestApproval } from "@temporal/primitives";

const decision = await requestApproval({
  workflowId: input.workflowId,
  title: "Approve Request",
  description: "Please review",
  timeout: "24 hours"
});
// Returns: { status: "approved" | "rejected", approvedBy, comment }
```

## Signals and Queries (Human-in-the-Loop)

For workflows requiring human decisions:

```typescript
import {
  defineSignal,
  defineQuery,
  setHandler,
  condition,
} from "@temporalio/workflow";

// Define signals and queries
export const approvalSignal = defineSignal<[{ approved: boolean; by: string }]>("approval");
export const statusQuery = defineQuery<string>("getStatus");

export async function approvalWorkflow(input: Input): Promise<Output> {
  return await withWorkflowTracking(input.workflowId, async () => {
    let approved = false;
    let approver = "";

    // Set up handlers
    setHandler(approvalSignal, (payload) => {
      approved = payload.approved;
      approver = payload.by;
    });

    setHandler(statusQuery, () => approved ? "approved" : "pending");

    // Wait for signal with timeout
    const received = await condition(() => approved, "24 hours");

    if (!received) {
      throw new Error("Approval timed out");
    }

    return { result: { approved, approver } };
  });
}
```

## Database Synchronization

### Automatic (via wrapper)
The wrapper handles completion/failure automatically.

### Manual Updates
For progress tracking during long workflows:

```typescript
import { updateWorkflowStatus } from "@shared/activities/workflowTracking";

// In an activity
export async function longRunningActivity(workflowId: string) {
  await updateWorkflowStatus({
    workflowId,
    status: "running",
    metadata: { stage: "processing", progress: 25 }
  });

  // ... do work ...

  await updateWorkflowStatus({
    workflowId,
    status: "running",
    metadata: { stage: "finalizing", progress: 90 }
  });
}
```

Status values: `pending`, `running`, `awaiting_approval`, `completed`, `failed`, `terminated`

## Type Definitions

Standard types.ts structure:

```typescript
// Workflow I/O
export interface MyWorkflowInput {
  workflowId: string;       // Always required
  userId?: string;          // Common field
  // ... workflow-specific fields
}

export interface MyWorkflowOutput {
  result: {
    // ... result fields
  };
  metadata?: Record<string, unknown>;
}

// Activity I/O (one pair per activity)
export interface FetchDataInput {
  url: string;
}

export interface FetchDataOutput {
  data: unknown;
  statusCode: number;
}
```

## AI Integration

Always import from shared module:

```typescript
import { google, openai, generateText, generateObject } from "@shared/ai/index.js";
```

Standard usage:
```typescript
const { text } = await generateText({
  model: google("gemini-3-flash-preview"),
  prompt: "Your prompt here",
  system: "System prompt"
});
```

For structured output:
```typescript
import { z } from "zod";

const schema = z.object({
  items: z.array(z.string()),
  count: z.number()
});

const { object } = await generateObject({
  model: google("gemini-3-flash-preview"),
  prompt: "Extract items",
  schema
});
```

## Security: HTML Sanitization

Before passing user content to AI:

```typescript
import { sanitizeHtmlToText } from "@shared/activities/htmlSanitizer";

const safeContent = sanitizeHtmlToText(userHtml, {
  maxLength: 50000,
  removePatterns: true  // Removes prompt injection attempts
});
```

## Child Workflows

For spawning independent workflows:

```typescript
import { startChild, ParentClosePolicy } from "@temporalio/workflow";

await startChild(childWorkflow, {
  workflowId: `child-${Date.now()}`,
  taskQueue: workflowInfo().taskQueue,
  args: [childInput],
  parentClosePolicy: ParentClosePolicy.ABANDON  // Child continues if parent stops
});
```
