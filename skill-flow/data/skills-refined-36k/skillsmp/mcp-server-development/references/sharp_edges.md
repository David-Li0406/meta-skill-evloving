# Mcp Server Development - Sharp Edges

## Tool Description Ignored

### **Id**
tool-description-ignored
### **Summary**
AI ignores tool because description is unclear
### **Severity**
critical
### **Situation**
Tool exists but AI never selects it for obvious use cases
### **Why**
  LLMs choose tools based on description matching.
  Vague descriptions don't trigger selection.
  Technical jargon confuses the model.
  
### **Solution**
  // BAD: Vague, technical description
  {
      name: "sync_data",
      description: "Synchronizes data between systems",
      // What data? Which systems? When to use?
  }
  
  // GOOD: Clear, actionable description
  {
      name: "sync_data",
      description: `
          Synchronizes user data from your app to the CRM.
          Use when: User asks to update CRM, sync contacts,
          or push customer data to sales team.
          Returns: Number of records synced, any errors.
          Note: Only syncs users modified in last 24 hours.
      `,
  }
  
  // TIPS for descriptions:
  // 1. Start with what it does (verb)
  // 2. Say WHEN to use it (use cases)
  // 3. Mention what it returns
  // 4. Note limitations or prerequisites
  // 5. Use user-facing language, not API jargon
  
### **Symptoms**
  - AI uses wrong tool for task
  - AI says "I don't have a tool for that" when tool exists
  - AI asks for manual steps instead of using tool
### **Detection Pattern**
description.*:|description":

## Schema Mismatch Silent Failure

### **Id**
schema-mismatch-silent-failure
### **Summary**
Tool silently fails because AI sends wrong data shape
### **Severity**
critical
### **Situation**
Tool returns error or wrong result, no clear reason why
### **Why**
  inputSchema doesn't match what AI actually sends.
  Missing required field validation.
  Type coercion masks problems.
  
### **Solution**
  // Define schemas with explicit examples and constraints
  const ToolSchema = {
      type: "object",
      properties: {
          query: {
              type: "string",
              description: "Search query. Example: 'users created this week'",
              minLength: 1,
              maxLength: 500
          },
          filters: {
              type: "object",
              description: "Optional filters. Example: { status: 'active' }",
              properties: {
                  status: {
                      type: "string",
                      enum: ["active", "inactive", "pending"]
                  },
                  createdAfter: {
                      type: "string",
                      format: "date-time"
                  }
              }
          }
      },
      required: ["query"],
      additionalProperties: false  // Reject unknown fields!
  };
  
  // Always validate at runtime
  import Ajv from 'ajv';
  const ajv = new Ajv();
  const validate = ajv.compile(ToolSchema);
  
  if (!validate(request.params.arguments)) {
      return {
          content: [{
              type: "text",
              text: `Schema validation failed: ${ajv.errorsText(validate.errors)}`
          }],
          isError: true
      };
  }
  
### **Symptoms**
  - Intermittent tool failures
  - "undefined" in tool responses
  - Works in testing, fails with AI
### **Detection Pattern**
inputSchema|properties|required

## Transport Timeout

### **Id**
transport-timeout
### **Summary**
Long-running tool times out, loses work
### **Severity**
high
### **Situation**
Tool starts work, connection times out, no result
### **Why**
  stdio transport has no built-in timeout handling.
  HTTP transport defaults to short timeouts.
  Long operations block the connection.
  
### **Solution**
  // Pattern 1: Return immediately, poll for result
  async function handleLongOperation(request) {
      // Start async job
      const jobId = await startBackgroundJob(request.params);
  
      // Return job ID immediately
      return {
          content: [{
              type: "text",
              text: JSON.stringify({
                  status: "started",
                  jobId,
                  checkWith: "check_job_status",
                  message: "Operation started. Use check_job_status to monitor."
              })
          }]
      };
  }
  
  // Companion tool to check status
  {
      name: "check_job_status",
      description: "Check status of a long-running operation",
      inputSchema: {
          type: "object",
          properties: {
              jobId: { type: "string" }
          },
          required: ["jobId"]
      }
  }
  
  async function handleJobStatus(jobId) {
      const job = await getJob(jobId);
      return {
          content: [{
              type: "text",
              text: JSON.stringify({
                  status: job.status, // "running" | "completed" | "failed"
                  progress: job.progress,
                  result: job.status === "completed" ? job.result : null,
                  error: job.status === "failed" ? job.error : null
              })
          }]
      };
  }
  
  // Pattern 2: Stream progress (if transport supports)
  // Use SSE or Streamable HTTP for progress updates
  
