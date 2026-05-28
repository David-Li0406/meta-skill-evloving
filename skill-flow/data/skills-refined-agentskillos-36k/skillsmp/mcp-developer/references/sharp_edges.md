# Mcp Developer - Sharp Edges

## Tool Name Collisions Across Servers

### **Id**
tool-name-collision
### **Severity**
critical
### **Situation**
  Multiple MCP servers define tools with the same name. Client loads both
  servers, behavior becomes unpredictable.
  
### **Why**
  MCP tool names are global within a client session. If two servers both
  define "search", the client may call either one arbitrarily. No namespace
  isolation by default.
  
### **Solution**
  Prefix tool names with server namespace:
  
  // BAD: Generic name
  const tools = [{
    name: 'search',
    description: 'Search for items'
  }];
  
  // GOOD: Namespaced name
  const tools = [{
    name: 'docs_search',  // or 'myapp_search'
    description: 'Search documentation'
  }];
  
  // Alternative: Use server name as automatic prefix
  class NamespacedServer extends Server {
    private namespace: string;
  
    constructor(namespace: string, config: ServerConfig) {
      super(config);
      this.namespace = namespace;
    }
  
    registerTool(name: string, handler: ToolHandler) {
      super.registerTool(`${this.namespace}_${name}`, handler);
    }
  }
  
  const server = new NamespacedServer('docs', { ... });
  server.registerTool('search', handleSearch);  // Becomes 'docs_search'
  
### **Symptoms**
  - Wrong tool called when multiple servers loaded
  - Intermittent failures depending on server load order
  - Tool works in isolation but not in production
