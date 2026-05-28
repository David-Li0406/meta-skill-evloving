---
name: aws-development
description: Use when developing applications for AWS cloud platform with best practices and cost optimization
---

# AWS Development

Guidelines for building applications on AWS with security, performance, and cost optimization.

## When to Use

- Designing AWS-native applications
- Implementing serverless architectures
- Setting up AWS infrastructure
- Cost optimization reviews
- Security assessments for AWS workloads

## Core AWS Principles

1. **Well-Architected Framework** - Security, Reliability, Performance, Cost, Operations, Sustainability
2. **Least Privilege** - Minimal IAM permissions
3. **Defense in Depth** - Multiple security layers
4. **Automation First** - Infrastructure as Code
5. **Pay for What You Use** - Cost optimization
6. **Design for Failure** - Assume components will fail

## IAM Security Best Practices

### IAM Policies
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-app-bucket/user-uploads/*",
      "Condition": {
        "StringEquals": {
          "s3:x-amz-acl": "private"
        }
      }
    }
  ]
}
```

### IAM Roles for Services
```yaml
# Terraform example
resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_execution_role.name
}
```

### Security Checklist
- [ ] Enable MFA for all users
- [ ] Use IAM roles instead of access keys
- [ ] Rotate credentials regularly
- [ ] Enable CloudTrail for audit logging
- [ ] Use AWS Config for compliance
- [ ] Implement VPC security groups properly
- [ ] Enable encryption at rest and in transit
- [ ] Use AWS Secrets Manager for sensitive data

## Serverless Architecture

### Lambda Best Practices
```python
import json
import os
from typing import Dict, Any
import boto3
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.utilities.typing import LambdaContext

# Use Lambda Powertools for observability
logger = Logger()
tracer = Tracer()
metrics = Metrics()

@metrics.log_metrics
@tracer.capture_lambda_handler
@logger.inject_lambda_context
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    """
    Process S3 events and update database.
    """
    try:
        # Initialize clients outside handler for reuse
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ['TABLE_NAME'])
        
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            
            # Add custom metrics
            metrics.add_metric(name="FilesProcessed", unit="Count", value=1)
            
            # Process the file
            process_file(bucket, key, table)
            
        return {
            'statusCode': 200,
            'body': json.dumps('Success')
        }
        
    except Exception as e:
        logger.exception("Error processing event")
        metrics.add_metric(name="ProcessingErrors", unit="Count", value=1)
        raise

def process_file(bucket: str, key: str, table) -> None:
    """Process individual file and update database."""
    # Implementation here
    pass
```

### API Gateway + Lambda
```yaml
# SAM template
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 30
    Runtime: python3.11
    Environment:
      Variables:
        TABLE_NAME: !Ref UserTable

Resources:
  UserApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      Cors:
        AllowMethods: "'GET,POST,PUT,DELETE'"
        AllowHeaders: "'Content-Type,X-Amz-Date,Authorization'"
        AllowOrigin: "'*'"

  GetUserFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: get_user.lambda_handler
      Events:
        GetUser:
          Type: Api
          Properties:
            RestApiId: !Ref UserApi
            Path: /users/{id}
            Method: get
            
  UserTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
```

## Storage Solutions

### S3 Best Practices
```python
import boto3
from botocore.exceptions import ClientError

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client('s3')
    
    def upload_file_with_lifecycle(self, file_path: str, bucket: str, key: str) -> bool:
        """Upload file with proper metadata and lifecycle policies."""
        try:
            extra_args = {
                'ServerSideEncryption': 'AES256',
                'Metadata': {
                    'uploaded_by': 'api',
                    'timestamp': str(datetime.utcnow())
                },
                'StorageClass': 'STANDARD_IA'  # Cost optimization
            }
            
            self.s3_client.upload_file(file_path, bucket, key, ExtraArgs=extra_args)
            return True
            
        except ClientError as e:
            logger.error(f"Upload failed: {e}")
            return False
    
    def generate_presigned_url(self, bucket: str, key: str, expiration: int = 3600) -> str:
        """Generate presigned URL for secure temporary access."""
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            logger.error(f"Presigned URL generation failed: {e}")
            raise
```

### DynamoDB Patterns
```python
import boto3
from boto3.dynamodb.conditions import Key, Attr

class UserRepository:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('Users')
    
    def get_user_by_id(self, user_id: str) -> dict:
        """Get user by partition key."""
        try:
            response = self.table.get_item(Key={'id': user_id})
            return response.get('Item')
        except ClientError as e:
            logger.error(f"Get user failed: {e}")
            raise
    
    def query_users_by_status(self, status: str) -> list:
        """Query using GSI."""
        try:
            response = self.table.query(
                IndexName='status-index',
                KeyConditionExpression=Key('status').eq(status),
                FilterExpression=Attr('active').eq(True),
                Limit=100
            )
            return response['Items']
        except ClientError as e:
            logger.error(f"Query failed: {e}")
            raise
    
    def batch_write_users(self, users: list) -> bool:
        """Efficient batch writing."""
        try:
            with self.table.batch_writer() as batch:
                for user in users:
                    batch.put_item(Item=user)
            return True
        except ClientError as e:
            logger.error(f"Batch write failed: {e}")
            return False
```

## Event-Driven Architecture

### SQS + Lambda Integration
```python
import json
from typing import Dict, Any
import boto3

def sqs_handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """Process SQS messages with proper error handling."""
    
    successful_messages = []
    failed_messages = []
    
    for record in event['Records']:
        try:
            # Parse message
            message_body = json.loads(record['body'])
            
            # Process message
            result = process_message(message_body)
            
            if result:
                successful_messages.append(record['messageId'])
            else:
                failed_messages.append({
                    'itemIdentifier': record['messageId']
                })
                
        except Exception as e:
            logger.exception(f"Failed to process message {record['messageId']}")
            failed_messages.append({
                'itemIdentifier': record['messageId']
            })
    
    # Return partial batch failures for retry
    if failed_messages:
        return {
            'batchItemFailures': failed_messages
        }
    
    return {'statusCode': 200}

def process_message(message: Dict[str, Any]) -> bool:
    """Process individual message."""
    # Implementation here
    return True
```

### EventBridge Patterns
```yaml
# Custom event bus
CustomEventBus:
  Type: AWS::Events::EventBus
  Properties:
    Name: myapp-events

# Rule for user events
UserEventRule:
  Type: AWS::Events::Rule
  Properties:
    EventBusName: !Ref CustomEventBus
    EventPattern:
      source: ["myapp.users"]
      detail-type: ["User Created", "User Updated"]
    Targets:
      - Arn: !GetAtt ProcessUserFunction.Arn
        Id: "ProcessUserTarget"
```

## Monitoring and Observability

### CloudWatch Implementation
```python
import boto3
import time
from contextlib import contextmanager

class CloudWatchMetrics:
    def __init__(self, namespace: str):
        self.cloudwatch = boto3.client('cloudwatch')
        self.namespace = namespace
    
    def put_metric(self, metric_name: str, value: float, unit: str = 'Count', dimensions: dict = None):
        """Put custom metric to CloudWatch."""
        try:
            metric_data = {
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': time.time()
            }
            
            if dimensions:
                metric_data['Dimensions'] = [
                    {'Name': k, 'Value': v} for k, v in dimensions.items()
                ]
            
            self.cloudwatch.put_metric_data(
                Namespace=self.namespace,
                MetricData=[metric_data]
            )
            
        except Exception as e:
            logger.error(f"Failed to put metric: {e}")
    
    @contextmanager
    def timer(self, metric_name: str, dimensions: dict = None):
        """Context manager for timing operations."""
        start_time = time.time()
        try:
            yield
        finally:
            duration = (time.time() - start_time) * 1000  # Convert to milliseconds
            self.put_metric(metric_name, duration, 'Milliseconds', dimensions)
```

### X-Ray Tracing
```python
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# Patch AWS SDK calls
patch_all()

@xray_recorder.capture('database_operation')
def query_database(user_id: str) -> dict:
    """Database query with X-Ray tracing."""
    subsegment = xray_recorder.current_subsegment()
    subsegment.put_metadata('user_id', user_id)
    
    try:
        # Database operation
        result = database.query(user_id)
        subsegment.put_annotation('success', True)
        return result
        
    except Exception as e:
        subsegment.put_annotation('success', False)
        subsegment.add_exception(e)
        raise
```

## Cost Optimization

### Lambda Cost Optimization
```python
# Use appropriate memory settings
# Monitor with AWS Lambda Power Tuning tool

def optimized_lambda_handler(event, context):
    """Lambda with cost optimization considerations."""
    
    # Reuse connections (initialize outside handler in real code)
    # Use connection pooling
    # Optimize memory allocation
    # Use provisioned concurrency for consistent traffic
    
    # Batch operations when possible
    batch_size = 25  # DynamoDB batch limit
    items = event.get('items', [])
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        process_batch(batch)
```

### S3 Cost Optimization
```yaml
# Lifecycle policies
S3BucketPolicy:
  Type: AWS::S3::Bucket
  Properties:
    LifecycleConfiguration:
      Rules:
        - Id: ArchiveOldFiles
          Status: Enabled
          Transitions:
            - TransitionInDays: 30
              StorageClass: STANDARD_IA
            - TransitionInDays: 90
              StorageClass: GLACIER
            - TransitionInDays: 365
              StorageClass: DEEP_ARCHIVE
        - Id: DeleteOldLogs
          Status: Enabled
          ExpirationInDays: 2555  # 7 years
          Prefix: logs/
```

## Infrastructure as Code

### CDK Example (Python)
```python
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    Duration
)

class ServerlessApiStack(Stack):
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        
        # DynamoDB table
        table = dynamodb.Table(
            self, "UserTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery=True,
            removal_policy=RemovalPolicy.DESTROY  # For dev only
        )
        
        # Lambda function
        lambda_function = _lambda.Function(
            self, "UserHandler",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset("lambda"),
            handler="index.handler",
            timeout=Duration.seconds(30),
            environment={
                "TABLE_NAME": table.table_name
            }
        )
        
        # Grant permissions
        table.grant_read_write_data(lambda_function)
        
        # API Gateway
        api = apigw.RestApi(
            self, "UserApi",
            rest_api_name="User Service",
            description="User management API"
        )
        
        users_resource = api.root.add_resource("users")
        users_resource.add_method(
            "GET", 
            apigw.LambdaIntegration(lambda_function)
        )
```

## Security Checklist

- [ ] Enable CloudTrail in all regions
- [ ] Use AWS Config for compliance monitoring
- [ ] Implement VPC Flow Logs
- [ ] Enable GuardDuty for threat detection
- [ ] Use AWS Security Hub for central management
- [ ] Implement resource-based policies
- [ ] Use AWS WAF for web applications
- [ ] Enable EBS encryption by default
- [ ] Use KMS for encryption key management
- [ ] Implement network segmentation with VPCs

## Performance Best Practices

- [ ] Use CloudFront for global content delivery
- [ ] Implement caching strategies (ElastiCache/DAX)
- [ ] Optimize DynamoDB with proper partition keys
- [ ] Use RDS read replicas for read-heavy workloads
- [ ] Implement auto-scaling for variable loads
- [ ] Monitor performance with CloudWatch Insights
- [ ] Use Lambda provisioned concurrency for low latency
- [ ] Optimize S3 transfer acceleration for large files

## Common Anti-Patterns

### Avoid Over-Provisioning
```python
# ❌ Fixed large instance when load varies
instance_type = "m5.8xlarge"  # Always expensive

# ✅ Auto-scaling with appropriate instances
min_capacity = 2
max_capacity = 50
target_cpu_utilization = 70
```

### Don't Ignore Cost Monitoring
```python
# ✅ Implement cost alerts
import boto3

def create_cost_alert():
    budgets_client = boto3.client('budgets')
    
    budgets_client.create_budget(
        AccountId='123456789012',
        Budget={
            'BudgetName': 'Monthly Cost Alert',
            'BudgetLimit': {
                'Amount': '1000',
                'Unit': 'USD'
            },
            'TimeUnit': 'MONTHLY',
            'BudgetType': 'COST'
        }
    )
```

## Troubleshooting Commands

```bash
# CloudFormation
aws cloudformation describe-stack-events --stack-name mystack

# Lambda logs
aws logs tail /aws/lambda/function-name --follow

# DynamoDB metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/DynamoDB \
  --metric-name ConsumedReadCapacityUnits \
  --dimensions Name=TableName,Value=MyTable

# Cost analysis
aws ce get-cost-and-usage \
  --time-period Start=2023-01-01,End=2023-02-01 \
  --granularity MONTHLY \
  --metrics BlendedCost

# Security analysis
aws config get-compliance-details-by-config-rule \
  --config-rule-name s3-bucket-public-read-prohibited
```

## Remember

> AWS is a toolkit, not a solution. Choose the right service for each job, design for failure, and always monitor costs. Security and performance are not afterthoughts.