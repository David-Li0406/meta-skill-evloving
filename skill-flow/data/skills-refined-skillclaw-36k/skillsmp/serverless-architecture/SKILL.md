---
name: Serverless Architecture
description: This skill should be used when the user asks to "serverless, Lambda function, Azure Functions, Cloud Functions, serverless patterns, FaaS, event-driven architecture, cold start optimization", or needs help with Lambda, Functions, serverless patterns, and event-driven systems.
version: 1.0.0
---

# Serverless Architecture

Comprehensive guidance for designing, implementing, and operating serverless applications across AWS Lambda, Azure Functions, Google Cloud Functions, and other FaaS platforms.

## Core Concepts

### Function as a Service (FaaS)

| Concept | Description |
|---------|-------------|
| Cold Start | Initial latency when function instance is created |
| Warm Start | Faster execution when reusing existing instance |
| Concurrency | Number of simultaneous function executions |
| Provisioned Concurrency | Pre-warmed instances for consistent latency |
| Event Source | Trigger that invokes the function |

### Serverless Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                    Event Sources                             │
├──────────┬──────────┬──────────┬──────────┬────────────────┤
│   API    │  Queue   │ Schedule │  Stream  │   Database     │
│ Gateway  │  (SQS)   │ (Cron)   │ (Kinesis)│   (DynamoDB)   │
└────┬─────┴────┬─────┴────┬─────┴────┬─────┴───────┬────────┘
     │          │          │          │             │
     ▼          ▼          ▼          ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Lambda Functions                          │
├─────────────────────────────────────────────────────────────┤
│  • API Handlers  • Event Processors  • Scheduled Jobs       │
│  • Stream Consumers  • Database Triggers  • Webhooks        │
└─────────────────────────────────────────────────────────────┘
```

## AWS Lambda

### Basic Function Structure

```python
# handler.py - Python Lambda function
import json
import logging
import os
from typing import Any, Dict

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize outside handler for connection reuse (warm starts)
# db_connection = create_db_connection()

def handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """
    Main Lambda handler function.

    Args:
        event: Event data from trigger source
        context: Lambda runtime context

    Returns:
        Response object
    """
    logger.info(f"Processing event: {json.dumps(event)}")

    try:
        # Extract request data
        body = json.loads(event.get('body', '{}'))

        # Business logic here
        result = process_request(body)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': True,
                'data': result
            })
        }

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        logger.error(f"Internal error: {e}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }

def process_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """Process the incoming request."""
    # Implementation here
    return {'processed': True}
```

### Node.js Lambda Function

```javascript
// handler.js - Node.js Lambda function
const AWS = require('aws-sdk');

// Initialize outside handler for connection reuse
const dynamodb = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event, context) => {
    // Don't wait for empty event loop (for connection pooling)
    context.callbackWaitsForEmptyEventLoop = false;

    console.log('Event:', JSON.stringify(event, null, 2));

    try {
        const body = JSON.parse(event.body || '{}');

        // Process request
        const result = await processRequest(body);

        return {
            statusCode: 200,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            body: JSON.stringify({
                success: true,
                data: result,
            }),
        };
    } catch (error) {
        console.error('Error:', error);

        return {
            statusCode: error.statusCode || 500,
            body: JSON.stringify({
                error: error.message || 'Internal server error',
            }),
        };
    }
};

async function processRequest(data) {
    // DynamoDB operation example
    const params = {
        TableName: process.env.TABLE_NAME,
        Item: {
            id: data.id,
            createdAt: new Date().toISOString(),
            ...data,
        },
    };

    await dynamodb.put(params).promise();
    return { id: data.id };
}
```

### SAM Template (AWS)

```yaml
# template.yaml - AWS SAM template
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Serverless API

Globals:
  Function:
    Timeout: 30
    MemorySize: 256
    Runtime: python3.11
    Environment:
      Variables:
        LOG_LEVEL: INFO
        TABLE_NAME: !Ref DataTable

