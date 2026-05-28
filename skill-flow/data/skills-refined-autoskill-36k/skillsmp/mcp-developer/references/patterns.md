# MCP Developer

## Patterns


---
  #### **Name**
Minimal Tool Definition
  #### **Description**
Tools with clear, focused scope and intuitive parameters
  #### **When**
Creating new MCP tools
  #### **Example**
    import { z } from 'zod';
    
    // BAD: Kitchen sink tool
    const badTool = {
      name: 'manage_database',
      description: 'Manage database operations',
      inputSchema: z.object({
        action: z.enum(['create', 'read', 'update', 'delete', 'list', 'backup', 'restore']),
        table: z.string(),
        id: z.string().optional(),
        data: z.record(z.any()).optional(),
        filter: z.record(z.any()).optional(),
        limit: z.number().optional(),
        // ... 10 more optional fields
      })
    };
    
    // GOOD: Atomic, focused tools
    const listUsers = {
      name: 'list_users',
      description: 'List users with optional filtering. Returns array of {id, name, email}.',
      inputSchema: z.object({
        limit: z.number().max(100).default(20).describe('Max users to return'),
        email_contains: z.string().optional().describe('Filter by email substring')
      })
    };
    
    const getUser = {
      name: 'get_user',
      description: 'Get a single user by ID. Returns full user profile.',
      inputSchema: z.object({
        user_id: z.string().describe('The user ID from list_users')
      })
    };
    
    const updateUser = {
      name: 'update_user',
      description: 'Update user fields. Only provided fields are changed.',
      inputSchema: z.object({
        user_id: z.string().describe('The user ID to update'),
        name: z.string().optional().describe('New display name'),
        email: z.string().email().optional().describe('New email address')
      })
    };
    

---
  #### **Name**
Resource with URI Template
  #### **Description**
Expose data sources via resource URIs for LLM browsing
  #### **When**
Exposing data that LLM should browse or reference
  #### **Example**
    import { Server } from '@modelcontextprotocol/sdk/server/index.js';
    
    const server = new Server({
      name: 'docs-server',
      version: '1.0.0'
    }, {
      capabilities: {
        resources: {}
      }
    });
    
    // List available resources
    server.setRequestHandler('resources/list', async () => {
      return {
        resources: [
          {
            uri: 'docs://api/endpoints',
            name: 'API Endpoints',
            description: 'List of all REST API endpoints',
            mimeType: 'text/markdown'
          },
          {
            uri: 'docs://api/errors',
            name: 'Error Codes',
            description: 'API error codes and meanings',
            mimeType: 'application/json'
          }
        ]
      };
    });
    
    // Read specific resource
    server.setRequestHandler('resources/read', async (request) => {
      const { uri } = request.params;
    
      switch (uri) {
        case 'docs://api/endpoints':
          return {
            contents: [{
              uri,
              mimeType: 'text/markdown',
              text: await loadEndpointsDoc()
            }]
          };
    
        case 'docs://api/errors':
          return {
            contents: [{
              uri,
              mimeType: 'application/json',
              text: JSON.stringify(errorCodes, null, 2)
            }]
          };
    
        default:
          throw new Error(`Unknown resource: ${uri}`);
      }
    });
    

---
  #### **Name**
Prompt Template with Arguments
  #### **Description**
Reusable prompt templates with variable slots
  #### **When**
Providing structured prompts for common operations
  #### **Example**
    server.setRequestHandler('prompts/list', async () => {
      return {
        prompts: [
          {
            name: 'code_review',
            description: 'Review code for issues and improvements',
            arguments: [
              {
                name: 'language',
                description: 'Programming language',
                required: true
              },
              {
                name: 'focus',
                description: 'What to focus on: security, performance, style',
                required: false
              }
            ]
          }
        ]
      };
    });
    
    server.setRequestHandler('prompts/get', async (request) => {
      const { name, arguments: args } = request.params;
    
      if (name === 'code_review') {
        const language = args?.language || 'unknown';
        const focus = args?.focus || 'all aspects';
    
        return {
          messages: [
            {
              role: 'user',
              content: {
                type: 'text',
                text: `Review the following ${language} code, focusing on ${focus}.
                       Identify issues and suggest improvements.`
              }
            }
          ]
        };
      }
    
      throw new Error(`Unknown prompt: ${name}`);
    });
    

---
  #### **Name**
Stdio Transport Server
  #### **Description**
MCP server using stdio for Claude Desktop integration
  #### **When**
