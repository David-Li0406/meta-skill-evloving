---
name: aws-serverless
description: Use this skill when building production-ready serverless applications on AWS, including Lambda functions, API Gateway, DynamoDB, and event-driven patterns.
---

# AWS Serverless

## Patterns

### Lambda Handler Pattern

Proper Lambda function structure with error handling.

**When to use**: Any Lambda function implementation, API handlers, event processors, scheduled tasks.

```javascript
// Node.js Lambda Handler
// handler.js

const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, GetCommand } = require('@aws-sdk/lib-dynamodb');

const client = new DynamoDBClient({});
const docClient = DynamoDBDocumentClient.from(client);

exports.handler = async (event, context) => {
  context.callbackWaitsForEmptyEventLoop = false;

  try {
    const body = typeof event.body === 'string' ? JSON.parse(event.body) : event.body;
    const result = await processRequest(body);
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify(result)
    };
  } catch (error) {
    console.error('Error:', JSON.stringify({
      error: error.message,
      stack: error.stack,
      requestId: context.awsRequestId
    }));
    return {
      statusCode: error.statusCode || 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        error: error.message || 'Internal server error'
      })
    };
  }
};

async function processRequest(data) {
  const result = await docClient.send(new GetCommand({
    TableName: process.env.TABLE_NAME,
    Key: { id: data.id }
  }));
  return result.Item;
}
```

### API Gateway Integration Pattern

REST API and HTTP API integration with Lambda.

**When to use**: Building REST APIs backed by Lambda, need HTTP endpoints for functions.

```yaml
# template.yaml (SAM)
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: nodejs20.x
    Timeout: 30
    MemorySize: 256
    Environment:
      Variables:
        TABLE_NAME: !Ref ItemsTable

Resources:
  HttpApi:
    Type: AWS::Serverless::HttpApi
    Properties:
      StageName: prod
      CorsConfiguration:
        AllowOrigins:
          - "*"
        AllowMethods:
          - GET
          - POST
          - DELETE
        AllowHeaders:
          - "*"

  GetItemFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/get.handler
      Events:
        GetItem:
          Type: HttpApi
          Properties:
            ApiId: !Ref HttpApi
            Path: /items/{id}
            Method: GET
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref ItemsTable

  CreateItemFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/create.handler
      Events:
        CreateItem:
          Type: HttpApi
          Properties:
            ApiId: !Ref HttpApi
            Path: /items
            Method: POST
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref ItemsTable

  ItemsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
      BillingMode: PAY_PER_REQUEST

Outputs:
  ApiUrl:
    Value: !Sub "https://${HttpApi}.execute-api.${AWS::Region}.amazonaws.com/prod"
```

### Event-Driven SQS Pattern

Lambda triggered by SQS for reliable async processing.

**When to use**: Decoupled, asynchronous processing, need retry logic and DLQ, processing messages in batches.

```yaml
# template.yaml
Resources:
  ProcessorFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: src/handlers/processor.handler
      Events:
        SQSEvent:
          Type: SQS
          Properties:
            Queue: !GetAtt ProcessingQueue.Arn
            BatchSize: 10
            FunctionResponseTypes:
              - ReportBatchItemFailures

  ProcessingQueue:
    Type: AWS::SQS::Queue
    Properties:
      VisibilityTimeout: 180
      RedrivePolicy:
        deadLetterTargetArn: !GetAtt DeadLetterQueue.Arn
        maxReceiveCount: 3

  DeadLetterQueue:
    Type: AWS::SQS::Queue
    Properties:
      MessageRetentionPeriod: 1209600
```

## Anti-Patterns

### ❌ Monolithic Lambda

**Why bad**: Large deployment packages cause slow cold starts, hard to scale individual operations, updates affect entire system.

### ❌ Large Dependencies

**Why bad**: Increases deployment package size, slows down cold starts significantly, most of SDK/library may be unused.

### ❌ Synchronous Calls in VPC

**Why bad**: VPC-attached Lambdas have ENI setup overhead, blocking DNS lookups or connections worsen cold starts.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | high | Measure your INIT phase |
| Issue | high | Set appropriate timeout |
| Issue | high | Increase memory allocation |
| Issue | medium | Verify VPC configuration |
| Issue | medium | Tell Lambda not to wait for event loop |
| Issue | medium | For large file uploads |
| Issue | high | Use different buckets/prefixes |

## Principles

- Right-size memory and timeout (measure before optimizing).
- Minimize cold starts for latency-sensitive workloads.
- Use SnapStart for Java/.NET functions.
- Prefer HTTP API over REST API for simple use cases.
- Design for failure with DLQs and retries.
- Keep deployment packages small.
- Use environment variables for configuration.
- Implement structured logging with correlation IDs.

## Reference System Usage

Always consult the provided reference files for guidance on creation, diagnosis, and review of serverless applications.