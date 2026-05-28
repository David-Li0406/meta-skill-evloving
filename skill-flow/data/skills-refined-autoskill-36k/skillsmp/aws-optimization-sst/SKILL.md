---
name: aws-optimization-sst
description: Optimizing AWS resources and costs using SST - leveraging SST's features for efficient, cost-effective infrastructure
---

# AWS Optimization with SST

This skill covers best practices for optimizing AWS resources using SST, focusing on performance, cost, and developer experience.

## Core Principles

- **Right-size resources**: Don't over-provision
- **Use SST's defaults**: They're already optimized
- **Leverage caching**: Reduce redundant work
- **Optimize cold starts**: Minimize Lambda initialization time
- **Monitor and iterate**: Use data to guide optimization

## Lambda Function Optimization

### Pattern 1: Function Configuration

```typescript
// sst.config.ts
new sst.aws.Function("Api", {
  handler: "src/api.handler",
  memory: "512 MB",      // Start here, adjust based on metrics
  timeout: "30 seconds", // Don't use default 3 seconds
  architecture: "arm64", // 20% cheaper and often faster
  nodejs: {
    esbuild: {
      minify: true,       // Smaller bundle
      external: [         // Don't bundle AWS SDK v3
        "@aws-sdk/*"
      ]
    }
  }
});
```

**Memory considerations:**
- Start with 512 MB
- Monitor execution time vs cost
- More memory = more CPU = faster execution
- Sometimes higher memory is cheaper (finishes faster)

**Architecture:**
- Use `arm64` (Graviton2) for 20% cost savings
- Same or better performance
- Works for most workloads

### Pattern 2: Bundle Size Optimization

```typescript
// Optimize imports - tree-shaking friendly
✅ import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
❌ import * as AWS from "aws-sdk";

// Use specific SDK clients
✅ import { GetCommand } from "@aws-sdk/lib-dynamodb";
❌ import { DocumentClient } from "aws-sdk/clients/dynamodb";
```

**Bundle size tips:**
- Use AWS SDK v3 (modular)
- Import only what you need
- Mark heavy deps as external
- Use dynamic imports for large libraries

```typescript
// Dynamic import for rarely-used code
export async function generatePDF(data: Data) {
  const puppeteer = await import("puppeteer");
  // Only loads when actually called
}
```

### Pattern 3: Connection Reuse

```typescript
// ✅ Initialize outside handler (reused across invocations)
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({
  maxAttempts: 3,
  requestHandler: {
    connectionTimeout: 3000,
    socketTimeout: 3000
  }
});

export async function handler(event) {
  // Use client here
}

// ❌ Don't initialize inside handler
export async function handler(event) {
  const client = new DynamoDBClient({});
  // Creates new connection every time
}
```

### Pattern 4: Provisioned Concurrency

For consistently high traffic:

```typescript
new sst.aws.Function("HighTraffic", {
  handler: "src/api.handler",
  transform: {
    function: {
      reservedConcurrentExecutions: 10,
      // Provisioned concurrency keeps instances warm
    }
  }
});
```

**When to use:**
- Consistent traffic patterns
- Latency-sensitive applications
- Cost justified by reduced cold starts

## DynamoDB Optimization

### Pattern 1: Table Configuration

```typescript
const table = new sst.aws.Dynamo("Database", {
  fields: {
    pk: "string",
    sk: "string"
  },
  primaryIndex: { hashKey: "pk", rangeKey: "sk" },
  
  // Use on-demand for variable traffic
  // Use provisioned for predictable traffic
  stream: "new-and-old-images", // Only if needed for triggers
  
  transform: {
    table: {
      // Enable point-in-time recovery for production
      pointInTimeRecovery: $app.stage === "production"
        ? { enabled: true }
        : undefined,
      
      // TTL for automatic data expiration
      timeToLiveAttribute: "expiresAt"
    }
  }
});
```

### Pattern 2: Query Optimization

```typescript
// ✅ Use Query with specific partition key
await client.send(new QueryCommand({
  TableName: Resource.Database.name,
  KeyConditionExpression: "pk = :pk",
  ExpressionAttributeValues: { ":pk": "USER#123" }
}));

// ❌ Don't use Scan unless absolutely necessary
await client.send(new ScanCommand({
  TableName: Resource.Database.name
}));
// Scans entire table - expensive and slow!
```

### Pattern 3: Batch Operations

```typescript
// Write multiple items efficiently
import { BatchWriteCommand } from "@aws-sdk/lib-dynamodb";

// Batch up to 25 items per request
const batches = chunk(items, 25);

for (const batch of batches) {
  await client.send(new BatchWriteCommand({
    RequestItems: {
      [Resource.Database.name]: batch.map(item => ({
        PutRequest: { Item: item }
      }))
    }
  }));
}
```

### Pattern 4: Projection Expressions

