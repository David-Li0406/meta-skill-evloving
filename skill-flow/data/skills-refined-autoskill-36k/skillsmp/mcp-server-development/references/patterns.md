# MCP Server Development

## Patterns


---
  #### **Name**
High-Level Tool Design
  #### **Description**
Design tools for AI understanding, not API mirroring
  #### **When**
Defining MCP server tools
  #### **Example**
    // BAD: Low-level API mirroring
    // These tools force AI to understand your API's quirks
    tools: [
        { name: "create_user", ... },
        { name: "set_user_role", ... },
        { name: "add_user_to_team", ... },
        { name: "send_welcome_email", ... },
    ]
    
    // GOOD: High-level operations
    // AI understands intent, server handles orchestration
    server.setRequestHandler(ListToolsRequestSchema, async () => ({
        tools: [
            {
                name: "onboard_team_member",
                description: `
                    Onboard a new team member completely.
                    Creates user, assigns role, adds to team,
                    sends welcome email, and returns credentials.
                    Use this when adding someone to the organization.
                `,
                inputSchema: {
                    type: "object",
                    properties: {
                        email: {
                            type: "string",
                            description: "Email address for the new member"
                        },
                        role: {
                            type: "string",
                            enum: ["admin", "member", "viewer"],
                            description: "Permission level"
                        },
                        team: {
                            type: "string",
                            description: "Team to add member to"
                        }
                    },
                    required: ["email", "role", "team"]
                }
            }
        ]
    }));
    

---
  #### **Name**
Strict Schema Validation
  #### **Description**
Validate all inputs with Zod or similar
  #### **When**
Implementing any tool handler
  #### **Example**
    import { z } from 'zod';
    
    // Define strict schemas
    const CreateProjectSchema = z.object({
        name: z.string()
            .min(1, "Name required")
            .max(100, "Name too long")
            .regex(/^[a-z0-9-]+$/, "Lowercase, numbers, hyphens only"),
        template: z.enum(["web", "api", "mobile"]),
        settings: z.object({
            isPublic: z.boolean().default(false),
            language: z.enum(["typescript", "python", "go"]).optional()
        }).optional()
    });
    
    // Validate in handler
    server.setRequestHandler(CallToolRequestSchema, async (request) => {
        if (request.params.name === "create_project") {
            // Parse and validate
            const parseResult = CreateProjectSchema.safeParse(
                request.params.arguments
            );
    
            if (!parseResult.success) {
                return {
                    content: [{
                        type: "text",
                        text: `Invalid input: ${parseResult.error.message}`
                    }],
                    isError: true
                };
            }
    
            // Use validated data
            const { name, template, settings } = parseResult.data;
            // ... implementation
        }
    });
    

---
  #### **Name**
Resources for Context
  #### **Description**
Use resources to provide readable context, not actions
  #### **When**
AI needs information but shouldn't act on it yet
  #### **Example**
    // Resources provide context that AI reads before acting
    
    server.setRequestHandler(ListResourcesRequestSchema, async () => ({
        resources: [
            {
                uri: "project://current/structure",
                name: "Project Structure",
                description: "Current project files and organization",
                mimeType: "application/json"
            },
            {
                uri: "project://current/config",
                name: "Project Configuration",
                description: "Settings and environment config",
                mimeType: "application/json"
            },
            {
                uri: "database://schema",
                name: "Database Schema",
                description: "Current database tables and relationships",
                mimeType: "text/plain"
            }
        ]
    }));
    
    server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
        const uri = request.params.uri;
    
        if (uri === "project://current/structure") {
            const structure = await getProjectStructure();
            return {
                contents: [{
                    uri,
                    mimeType: "application/json",
                    text: JSON.stringify(structure, null, 2)
                }]
            };
        }
    
        if (uri === "database://schema") {
            const schema = await getDatabaseSchema();
            return {
                contents: [{
                    uri,
                    mimeType: "text/plain",
                    text: formatSchemaAsText(schema)
                }]
            };
        }
    
        throw new Error(`Unknown resource: ${uri}`);
    });
    

