# Amazon DynamoDB

**Category**: cloud-providers/aws-services
**Description**: Fully managed NoSQL database service
**Homepage**: https://aws.amazon.com/dynamodb

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*DynamoDB JavaScript packages*

- `@aws-sdk/client-dynamodb` - DynamoDB SDK v3
- `@aws-sdk/lib-dynamodb` - DynamoDB Document Client v3
- `@aws-sdk/util-dynamodb` - DynamoDB utilities
- `dynamodb` - Alternative client
- `dynamoose` - DynamoDB ORM
- `dynamodb-toolbox` - DynamoDB toolkit

#### PYPI
*DynamoDB Python packages*

- `boto3` - AWS SDK (includes DynamoDB)
- `pynamodb` - DynamoDB ORM
- `dynamodb-json` - JSON marshalling

#### GO
*DynamoDB Go packages*

- `github.com/aws/aws-sdk-go-v2/service/dynamodb` - DynamoDB SDK v2
- `github.com/guregu/dynamo` - DynamoDB ORM

#### MAVEN
*DynamoDB Java packages*

- `software.amazon.awssdk:dynamodb` - SDK v2
- `software.amazon.awssdk:dynamodb-enhanced` - Enhanced client
- `com.amazonaws:aws-java-sdk-dynamodb` - SDK v1

#### NUGET
*DynamoDB .NET packages*

- `AWSSDK.DynamoDBv2` - .NET SDK

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]@aws-sdk/client-dynamodb['"]`
- DynamoDB SDK v3 import
- Example: `import { DynamoDBClient } from '@aws-sdk/client-dynamodb';`

**Pattern**: `from\s+['"]@aws-sdk/lib-dynamodb['"]`
- Document Client import
- Example: `import { DynamoDBDocumentClient } from '@aws-sdk/lib-dynamodb';`

**Pattern**: `from\s+['"]dynamoose['"]`
- Dynamoose ORM import
- Example: `import dynamoose from 'dynamoose';`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+pynamodb\s+import`
- PynamoDB import
- Example: `from pynamodb.models import Model`

**Pattern**: `boto3\.resource\(['"]dynamodb['"]\)|boto3\.client\(['"]dynamodb['"]\)`
- Boto3 DynamoDB resource/client
- Example: `dynamodb = boto3.resource('dynamodb')`

#### Go
Extensions: `.go`

**Pattern**: `"github\.com/aws/aws-sdk-go-v2/service/dynamodb"`
- DynamoDB Go SDK import
- Example: `import "github.com/aws/aws-sdk-go-v2/service/dynamodb"`

### Code Patterns

**Pattern**: `dynamodb\.|DynamoDB|PutItem|GetItem|Query|Scan|UpdateItem|DeleteItem`
- DynamoDB operations
- Example: `await client.send(new PutItemCommand(...))`

**Pattern**: `AWS_DYNAMODB_|DYNAMODB_`
- DynamoDB environment variables
- Example: `AWS_DYNAMODB_TABLE_NAME`

**Pattern**: `arn:aws:dynamodb:[a-z0-9-]+:[0-9]+:table/`
- DynamoDB table ARN
- Example: `arn:aws:dynamodb:us-east-1:123456789:table/MyTable`

**Pattern**: `Type:\s*['"]?AWS::DynamoDB::Table`
- CloudFormation DynamoDB resource
- Example: In SAM/CloudFormation templates

**Pattern**: `KeyConditionExpression|FilterExpression|ProjectionExpression`
- DynamoDB query expressions
- Example: `KeyConditionExpression: 'pk = :pk'`

**Pattern**: `:4566/|localhost:8000|dynamodb-local`
- Local DynamoDB
- Example: `http://localhost:8000`

---

## Environment Variables

- `AWS_DYNAMODB_TABLE_NAME` - Table name
- `DYNAMODB_ENDPOINT` - Custom endpoint
- `DYNAMODB_TABLE` - Table name
- `AWS_SAM_LOCAL` - SAM local mode

## Detection Notes

- NoSQL key-value and document database
- Single-table design is recommended
- DynamoDB Local for development
- Streams for change data capture
- Global tables for multi-region

---

## Secrets Detection

### Credentials

See AWS patterns for credential detection. DynamoDB uses standard AWS authentication via IAM.

---

## TIER 3: Configuration Extraction

### Table Name Extraction

**Pattern**: `(?:TableName|table[_-]?name|DYNAMODB_TABLE)\s*[=:]\s*['"]?([a-zA-Z0-9_.-]+)['"]?`
- DynamoDB table name
- Extracts: `table_name`
- Example: `TableName: my-table`

### Endpoint Extraction

**Pattern**: `(?:endpoint|DYNAMODB_ENDPOINT)\s*[=:]\s*['"]?(https?://[^\s'"]+)['"]?`
- Custom DynamoDB endpoint
- Extracts: `endpoint`
- Example: `endpoint: http://localhost:8000`

### Region Extraction

**Pattern**: `(?:region|AWS_REGION)\s*[=:]\s*['"]?([a-z]{2}-[a-z]+-[0-9]+)['"]?`
- AWS region
- Extracts: `region`
- Example: `region: us-east-1`