Resources:
  # API Gateway
  ApiGateway:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      Cors:
        AllowMethods: "'GET,POST,PUT,DELETE,OPTIONS'"
        AllowHeaders: "'Content-Type,Authorization'"
        AllowOrigin: "'*'"
      Auth:
        DefaultAuthorizer: CognitoAuthorizer
        Authorizers:
          CognitoAuthorizer:
            UserPoolArn: !GetAtt UserPool.Arn

  # Lambda Functions
  CreateItemFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: handlers/items.create
      Events:
        Api:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /items
            Method: POST
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref DataTable
      # Provisioned concurrency for low latency
      ProvisionedConcurrencyConfig:
        ProvisionedConcurrentExecutions: 5

  GetItemFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: handlers/items.get
      Events:
        Api:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /items/{id}
            Method: GET
      Policies:
        - DynamoDBReadPolicy:
            TableName: !Ref DataTable

  # Async processor (SQS triggered)
  ProcessorFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: handlers/processor.handle
      Events:
        SQSEvent:
          Type: SQS
          Properties:
            Queue: !GetAtt ProcessingQueue.Arn
            BatchSize: 10
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref DataTable

  # Scheduled function
  CleanupFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: handlers/cleanup.handle
      Events:
        Schedule:
          Type: Schedule
          Properties:
            Schedule: rate(1 day)
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref DataTable

  # DynamoDB Table
  DataTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
        - AttributeName: sk
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
        - AttributeName: sk
          KeyType: RANGE
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true

  # SQS Queue
  ProcessingQueue:
    Type: AWS::SQS::Queue
    Properties:
      VisibilityTimeout: 180
      RedrivePolicy:
        deadLetterTargetArn: !GetAtt DeadLetterQueue.Arn
        maxReceiveCount: 3

  DeadLetterQueue:
    Type: AWS::SQS::Queue

  # Cognito User Pool
  UserPool:
    Type: AWS::Cognito::UserPool
    Properties:
      UserPoolName: !Sub ${AWS::StackName}-users

Outputs:
  ApiEndpoint:
    Value: !Sub "https://${ApiGateway}.execute-api.${AWS::Region}.amazonaws.com/prod"
```

## Azure Functions

### HTTP Trigger Function

```csharp
// Function.cs - Azure Functions (C#)
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

public static class ItemFunction
{
    [FunctionName("CreateItem")]
    public static async Task<IActionResult> CreateItem(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "items")]
        HttpRequest req,
        [CosmosDB(
            databaseName: "mydb",
            collectionName: "items",
            ConnectionStringSetting = "CosmosDBConnection")]
        IAsyncCollector<dynamic> documentsOut,
        ILogger log)
    {
        log.LogInformation("Creating new item");

        string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
        dynamic data = JsonConvert.DeserializeObject(requestBody);

        var item = new {
            id = Guid.NewGuid().ToString(),
            name = data?.name,
            createdAt = DateTime.UtcNow
        };

        await documentsOut.AddAsync(item);

        return new OkObjectResult(item);
    }

    [FunctionName("ProcessQueue")]
    public static async Task ProcessQueue(
        [QueueTrigger("myqueue", Connection = "AzureWebJobsStorage")]
        string queueMessage,
        [CosmosDB(
            databaseName: "mydb",
            collectionName: "items",
            ConnectionStringSetting = "CosmosDBConnection")]
        IAsyncCollector<dynamic> documentsOut,
        ILogger log)
    {
        log.LogInformation($"Processing message: {queueMessage}");

        var data = JsonConvert.DeserializeObject<dynamic>(queueMessage);
        await documentsOut.AddAsync(data);
    }
}
```

### Azure Functions Configuration

```json
// host.json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request"
      }
    }
  },
  "extensions": {
    "http": {
      "routePrefix": "api",
      "maxConcurrentRequests": 100,
      "maxOutstandingRequests": 200
    },
    "queues": {
      "batchSize": 16,
      "maxDequeueCount": 5,
      "newBatchThreshold": 8
    }
  },
  "functionTimeout": "00:05:00"
}
```

## Google Cloud Functions

### HTTP Function (Python)

```python
# main.py - Google Cloud Functions
import functions_framework
from flask import jsonify, request
from google.cloud import firestore
import logging

