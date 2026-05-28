# AWS Lambda

**Category**: cloud-providers/aws-services
**Description**: Serverless compute service
**Homepage**: https://aws.amazon.com/lambda

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*AWS Lambda packages*

- `@aws-sdk/client-lambda` - Lambda SDK v3
- `aws-lambda` - Lambda types
- `@types/aws-lambda` - TypeScript definitions
- `serverless` - Serverless Framework
- `@serverless/components` - Serverless components
- `lambda-local` - Local Lambda testing
- `aws-lambda-local` - Local invocation
- `claudia` - Lambda deployment tool

#### PYPI
*AWS Lambda Python packages*

- `boto3` - AWS SDK (includes Lambda)
- `aws-lambda-powertools` - Lambda utilities
- `mangum` - ASGI adapter for Lambda
- `zappa` - Django/Flask on Lambda
- `chalice` - AWS Chalice framework

#### GO
*AWS Lambda Go packages*

- `github.com/aws/aws-lambda-go` - Lambda Go runtime
- `github.com/aws/aws-sdk-go-v2/service/lambda` - Lambda SDK

#### MAVEN
*AWS Lambda Java packages*

- `com.amazonaws:aws-lambda-java-core` - Core Lambda
- `com.amazonaws:aws-lambda-java-events` - Event types
- `software.amazon.awssdk:lambda` - SDK v2

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Lambda usage*

- `serverless.yml` - Serverless Framework
- `serverless.yaml` - Alternative
- `sam.yaml` - AWS SAM template
- `sam.yml` - Alternative
- `template.yaml` - SAM/CloudFormation
- `template.yml` - Alternative
- `.chalice/config.json` - Chalice config
- `zappa_settings.json` - Zappa config

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]@aws-sdk/client-lambda['"]`
- Lambda SDK v3 import
- Example: `import { LambdaClient } from '@aws-sdk/client-lambda';`

**Pattern**: `from\s+['"]aws-lambda['"]`
- Lambda types import
- Example: `import { Handler } from 'aws-lambda';`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+aws_lambda_powertools\s+import`
- Lambda Powertools import
- Example: `from aws_lambda_powertools import Logger`

**Pattern**: `def\s+handler\s*\([^)]*context[^)]*\)|def\s+lambda_handler`
- Lambda handler function
- Example: `def handler(event, context):`

#### Go
Extensions: `.go`

**Pattern**: `"github\.com/aws/aws-lambda-go/lambda"`
- Lambda Go runtime import
- Example: `import "github.com/aws/aws-lambda-go/lambda"`

**Pattern**: `lambda\.Start\(`
- Lambda handler registration
- Example: `lambda.Start(handler)`

### Code Patterns

**Pattern**: `exports\.handler|module\.exports\.handler`
- Node.js Lambda handler export
- Example: `exports.handler = async (event) => {...}`

**Pattern**: `AWS_LAMBDA_|LAMBDA_|_HANDLER`
- Lambda environment variables
- Example: `AWS_LAMBDA_FUNCTION_NAME`

**Pattern**: `arn:aws:lambda:[a-z0-9-]+:[0-9]+:function:`
- Lambda function ARN
- Example: `arn:aws:lambda:us-east-1:123456789:function:myFunc`

**Pattern**: `lambda\.invoke|InvokeCommand|invoke_function`
- Lambda invocation
- Example: `client.invoke({FunctionName: 'myFunc'})`

**Pattern**: `Type:\s*['"]?AWS::Serverless::Function|Type:\s*['"]?AWS::Lambda::Function`
- CloudFormation Lambda resources
- Example: SAM/CloudFormation templates

---

## Environment Variables

- `AWS_LAMBDA_FUNCTION_NAME` - Function name
- `AWS_LAMBDA_FUNCTION_VERSION` - Function version
- `AWS_LAMBDA_FUNCTION_MEMORY_SIZE` - Memory size
- `AWS_LAMBDA_LOG_GROUP_NAME` - CloudWatch log group
- `AWS_LAMBDA_LOG_STREAM_NAME` - CloudWatch log stream
- `AWS_EXECUTION_ENV` - Execution environment
- `_HANDLER` - Handler location
- `LAMBDA_TASK_ROOT` - Task root directory
- `LAMBDA_RUNTIME_DIR` - Runtime directory

## Detection Notes

- Handler format: file.function for most runtimes
- SAM and Serverless Framework are common deployment tools
- Lambda Powertools provides best practices utilities
- Container image support for custom runtimes

---

## Secrets Detection

### Credentials

See AWS patterns for credential detection. Lambda uses standard AWS authentication via IAM roles.

---

## TIER 3: Configuration Extraction

### Function Name Extraction

**Pattern**: `(?:FunctionName|function[_-]?name)\s*[=:]\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Lambda function name
- Extracts: `function_name`
- Example: `FunctionName: my-function`

### Handler Extraction

**Pattern**: `(?:Handler|handler)\s*[=:]\s*['"]?([a-zA-Z0-9._]+)['"]?`
- Lambda handler specification
- Extracts: `handler`
- Example: `Handler: index.handler`

### Memory Size Extraction

**Pattern**: `(?:MemorySize|memory[_-]?size)\s*[=:]\s*['"]?([0-9]+)['"]?`
- Lambda memory allocation
- Extracts: `memory_size`
- Example: `MemorySize: 1024`

### Runtime Extraction

**Pattern**: `(?:Runtime|runtime)\s*[=:]\s*['"]?([a-zA-Z0-9.]+)['"]?`
- Lambda runtime
- Extracts: `runtime`
- Example: `Runtime: nodejs18.x`
