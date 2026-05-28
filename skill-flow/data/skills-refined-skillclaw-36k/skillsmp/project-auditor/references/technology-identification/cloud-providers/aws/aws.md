# AWS

**Category**: cloud-providers
**Description**: Amazon Web Services cloud platform SDKs and tools
**Homepage**: https://aws.amazon.com

---

## TIER 1: Quick Detection (SBOM-based)

These patterns are used during quick scans that only analyze the SBOM.

### Package Detection

#### NPM
*AWS JavaScript SDK v2 and v3*

- `aws-sdk` - AWS SDK v2 for JavaScript
- `@aws-sdk/client-s3` - S3 client (v3)
- `@aws-sdk/client-dynamodb` - DynamoDB client (v3)
- `@aws-sdk/client-lambda` - Lambda client (v3)
- `@aws-sdk/client-sqs` - SQS client (v3)
- `@aws-sdk/client-sns` - SNS client (v3)
- `@aws-sdk/client-ec2` - EC2 client (v3)
- `@aws-sdk/client-iam` - IAM client (v3)
- `@aws-sdk/client-sts` - STS client (v3)
- `@aws-sdk/client-secrets-manager` - Secrets Manager client (v3)
- `@aws-sdk/client-cloudwatch` - CloudWatch client (v3)
- `@aws-sdk/client-cognito-identity-provider` - Cognito client (v3)
- `@aws-sdk/client-kms` - KMS client (v3)
- `@aws-sdk/client-ssm` - SSM client (v3)
- `@aws-sdk/client-cloudformation` - CloudFormation client (v3)
- `@aws-sdk/client-rds` - RDS client (v3)
- `@aws-sdk/client-elasticache` - ElastiCache client (v3)
- `@aws-sdk/lib-dynamodb` - DynamoDB Document client (v3)

#### PYPI
*AWS Python SDK*

- `boto3` - AWS SDK for Python
- `botocore` - Low-level AWS SDK for Python
- `aioboto3` - Async AWS SDK for Python
- `aiobotocore` - Async botocore
- `aws-cdk-lib` - AWS CDK library
- `aws-cdk.core` - AWS CDK core (v1)
- `moto` - AWS service mocking library

#### GO
*AWS Go SDK*

- `github.com/aws/aws-sdk-go` - AWS SDK for Go v1
- `github.com/aws/aws-sdk-go-v2` - AWS SDK for Go v2
- `github.com/aws/aws-cdk-go` - AWS CDK for Go

#### MAVEN
*AWS Java SDK*

- `software.amazon.awssdk:s3` - S3 client (v2)
- `software.amazon.awssdk:dynamodb` - DynamoDB client (v2)
- `software.amazon.awssdk:lambda` - Lambda client (v2)
- `software.amazon.awssdk:sqs` - SQS client (v2)
- `software.amazon.awssdk:sns` - SNS client (v2)
- `com.amazonaws:aws-java-sdk` - AWS SDK v1 for Java
- `com.amazonaws:aws-java-sdk-core` - Core v1 SDK
- `com.amazonaws:aws-lambda-java-core` - Lambda Java runtime

#### RUBYGEMS
*AWS Ruby SDK*

- `aws-sdk` - AWS SDK for Ruby (full)
- `aws-sdk-core` - Core SDK
- `aws-sdk-s3` - S3 client
- `aws-sdk-dynamodb` - DynamoDB client
- `aws-sdk-lambda` - Lambda client

#### NUGET
*AWS .NET SDK*

- `AWSSDK.Core` - Core SDK
- `AWSSDK.S3` - S3 client
- `AWSSDK.DynamoDBv2` - DynamoDB client
- `AWSSDK.Lambda` - Lambda client

---

## TIER 2: Deep Detection (File-based)

These patterns require scanning repository files and take longer to run.

### Configuration Files
*Known configuration files that indicate AWS usage*