---
  #### **Name**
Prompts as Workflows
  #### **Description**
Use prompts to guide complex multi-step operations
  #### **When**
AI needs structured guidance for common tasks
  #### **Example**
    server.setRequestHandler(ListPromptsRequestSchema, async () => ({
        prompts: [
            {
                name: "debug_error",
                description: "Structured workflow for debugging errors",
                arguments: [
                    {
                        name: "error_message",
                        description: "The error message to debug",
                        required: true
                    }
                ]
            },
            {
                name: "code_review",
                description: "Systematic code review workflow",
                arguments: [
                    {
                        name: "file_path",
                        description: "File to review",
                        required: true
                    }
                ]
            }
        ]
    }));
    
    server.setRequestHandler(GetPromptRequestSchema, async (request) => {
        if (request.params.name === "debug_error") {
            const errorMsg = request.params.arguments?.error_message;
            return {
                messages: [
                    {
                        role: "user",
                        content: {
                            type: "text",
                            text: `Debug this error systematically:
    
            Error: ${errorMsg}
    
            Step 1: Read the relevant source file
            Step 2: Check recent changes (git log)
            Step 3: Search for similar patterns
            Step 4: Identify root cause
            Step 5: Propose fix with explanation
    
            Start with Step 1.`
                        }
                    }
                ]
            };
        }
    });
    

---
  #### **Name**
Error Handling with Context
  #### **Description**
Return errors that help AI understand and recover
  #### **When**
Any tool call might fail
  #### **Example**
    async function handleTool(request: CallToolRequest) {
        try {
            const result = await executeToolLogic(request);
            return {
                content: [{
                    type: "text",
                    text: JSON.stringify(result)
                }]
            };
        } catch (error) {
            // Provide actionable error info
            return {
                content: [{
                    type: "text",
                    text: formatError(error)
                }],
                isError: true
            };
        }
    }
    
    function formatError(error: Error): string {
        // AI-friendly error format
        return JSON.stringify({
            error: true,
            type: error.name,
            message: error.message,
            // Suggest recovery actions
            suggestions: getSuggestions(error),
            // Context for debugging
            context: {
                timestamp: new Date().toISOString(),
                requestId: getCurrentRequestId()
            }
        });
    }
    
    function getSuggestions(error: Error): string[] {
        if (error.message.includes("not found")) {
            return [
                "Verify the resource exists",
                "Check spelling and case sensitivity",
                "List available resources first"
            ];
        }
        if (error.message.includes("permission")) {
            return [
                "Verify user has required permissions",
                "Check authentication status"
            ];
        }
        return ["Retry the operation", "Contact support if issue persists"];
    }
    

## Anti-Patterns


---
  #### **Name**
Tool Explosion
  #### **Description**
Creating a tool for every API endpoint
  #### **Why**
LLMs struggle with many tools, makes selection unreliable
  #### **Instead**
Group related operations into higher-level tools.

---
  #### **Name**
Untyped Inputs
  #### **Description**
Accepting arbitrary JSON without schema
  #### **Why**
AI sends unexpected data, causes runtime errors
  #### **Instead**
Use Zod or JSON Schema, validate everything.

---
  #### **Name**
Silent Failures
  #### **Description**
Returning success when operations fail
  #### **Why**
AI continues with bad state, makes worse decisions
  #### **Instead**
Return isError: true with clear error message and suggestions.

---
  #### **Name**
Sync-Only Operations
  #### **Description**
Blocking on long-running operations
  #### **Why**
Timeouts, poor UX, resource exhaustion
  #### **Instead**
Use async patterns, return job IDs for long operations.

---
  #### **Name**
No Logging
  #### **Description**
Not logging tool calls and responses
  #### **Why**
Can't debug AI behavior, miss patterns
  #### **Instead**
Log every request/response with correlation IDs.