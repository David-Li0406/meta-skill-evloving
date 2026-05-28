# MCP Security

## Patterns


---
  #### **Name**
OAuth 2.0 Implementation
  #### **Description**
Implement OAuth 2.0 for user authentication
  #### **When**
Server needs to identify users or access user resources
  #### **Example**
    import { OAuthProvider } from '@mcp/oauth';
    
    const oauth = new OAuthProvider({
        clientId: process.env.OAUTH_CLIENT_ID,
        clientSecret: process.env.OAUTH_CLIENT_SECRET,
        authorizationUrl: 'https://auth.example.com/authorize',
        tokenUrl: 'https://auth.example.com/token',
        scopes: ['read', 'write']
    });
    
    server.setRequestHandler(CallToolRequestSchema, async (request, context) => {
        // Verify OAuth token
        const user = await oauth.verifyToken(context.authToken);
        if (!user) {
            return {
                content: [{
                    type: "text",
                    text: "Authentication required. Please connect your account."
                }],
                isError: true
            };
        }
    
        // Check authorization for specific tool
        if (!user.scopes.includes(requiredScope(request.params.name))) {
            return {
                content: [{
                    type: "text",
                    text: `Permission denied. Required scope: ${requiredScope(request.params.name)}`
                }],
                isError: true
            };
        }
    
        // Proceed with authenticated request
        return handleTool(request, user);
    });
    

---
  #### **Name**
Rate Limiting
  #### **Description**
Implement per-user and global rate limits
  #### **When**
Any production MCP server
  #### **Example**
    import { RateLimiterRedis } from 'rate-limiter-flexible';
    import Redis from 'ioredis';
    
    const redis = new Redis(process.env.REDIS_URL);
    
    // Per-user rate limiter
    const userLimiter = new RateLimiterRedis({
        storeClient: redis,
        keyPrefix: 'mcp_user_',
        points: 100,        // 100 requests
        duration: 60,       // per 60 seconds
        blockDuration: 60,  // block for 60 seconds if exceeded
    });
    
    // Per-tool rate limiter (expensive operations)
    const expensiveLimiter = new RateLimiterRedis({
        storeClient: redis,
        keyPrefix: 'mcp_expensive_',
        points: 10,
        duration: 60,
    });
    
    async function checkRateLimit(userId: string, toolName: string) {
        try {
            await userLimiter.consume(userId);
    
            if (isExpensiveTool(toolName)) {
                await expensiveLimiter.consume(`${userId}_${toolName}`);
            }
    
            return { allowed: true };
        } catch (error) {
            return {
                allowed: false,
                retryAfter: Math.ceil(error.msBeforeNext / 1000),
                message: `Rate limit exceeded. Retry in ${Math.ceil(error.msBeforeNext / 1000)} seconds.`
            };
        }
    }
    

---
  #### **Name**
Input Validation
  #### **Description**
Strict validation of all tool inputs
  #### **When**
Any tool that accepts parameters
  #### **Example**
    import { z } from 'zod';
    
    // Define strict schemas per tool
    const schemas = {
        search_files: z.object({
            query: z.string()
                .min(1, "Query required")
                .max(200, "Query too long")
                .refine(s => !s.includes('..'), "Path traversal not allowed"),
            path: z.string()
                .startsWith('/', "Must be absolute path")
                .refine(s => !s.includes('..'), "Path traversal not allowed")
                .optional(),
            limit: z.number().int().min(1).max(100).default(10)
        }),
    
        execute_command: z.object({
            command: z.string()
                .max(1000)
                // Whitelist allowed commands
                .refine(cmd => ALLOWED_COMMANDS.some(ac =>
                    cmd.startsWith(ac)
                ), "Command not allowed"),
            timeout: z.number().int().min(1000).max(30000).default(5000)
        })
    };
    
    function validateInput(toolName: string, args: unknown) {
        const schema = schemas[toolName];
        if (!schema) {
            throw new Error(`Unknown tool: ${toolName}`);
        }
    
        const result = schema.safeParse(args);
        if (!result.success) {
            throw new ValidationError(result.error.message);
        }
    
        return result.data;
    }
    

---
  #### **Name**
Audit Logging
  #### **Description**
Log all tool calls for security audit
  #### **When**
Any production MCP server
  #### **Example**
    interface AuditLog {
        timestamp: string;
        requestId: string;
        userId: string;
        tool: string;
        arguments: Record<string, unknown>;
        result: 'success' | 'error' | 'denied';
        duration: number;
        metadata: Record<string, unknown>;
    }
    
    class AuditLogger {
        async log(entry: AuditLog) {
            // Sanitize sensitive data before logging
            const sanitized = this.sanitize(entry);
    
            // Log to multiple destinations
            await Promise.all([
                this.logToDatabase(sanitized),
                this.logToCloudWatch(sanitized),
            ]);
    
            // Alert on suspicious patterns
            if (this.isSuspicious(entry)) {
                await this.alert(entry);
            }
        }
    
        private sanitize(entry: AuditLog): AuditLog {
            // Remove sensitive fields
            const sanitizedArgs = { ...entry.arguments };
            for (const key of SENSITIVE_FIELDS) {
                if (sanitizedArgs[key]) {
                    sanitizedArgs[key] = '[REDACTED]';
                }
            }
            return { ...entry, arguments: sanitizedArgs };
        }
    
        private isSuspicious(entry: AuditLog): boolean {
            return (
                entry.result === 'denied' ||
                entry.arguments.toString().includes('..') ||
                this.rateTooHigh(entry.userId)
            );
        }
    }
    

## Anti-Patterns


---
  #### **Name**
IP Allowlisting Only
  #### **Description**
Relying on IP allowlisting for security
  #### **Why**
Claude's IPs can be shared, doesn't identify users
  #### **Instead**
Use OAuth 2.0 for authentication.

---
  #### **Name**
No Rate Limiting
  #### **Description**
Allowing unlimited requests
  #### **Why**
AI can make thousands of requests, draining resources or money
  #### **Instead**
Implement per-user and per-tool rate limits.

---
  #### **Name**
Trusting AI Input
  #### **Description**
Using AI-provided input without validation
  #### **Why**
AI can be manipulated, sends unexpected data
  #### **Instead**
Validate everything with strict schemas.

---
  #### **Name**
Silent Denials
  #### **Description**
Silently failing on auth/permission issues
  #### **Why**
AI continues with wrong assumptions
  #### **Instead**
Return clear error with required action.