# Amazon DynamoDB

**Category**: databases
**Description**: Amazon DynamoDB NoSQL database
**Homepage**: https://aws.amazon.com/dynamodb/

## Package Detection

### NPM
*DynamoDB Node.js SDKs*

- `@aws-sdk/client-dynamodb`
- `@aws-sdk/lib-dynamodb`
- `dynamodb-toolbox`
- `dynamoose`

### PYPI
*DynamoDB Python SDKs*

- `pynamodb`

### MAVEN
*DynamoDB Java SDKs*

- `software.amazon.awssdk:dynamodb`
- `software.amazon.awssdk:dynamodb-enhanced`

### GO
*DynamoDB Go SDK*

- `github.com/aws/aws-sdk-go-v2/service/dynamodb`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]@aws-sdk/client-dynamodb['"]`
- Type: esm_import

**Pattern**: `from\s+['"]@aws-sdk/lib-dynamodb['"]`
- Type: esm_import

**Pattern**: `from\s+['"]dynamoose['"]`
- Type: esm_import

### Python

**Pattern**: `boto3\.resource\(['"]dynamodb['"]\)`
- Type: python_import

**Pattern**: `from\s+pynamodb`
- Type: python_import

## Environment Variables

*DynamoDB table name*

*DynamoDB endpoint (local)*

*DynamoDB table name*


## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
