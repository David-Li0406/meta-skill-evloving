---
name: sst-dev
description: Best practices, patterns, and conventions for working with SST.dev (Serverless Stack) for AWS infrastructure
---

# SST.dev Development Skill

This skill provides comprehensive guidance for working with SST (Serverless Stack), covering infrastructure patterns, best practices, and common use cases.

## Core Philosophy

SST embraces these principles:
- **Type-safe infrastructure**: Full TypeScript support from infrastructure to runtime
- **Resource bindings**: Type-safe access to resources via `Resource`
- **Convention over configuration**: Sensible defaults, customize when needed
- **Developer experience**: Fast feedback loops, excellent local development

## Key Concepts

### Resource Bindings

The most powerful SST feature - type-safe resource access:

```typescript
// In sst.config.ts
const bucket = new sst.aws.Bucket("MyBucket");
const api = new sst.aws.Function("MyApi", {
  handler: "src/api.handler",
  link: [bucket]  // Link the bucket
});

// In src/api.ts
import { Resource } from "sst";

export async function handler() {
  // Type-safe access!
  await s3.putObject({
    Bucket: Resource.MyBucket.name,
    // ...
  });
}
```

**Key points:**
- Use `link` to connect resources
- Access via `Resource.[ResourceName]`
- Full TypeScript autocomplete and type safety
- No environment variables needed

### Infrastructure as Code

Define resources in `sst.config.ts`:

```typescript
export default $config({
  app(input) {
    return {
      name: "my-app",
      removal: input?.stage === "production" ? "retain" : "remove",
    };
  },
  async run() {
    // Define your infrastructure
    const bucket = new sst.aws.Bucket("Uploads");
    const api = new sst.aws.Function("Api", {
      handler: "src/api.handler",
      link: [bucket],
      url: true  // Enable function URL
    });

    return {
      api: api.url,
      bucket: bucket.name
    };
  },
});
```

## Common Patterns

### Pattern 1: Function with Database Access

```typescript
// sst.config.ts
const db = new sst.aws.Dynamo("Database", {
  fields: {
    pk: "string",
    sk: "string"
  },
  primaryIndex: { hashKey: "pk", rangeKey: "sk" }
});

const handler = new sst.aws.Function("Handler", {
  handler: "src/handler.main",
  link: [db]
});

// src/handler.ts
import { Resource } from "sst";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, PutCommand } from "@aws-sdk/lib-dynamodb";

const client = DynamoDBDocumentClient.from(new DynamoDBClient({}));

export async function main(event) {
  await client.send(new PutCommand({
    TableName: Resource.Database.name,
    Item: { pk: "user", sk: "123", data: "..." }
  }));
}
```

### Pattern 2: Remix with SST

```typescript
// sst.config.ts
const bucket = new sst.aws.Bucket("Uploads");

const remix = new sst.aws.Remix("MyApp", {
  link: [bucket],  // Link resources to Remix
  domain: "app.example.com"
});

// In Remix loader/action
import { Resource } from "sst";

export async function loader() {
  const url = await getSignedUrl(s3, new GetObjectCommand({
    Bucket: Resource.Uploads.name,
    Key: "file.pdf"
  }));
  
  return { url };
}
```

### Pattern 3: API with Auth

```typescript
const auth = new sst.aws.Auth("Auth", {
  authenticator: "src/auth.handler"
});

const api = new sst.aws.ApiGatewayV2("Api", {
  link: [auth],
  transform: {
    route: {
      handler: {
        link: [auth]
      }
    }
  }
});

api.route("GET /private", "src/private.handler", {
  auth: { iam: true }
});
```

### Pattern 4: Environment-Specific Configuration

```typescript
export default $config({
  app(input) {
    return {
      name: "my-app",
      removal: input?.stage === "production" ? "retain" : "remove",
    };
  },
  async run() {
    const isProd = $app.stage === "production";
    
    const db = new sst.aws.Dynamo("Database", {
      // Production settings
      ...(isProd && {
        transform: {
          table: {
            pointInTimeRecovery: { enabled: true }
          }
        }
      })
    });

    return { stage: $app.stage };
  }
});
```

## Resource Types