```typescript
// Only fetch fields you need
await client.send(new GetCommand({
  TableName: Resource.Database.name,
  Key: { pk: "USER#123", sk: "PROFILE" },
  ProjectionExpression: "name, email" // Don't fetch everything
}));
```

### Pattern 5: GSI Design

```typescript
// Sparse indexes save cost
const table = new sst.aws.Dynamo("Database", {
  fields: {
    pk: "string",
    sk: "string",
    gsi1pk: "string", // Only set on items that need indexing
    gsi1sk: "string"
  },
  primaryIndex: { hashKey: "pk", rangeKey: "sk" },
  globalIndexes: {
    gsi1: {
      hashKey: "gsi1pk",
      rangeKey: "gsi1sk",
      projection: "keys_only" // Cheapest option
    }
  }
});

// Only active users have gsi1pk
{
  pk: "USER#123",
  sk: "PROFILE",
  status: "active",
  gsi1pk: "ACTIVE#USER", // Only active users
  gsi1sk: "USER#123"
}
```

## S3 Optimization

### Pattern 1: Bucket Configuration

```typescript
const bucket = new sst.aws.Bucket("Uploads", {
  transform: {
    bucket: {
      // Lifecycle rules for cost savings
      lifecycleConfiguration: {
        rules: [
          {
            id: "archive-old-files",
            status: "Enabled",
            transitions: [
              {
                days: 30,
                storageClass: "INTELLIGENT_TIERING"
              },
              {
                days: 90,
                storageClass: "GLACIER"
              }
            ]
          },
          {
            id: "delete-temp-files",
            status: "Enabled",
            expiration: { days: 7 },
            filter: {
              prefix: "temp/"
            }
          }
        ]
      }
    }
  }
});
```

### Pattern 2: Intelligent Tiering

```typescript
// Automatically moves objects between access tiers
{
  storageClass: "INTELLIGENT_TIERING"
}

// Tiers:
// - Frequent Access (default)
// - Infrequent Access (30 days)
// - Archive Instant Access (90 days)
// - Archive Access (90+ days)
// - Deep Archive Access (180+ days)
```

### Pattern 3: CloudFront for Static Assets

```typescript
const cdn = new sst.aws.Router("CDN", {
  routes: {
    "/*": {
      bucket: bucket
    }
  },
  transform: {
    distribution: {
      defaultCacheBehavior: {
        compress: true, // Enable compression
        viewerProtocolPolicy: "redirect-to-https",
        cachePolicyId: "658327ea-f89d-4fab-a63d-7e88639e58f6" // CachingOptimized
      }
    }
  }
});
```

### Pattern 4: Presigned URLs

```typescript
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { GetObjectCommand } from "@aws-sdk/client-s3";

// Generate time-limited URL
const url = await getSignedUrl(
  s3Client,
  new GetObjectCommand({
    Bucket: Resource.Uploads.name,
    Key: fileKey
  }),
  { expiresIn: 3600 } // 1 hour
);

// No Lambda invocation needed for downloads
```

## API Gateway Optimization

### Pattern 1: HTTP API vs REST API

```typescript
// Use HTTP API (cheaper, faster)
new sst.aws.ApiGatewayV2("Api", {
  routes: {
    "GET /posts": "src/posts.list",
    "POST /posts": "src/posts.create"
  }
});

// HTTP API is 71% cheaper than REST API
// Same features for most use cases
```

### Pattern 2: Response Caching

```typescript
new sst.aws.ApiGatewayV2("Api", {
  routes: {
    "GET /posts": {
      function: "src/posts.list",
      // Cache at API Gateway level
      cache: {
        ttl: "5 minutes"
      }
    }
  }
});
```

### Pattern 3: Request Validation

```typescript
// Reject invalid requests early (before Lambda invocation)
new sst.aws.ApiGatewayV2("Api", {
  routes: {
    "POST /posts": {
      function: "src/posts.create",
      authorizer: "iam",
      // Validate request before invoking Lambda
    }
  }
});
```

## Remix Optimization with SST

### Pattern 1: Server Bundle Optimization

```typescript
// remix.config.js
export default {
  serverBuildPath: "build/server/index.mjs",
  serverMinify: true,
  serverModuleFormat: "esm",
  // Don't bundle Node.js built-ins
  serverDependenciesToBundle: [
    /^(?!node:)/, // Bundle everything except node: imports
  ]
};
```

### Pattern 2: Asset Optimization

```typescript
const remix = new sst.aws.Remix("Web", {
  environment: {
    ASSET_URL: cdn.url // Serve assets from CloudFront
  },
  transform: {
    server: {
      // Optimize Lambda
      memory: "512 MB",
      architecture: "arm64"
    }
  }
});
```

### Pattern 3: Edge Caching