Building servers for local Claude Desktop use
  #### **Example**
    import { Server } from '@modelcontextprotocol/sdk/server/index.js';
    import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
    
    const server = new Server({
      name: 'my-mcp-server',
      version: '1.0.0'
    }, {
      capabilities: {
        tools: {},
        resources: {}
      }
    });
    
    // Register tools
    server.setRequestHandler('tools/list', async () => ({
      tools: [
        {
          name: 'greet',
          description: 'Generate a greeting',
          inputSchema: {
            type: 'object',
            properties: {
              name: { type: 'string', description: 'Name to greet' }
            },
            required: ['name']
          }
        }
      ]
    }));
    
    server.setRequestHandler('tools/call', async (request) => {
      const { name, arguments: args } = request.params;
    
      if (name === 'greet') {
        return {
          content: [{
            type: 'text',
            text: `Hello, ${args.name}!`
          }]
        };
      }
    
      throw new Error(`Unknown tool: ${name}`);
    });
    
    // Connect via stdio
    const transport = new StdioServerTransport();
    await server.connect(transport);
    

---
  #### **Name**
SSE Transport for Remote Servers
  #### **Description**
HTTP + Server-Sent Events transport for web deployment
  #### **When**
Deploying MCP server as web service
  #### **Example**
    import { Server } from '@modelcontextprotocol/sdk/server/index.js';
    import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
    import express from 'express';
    
    const app = express();
    const server = new Server({
      name: 'remote-mcp',
      version: '1.0.0'
    }, {
      capabilities: { tools: {} }
    });
    
    // Store active transports
    const transports = new Map<string, SSEServerTransport>();
    
    // SSE endpoint for clients
    app.get('/mcp/sse', async (req, res) => {
      const sessionId = crypto.randomUUID();
    
      const transport = new SSEServerTransport('/mcp/message', res);
      transports.set(sessionId, transport);
    
      res.on('close', () => {
        transports.delete(sessionId);
      });
    
      await server.connect(transport);
    });
    
    // Message endpoint for client requests
    app.post('/mcp/message', express.json(), async (req, res) => {
      const sessionId = req.headers['x-session-id'] as string;
      const transport = transports.get(sessionId);
    
      if (!transport) {
        return res.status(404).json({ error: 'Session not found' });
      }
    
      await transport.handlePostMessage(req, res);
    });
    
    app.listen(3000);
    

---
  #### **Name**
Actionable Error Responses
  #### **Description**
Errors that guide LLM toward resolution
  #### **When**
Handling tool errors
  #### **Example**
    server.setRequestHandler('tools/call', async (request) => {
      const { name, arguments: args } = request.params;
    
      if (name === 'create_file') {
        // BAD: Vague error
        // throw new Error('Invalid path');
    
        // GOOD: Actionable error
        if (!args.path) {
          return {
            content: [{
              type: 'text',
              text: 'Error: path is required. Example: create_file({ path: "src/index.ts", content: "..." })'
            }],
            isError: true
          };
        }
    
        if (args.path.includes('..')) {
          return {
            content: [{
              type: 'text',
              text: 'Error: path cannot contain "..". Use absolute paths from project root. Current allowed roots: /src, /tests'
            }],
            isError: true
          };
        }
    
        if (await fileExists(args.path)) {
          return {
            content: [{
              type: 'text',
              text: `Error: ${args.path} already exists. Use update_file to modify existing files, or delete_file first.`
            }],
            isError: true
          };
        }
    
        // Proceed with creation...
      }
    });
    

## Anti-Patterns


---
  #### **Name**
Mega-Tool
  #### **Description**
One tool that does many unrelated things via mode parameter
  #### **Why**
    LLMs struggle with tools that have many optional parameters and mode switches.
    They pick wrong modes, forget required parameters for each mode, and generate
    invalid combinations. Error messages become confusing.
    
  #### **Instead**
Create separate, focused tools. "create_file", "read_file", "delete_file" instead of "file_operation"

---
  #### **Name**
Implicit Schema
  #### **Description**
Not using Zod or JSON Schema for input validation
  #### **Why**
    LLMs read your schema to understand what to pass. Without explicit schema,
    they guess parameter names and types. You get runtime errors instead of
    validation errors.
    
  #### **Instead**
Always define inputSchema with descriptions for every parameter

---
  #### **Name**
Tools That Print
  #### **Description**
Tools that output directly instead of returning content
  #### **Why**
    MCP tools communicate through structured responses. console.log output
    is lost. The LLM never sees what your tool printed.
    
  #### **Instead**
Return all output in the content array of tool response

---
  #### **Name**
Blocking Operations in Handlers
  #### **Description**
Long-running sync operations in tool handlers
  #### **Why**
    MCP uses async messaging. Blocking operations freeze the server, timeout
    clients, and make the LLM think the tool failed.
    
  #### **Instead**
Use async operations, return progress indicators for long tasks

---
  #### **Name**
Secrets in Tool Output
  #### **Description**
Including API keys or tokens in tool responses
  #### **Why**
    Tool responses go to the LLM. Secrets in responses can leak into conversation
    history, logs, or LLM outputs to users.
    
  #### **Instead**
Never include secrets in responses. Use server-side storage.

---
  #### **Name**
Stateless Tool Assumption
  #### **Description**
Designing tools without considering session state
  #### **Why**
    MCP sessions are stateful. A tool that requires re-authentication on every
    call frustrates users and wastes tokens.
    
  #### **Instead**
Maintain session state server-side, initialize once per session