db = firestore.Client()

@functions_framework.http
def create_item(request):
    """HTTP Cloud Function for creating items."""

    # Handle CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    try:
        data = request.get_json()

        # Validate input
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), 400

        # Save to Firestore
        doc_ref = db.collection('items').document()
        doc_ref.set({
            'name': data['name'],
            'created_at': firestore.SERVER_TIMESTAMP,
        })

        return jsonify({
            'id': doc_ref.id,
            'name': data['name'],
        }), 201

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@functions_framework.cloud_event
def process_pubsub(cloud_event):
    """Pub/Sub triggered Cloud Function."""
    import base64

    data = base64.b64decode(cloud_event.data["message"]["data"]).decode()
    logging.info(f"Processing message: {data}")

    # Process the message
    db.collection('processed').add({
        'data': data,
        'processed_at': firestore.SERVER_TIMESTAMP,
    })
```

## Cold Start Optimization

### Strategies

| Strategy | AWS Lambda | Azure Functions | Cloud Functions |
|----------|------------|-----------------|-----------------|
| Provisioned Concurrency | ✅ | ✅ (Premium) | ✅ (min instances) |
| Keep-Warm Pings | ⚠️ (workaround) | ⚠️ (workaround) | ⚠️ (workaround) |
| Smaller Packages | ✅ | ✅ | ✅ |
| Native Compilation | ✅ (GraalVM) | ✅ | ✅ |
| Connection Pooling | ✅ | ✅ | ✅ |

### Bundle Optimization

```javascript
// webpack.config.js - Optimize Lambda bundle
const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
    mode: 'production',
    target: 'node',
    entry: './src/handler.js',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'handler.js',
        libraryTarget: 'commonjs2',
    },
    externals: [
        'aws-sdk', // Available in Lambda runtime
    ],
    optimization: {
        minimize: true,
        minimizer: [new TerserPlugin()],
    },
};
```

### Connection Reuse Pattern

```python
# Reuse connections across invocations
import boto3
from functools import lru_cache

@lru_cache(maxsize=1)
def get_dynamodb_table():
    """Cache DynamoDB table resource."""
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(os.environ['TABLE_NAME'])

@lru_cache(maxsize=1)
def get_secrets():
    """Cache secrets manager client."""
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=os.environ['SECRET_ID'])
    return json.loads(response['SecretString'])
```

## Event-Driven Patterns

### Fan-Out Pattern

```yaml
# Fan-out with SNS and SQS
Resources:
  EventTopic:
    Type: AWS::SNS::Topic

  ProcessorQueue1:
    Type: AWS::SQS::Queue

  ProcessorQueue2:
    Type: AWS::SQS::Queue

  Subscription1:
    Type: AWS::SNS::Subscription
    Properties:
      TopicArn: !Ref EventTopic
      Protocol: sqs
      Endpoint: !GetAtt ProcessorQueue1.Arn
      FilterPolicy:
        eventType: ["type_a"]

  Subscription2:
    Type: AWS::SNS::Subscription
    Properties:
      TopicArn: !Ref EventTopic
      Protocol: sqs
      Endpoint: !GetAtt ProcessorQueue2.Arn
      FilterPolicy:
        eventType: ["type_b"]
