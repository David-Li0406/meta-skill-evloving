# API Design Patterns

Designing Hono APIs for framework agents.

## Core Endpoints

Every framework agent needs these endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/diagnose` | POST | Assess current state |
| `/intervene` | POST | Apply intervention for state |
| `/process/start` | POST | Start full workflow |
| `/process/{runId}/status` | GET | Check workflow status |
| `/health` | GET | Health check |

## Diagnostic Endpoint

```typescript
import { registerApiRoute } from "@mastra/core/server";
import { z } from "zod";
import { DiagnoseRequestSchema, DiagnoseResponseSchema } from "../schemas/api.js";

registerApiRoute("/diagnose", {
  method: "POST",
  handler: async (c) => {
    const mastra = c.get("mastra");
    const body = await c.req.json();

    // Validate input
    const parsed = DiagnoseRequestSchema.safeParse(body);
    if (!parsed.success) {
      return c.json({ error: parsed.error.issues }, 400);
    }

    const { situation, topic, workDone } = parsed.data;

    // Get assessment from tool
    const assessTool = mastra.getTool("assess-research-state");
    const result = await assessTool.execute(
      { situation, topic, workDone },
      { mastra }
    );

    // Validate output
    const response = DiagnoseResponseSchema.parse({
      ...result,
      timestamp: new Date().toISOString(),
    });

    return c.json(response);
  },
});
```

## Intervention Endpoint

```typescript
// Intervention request: state ID + context
const InterveneRequestSchema = z.object({
  stateId: ResearchStateSchema,
  topic: z.string(),
  context: z.record(z.unknown()).optional(),
});

registerApiRoute("/intervene", {
  method: "POST",
  handler: async (c) => {
    const mastra = c.get("mastra");
    const body = await c.req.json();

    const parsed = InterveneRequestSchema.safeParse(body);
    if (!parsed.success) {
      return c.json({ error: parsed.error.issues }, 400);
    }

    const { stateId, topic, context } = parsed.data;

    // Route to appropriate intervention tool
    let result;
    switch (stateId) {
      case "R1":
        const phase0Tool = mastra.getTool("run-phase0-analysis");
        result = await phase0Tool.execute({ topic }, { mastra });
        break;
      case "R1.5":
        const vocabTool = mastra.getTool("build-vocabulary-map");
        result = await vocabTool.execute({ topic, ...context }, { mastra });
        break;
      case "R2":
        const perspectiveTool = mastra.getTool("expand-perspectives");
        result = await perspectiveTool.execute({ topic }, { mastra });
        break;
      default:
        return c.json({ error: `No intervention for state ${stateId}` }, 400);
    }

    return c.json({
      stateId,
      interventionApplied: true,
      result,
      timestamp: new Date().toISOString(),
    });
  },
});
```

## Workflow Endpoints

```typescript
// Start workflow
registerApiRoute("/process/start", {
  method: "POST",
  handler: async (c) => {
    const mastra = c.get("mastra");
    const body = await c.req.json();

    const parsed = StartResearchRequestSchema.safeParse(body);
    if (!parsed.success) {
      return c.json({ error: parsed.error.issues }, 400);
    }

    const workflow = mastra.getWorkflow("research-workflow");
    const run = workflow.createRun();

    // Start async - don't await completion
    run.start({ inputData: parsed.data }).catch(console.error);

    return c.json({
      runId: run.id,
      status: "started",
      checkStatusUrl: `/process/${run.id}/status`,
    });
  },
});

// Check workflow status
registerApiRoute("/process/:runId/status", {
  method: "GET",
  handler: async (c) => {
    const mastra = c.get("mastra");
    const runId = c.req.param("runId");

    const workflow = mastra.getWorkflow("research-workflow");
    const run = await workflow.getRun(runId);

    if (!run) {
      return c.json({ error: "Run not found" }, 404);
    }

    return c.json({
      runId,
      status: run.status,
      currentStep: run.currentStep,
      completedSteps: Object.keys(run.steps || {}),
      output: run.status === "completed" ? run.output : undefined,
      error: run.status === "failed" ? run.error : undefined,
    });
  },
});