### **Symptoms**
  - Tool hangs then fails
  - Partial work lost
  - "Connection closed" errors
### **Detection Pattern**
await|async|Promise|setTimeout

## State Between Requests

### **Id**
state-between-requests
### **Summary**
Server loses state between requests, breaks multi-step operations
### **Severity**
high
### **Situation**
AI does step 1, step 2 fails because state from step 1 is gone
### **Why**
  MCP doesn't guarantee request ordering or session persistence.
  Stateless design required for scalability.
  In-memory state lost on restart.
  
### **Solution**
  // DON'T rely on in-memory state between requests
  // BAD:
  let currentProject = null;  // Lost between requests!
  
  // GOOD: Use external state or include context in each request
  // Option 1: Database/Redis for state
  async function getContext(contextId: string) {
      return await redis.get(`context:${contextId}`);
  }
  
  async function saveContext(contextId: string, data: any) {
      await redis.set(`context:${contextId}`, data, 'EX', 3600);
  }
  
  // Option 2: Return context to AI, have it send back
  {
      name: "start_operation",
      description: "Start an operation. Returns context to use in follow-up calls."
  }
  
  async function handleStart() {
      const context = await initializeOperation();
      return {
          content: [{
              type: "text",
              text: JSON.stringify({
                  message: "Operation started",
                  context: encryptAndEncode(context),
                  nextStep: "Call continue_operation with this context"
              })
          }]
      };
  }
  
  // Option 3: Idempotent operations that don't need state
  // Each request is self-contained
  
### **Symptoms**
  - Multi-step workflows fail partway
  - "Not found" errors on second step
  - Works in testing, fails in production
### **Detection Pattern**
let |var |this\.

## Resource Uri Collision

### **Id**
resource-uri-collision
### **Summary**
Resource URIs conflict or are ambiguous
### **Severity**
medium
### **Situation**
Wrong resource returned, or resource not found
### **Why**
  URI scheme not well-defined.
  Dynamic resources use conflicting patterns.
  No namespace isolation.
  
### **Solution**
  // Define clear URI scheme upfront
  const URI_SCHEME = {
      // Static resources
      config: "config://settings",
      schema: "schema://database/main",
  
      // Dynamic resources with clear pattern
      file: (path: string) => `file://project/${encodeURIComponent(path)}`,
      user: (id: string) => `user://profile/${id}`,
      query: (name: string) => `query://saved/${name}`,
  };
  
  // Validate URIs on registration
  function validateUri(uri: string): boolean {
      const patterns = [
          /^config:\/\/\w+$/,
          /^file:\/\/project\/.+$/,
          /^user:\/\/profile\/\w+$/,
      ];
      return patterns.some(p => p.test(uri));
  }
  
  // Parse URIs consistently
  function parseUri(uri: string): { type: string, path: string } {
      const match = uri.match(/^(\w+):\/\/(.+)$/);
      if (!match) throw new Error(`Invalid URI: ${uri}`);
      return { type: match[1], path: match[2] };
  }
  
  // List resources with clear descriptions
  server.setRequestHandler(ListResourcesRequestSchema, async () => ({
      resources: [
          {
              uri: URI_SCHEME.config,
              name: "Application Config",
              description: "Current application settings (read-only)"
          },
          // Dynamic resource template
          {
              uriTemplate: "file://project/{path}",
              name: "Project Files",
              description: "Files in the current project. {path} is relative path."
          }
      ]
  }));
  
### **Symptoms**
  - Wrong content returned
  - "Resource not found" for valid resources
  - Confusion about which resource to request
### **Detection Pattern**
uri:|uriTemplate