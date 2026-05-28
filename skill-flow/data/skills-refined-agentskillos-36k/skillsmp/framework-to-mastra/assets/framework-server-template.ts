/**
 * Framework Server Template (Mastra v1 Beta + Hono)
 *
 * Template for setting up a Hono server with framework agent endpoints.
 *
 * Customization points marked with {{PLACEHOLDER}}:
 * - {{FRAMEWORK_NAME}}: kebab-case framework identifier
 * - {{AGENT_IMPORT}}: Import statement for framework agent
 * - {{WORKFLOW_IMPORT}}: Import statement for framework workflow
 * - {{TOOL_IMPORTS}}: Import statements for framework tools
 */

import { serve } from "@hono/node-server";
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { bearerAuth } from "hono/bearer-auth";
import { MastraServer } from "@mastra/hono";
import { Mastra } from "@mastra/core/mastra";
import { RuntimeContext } from "@mastra/core";
import { LibSQLStore } from "@mastra/libsql";
import { z } from "zod";

// {{AGENT_IMPORT}}
// import { researchAgent } from "./mastra/agents/research-agent.js";

// {{WORKFLOW_IMPORT}}
// import { researchWorkflow } from "./mastra/workflows/research-workflow.js";

// {{TOOL_IMPORTS}}
// import { assessStateTool, runPhase0Tool } from "./mastra/tools/index.js";

// ============================================================================
// Mastra Instance Configuration
// ============================================================================

const mastra = new Mastra({
  agents: {
    // {{FRAMEWORK_NAME}}Agent,
  },
  workflows: {
    // {{FRAMEWORK_NAME}}Workflow,
  },
  storage: new LibSQLStore({
    url: process.env.LIBSQL_URL || "file:./data/mastra.db",
  }),
  // Optional: Vector store for RAG
  // vectors: {
  //   default: new PgVector({ connectionString: process.env.DATABASE_URL }),
  // },
});

// ============================================================================
// Hono App Setup
// ============================================================================

const app = new Hono();

// Middleware
app.use("*", logger());
app.use(
  "*",
  cors({
    origin: process.env.ALLOWED_ORIGINS?.split(",") || ["http://localhost:3000"],
    allowMethods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allowHeaders: ["Content-Type", "Authorization", "X-User-Id"],
  })
);

// Authentication (optional - uncomment to enable)
// app.use("/api/*", bearerAuth({ token: process.env.API_TOKEN! }));

// ============================================================================
// Initialize Mastra Server
// ============================================================================

const server = new MastraServer({
  app,
  mastra,
  prefix: "/api",
});

await server.init();

// ============================================================================
// Custom Framework Endpoints
// ============================================================================

// Request schemas
const DiagnoseRequestSchema = z.object({
  situation: z.string().min(10),
  topic: z.string().optional(),
  workDone: z.array(z.string()).optional(),
});

const InterveneRequestSchema = z.object({
  stateId: z.string(),
  topic: z.string(),
  context: z.record(z.unknown()).optional(),
});

const StartProcessRequestSchema = z.object({
  topic: z.string(),
  depth: z.enum(["quick", "working", "expert"]).default("working"),
  context: z.record(z.unknown()).optional(),
});

// Diagnose endpoint
app.post("/api/diagnose", async (c) => {
  const body = await c.req.json();

  const parsed = DiagnoseRequestSchema.safeParse(body);
  if (!parsed.success) {
    return c.json({ error: "Validation failed", details: parsed.error.issues }, 400);
  }

  const userId = c.req.header("x-user-id") || "anonymous";

  // Create runtime context
  const runtimeContext = new RuntimeContext();
  runtimeContext.set("user-id", userId);

  // Get assessment tool and execute
  const assessTool = mastra.getTool("assess-{{FRAMEWORK_NAME}}-state");
  if (!assessTool) {
    return c.json({ error: "Assessment tool not found" }, 500);
  }

  const result = await assessTool.execute(parsed.data, { mastra, runtimeContext });

  return c.json({
    ...result,
    timestamp: new Date().toISOString(),
  });
});