// Get workflow result (blocking)
registerApiRoute("/process/:runId/result", {
  method: "GET",
  handler: async (c) => {
    const mastra = c.get("mastra");
    const runId = c.req.param("runId");
    const timeout = parseInt(c.req.query("timeout") || "30000");

    const workflow = mastra.getWorkflow("research-workflow");

    // Poll until complete or timeout
    const startTime = Date.now();
    while (Date.now() - startTime < timeout) {
      const run = await workflow.getRun(runId);

      if (!run) {
        return c.json({ error: "Run not found" }, 404);
      }

      if (run.status === "completed") {
        return c.json({ status: "completed", output: run.output });
      }

      if (run.status === "failed") {
        return c.json({ status: "failed", error: run.error }, 500);
      }

      // Wait before polling again
      await new Promise(r => setTimeout(r, 1000));
    }

    return c.json({ status: "timeout", message: "Workflow still running" }, 202);
  },
});
```

## Agent Chat Endpoint

For conversational interaction:

```typescript
registerApiRoute("/chat", {
  method: "POST",
  handler: async (c) => {
    const mastra = c.get("mastra");
    const body = await c.req.json();
    const userId = c.req.header("x-user-id") || "anonymous";

    const { message, topic, threadId } = body;

    // Get or create thread
    const thread = threadId || `chat-${userId}-${Date.now()}`;

    const agent = mastra.getAgent("research-agent");
    const result = await agent.generate(message, {
      memory: {
        thread,
        resource: userId,
      },
    });

    return c.json({
      response: result.text,
      threadId: thread,
      usage: result.usage,
    });
  },
});

// Streaming chat
registerApiRoute("/chat/stream", {
  method: "POST",
  handler: async (c) => {
    const mastra = c.get("mastra");
    const body = await c.req.json();
    const userId = c.req.header("x-user-id") || "anonymous";

    const { message, threadId } = body;
    const thread = threadId || `chat-${userId}-${Date.now()}`;

    const agent = mastra.getAgent("research-agent");
    const stream = await agent.stream(message, {
      memory: {
        thread,
        resource: userId,
      },
    });

    return new Response(stream.textStream, {
      headers: {
        "Content-Type": "text/event-stream",
        "X-Thread-Id": thread,
      },
    });
  },
});
```

## Memory Endpoints

For accessing stored research:

```typescript
// Get prior vocabulary maps
registerApiRoute("/vocabulary/:topic", {
  method: "GET",
  handler: async (c) => {
    const mastra = c.get("mastra");
    const topic = c.req.param("topic");
    const userId = c.req.header("x-user-id");

    const vocabTool = mastra.getTool("retrieve-vocabulary");
    const result = await vocabTool.execute({ topic, userId }, { mastra });

    return c.json(result);
  },
});

// Get research threads
registerApiRoute("/threads", {
  method: "GET",
  handler: async (c) => {
    const mastra = c.get("mastra");
    const userId = c.req.header("x-user-id");
    const page = parseInt(c.req.query("page") || "1");

    const threads = await mastra.storage?.listThreads({
      resourceId: userId,
      page,
      perPage: 20,
    });

    return c.json({
      threads: threads?.map(t => ({
        id: t.id,
        topic: t.metadata?.topic,
        status: t.metadata?.status,
        lastActivity: t.metadata?.updatedAt,
      })),
      page,
    });
  },
});
```

## Error Handling

```typescript
// Global error handler
app.onError((err, c) => {
  console.error("API error:", err);

  // Zod validation errors
  if (err.name === "ZodError") {
    return c.json({
      error: "Validation error",
      details: err.issues,
    }, 400);
  }

  // Not found
  if (err.message.includes("not found")) {
    return c.json({ error: err.message }, 404);
  }

  // Rate limiting
  if (err.message.includes("rate limit")) {
    return c.json({
      error: "Rate limit exceeded",
      retryAfter: 60,
    }, 429);
  }

  // Generic error
  return c.json({
    error: "Internal server error",
    message: process.env.NODE_ENV === "development" ? err.message : undefined,
  }, 500);
});

// Not found handler
app.notFound((c) => {
  return c.json({
    error: "Endpoint not found",
    availableEndpoints: [
      "POST /diagnose",
      "POST /intervene",
      "POST /process/start",
      "GET /process/:runId/status",
      "POST /chat",
      "GET /health",
    ],
  }, 404);
});
```

## Authentication

```typescript
import { bearerAuth } from "hono/bearer-auth";
import { jwt } from "hono/jwt";

// API key auth
app.use("/api/*", bearerAuth({
  token: process.env.API_TOKEN!,
}));

// Or JWT auth
app.use("/api/*", jwt({
  secret: process.env.JWT_SECRET!,
}));

// Extract user from JWT
app.use("/api/*", async (c, next) => {
  const payload = c.get("jwtPayload");
  c.set("userId", payload?.sub);
  await next();
});
```

## OpenAPI Documentation

```typescript
import { swaggerUI } from "@hono/swagger-ui";

// Serve OpenAPI spec
const server = new MastraServer({
  app,
  mastra,
  openapiPath: "/openapi.json",
});

// Swagger UI
app.get("/docs", swaggerUI({ url: "/openapi.json" }));
```

## Best Practices

1. **Validate Input**: Always parse request body with Zod
2. **Validate Output**: Ensure responses match schema
3. **Include Timestamps**: Add timestamp to all responses
4. **User Context**: Extract userId from headers
5. **Async Workflows**: Return immediately, provide status endpoint
6. **Error Details**: In dev, include error messages
7. **Rate Limiting**: Protect expensive endpoints
8. **OpenAPI**: Document all endpoints
