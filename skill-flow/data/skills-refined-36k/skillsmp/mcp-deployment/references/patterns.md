# MCP Deployment

## Patterns


---
  #### **Name**
Docker Containerization
  #### **Description**
Package MCP server as Docker container
  #### **When**
Any production deployment
  #### **Example**
    # Dockerfile for MCP server
    FROM node:20-slim
    
    WORKDIR /app
    
    # Install dependencies
    COPY package*.json ./
    RUN npm ci --only=production
    
    # Copy source
    COPY dist/ ./dist/
    
    # Security: Non-root user
    RUN addgroup --system mcp && adduser --system --group mcp
    USER mcp
    
    # Health check
    HEALTHCHECK --interval=30s --timeout=3s \
      CMD curl -f http://localhost:3000/health || exit 1
    
    # Expose port for HTTP transport
    EXPOSE 3000
    
    # Start server
    CMD ["node", "dist/index.js"]
    
    # docker-compose.yml
    version: '3.8'
    services:
      mcp-server:
        build: .
        ports:
          - "3000:3000"
        environment:
          - NODE_ENV=production
          - OAUTH_CLIENT_ID=${OAUTH_CLIENT_ID}
          - REDIS_URL=redis://redis:6379
        depends_on:
          - redis
        restart: unless-stopped
    
      redis:
        image: redis:7-alpine
        volumes:
          - redis-data:/data
    
    volumes:
      redis-data:
    

---
  #### **Name**
Transport Selection
  #### **Description**
Choose appropriate MCP transport for deployment
  #### **When**
Planning MCP server architecture
  #### **Example**
    // Transport options and when to use
    
    // 1. stdio - Local development, Claude Code
    // - Simple, no network
    // - No horizontal scaling
    // - Used by Claude Code CLI
    const stdioServer = new Server({
        transport: new StdioServerTransport()
    });
    
    // 2. Streamable HTTP - Production, scalable
    // - HTTP/SSE for streaming
    // - Horizontally scalable (with session affinity)
    // - Works behind load balancers
    const httpServer = new Server({
        transport: new StreamableHTTPTransport({
            port: 3000,
            path: '/mcp'
        })
    });
    
    // 3. Remote MCP (for Claude.ai)
    // - HTTPS required
    // - OAuth 2.0 required
    // - Must be publicly accessible
    // Follow: https://docs.anthropic.com/claude/docs/custom-connectors
    
    // Decision matrix:
    // | Use Case           | Transport        |
    // |--------------------|------------------|
    // | Local dev          | stdio            |
    // | Claude Code        | stdio            |
    // | Production API     | Streamable HTTP  |
    // | Claude.ai Custom   | Remote MCP       |
    // | Edge deployment    | Streamable HTTP  |
    

---
  #### **Name**
Monitoring Setup
  #### **Description**
Monitor MCP server health and usage
  #### **When**
Any production deployment
  #### **Example**
    import { metrics } from './metrics';
    
    // Track key MCP metrics
    const mcpMetrics = {
        toolCalls: new metrics.Counter({
            name: 'mcp_tool_calls_total',
            help: 'Total number of tool calls',
            labelNames: ['tool', 'status']
        }),
    
        toolLatency: new metrics.Histogram({
            name: 'mcp_tool_latency_seconds',
            help: 'Tool call latency',
            labelNames: ['tool'],
            buckets: [0.1, 0.5, 1, 2, 5, 10]
        }),
    
        activeConnections: new metrics.Gauge({
            name: 'mcp_active_connections',
            help: 'Number of active MCP connections'
        }),
    
        rateLimitHits: new metrics.Counter({
            name: 'mcp_rate_limit_hits_total',
            help: 'Number of rate limit hits',
            labelNames: ['user', 'tool']
        })
    };
    
    // Instrument handlers
    server.setRequestHandler(CallToolRequestSchema, async (request) => {
        const timer = mcpMetrics.toolLatency.startTimer({
            tool: request.params.name
        });
    
        try {
            const result = await handleTool(request);
            mcpMetrics.toolCalls.inc({
                tool: request.params.name,
                status: result.isError ? 'error' : 'success'
            });
            return result;
        } finally {
            timer();
        }
    });
    
    // Expose metrics endpoint
    app.get('/metrics', async (req, res) => {
        res.set('Content-Type', metrics.contentType);
        res.end(await metrics.register.metrics());
    });
    

---
  #### **Name**
Scaling Patterns
  #### **Description**
Scale MCP servers for high traffic
  #### **When**
Expecting significant usage
  #### **Example**
    // Stateless design for horizontal scaling
    
    // 1. No in-memory state (use Redis)
    import { Redis } from 'ioredis';
    const redis = new Redis(process.env.REDIS_URL);
    
    async function getSession(sessionId: string) {
        const data = await redis.get(`session:${sessionId}`);
        return data ? JSON.parse(data) : null;
    }
    
    // 2. Load balancer with session affinity
    // For Streamable HTTP with SSE:
    // nginx.conf:
    // upstream mcp {
    //     ip_hash;  # Session affinity
    //     server mcp1:3000;
    //     server mcp2:3000;
    //     server mcp3:3000;
    // }
    
    // 3. Kubernetes horizontal autoscaling
    // apiVersion: autoscaling/v2
    // kind: HorizontalPodAutoscaler
    // metadata:
    //   name: mcp-server
    // spec:
    //   scaleTargetRef:
    //     apiVersion: apps/v1
    //     kind: Deployment
    //     name: mcp-server
    //   minReplicas: 2
    //   maxReplicas: 10
    //   metrics:
    //   - type: Resource
    //     resource:
    //       name: cpu
    //       target:
    //         type: Utilization
    //         averageUtilization: 70
    
    // 4. Warm pools for cold start
    // Keep minimum replicas always running
    // Pre-warm database connections
    // Cache frequently accessed data
    

## Anti-Patterns


---
  #### **Name**
Local-Only Testing
  #### **Description**
Only testing locally before deployment
  #### **Why**
Network, auth, and scaling issues only appear in production
  #### **Instead**
Test in staging environment with production-like conditions.

---
  #### **Name**
No Monitoring
  #### **Description**
Deploying without observability
  #### **Why**
Can't debug issues, don't know usage patterns
  #### **Instead**
Set up metrics, logging, and alerting before launch.

---
  #### **Name**
Stateful Servers
  #### **Description**
Storing state in memory between requests
  #### **Why**
Can't scale horizontally, state lost on restart
  #### **Instead**
Use external state storage (Redis, database).