### Compute
- `Function`: Lambda functions with great DX
- `Remix`: Remix applications
- `Nextjs`: Next.js applications
- `Astro`: Astro applications

### Storage
- `Bucket`: S3 buckets with automatic policies
- `Dynamo`: DynamoDB tables with typed indexes

### APIs
- `ApiGatewayV2`: HTTP/WebSocket APIs
- `Router`: Route handling

### Auth & Security
- `Auth`: Authentication setup
- `Secret`: Secure secret management

### Queues & Events
- `Queue`: SQS queues
- `SnsTopic`: SNS topics
- `EventBus`: EventBridge buses

## Best Practices

### 1. Use Resource Bindings Over Environment Variables

❌ **Don't:**
```typescript
const tableName = process.env.TABLE_NAME!;
```

✅ **Do:**
```typescript
const tableName = Resource.Database.name;
```

### 2. Keep Infrastructure Simple

❌ **Don't over-engineer:**
```typescript
// Don't create unnecessary layers
const commonConfig = createConfigBuilder()
  .withDefaults()
  .withRetries()
  .build();
```

✅ **Do keep it simple:**
```typescript
const fn = new sst.aws.Function("Handler", {
  handler: "src/handler.main",
  timeout: "30 seconds"
});
```

### 3. Link Resources Appropriately

Only link what you need:

```typescript
// If a function only needs the bucket, only link the bucket
const fn = new sst.aws.Function("ProcessUpload", {
  handler: "src/process.handler",
  link: [bucket]  // Not the entire database, auth, etc.
});
```

### 4. Use Transforms for AWS-Specific Needs

When you need direct AWS resource access:

```typescript
new sst.aws.Bucket("Uploads", {
  transform: {
    bucket: {
      lifecycleConfiguration: {
        rules: [{
          expiration: { days: 30 },
          status: "Enabled"
        }]
      }
    }
  }
});
```

### 5. Type Your Handlers Properly

```typescript
import type { APIGatewayProxyEventV2, APIGatewayProxyResultV2 } from "aws-lambda";

export async function handler(
  event: APIGatewayProxyEventV2
): Promise<APIGatewayProxyResultV2> {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: "Hello" })
  };
}
```

### 6. Organize Large Stacks

```typescript
// sst.config.ts
async run() {
  const storage = await import("./infra/storage");
  const api = await import("./infra/api");
  const web = await import("./infra/web");
  
  const { bucket, database } = await storage.setup();
  const { apiUrl } = await api.setup({ bucket, database });
  const { siteUrl } = await web.setup({ apiUrl });
  
  return { apiUrl, siteUrl };
}
```

## Local Development

### Running Locally

```bash
# Start SST dev mode
sst dev

# In another terminal, run your app
npm run dev
```

### Console Access

```bash
# Open SST Console for your stage
sst console

# Deploy to a specific stage
sst deploy --stage production
```

### Testing Resources Locally

SST automatically sets up local versions:

```typescript
// Works the same locally and deployed
import { Resource } from "sst";

const tableName = Resource.Database.name;  // Points to local or deployed based on context
```

## Common Gotchas

### 1. Resource Name Changes

Renaming resources can cause issues. Use explicit IDs:

```typescript
// Better: use explicit ID
const bucket = new sst.aws.Bucket("Uploads", {
  // Explicit physical name if needed
});
```

### 2. Circular Dependencies

Avoid circular links:

```typescript
❌ // Don't
const fnA = new sst.aws.Function("A", { 
  link: [fnB] 
});
const fnB = new sst.aws.Function("B", { 
  link: [fnA] 
});

✅ // Do: use SNS/SQS or store state in DB
```

### 3. Cold Starts

Lambda cold starts are real. Optimize:

```typescript
// Keep warm-up code outside handler
const client = new DynamoDBClient({});

export async function handler(event) {
  // Handler uses pre-initialized client
}
```

## Migration and Updates

### Updating SST

```bash
npm update sst
# or
pnpm update sst
```

### Breaking Changes

Always check the changelog when upgrading major versions. SST provides migration guides for breaking changes.

## Further Reading

- Official SST Docs: https://sst.dev/docs
- SST Examples: https://github.com/sst/examples
- SST Discord: Great for questions and support