- `serverless.yml` - Serverless Framework configuration
- `serverless.yaml` - Serverless Framework configuration
- `sam.yml` - AWS SAM template
- `sam.yaml` - AWS SAM template
- `template.yml` - CloudFormation/SAM template
- `template.yaml` - CloudFormation/SAM template
- `cdk.json` - AWS CDK configuration
- `cdk.context.json` - AWS CDK context
- `.aws/credentials` - AWS credentials file
- `.aws/config` - AWS config file
- `buildspec.yml` - AWS CodeBuild specification
- `buildspec.yaml` - AWS CodeBuild specification
- `appspec.yml` - AWS CodeDeploy specification
- `appspec.yaml` - AWS CodeDeploy specification
- `taskdef.json` - ECS task definition
- `.chalice/config.json` - AWS Chalice configuration

### Configuration Directories
*Known directories that indicate AWS usage*

- `.aws/` - AWS configuration directory
- `cdk.out/` - AWS CDK output directory
- `.chalice/` - AWS Chalice directory

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`, `.mjs`

**Pattern**: `from\s+['"]aws-sdk['"]`
- AWS SDK v2 ES6 import
- Example: `import AWS from 'aws-sdk';`

**Pattern**: `require\(['"]aws-sdk['"]\)`
- AWS SDK v2 CommonJS require
- Example: `const AWS = require('aws-sdk');`

**Pattern**: `from\s+['"]@aws-sdk/client-`
- AWS SDK v3 ES6 import
- Example: `import { S3Client } from '@aws-sdk/client-s3';`

**Pattern**: `require\(['"]@aws-sdk/client-`
- AWS SDK v3 CommonJS require
- Example: `const { S3Client } = require('@aws-sdk/client-s3');`

#### Python
Extensions: `.py`

**Pattern**: `^import\s+boto3`
- boto3 import
- Example: `import boto3`

**Pattern**: `^from\s+boto3\s+import`
- boto3 from import
- Example: `from boto3 import client`

**Pattern**: `^import\s+botocore`
- botocore import
- Example: `import botocore`

**Pattern**: `^from\s+botocore\s+import`
- botocore from import
- Example: `from botocore.exceptions import ClientError`

**Pattern**: `^from\s+aws_cdk\s+import`
- AWS CDK import
- Example: `from aws_cdk import Stack, App`

#### Go
Extensions: `.go`

**Pattern**: `"github\.com/aws/aws-sdk-go`
- AWS SDK Go v1 import
- Example: `import "github.com/aws/aws-sdk-go/aws"`

**Pattern**: `"github\.com/aws/aws-sdk-go-v2`
- AWS SDK Go v2 import
- Example: `import "github.com/aws/aws-sdk-go-v2/service/s3"`

### Code Patterns
*AWS CloudFormation/SAM template patterns*

**Pattern**: `^AWSTemplateFormatVersion:`
- CloudFormation template declaration
- Example: `AWSTemplateFormatVersion: '2010-09-09'`

**Pattern**: `^Transform:\s*AWS::Serverless`
- SAM transform declaration
- Example: `Transform: AWS::Serverless-2016-10-31`

**Pattern**: `^Resources:\s*$`
- CloudFormation Resources section
- Example: `Resources:`

**Pattern**: `^\s+Type:\s*AWS::`
- AWS resource type
- Example: `Type: AWS::Lambda::Function`

**Pattern**: `^\s+Type:\s*AWS::Serverless::`
- SAM resource type
- Example: `Type: AWS::Serverless::Function`

**Pattern**: `!Ref\s+`
- CloudFormation intrinsic function
- Example: `!Ref MyBucket`

**Pattern**: `!GetAtt\s+`
- CloudFormation GetAtt function
- Example: `!GetAtt MyBucket.Arn`

**Pattern**: `!Sub\s+`
- CloudFormation Sub function
- Example: `!Sub '${AWS::StackName}-bucket'`

---

## Environment Variables

- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `AWS_SESSION_TOKEN` - AWS session token
- `AWS_REGION` - AWS region
- `AWS_DEFAULT_REGION` - Default AWS region
- `AWS_PROFILE` - AWS profile name
- `AWS_CONFIG_FILE` - Path to AWS config
- `AWS_SHARED_CREDENTIALS_FILE` - Path to credentials
- `AWS_LAMBDA_FUNCTION_NAME` - Lambda function name
- `AWS_LAMBDA_FUNCTION_VERSION` - Lambda function version
- `AWS_EXECUTION_ENV` - Lambda execution environment
- `AWS_LAMBDA_LOG_GROUP_NAME` - Lambda CloudWatch log group
- `AWS_LAMBDA_LOG_STREAM_NAME` - Lambda log stream
- `AWS_CONTAINER_CREDENTIALS_RELATIVE_URI` - ECS credentials URI
- `AWS_SDK_LOAD_CONFIG` - Load SDK config from file

## Detection Notes

- `boto3` and `aws-sdk` packages are the strongest indicators
- AWS SDK v3 (`@aws-sdk/*`) is modular with per-service packages
- CloudFormation templates use YAML with `AWSTemplateFormatVersion`
- SAM templates extend CloudFormation with `Transform: AWS::Serverless`
- AWS CDK generates CloudFormation from code
- Look for `.aws/` directory for local AWS configuration
- ECS/Lambda environment variables indicate AWS deployment

---

## Secrets Detection

### API Keys and Credentials

#### AWS Access Key ID
**Pattern**: `AKIA[0-9A-Z]{16}`
**Severity**: critical
**Description**: AWS Access Key ID - used for programmatic access to AWS services
**Example**: `AKIAIOSFODNN7EXAMPLE`

#### AWS Secret Access Key
**Pattern**: `(?:aws_secret_access_key|AWS_SECRET_ACCESS_KEY|secret_access_key|SecretAccessKey)\s*[=:]\s*['"]?([A-Za-z0-9/+=]{40})['"]?`
**Severity**: critical
**Description**: AWS Secret Access Key - paired with Access Key ID for authentication
**Example**: `aws_secret_access_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"`

#### AWS Session Token
**Pattern**: `(?:aws_session_token|AWS_SESSION_TOKEN)\s*[=:]\s*['"]?([A-Za-z0-9/+=]{100,})['"]?`
**Severity**: high
**Description**: Temporary session token for AWS STS
**Example**: `AWS_SESSION_TOKEN=FwoGZX...long_token`

### Validation

#### API Documentation
- **IAM Credentials**: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
- **STS API**: https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html
- **Security Best Practices**: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html

#### Validation Endpoint
**API**: AWS STS GetCallerIdentity
**Endpoint**: `https://sts.amazonaws.com/`
**Method**: POST
**Headers**: `Authorization: AWS4-HMAC-SHA256 ...`
**Purpose**: Validates if credentials are active and returns account/user info

```bash
# Validate AWS credentials
aws sts get-caller-identity
```

#### Validation Code (Python)
```python
import boto3
from botocore.exceptions import ClientError

def validate_aws_credentials(access_key, secret_key, session_token=None):
    """Validate AWS credentials by calling STS GetCallerIdentity"""
    try:
        client = boto3.client(
            'sts',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token
        )
        response = client.get_caller_identity()
        return {
            'valid': True,
            'account': response['Account'],
            'arn': response['Arn'],
            'user_id': response['UserId']
        }
    except ClientError as e:
        return {'valid': False, 'error': str(e)}
```

---

## TIER 3: Configuration Extraction

These patterns extract specific AWS resource identifiers and configuration.

### AWS Account ID Extraction

**Pattern**: `([0-9]{12})\.dkr\.ecr\.([a-z]{2}-[a-z]+-[0-9])\.amazonaws\.com`
- AWS account from ECR URL
- Extracts: `account_id`, `region`
- Example: `123456789012.dkr.ecr.us-west-2.amazonaws.com`

**Pattern**: `arn:aws(?:-[a-z]+)?:([a-z0-9-]+):([a-z]{2}-[a-z]+-[0-9]|):([0-9]{12}):([^\s'"]+)`
- AWS account from ARN
- Extracts: `service`, `region`, `account_id`, `resource`
- Example: `arn:aws:iam::123456789012:role/MyRole`

### Region Extraction

**Pattern**: `region\s*[=:]\s*['"]?([a-z]{2}-[a-z]+-[0-9])['"]?`
- AWS region from config
- Extracts: `region`
- Example: `region = "us-west-2"`

**Pattern**: `AWS_DEFAULT_REGION\s*[=:]\s*['"]?([a-z]{2}-[a-z]+-[0-9])['"]?`
- AWS region from environment
- Extracts: `region`
- Example: `AWS_DEFAULT_REGION=us-west-2`

### S3 Bucket Extraction

**Pattern**: `s3://([a-z0-9][a-z0-9.-]{1,61}[a-z0-9])/?`
- S3 bucket from URI
- Extracts: `bucket_name`
- Example: `s3://my-application-bucket/`

**Pattern**: `bucket\s*[=:]\s*['"]([a-z0-9][a-z0-9.-]{1,61}[a-z0-9])['"]`
- S3 bucket from config
- Extracts: `bucket_name`
- Example: `bucket = "terraform-state-bucket"`

### IAM Role Extraction

**Pattern**: `role-to-assume:\s*arn:aws:iam::([0-9]{12}):role/([^\s'"]+)`
- IAM role from GitHub Actions OIDC
- Extracts: `account_id`, `role_name`
- Example: `role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole`

**Pattern**: `execution_role_arn\s*[=:]\s*['"]?arn:aws:iam::([0-9]{12}):role/([^'"]+)['"]?`
- ECS/Lambda execution role
- Extracts: `account_id`, `role_name`
- Example: `execution_role_arn = "arn:aws:iam::123456789012:role/ecsTaskRole"`

### Lambda Function Extraction

**Pattern**: `function_name\s*[=:]\s*['"]([a-zA-Z0-9_-]+)['"]`
- Lambda function name
- Extracts: `function_name`
- Example: `function_name = "my-api-handler"`

### API Gateway Extraction

**Pattern**: `([a-z0-9]+)\.execute-api\.([a-z]{2}-[a-z]+-[0-9])\.amazonaws\.com`
- API Gateway endpoint
- Extracts: `api_id`, `region`
- Example: `abc123xyz.execute-api.us-west-2.amazonaws.com`

### RDS Extraction

**Pattern**: `([a-z][a-z0-9-]+)\.([a-z0-9]+)\.([a-z]{2}-[a-z]+-[0-9])\.rds\.amazonaws\.com`
- RDS endpoint
- Extracts: `instance_id`, `cluster_id`, `region`
- Example: `mydb.cluster-abc123.us-west-2.rds.amazonaws.com`

### DynamoDB Table Extraction

**Pattern**: `table_name\s*[=:]\s*['"]([a-zA-Z0-9_.-]+)['"]`
- DynamoDB table name
- Extracts: `table_name`
- Example: `table_name = "users-table"`

### SQS Queue Extraction

**Pattern**: `https://sqs\.([a-z]{2}-[a-z]+-[0-9])\.amazonaws\.com/([0-9]{12})/([a-zA-Z0-9_-]+)`
- SQS queue URL
- Extracts: `region`, `account_id`, `queue_name`
- Example: `https://sqs.us-west-2.amazonaws.com/123456789012/my-queue`

### Secrets Manager Extraction

**Pattern**: `arn:aws:secretsmanager:([a-z]{2}-[a-z]+-[0-9]):([0-9]{12}):secret:([^:'"]+)`
- Secrets Manager ARN
- Extracts: `region`, `account_id`, `secret_name`
- Example: `arn:aws:secretsmanager:us-west-2:123456789012:secret:prod/db-creds`

### Extraction Output Example

```json
{
  "extractions": {
    "aws_accounts": [
      {
        "account_id": "123456789012",
        "regions": ["us-west-2", "us-east-1"],
        "source_files": ["Dockerfile", "terraform/main.tf"]
      }
    ],
    "s3_buckets": [
      {
        "name": "terraform-state-bucket",
        "source_file": "backend.tf",
        "line": 5
      }
    ],
    "iam_roles": [
      {
        "role_name": "GitHubActionsRole",
        "account_id": "123456789012",
        "source_file": ".github/workflows/deploy.yml",
        "line": 25
      }
    ],
    "rds_instances": [
      {
        "instance_id": "mydb",
        "region": "us-west-2",
        "source_file": "config/database.yml"
      }
    ],
    "api_gateways": [
      {
        "api_id": "abc123xyz",
        "region": "us-west-2",
        "source_file": "serverless.yml"
      }
    ]
  }
}
```
