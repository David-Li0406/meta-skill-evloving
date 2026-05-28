---
name: serverless
description: Serverless architecture pattern for event-driven, function-based applications
license: MIT
compatibility: opencode
metadata:
  category: architecture
  pattern: serverless
  deployment: faas
---

## What I do

I provide guidance on building serverless applications using Functions-as-a-Service (FaaS) and managed services.

## When to use me

Load this skill when:
- Event-driven workloads
- Variable/unpredictable traffic patterns
- Want to minimize operational overhead
- Pay-per-use cost model preferred
- Rapid iteration and deployment
- Don't need long-running processes

## Core Principles

### 1. Stateless Functions
Functions don't maintain state between invocations.

### 2. Event-Driven
Functions triggered by events (HTTP, queue, schedule, etc.).

### 3. Managed Infrastructure
No server management - cloud provider handles scaling.

### 4. Pay Per Execution
Only pay for actual function execution time.

## Function Structure

```typescript
// AWS Lambda handler
export const handler = async (event: APIGatewayEvent) => {
  const userId = event.pathParameters?.id;
  
  const user = await dynamodb.get({
    TableName: 'Users',
    Key: { id: userId },
  });
  
  return {
    statusCode: 200,
    body: JSON.stringify(user),
  };
};
```

## Event Sources

### HTTP (API Gateway)
```typescript
// GET /users/{id}
export const getUser = async (event: APIGatewayEvent) => {
  // Handle GET request
};

// POST /users
export const createUser = async (event: APIGatewayEvent) => {
  // Handle POST request
};
```

### Queue (SQS, EventBridge)
```typescript
export const processOrder = async (event: SQSEvent) => {
  for (const record of event.Records) {
    const order = JSON.parse(record.body);
    await processOrderLogic(order);
  }
};
```

### Schedule (Cron)
```typescript
// Run every hour
export const cleanupOldRecords = async () => {
  const cutoffDate = new Date();
  cutoffDate.setHours(cutoffDate.getHours() - 24);
  
  await dynamodb.delete({
    TableName: 'TempRecords',
    Key: { createdAt: { $lt: cutoffDate } },
  });
};
```

## Advantages

1. **No Server Management**: Focus on code, not infrastructure
2. **Auto-Scaling**: Automatic scaling to demand
3. **Cost Efficient**: Pay only for execution time
4. **Fast Deployment**: Deploy functions independently
5. **Built-in HA**: High availability by default

## Challenges

1. **Cold Starts**: Initial invocation latency
2. **Execution Limits**: Timeout constraints (15 min AWS Lambda)
3. **Vendor Lock-in**: Platform-specific code
4. **Debugging**: Harder to debug distributed functions
5. **State Management**: No local state between invocations

## Best Practices

1. **Keep functions small**: Single responsibility
2. **Minimize cold starts**: Keep dependencies minimal
3. **Use managed services**: DynamoDB, S3, SQS instead of self-hosted
4. **Handle errors gracefully**: Implement retries and dead letter queues
5. **Monitor everything**: CloudWatch, distributed tracing
6. **Optimize bundle size**: Tree-shake dependencies

## Example Stack (AWS)

```
API Gateway → Lambda → DynamoDB
                    → S3
                    → SQS → Lambda → External API
```

## Infrastructure as Code

```yaml
# serverless.yml
service: user-service

provider:
  name: aws
  runtime: nodejs18.x

functions:
  getUser:
    handler: src/handlers/getUser.handler
    events:
      - http:
          path: users/{id}
          method: get
  
  createUser:
    handler: src/handlers/createUser.handler
    events:
      - http:
          path: users
          method: post

resources:
  Resources:
    UsersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: Users
        BillingMode: PAY_PER_REQUEST
```

## References

- AWS Lambda documentation
- Serverless Framework
- AWS SAM (Serverless Application Model)
