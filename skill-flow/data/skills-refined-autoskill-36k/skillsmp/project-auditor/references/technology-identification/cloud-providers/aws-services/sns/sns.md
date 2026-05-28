# Amazon SNS (Simple Notification Service)

**Category**: cloud-providers/aws-services
**Description**: Pub/sub messaging and mobile notifications
**Homepage**: https://aws.amazon.com/sns

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*SNS JavaScript packages*

- `@aws-sdk/client-sns` - SNS SDK v3

#### PYPI
*SNS Python packages*

- `boto3` - AWS SDK (includes SNS)

#### GO
*SNS Go packages*

- `github.com/aws/aws-sdk-go-v2/service/sns` - SNS SDK v2

#### MAVEN
*SNS Java packages*

- `software.amazon.awssdk:sns` - SDK v2
- `com.amazonaws:aws-java-sdk-sns` - SDK v1

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]@aws-sdk/client-sns['"]`
- SNS SDK v3 import
- Example: `import { SNSClient } from '@aws-sdk/client-sns';`

#### Python
Extensions: `.py`

**Pattern**: `boto3\.resource\(['"]sns['"]\)|boto3\.client\(['"]sns['"]\)`
- Boto3 SNS resource/client
- Example: `sns = boto3.client('sns')`

### Code Patterns

**Pattern**: `sns\.|SNS|Publish|Subscribe|CreateTopic|TopicArn`
- SNS operations
- Example: `client.publish(TopicArn=arn, Message=message)`

**Pattern**: `SNS_TOPIC_ARN|SNS_TOPIC_NAME`
- SNS environment variables
- Example: `SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123:my-topic`

**Pattern**: `arn:aws:sns:[a-z0-9-]+:[0-9]+:`
- SNS topic ARN
- Example: `arn:aws:sns:us-east-1:123456789:my-topic`

**Pattern**: `Type:\s*['"]?AWS::SNS::Topic`
- CloudFormation SNS resource

---

## Environment Variables

- `SNS_TOPIC_ARN` - Topic ARN
- `SNS_TOPIC_NAME` - Topic name
- `AWS_SNS_TOPIC_ARN` - Alternative topic ARN

## Detection Notes

- Pub/sub messaging pattern
- SMS, email, and push notifications
- Fan-out to multiple SQS queues
- FIFO topics for ordered delivery

---

## TIER 3: Configuration Extraction

### Topic ARN Extraction

**Pattern**: `(?:TopicArn|topic[_-]?arn|SNS_TOPIC_ARN)\s*[=:]\s*['"]?(arn:aws:sns:[^\s'"]+)['"]?`
- SNS topic ARN
- Extracts: `topic_arn`
- Example: `TopicArn: arn:aws:sns:us-east-1:123:my-topic`