```

### Saga Pattern (Distributed Transactions)

```python
# Step Functions state machine for saga pattern
{
    "StartAt": "CreateOrder",
    "States": {
        "CreateOrder": {
            "Type": "Task",
            "Resource": "${CreateOrderFunctionArn}",
            "Catch": [{
                "ErrorEquals": ["States.ALL"],
                "Next": "CompensateOrder"
            }],
            "Next": "ReserveInventory"
        },
        "ReserveInventory": {
            "Type": "Task",
            "Resource": "${ReserveInventoryFunctionArn}",
            "Catch": [{
                "ErrorEquals": ["States.ALL"],
                "Next": "CompensateInventory"
            }],
            "Next": "ProcessPayment"
        },
        "ProcessPayment": {
            "Type": "Task",
            "Resource": "${ProcessPaymentFunctionArn}",
            "Catch": [{
                "ErrorEquals": ["States.ALL"],
                "Next": "CompensatePayment"
            }],
            "Next": "Success"
        },
        "CompensatePayment": {
            "Type": "Task",
            "Resource": "${RefundPaymentFunctionArn}",
            "Next": "CompensateInventory"
        },
        "CompensateInventory": {
            "Type": "Task",
            "Resource": "${ReleaseInventoryFunctionArn}",
            "Next": "CompensateOrder"
        },
        "CompensateOrder": {
            "Type": "Task",
            "Resource": "${CancelOrderFunctionArn}",
            "Next": "Failed"
        },
        "Success": { "Type": "Succeed" },
        "Failed": { "Type": "Fail" }
    }
}
```

## Best Practices

### Security

```yaml
# IAM least privilege
- Effect: Allow
  Action:
    - dynamodb:GetItem
    - dynamodb:PutItem
  Resource: !GetAtt DataTable.Arn

# VPC for database access
VpcConfig:
  SecurityGroupIds:
    - !Ref LambdaSecurityGroup
  SubnetIds:
    - !Ref PrivateSubnet1
    - !Ref PrivateSubnet2
```

### Observability

```python
# Structured logging with correlation
import aws_lambda_powertools
from aws_lambda_powertools import Logger, Tracer, Metrics

logger = Logger()
tracer = Tracer()
metrics = Metrics()

@logger.inject_lambda_context
@tracer.capture_lambda_handler
@metrics.log_metrics
def handler(event, context):
    logger.info("Processing request", extra={"event": event})
    metrics.add_metric(name="RequestCount", unit="Count", value=1)

    with tracer.capture_method():
        result = process_data(event)

    return result
```

### Error Handling

```python
# Retry with exponential backoff
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
def call_external_service(data):
    response = requests.post(SERVICE_URL, json=data, timeout=5)
    response.raise_for_status()
    return response.json()
```

## Testing

```python
# test_handler.py
import pytest
from unittest.mock import patch, MagicMock
from handler import handler

@pytest.fixture
def api_gateway_event():
    return {
        'httpMethod': 'POST',
        'path': '/items',
        'body': '{"name": "test"}',
        'headers': {'Content-Type': 'application/json'},
    }

@pytest.fixture
def lambda_context():
    context = MagicMock()
    context.function_name = 'test-function'
    context.memory_limit_in_mb = 256
    context.invoked_function_arn = 'arn:aws:lambda:us-east-1:123456789:function:test'
    context.aws_request_id = 'test-request-id'
    return context

def test_handler_success(api_gateway_event, lambda_context):
    with patch('handler.dynamodb') as mock_db:
        mock_db.put_item.return_value = {}

        response = handler(api_gateway_event, lambda_context)

        assert response['statusCode'] == 200
        assert 'success' in response['body']

def test_handler_validation_error(lambda_context):
    event = {'body': '{}'}  # Missing required fields

    response = handler(event, lambda_context)

    assert response['statusCode'] == 400
```

## Deployment Commands

```bash
# AWS SAM
sam build
sam deploy --guided

# Serverless Framework
serverless deploy --stage prod

# AWS CDK
cdk deploy --all

# Azure Functions
func azure functionapp publish <app-name>

# Google Cloud Functions
gcloud functions deploy create_item \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated
```
