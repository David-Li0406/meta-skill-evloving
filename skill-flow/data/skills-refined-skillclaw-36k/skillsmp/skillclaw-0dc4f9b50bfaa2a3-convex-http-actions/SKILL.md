---
name: convex-http-actions
description: Use this skill when you need to build HTTP endpoints for webhooks, external API integrations, and custom routes in Convex applications.
---

# Skill body

## Documentation Sources

Before implementing, do not assume; fetch the latest documentation:

- Primary: [Convex HTTP Actions Documentation](https://docs.convex.dev/functions/http-actions)
- Actions Overview: [Convex Actions Overview](https://docs.convex.dev/functions/actions)
- Authentication: [Convex Authentication](https://docs.convex.dev/auth)
- For broader context: [Convex LLMs](https://docs.convex.dev/llms.txt)

## Instructions

### HTTP Actions Overview

HTTP actions allow you to define HTTP endpoints in Convex that can:

- Receive webhooks from third-party services
- Create custom API routes
- Handle file uploads
- Integrate with external services
- Serve dynamic content

### Basic HTTP Router Setup

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

// Simple GET endpoint
http.route({
  path: "/health",
  method: "GET",
  handler: httpAction(async (ctx, request) => {
    return new Response(JSON.stringify({ status: "ok" }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  }),
});

export default http;
```

### Request Handling

```typescript
// convex/http.ts
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

// Handle JSON body
http.route({
  path: "/api/data",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    // Parse JSON body
    const body = await request.json();
    
    // Access headers
    const authHeader = request.headers.get("Authorization");
    
    // Access URL parameters
    const url = new URL(request.url);
    const queryParam = url.searchParams.get("filter");

    return new Response(
      JSON.stringify({ received: body, filter: queryParam }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }
    );
  }),
});

// Handle form data
http.route({
  path: "/api/form",
  method: "POST",
  handler: httpAction(async (ctx, request) => {
    const formData = await request.formData();
    const name = formData.get("name");
    const email = formData.get("email");

    return new Response(
      JSON.stringify({ received: { name, email } }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }
    );
  }),
});
```