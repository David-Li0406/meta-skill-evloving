# AWS Serverless

## Patterns


---
  #### **Name**
Lambda Handler Pattern
  #### **Description**
Proper Lambda function structure with error handling
  #### **When To Use**
    - Any Lambda function implementation
    - API handlers, event processors, scheduled tasks
  #### **Implementation**
    ```javascript
    // Node.js Lambda Handler
    // handler.js
    
    // Initialize outside handler (reused across invocations)
    const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
    const { DynamoDBDocumentClient, GetCommand } = require('@aws-sdk/lib-dynamodb');
    
    const client = new DynamoDBClient({});
    const docClient = DynamoDBDocumentClient.from(client);
    
    // Handler function
    exports.handler = async (event, context) => {
      // Optional: Don't wait for event loop to clear (Node.js)
      context.callbackWaitsForEmptyEventLoop = false;
    
      try {
        // Parse input based on event source
        const body = typeof event.body === 'string'
          ? JSON.parse(event.body)
          : event.body;
    
        // Business logic
        const result = await processRequest(body);
    
        // Return API Gateway compatible response
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
      // Your business logic here
      const result = await docClient.send(new GetCommand({
        TableName: process.env.TABLE_NAME,
        Key: { id: data.id }
      }));
      return result.Item;
    }
    ```
    
    ```python
    # Python Lambda Handler
    # handler.py
    
    import json
    import os
    import logging
    import boto3
    from botocore.exceptions import ClientError
    
    # Initialize outside handler (reused across invocations)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    
    def handler(event, context):
        try:
            # Parse input
            body = json.loads(event.get('body', '{}')) if isinstance(event.get('body'), str) else event.get('body', {})
    
            # Business logic
            result = process_request(body)
    
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(result)
            }
    
        except ClientError as e:
            logger.error(f"DynamoDB error: {e.response['Error']['Message']}")
            return error_response(500, 'Database error')
    
        except json.JSONDecodeError:
            return error_response(400, 'Invalid JSON')
    
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return error_response(500, 'Internal server error')
    
    def process_request(data):
        response = table.get_item(Key={'id': data['id']})
        return response.get('Item')
    
    def error_response(status_code, message):
        return {
            'statusCode': status_code,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': message})
        }
    ```
    
  #### **Best Practices**
    - Initialize clients outside handler (reused across warm invocations)
    - Always return proper API Gateway response format
    - Log with structured JSON for CloudWatch Insights
    - Include request ID in error logs for tracing

---
  #### **Name**
API Gateway Integration Pattern
  #### **Description**
REST API and HTTP API integration with Lambda
  #### **When To Use**
    - Building REST APIs backed by Lambda
    - Need HTTP endpoints for functions
  #### **Structure**
    project/
    ├── template.yaml      # SAM template
    ├── src/
    │   ├── handlers/
    │   │   ├── get.js
    │   │   ├── create.js
    │   │   └── delete.js
    │   └── lib/
    │       └── dynamodb.js
    └── events/
        └── event.json     # Test events
    
  #### **Implementation**
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
      # HTTP API (recommended for simple use cases)
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
    
      # Lambda Functions
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
    
      # DynamoDB Table
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
    
    ```javascript
    // src/handlers/get.js
    const { getItem } = require('../lib/dynamodb');
    
    exports.handler = async (event) => {
      const id = event.pathParameters?.id;
    
      if (!id) {
        return {
          statusCode: 400,
          body: JSON.stringify({ error: 'Missing id parameter' })
        };
      }
    
      const item = await getItem(id);
    
      if (!item) {
        return {
          statusCode: 404,
          body: JSON.stringify({ error: 'Item not found' })
        };
      }
    
      return {
        statusCode: 200,
        body: JSON.stringify(item)
      };
    };
    ```
    
  #### **Api Comparison**
    ##### **Http Api**
      - Lower latency (~10ms)
      - Lower cost (50-70% cheaper)
      - Simpler, fewer features
      -         ####### **Best For**
Most REST APIs
    ##### **Rest Api**
      - More features (caching, request validation, WAF)
      - Usage plans and API keys
      - Request/response transformation
      -         ####### **Best For**
Complex APIs, enterprise features

---
  #### **Name**
Event-Driven SQS Pattern
  #### **Description**