### **Detection Pattern**
name:\s*['"](?:search|query|get|list|create|update|delete)['"]

## Zod Schema vs JSON Schema Mismatch

### **Id**
schema-type-mismatch
### **Severity**
critical
### **Situation**
  Using Zod schema internally but MCP expects JSON Schema. Tool fails
  validation or LLM misunderstands parameter types.
  
### **Why**
  MCP protocol uses JSON Schema format. If you pass Zod schema object
  directly, it won't be understood. Need to convert Zod to JSON Schema.
  
### **Solution**
  Use zod-to-json-schema or zodToJsonSchema:
  
  import { z } from 'zod';
  import { zodToJsonSchema } from 'zod-to-json-schema';
  
  // Define with Zod (for runtime validation)
  const inputSchema = z.object({
    query: z.string().min(1).describe('Search query'),
    limit: z.number().max(100).default(10).describe('Max results')
  });
  
  // Convert for MCP protocol
  const tool = {
    name: 'search',
    description: 'Search items',
    inputSchema: zodToJsonSchema(inputSchema, {
      $refStrategy: 'none'  // Inline all definitions
    })
  };
  
  // Validate input in handler
  server.setRequestHandler('tools/call', async (request) => {
    const { arguments: args } = request.params;
  
    const parsed = inputSchema.safeParse(args);
    if (!parsed.success) {
      return {
        content: [{
          type: 'text',
          text: `Validation error: ${parsed.error.message}`
        }],
        isError: true
      };
    }
  
    // Use parsed.data with full type safety
  });
  
### **Symptoms**
  - LLM passes wrong types to tools
  - Validation errors at runtime with valid-looking input
  - Type information missing from tool list
### **Detection Pattern**
inputSchema:\s*z\.|inputSchema:\s*zodSchema

## Stdio Buffering Causes Message Loss

### **Id**
stdio-buffering
### **Severity**
critical
### **Situation**
  MCP server using stdio transport loses messages or appears to hang.
  Works in development, fails in production or with certain clients.
  
### **Why**
  Node.js buffers stdout by default when not connected to TTY. Messages
  may not flush immediately. Long responses may be split across buffers.
  stderr logging can interleave with protocol messages.
  
### **Solution**
  Ensure proper stdio handling:
  
  // Force line-buffered output
  process.stdout.setDefaultEncoding('utf8');
  
  // DON'T use console.log for debugging (goes to stdout)
  // Use stderr instead
  const debug = (msg: string) => {
    process.stderr.write(`[DEBUG] ${msg}\n`);
  };
  
  // Or use environment variable to control logging
  const DEBUG = process.env.DEBUG === 'true';
  const log = DEBUG
    ? (msg: string) => process.stderr.write(`${msg}\n`)
    : () => {};
  
  // Ensure clean stdout
  const transport = new StdioServerTransport();
  
  // Handle uncaught errors to stderr, not stdout
  process.on('uncaughtException', (err) => {
    process.stderr.write(`Uncaught: ${err.message}\n`);
    process.exit(1);
  });
  
  // Don't let anything else write to stdout
  const originalStdoutWrite = process.stdout.write.bind(process.stdout);
  process.stdout.write = (chunk: any) => {
    // Only allow JSON-RPC messages
    if (typeof chunk === 'string' && chunk.startsWith('{')) {
      return originalStdoutWrite(chunk);
    }
    process.stderr.write(`[BLOCKED] ${chunk}`);
    return true;
  };
  
### **Symptoms**
  - Server appears to hang but is running
  - Messages received out of order
  - Works in terminal, fails when spawned
  - Partial JSON errors in client
### **Detection Pattern**
console\.log\(|process\.stdout\.write(?!.*JSON)

## Unhandled Errors Crash Server

### **Id**
missing-error-handling
### **Severity**
critical
### **Situation**
  Tool handler throws unhandled exception. Server crashes, client
  disconnects, all in-progress work lost.
  
### **Why**
  MCP SDK doesn't catch all exceptions by default. An unhandled throw
  in a tool handler can crash the process. Unlike HTTP servers, there's
  no request isolation.
  
### **Solution**
  Wrap all handlers with error boundary:
  
  function safeHandler<T>(
    handler: (request: T) => Promise<any>
  ): (request: T) => Promise<any> {
    return async (request) => {
      try {
        return await handler(request);
      } catch (error) {
        const message = error instanceof Error
          ? error.message
          : String(error);
  
        return {
          content: [{
            type: 'text',
            text: `Internal error: ${message}. Please try again or report this issue.`
          }],
          isError: true
        };
      }
    };
  }
  
  // Usage
  server.setRequestHandler('tools/call', safeHandler(async (request) => {
    // Handler code that might throw
  }));
  
  // Global fallback
  process.on('uncaughtException', (err) => {
    process.stderr.write(`Fatal: ${err.message}\n`);
    // Attempt graceful shutdown
    server.close().finally(() => process.exit(1));
  });
  
  process.on('unhandledRejection', (reason) => {
    process.stderr.write(`Unhandled rejection: ${reason}\n`);
  });
  
### **Symptoms**
  - Server process exits unexpectedly
  - Client reports connection lost
  - Works for most calls, crashes on edge cases
### **Detection Pattern**
setRequestHandler.*async.*=>(?!.*try|catch)

## Resource URIs Not Properly Encoded

### **Id**
resource-uri-encoding
### **Severity**
high
### **Situation**
  Resource URI contains special characters (spaces, unicode). Client
  can't fetch resource, gets encoding errors.
  
### **Why**
  Resource URIs are transmitted as strings. Special characters must be
  percent-encoded. Client may decode differently than server expects.
  
### **Solution**
  Use consistent URI encoding:
  
  // Encode when creating URI
  function createResourceUri(type: string, path: string): string {
    const encodedPath = encodeURIComponent(path);
    return `${type}://${encodedPath}`;
  }
  
  // Decode when reading
  function parseResourceUri(uri: string): { type: string; path: string } {
    const [type, ...rest] = uri.split('://');
    const path = decodeURIComponent(rest.join('://'));
    return { type, path };
  }
  
  // Usage
  const uri = createResourceUri('file', 'docs/My Document.md');
  // Result: "file://docs%2FMy%20Document.md"
  
  server.setRequestHandler('resources/read', async (request) => {
    const { type, path } = parseResourceUri(request.params.uri);
    // path is now decoded: "docs/My Document.md"
  });
  
  // Consistent in resource list
  server.setRequestHandler('resources/list', async () => ({
    resources: files.map(file => ({
      uri: createResourceUri('file', file.path),
      name: file.name,  // Human readable (not encoded)
      mimeType: file.mimeType
    }))
  }));
  
### **Symptoms**
  - Resources with spaces/unicode fail to load
  - URL encoding errors in client
  - Resource works in English, fails in other languages
### **Detection Pattern**
uri.*`[^`]*\$\{[^}]*\}[^`]*`(?!.*encode)

## Long-Running Tools Timeout Without Progress

### **Id**
tool-timeout
### **Severity**
high
### **Situation**
  Tool performs long operation (API call, file processing). Client or
  LLM assumes tool failed and retries or gives up.
  
### **Why**
  MCP has implicit timeout expectations. If a tool takes more than a few
  seconds without response, clients may consider it failed. LLMs have
  context limits that make waiting impractical.
  
### **Solution**
  Report progress for long operations:
  
  // For truly long operations, use progress notification
  server.setRequestHandler('tools/call', async (request) => {
    if (request.params.name === 'process_large_file') {
      const { path } = request.params.arguments;
      const lines = await countLines(path);
  
      let processed = 0;
      for await (const batch of processBatches(path)) {
        processed += batch.length;
  
        // Send progress notification
        await server.notification({
          method: 'notifications/progress',
          params: {
            progressToken: request.params._meta?.progressToken,
            progress: processed,
            total: lines
          }
        });
      }
  
      return {
        content: [{
          type: 'text',
          text: `Processed ${lines} lines`
        }]
      };
    }
  });
  
  // Alternative: Return immediately with status, poll for result
  const jobs = new Map<string, JobStatus>();
  
  const tools = [
    {
      name: 'start_long_task',
      description: 'Starts a long task, returns job ID to check status'
    },
    {
      name: 'check_job',
      description: 'Check status of a running job'
    }
  ];
  
### **Symptoms**
  - Tool works for small inputs, times out for large
  - Client retries tool unnecessarily
  - LLM says "the tool seems to have failed"
### **Detection Pattern**
await.*fetch|await.*exec|await.*process(?!.*progress|timeout)

## Assuming Client Maintains State

### **Id**
client-state-assumption
### **Severity**
high
### **Situation**
  Server expects client to remember previous tool calls. Client doesn't,
  or different client connects.
  
### **Why**
  MCP sessions can reconnect. Different LLM turns may be different sessions.
  Clients don't necessarily maintain state between reconnections.
  
### **Solution**
  Keep state server-side, return IDs for reference:
  
  // Server-side state
  const sessions = new Map<string, SessionState>();
  
  function getSession(transport: Transport): SessionState {
    const id = transport.sessionId;
    if (!sessions.has(id)) {
      sessions.set(id, {
        userId: null,
        context: {},
        history: []
      });
    }
    return sessions.get(id)!;
  }
  
  server.setRequestHandler('tools/call', async (request) => {
    const session = getSession(request.transport);
  
    if (request.params.name === 'login') {
      // Store auth state server-side
      session.userId = await authenticate(request.params.arguments);
      return { content: [{ type: 'text', text: 'Logged in successfully' }] };
    }
  
    if (request.params.name === 'get_my_data') {
      if (!session.userId) {
        return {
          content: [{ type: 'text', text: 'Not logged in. Use login tool first.' }],
          isError: true
        };
      }
      // Use session.userId...
    }
  });
  
  // Clean up on disconnect
  transport.on('close', () => {
    sessions.delete(transport.sessionId);
  });
  
### **Symptoms**
  - Works on first call, fails on subsequent
  - Works in one conversation, fails in next
  - Authentication state lost randomly
### **Detection Pattern**
request\.params\.[^.]+\.userId|args\.sessionId

## Non-JSON Content Returned as JSON

### **Id**
json-content-type
### **Severity**
medium
### **Situation**
  Tool returns binary data, images, or other non-JSON content in
  text content type. Client fails to display or process it.
  
### **Why**
  MCP content types are limited. Binary content must be base64 encoded.
  Returning raw binary as text corrupts the data and breaks clients.
  
### **Solution**
  Use appropriate content types:
  
  server.setRequestHandler('tools/call', async (request) => {
    if (request.params.name === 'get_image') {
      const imageBuffer = await loadImage(request.params.arguments.path);
  
      return {
        content: [{
          type: 'image',
          data: imageBuffer.toString('base64'),
          mimeType: 'image/png'
        }]
      };
    }
  
    if (request.params.name === 'get_file') {
      const { path } = request.params.arguments;
      const content = await fs.readFile(path);
      const mimeType = getMimeType(path);
  
      if (isBinary(mimeType)) {
        return {
          content: [{
            type: 'resource',
            resource: {
              uri: `file://${path}`,
              mimeType,
              blob: content.toString('base64')
            }
          }]
        };
      }
  
      return {
        content: [{
          type: 'text',
          text: content.toString('utf8')
        }]
      };
    }
  });
  
### **Symptoms**
  - Binary files corrupted when retrieved
  - Images display as garbage text
  - Client reports invalid content
### **Detection Pattern**
type:\s*['"]text['"].*binary|buffer|image

## Tool Input Used in Prompts Without Sanitization

### **Id**
prompt-injection-via-input
### **Severity**
high
### **Situation**
  Tool takes user input, incorporates it into prompts or templates
  returned to LLM. Attacker crafts input to hijack LLM behavior.
  
### **Why**
  Tool outputs become part of LLM context. Malicious input like
  "ignore previous instructions and..." can alter LLM behavior if
  not properly handled.
  
### **Solution**
  Sanitize and isolate user input:
  
  // BAD: Direct interpolation
  server.setRequestHandler('tools/call', async (request) => {
    const { query } = request.params.arguments;
    return {
      content: [{
        type: 'text',
        text: `Search results for: ${query}\n\n${results}`
      }]
    };
  });
  
  // GOOD: Structured output with clear boundaries
  server.setRequestHandler('tools/call', async (request) => {
    const { query } = request.params.arguments;
  
    // Escape any control characters
    const sanitizedQuery = query
      .replace(/[\x00-\x1F\x7F]/g, '')  // Control chars
      .substring(0, 1000);  // Length limit
  
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          query: sanitizedQuery,
          resultCount: results.length,
          results: results.map(r => ({
            title: r.title,
            snippet: r.snippet.substring(0, 200)
          }))
        }, null, 2)
      }]
    };
  });
  
  // Return as structured data, not prose
  // LLM interprets JSON data differently than narrative text
  