// Intervene endpoint
app.post("/api/intervene", async (c) => {
  const body = await c.req.json();

  const parsed = InterveneRequestSchema.safeParse(body);
  if (!parsed.success) {
    return c.json({ error: "Validation failed", details: parsed.error.issues }, 400);
  }

  const { stateId, topic, context } = parsed.data;
  const userId = c.req.header("x-user-id") || "anonymous";

  const runtimeContext = new RuntimeContext();
  runtimeContext.set("user-id", userId);
  runtimeContext.set("topic", topic);

  // Map state to intervention tool
  const interventionMap: Record<string, string> = {
    // Map state IDs to intervention tool IDs
    // "R1": "run-phase0-analysis",
    // "R1.5": "build-vocabulary-map",
  };

  const toolId = interventionMap[stateId];
  if (!toolId) {
    return c.json({ error: `No intervention for state: ${stateId}` }, 400);
  }

  const tool = mastra.getTool(toolId);
  if (!tool) {
    return c.json({ error: `Intervention tool not found: ${toolId}` }, 500);
  }

  const result = await tool.execute({ topic, ...context }, { mastra, runtimeContext });

  return c.json({
    stateId,
    interventionApplied: true,
    result,
    timestamp: new Date().toISOString(),
  });
});

// Start workflow endpoint
app.post("/api/process/start", async (c) => {
  const body = await c.req.json();

  const parsed = StartProcessRequestSchema.safeParse(body);
  if (!parsed.success) {
    return c.json({ error: "Validation failed", details: parsed.error.issues }, 400);
  }

  const workflow = mastra.getWorkflow("{{FRAMEWORK_NAME}}-workflow");
  if (!workflow) {
    return c.json({ error: "Workflow not found" }, 500);
  }

  const run = workflow.createRun();

  // Start async
  run.start({ inputData: parsed.data }).catch((err) => {
    console.error("Workflow error:", err);
  });

  return c.json({
    runId: run.id,
    status: "started",
    statusUrl: `/api/process/${run.id}/status`,
  });
});

// Workflow status endpoint
app.get("/api/process/:runId/status", async (c) => {
  const runId = c.req.param("runId");

  const workflow = mastra.getWorkflow("{{FRAMEWORK_NAME}}-workflow");
  if (!workflow) {
    return c.json({ error: "Workflow not found" }, 500);
  }

  const run = await workflow.getRun(runId);
  if (!run) {
    return c.json({ error: "Run not found" }, 404);
  }

  return c.json({
    runId,
    status: run.status,
    currentStep: run.currentStep,
    output: run.status === "completed" ? run.output : undefined,
    error: run.status === "failed" ? run.error : undefined,
  });
});

// Chat endpoint
app.post("/api/chat", async (c) => {
  const body = await c.req.json();
  const { message, threadId } = body;
  const userId = c.req.header("x-user-id") || "anonymous";

  const thread = threadId || `chat-${userId}-${Date.now()}`;

  const runtimeContext = new RuntimeContext();
  runtimeContext.set("user-id", userId);

  const agent = mastra.getAgent("{{FRAMEWORK_NAME}}-agent");
  if (!agent) {
    return c.json({ error: "Agent not found" }, 500);
  }

  const result = await agent.generate(message, {
    runtimeContext,
    memory: {
      thread,
      resource: userId,
    },
  });

  return c.json({
    response: result.text,
    threadId: thread,
  });
});

// ============================================================================
// Health Endpoints
// ============================================================================

app.get("/health", async (c) => {
  const checks: Record<string, string> = {};

  // Check storage
  try {
    await mastra.storage?.getThreads({ limit: 1 });
    checks.storage = "healthy";
  } catch {
    checks.storage = "unhealthy";
  }

  const allHealthy = Object.values(checks).every((v) => v === "healthy");

  return c.json(
    {
      status: allHealthy ? "healthy" : "degraded",
      checks,
      timestamp: new Date().toISOString(),
    },
    allHealthy ? 200 : 503
  );
});

app.get("/ready", (c) => c.json({ ready: true }));

// ============================================================================
// Error Handling
// ============================================================================

app.onError((err, c) => {
  console.error("Server error:", err);

  if (err.name === "ZodError") {
    return c.json({ error: "Validation error", details: err.issues }, 400);
  }

  return c.json(
    {
      error: "Internal server error",
      message: process.env.NODE_ENV === "development" ? err.message : undefined,
    },
    500
  );
});

app.notFound((c) => {
  return c.json({ error: "Endpoint not found" }, 404);
});

// ============================================================================
// Start Server
// ============================================================================

const port = parseInt(process.env.PORT || "3000");

serve({
  fetch: app.fetch,
  port,
});

console.log(`{{FRAMEWORK_NAME}} agent server running on http://localhost:${port}`);

// Graceful shutdown
const shutdown = async () => {
  console.log("Shutting down gracefully...");
  process.exit(0);
};

process.on("SIGTERM", shutdown);
process.on("SIGINT", shutdown);