```typescript
// Use CloudFront for edge caching
export const headers = () => ({
  "Cache-Control": "public, max-age=3600, s-maxage=86400"
});

// Cache at edge for 24 hours
// Browser cache for 1 hour
```

## Cost Monitoring

### Pattern 1: Resource Tagging

```typescript
new sst.aws.Function("Api", {
  handler: "src/api.handler",
  transform: {
    function: {
      tags: {
        Environment: $app.stage,
        Service: "api",
        CostCenter: "engineering"
      }
    }
  }
});
```

### Pattern 2: Budget Alerts

```typescript
// Use AWS Budgets to track costs
// Set up alerts when approaching limits
// Review CloudWatch metrics regularly
```

### Pattern 3: Cost Allocation

```typescript
// Tag all resources consistently
const tags = {
  Project: "my-app",
  Environment: $app.stage,
  Team: "engineering"
};

// Apply to all resources
new sst.aws.Function("Api", {
  transform: {
    function: { tags }
  }
});
```

## Performance Monitoring

### Pattern 1: X-Ray Tracing

```typescript
new sst.aws.Function("Api", {
  handler: "src/api.handler",
  transform: {
    function: {
      tracingConfig: {
        mode: "Active" // Enable X-Ray tracing
      }
    }
  }
});

// In code
import { captureAWS } from "aws-xray-sdk-core";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";

const client = captureAWS(new DynamoDBClient({}));
```

### Pattern 2: CloudWatch Metrics

```typescript
import { CloudWatchClient, PutMetricDataCommand } from "@aws-sdk/client-cloudwatch";

const cloudwatch = new CloudWatchClient({});

await cloudwatch.send(new PutMetricDataCommand({
  Namespace: "MyApp",
  MetricData: [{
    MetricName: "ProcessingTime",
    Value: duration,
    Unit: "Milliseconds"
  }]
}));
```

## Environment-Specific Optimization

### Pattern 1: Development Environment

```typescript
if ($app.stage === "dev") {
  // Smaller, cheaper resources for dev
  new sst.aws.Function("Api", {
    memory: "256 MB",
    timeout: "10 seconds"
  });
}
```

### Pattern 2: Production Environment

```typescript
if ($app.stage === "production") {
  new sst.aws.Function("Api", {
    memory: "1024 MB",    // More resources
    timeout: "30 seconds",
    transform: {
      function: {
        reservedConcurrentExecutions: 10,
        pointInTimeRecovery: { enabled: true }
      }
    }
  });
}
```

## Best Practices Checklist

### Lambda Functions
- [ ] Use ARM64 architecture
- [ ] Minimize bundle size
- [ ] Reuse connections
- [ ] Set appropriate memory
- [ ] Set appropriate timeout
- [ ] Use environment variables for config

### DynamoDB
- [ ] Use single table design
- [ ] Query instead of Scan
- [ ] Use batch operations
- [ ] Design GSIs carefully
- [ ] Enable TTL for expiring data
- [ ] Use projection expressions

### S3
- [ ] Set lifecycle policies
- [ ] Use Intelligent Tiering
- [ ] Enable CloudFront for static assets
- [ ] Use presigned URLs
- [ ] Compress files before upload

### API Gateway
- [ ] Use HTTP API over REST API
- [ ] Enable response caching
- [ ] Validate requests early
- [ ] Use custom domains

### Monitoring
- [ ] Tag all resources
- [ ] Set up CloudWatch alarms
- [ ] Enable X-Ray tracing
- [ ] Review Cost Explorer monthly
- [ ] Set budget alerts

## Cost Optimization Strategies

### 1. Right-Size Resources

Monitor and adjust:
```bash
# Check Lambda memory usage
# If max memory used < 60% of allocated, reduce
```

### 2. Use Reserved Capacity

For predictable workloads:
- DynamoDB Reserved Capacity
- Lambda Provisioned Concurrency
- Savings Plans

### 3. Cleanup Unused Resources

```bash
# Regular audit
sst remove --stage old-feature
```

### 4. Optimize Data Transfer

- Use CloudFront for global distribution
- Keep data in same region
- Use VPC endpoints for AWS services

## Common Anti-Patterns

❌ **Don't:**
- Over-provision memory "just in case"
- Use Scan on large tables
- Keep all data forever
- Ignore CloudWatch metrics
- Deploy to multiple regions unnecessarily
- Use REST API when HTTP API works

✅ **Do:**
- Start small, scale based on metrics
- Use Query with partition keys
- Set up lifecycle policies
- Monitor and optimize regularly
- Deploy to one region initially
- Use HTTP API by default

## Further Reading

- AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/
- AWS Cost Optimization: https://aws.amazon.com/pricing/cost-optimization/
- Lambda Power Tuning: https://github.com/alexcasalboni/aws-lambda-power-tuning
- SST Docs: https://sst.dev/docs