### **Symptoms**
  - LLM behaves unexpectedly after certain tool calls
  - Tool output appears to contain instructions
  - Security audit flags injection risks
### **Detection Pattern**
text:.*`.*\$\{.*input|query|search.*\}`

## SSE Connection Limits Exhausted

### **Id**
sse-connection-limits
### **Severity**
medium
### **Situation**
  SSE-based MCP server accepts many connections. Browser or server
  hits connection limit, new clients can't connect.
  
### **Why**
  Browsers limit concurrent connections per domain (usually 6). SSE
  connections are long-lived. Servers may have file descriptor limits.
  Each tab/window may open new connection.
  
### **Solution**
  Implement connection management:
  
  class ConnectionManager {
    private connections = new Map<string, SSEServerTransport>();
    private maxConnections = parseInt(process.env.MAX_CONNECTIONS || '100');
  
    canAccept(): boolean {
      return this.connections.size < this.maxConnections;
    }
  
    add(id: string, transport: SSEServerTransport): boolean {
      if (!this.canAccept()) {
        return false;
      }
  
      // Check for duplicate from same user/session
      const existing = this.findBySession(transport.sessionId);
      if (existing) {
        this.remove(existing.id);  // Replace old connection
      }
  
      this.connections.set(id, transport);
      return true;
    }
  
    remove(id: string): void {
      const transport = this.connections.get(id);
      if (transport) {
        transport.close();
        this.connections.delete(id);
      }
    }
  }
  
  app.get('/mcp/sse', (req, res) => {
    if (!connectionManager.canAccept()) {
      return res.status(503).json({
        error: 'Too many connections',
        retryAfter: 30
      });
    }
  
    // Proceed with connection...
  });
  
  // Client-side: Share connection across tabs
  // Use SharedWorker or BroadcastChannel
  
