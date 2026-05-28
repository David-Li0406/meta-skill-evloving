# Amazon SQS (Simple Queue Service)

**Category**: cloud-providers/aws-services
**Description**: Fully managed message queuing service
**Homepage**: https://aws.amazon.com/sqs

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*SQS JavaScript packages*

- `@aws-sdk/client-sqs` - SQS SDK v3
- `sqs-consumer` - SQS message consumer
- `sqs-producer` - SQS message producer

#### PYPI
*SQS Python packages*

- `boto3` - AWS SDK (includes SQS)

#### GO
*SQS Go packages*

- `github.com/aws/aws-sdk-go-v2/service/sqs` - SQS SDK v2

#### MAVEN
*SQS Java packages*

- `software.amazon.awssdk:sqs` - SDK v2
- `com.amazonaws:aws-java-sdk-sqs` - SDK v1
- `org.springframework.cloud:spring-cloud-aws-messaging` - Spring integration

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]@aws-sdk/client-sqs['"]`
- SQS SDK v3 import
- Example: `import { SQSClient } from '@aws-sdk/client-sqs';`

**Pattern**: `from\s+['"]sqs-consumer['"]`
- SQS consumer import
- Example: `import { Consumer } from 'sqs-consumer';`

#### Python
Extensions: `.py`

**Pattern**: `boto3\.resource\(['"]sqs['"]\)|boto3\.client\(['"]sqs['"]\)`
- Boto3 SQS resource/client
- Example: `sqs = boto3.client('sqs')`

### Code Patterns

**Pattern**: `sqs\.|SQS|SendMessage|ReceiveMessage|DeleteMessage|QueueUrl`
- SQS operations
- Example: `client.send_message(QueueUrl=url, MessageBody=body)`

**Pattern**: `SQS_QUEUE_URL|SQS_QUEUE_NAME`
- SQS environment variables
- Example: `SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/...`

**Pattern**: `arn:aws:sqs:[a-z0-9-]+:[0-9]+:`
- SQS queue ARN
- Example: `arn:aws:sqs:us-east-1:123456789:my-queue`

**Pattern**: `sqs\.[a-z0-9-]+\.amazonaws\.com`
- SQS endpoint URL
- Example: `https://sqs.us-east-1.amazonaws.com/123456789/my-queue`

**Pattern**: `Type:\s*['"]?AWS::SQS::Queue`
- CloudFormation SQS resource

---

## Environment Variables

- `SQS_QUEUE_URL` - Queue URL
- `SQS_QUEUE_NAME` - Queue name
- `AWS_SQS_QUEUE_URL` - Alternative queue URL

## Detection Notes

- Standard and FIFO queue types
- Dead letter queues for failed messages
- Long polling for efficient message retrieval
- Visibility timeout prevents duplicate processing

---

## TIER 3: Configuration Extraction

### Queue URL Extraction

**Pattern**: `(?:QueueUrl|queue[_-]?url|SQS_QUEUE_URL)\s*[=:]\s*['"]?(https://sqs\.[^\s'"]+)['"]?`
- SQS queue URL
- Extracts: `queue_url`
- Example: `QueueUrl: https://sqs.us-east-1.amazonaws.com/123/my-queue`

### Queue Name Extraction

**Pattern**: `(?:QueueName|queue[_-]?name|SQS_QUEUE_NAME)\s*[=:]\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- SQS queue name
- Extracts: `queue_name`
- Example: `QueueName: my-queue`
