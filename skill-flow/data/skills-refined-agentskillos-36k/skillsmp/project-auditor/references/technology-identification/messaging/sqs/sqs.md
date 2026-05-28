# Amazon SQS

**Category**: messaging
**Description**: Amazon Simple Queue Service
**Homepage**: https://aws.amazon.com/sqs/

## Package Detection

### NPM
*SQS Node.js SDKs*

- `@aws-sdk/client-sqs`
- `sqs-consumer`
- `sqs-producer`

### MAVEN
*SQS Java SDKs*

- `software.amazon.awssdk:sqs`
- `com.amazonaws:aws-java-sdk-sqs`

### GO
*SQS Go SDK*

- `github.com/aws/aws-sdk-go-v2/service/sqs`

### NUGET
*SQS .NET SDK*

- `AWSSDK.SQS`

### Related Packages
- `serverless-offline-sqs`
- `elasticmq`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]@aws-sdk/client-sqs['"]`
- Type: esm_import

**Pattern**: `require\(['"]@aws-sdk/client-sqs['"]\)`
- Type: commonjs_require

**Pattern**: `from\s+['"]sqs-consumer['"]`
- Type: esm_import

**Pattern**: `AWS\.SQS`
- Type: aws_sdk_v2

### Python

**Pattern**: `boto3\.client\(['"]sqs['"]\)`
- Type: python_import

**Pattern**: `boto3\.resource\(['"]sqs['"]\)`
- Type: python_import

### Go

**Pattern**: `"github\.com/aws/aws-sdk-go-v2/service/sqs"`
- Type: go_import

**Pattern**: `"github\.com/aws/aws-sdk-go/service/sqs"`
- Type: go_import

## Environment Variables

*SQS queue URL*

*SQS queue URL (AWS prefixed)*

*SQS queue name*

*AWS region for SQS*

*AWS access key*

*AWS secret key*


## Detection Notes

- Check for SQS_QUEUE_URL environment variables
- Look for sqs.*.amazonaws.com references
- Often used with Lambda and SNS

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