### **Symptoms**
  - New clients can't connect
  - Browser shows connection pending indefinitely
  - Server logs show many active connections
### **Detection Pattern**
app\.get.*sse(?!.*limit|max|connections)

## Stale Resources After Update

### **Id**
resource-caching-stale
### **Severity**
medium
### **Situation**
  Resource content changes, but client shows old cached version.
  No mechanism to notify of resource changes.
  
### **Why**
  MCP doesn't have built-in resource change notifications (except
  for resources with notifications capability). Clients may cache
  resource content without knowing when to refresh.
  
### **Solution**
  Implement resource change notifications:
  
  const server = new Server({
    name: 'docs-server',
    version: '1.0.0'
  }, {
    capabilities: {
      resources: {
        subscribe: true  // Enable subscriptions
      }
    }
  });
  
  // Track subscriptions
  const subscriptions = new Map<string, Set<string>>();  // uri -> sessionIds
  
  server.setRequestHandler('resources/subscribe', async (request) => {
    const { uri } = request.params;
    const sessionId = request.transport.sessionId;
  
    if (!subscriptions.has(uri)) {
      subscriptions.set(uri, new Set());
    }
    subscriptions.get(uri)!.add(sessionId);
  
    return {};
  });
  
  // Notify on changes
  async function notifyResourceChange(uri: string): Promise<void> {
    const subscribers = subscriptions.get(uri);
    if (!subscribers) return;
  
    for (const sessionId of subscribers) {
      const transport = getTransport(sessionId);
      if (transport) {
        await transport.send({
          jsonrpc: '2.0',
          method: 'notifications/resources/updated',
          params: { uri }
        });
      }
    }
  }
  
  // Call when resource changes
  fs.watch(docsDir, (event, filename) => {
    const uri = `docs://${filename}`;
    notifyResourceChange(uri);
  });
  
### **Symptoms**
  - Changes not reflected until restart
  - Users report seeing old content
  - Cache-control headers not respected
### **Detection Pattern**
resources/read(?!.*subscribe|notify|watch)