Lambda triggered by SQS for reliable async processing
  #### **When To Use**
    - Decoupled, asynchronous processing
    - Need retry logic and DLQ
    - Processing messages in batches
  #### **Implementation**
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
                  - ReportBatchItemFailures  # Partial batch failure handling
    
      ProcessingQueue:
        Type: AWS::SQS::Queue
        Properties:
          VisibilityTimeout: 180  # 6x Lambda timeout
          RedrivePolicy:
            deadLetterTargetArn: !GetAtt DeadLetterQueue.Arn
            maxReceiveCount: 3
    
      DeadLetterQueue:
        Type: AWS::SQS::Queue
        Properties:
          MessageRetentionPeriod: 1209600  # 14 days
    ```
    
    ```javascript
    // src/handlers/processor.js
    exports.handler = async (event) => {
      const batchItemFailures = [];
    
      for (const record of event.Records) {
        try {
          const body = JSON.parse(record.body);
          await processMessage(body);
        } catch (error) {
          console.error(`Failed to process message ${record.messageId}:`, error);
          // Report this item as failed (will be retried)
          batchItemFailures.push({
            itemIdentifier: record.messageId
          });
        }
      }
    
      // Return failed items for retry
      return { batchItemFailures };
    };
    
    async function processMessage(message) {
      // Your processing logic
      console.log('Processing:', message);
    
      // Simulate work
      await saveToDatabase(message);
    }
    ```
    
    ```python
    # Python version
    import json
    import logging
    
    logger = logging.getLogger()
    
    def handler(event, context):
        batch_item_failures = []
    
        for record in event['Records']:
            try:
                body = json.loads(record['body'])
                process_message(body)
            except Exception as e:
                logger.error(f"Failed to process {record['messageId']}: {e}")
                batch_item_failures.append({
                    'itemIdentifier': record['messageId']
                })
    
        return {'batchItemFailures': batch_item_failures}
    ```
    
  #### **Best Practices**
    - Set VisibilityTimeout to 6x Lambda timeout
    - Use ReportBatchItemFailures for partial batch failure
    - Always configure a DLQ for poison messages
    - Process messages idempotently

---
  #### **Name**
DynamoDB Streams Pattern
  #### **Description**
React to DynamoDB table changes with Lambda
  #### **When To Use**
    - Real-time reactions to data changes
    - Cross-region replication
    - Audit logging, notifications
  #### **Implementation**
    ```yaml
    # template.yaml
    Resources:
      ItemsTable:
        Type: AWS::DynamoDB::Table
        Properties:
          TableName: items
          AttributeDefinitions:
            - AttributeName: id
              AttributeType: S
          KeySchema:
            - AttributeName: id
              KeyType: HASH
          BillingMode: PAY_PER_REQUEST
          StreamSpecification:
            StreamViewType: NEW_AND_OLD_IMAGES
    
      StreamProcessorFunction:
        Type: AWS::Serverless::Function
        Properties:
          Handler: src/handlers/stream.handler
          Events:
            Stream:
              Type: DynamoDB
              Properties:
                Stream: !GetAtt ItemsTable.StreamArn
                StartingPosition: TRIM_HORIZON
                BatchSize: 100
                MaximumRetryAttempts: 3
                DestinationConfig:
                  OnFailure:
                    Destination: !GetAtt StreamDLQ.Arn
    
      StreamDLQ:
        Type: AWS::SQS::Queue
    ```
    
    ```javascript
    // src/handlers/stream.js
    exports.handler = async (event) => {
      for (const record of event.Records) {
        const eventName = record.eventName;  // INSERT, MODIFY, REMOVE
    
        // Unmarshall DynamoDB format to plain JS objects
        const newImage = record.dynamodb.NewImage
          ? unmarshall(record.dynamodb.NewImage)
          : null;
        const oldImage = record.dynamodb.OldImage
          ? unmarshall(record.dynamodb.OldImage)
          : null;
    
        console.log(`${eventName}: `, { newImage, oldImage });
    
        switch (eventName) {
          case 'INSERT':
            await handleInsert(newImage);
            break;
          case 'MODIFY':
            await handleModify(oldImage, newImage);
            break;
          case 'REMOVE':
            await handleRemove(oldImage);
            break;
        }
      }
    };
    
    // Use AWS SDK v3 unmarshall
    const { unmarshall } = require('@aws-sdk/util-dynamodb');
    ```
    
  #### **Stream View Types**
    ##### **Keys Only**
Only key attributes
    ##### **New Image**
After modification
    ##### **Old Image**
Before modification
    ##### **New And Old Images**
Both before and after

---
  #### **Name**
Cold Start Optimization Pattern
  #### **Description**
Minimize Lambda cold start latency
  #### **When To Use**
    - Latency-sensitive applications
    - User-facing APIs
    - High-traffic functions
  #### **Implementation**
    ## 1. Optimize Package Size
    
    ```javascript
    // Use modular AWS SDK v3 imports
    // GOOD - only imports what you need
    const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
    const { DynamoDBDocumentClient, GetCommand } = require('@aws-sdk/lib-dynamodb');
    
    // BAD - imports entire SDK
    const AWS = require('aws-sdk');  // Don't do this!
    ```
    
    ## 2. Use SnapStart (Java/.NET)
    
    ```yaml
    # template.yaml
    Resources:
      JavaFunction:
        Type: AWS::Serverless::Function
        Properties:
          Handler: com.example.Handler::handleRequest
          Runtime: java21
          SnapStart:
            ApplyOn: PublishedVersions  # Enable SnapStart
          AutoPublishAlias: live
    ```
    
    ## 3. Right-size Memory
    
    ```yaml
    # More memory = more CPU = faster init
    Resources:
      FastFunction:
        Type: AWS::Serverless::Function
        Properties:
          MemorySize: 1024  # 1GB gets full vCPU
          Timeout: 30
    ```
    
    ## 4. Provisioned Concurrency (when needed)
    
    ```yaml
    Resources:
      CriticalFunction:
        Type: AWS::Serverless::Function
        Properties:
          Handler: src/handlers/critical.handler
          AutoPublishAlias: live
    
      ProvisionedConcurrency:
        Type: AWS::Lambda::ProvisionedConcurrencyConfig
        Properties:
          FunctionName: !Ref CriticalFunction
          Qualifier: live
          ProvisionedConcurrentExecutions: 5
    ```
    
    ## 5. Keep Init Light
    
    ```python
    # GOOD - Lazy initialization
    _table = None
    
    def get_table():
        global _table
        if _table is None:
            dynamodb = boto3.resource('dynamodb')
            _table = dynamodb.Table(os.environ['TABLE_NAME'])
        return _table
    
    def handler(event, context):
        table = get_table()  # Only initializes on first use
        # ...
    ```
    
  #### **Optimization Priority**
    ##### **1**
Reduce package size (biggest impact)
    ##### **2**
Use SnapStart for Java/.NET
    ##### **3**
Increase memory for faster init
    ##### **4**
Delay heavy imports
    ##### **5**
Provisioned concurrency (last resort)

---
  #### **Name**
SAM Local Development Pattern
  #### **Description**
Local testing and debugging with SAM CLI
  #### **When To Use**
    - Local development and testing
    - Debugging Lambda functions
    - Testing API Gateway locally
  #### **Implementation**
    ```bash
    # Install SAM CLI
    pip install aws-sam-cli
    
    # Initialize new project
    sam init --runtime nodejs20.x --name my-api
    
    # Build the project
    sam build
    
    # Run locally
    sam local start-api
    
    # Invoke single function
    sam local invoke GetItemFunction --event events/get.json
    
    # Local debugging (Node.js with VS Code)
    sam local invoke --debug-port 5858 GetItemFunction
    
    # Deploy
    sam deploy --guided
    ```
    
    ```json
    // events/get.json (test event)
    {
      "pathParameters": {
        "id": "123"
      },
      "httpMethod": "GET",
      "path": "/items/123"
    }
    ```
    
    ```json
    // .vscode/launch.json (for debugging)
    {
      "version": "0.2.0",
      "configurations": [
        {
          "name": "Attach to SAM CLI",
          "type": "node",
          "request": "attach",
          "address": "localhost",
          "port": 5858,
          "localRoot": "${workspaceRoot}/src",
          "remoteRoot": "/var/task/src",
          "protocol": "inspector"
        }
      ]
    }
    ```
    
  #### **Commands**
    ##### **Sam Build**
Build Lambda deployment packages
    ##### **Sam Local Start Api**
Start local API Gateway
    ##### **Sam Local Invoke**
Invoke single function
    ##### **Sam Deploy**
Deploy to AWS
    ##### **Sam Logs**
Tail CloudWatch logs

---
  #### **Name**
CDK Serverless Pattern
  #### **Description**
Infrastructure as code with AWS CDK
  #### **When To Use**
    - Complex infrastructure beyond Lambda
    - Prefer programming languages over YAML
    - Need reusable constructs
  #### **Implementation**
    ```typescript
    // lib/api-stack.ts
    import * as cdk from 'aws-cdk-lib';
    import * as lambda from 'aws-cdk-lib/aws-lambda';
    import * as apigateway from 'aws-cdk-lib/aws-apigateway';
    import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
    import { Construct } from 'constructs';
    
    export class ApiStack extends cdk.Stack {
      constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);
    
        // DynamoDB Table
        const table = new dynamodb.Table(this, 'ItemsTable', {
          partitionKey: { name: 'id', type: dynamodb.AttributeType.STRING },
          billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
          removalPolicy: cdk.RemovalPolicy.DESTROY, // For dev only
        });
    
        // Lambda Function
        const getItemFn = new lambda.Function(this, 'GetItemFunction', {
          runtime: lambda.Runtime.NODEJS_20_X,
          handler: 'get.handler',
          code: lambda.Code.fromAsset('src/handlers'),
          environment: {
            TABLE_NAME: table.tableName,
          },
          memorySize: 256,
          timeout: cdk.Duration.seconds(30),
        });
    
        // Grant permissions
        table.grantReadData(getItemFn);
    
        // API Gateway
        const api = new apigateway.RestApi(this, 'ItemsApi', {
          restApiName: 'Items Service',
          defaultCorsPreflightOptions: {
            allowOrigins: apigateway.Cors.ALL_ORIGINS,
            allowMethods: apigateway.Cors.ALL_METHODS,
          },
        });
    
        const items = api.root.addResource('items');
        const item = items.addResource('{id}');
    
        item.addMethod('GET', new apigateway.LambdaIntegration(getItemFn));
    
        // Output API URL
        new cdk.CfnOutput(this, 'ApiUrl', {
          value: api.url,
        });
      }
    }
    ```
    
    ```bash
    # CDK commands
    npm install -g aws-cdk
    cdk init app --language typescript
    cdk synth    # Generate CloudFormation
    cdk diff     # Show changes
    cdk deploy   # Deploy to AWS
    ```
    

## Anti-Patterns


---
  #### **Name**
Monolithic Lambda
  #### **Description**
Don't put all code in one function
  #### **Why Bad**
    Large deployment packages cause slow cold starts.
    Hard to scale individual operations.
    Updates affect entire system.
    
  #### **Bad Example**
    // One function handles everything
    exports.handler = async (event) => {
      switch(event.action) {
        case 'create': return createItem(event);
        case 'read': return readItem(event);
        case 'update': return updateItem(event);
        case 'delete': return deleteItem(event);
      }
    };
    
  #### **Good Example**
    // Separate functions for each operation
    // create.js, read.js, update.js, delete.js
    // Each with its own API Gateway route
    

---
  #### **Name**
Large Dependencies
  #### **Description**
Avoid bundling unnecessary packages
  #### **Why Bad**
    Increases deployment package size.
    Slows down cold starts significantly.
    Most of SDK/library may be unused.
    
  #### **Bad Example**
    // Imports entire AWS SDK v2
    const AWS = require('aws-sdk');
    const dynamodb = new AWS.DynamoDB.DocumentClient();
    
  #### **Good Example**
    // Import only needed clients from SDK v3
    const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
    const { DynamoDBDocumentClient } = require('@aws-sdk/lib-dynamodb');
    

---
  #### **Name**
Synchronous Calls in VPC
  #### **Description**
Avoid blocking calls that delay cold start
  #### **Why Bad**
    VPC-attached Lambdas have ENI setup overhead.
    Blocking DNS lookups or connections worsen cold starts.
    
  #### **Good Example**
    // Use async patterns, connection pooling
    // Ensure NAT Gateway is properly configured
    // Use VPC endpoints for AWS services
    