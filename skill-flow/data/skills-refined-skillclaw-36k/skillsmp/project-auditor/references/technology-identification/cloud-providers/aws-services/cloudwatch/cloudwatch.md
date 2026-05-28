# Amazon CloudWatch

**Category**: cloud-providers/aws-services
**Description**: Monitoring and observability service
**Homepage**: https://aws.amazon.com/cloudwatch

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*CloudWatch packages*

- `@aws-sdk/client-cloudwatch` - CloudWatch SDK v3
- `@aws-sdk/client-cloudwatch-logs` - CloudWatch Logs SDK
- `aws-embedded-metrics` - Embedded Metrics Format

#### PYPI
*CloudWatch Python packages*

- `boto3` - AWS SDK (includes CloudWatch)
- `aws-embedded-metrics` - EMF for Python
- `watchtower` - CloudWatch logging handler

#### GO
*CloudWatch Go packages*

- `github.com/aws/aws-sdk-go-v2/service/cloudwatch` - CloudWatch SDK
- `github.com/aws/aws-sdk-go-v2/service/cloudwatchlogs` - Logs SDK

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]@aws-sdk/client-cloudwatch['"]`
- CloudWatch SDK v3 import

**Pattern**: `from\s+['"]aws-embedded-metrics['"]`
- Embedded metrics import

#### Python
Extensions: `.py`

**Pattern**: `^from\s+watchtower\s+import`
- Watchtower import
- Example: `from watchtower import CloudWatchLogHandler`

### Code Patterns

**Pattern**: `cloudwatch\.|CloudWatch|PutMetricData|GetMetricData`
- CloudWatch operations

**Pattern**: `logs\.[a-z0-9-]+\.amazonaws\.com|monitoring\.[a-z0-9-]+\.amazonaws\.com`
- CloudWatch endpoints

**Pattern**: `CLOUDWATCH_|CW_LOG_GROUP`
- CloudWatch environment variables

**Pattern**: `arn:aws:logs:[a-z0-9-]+:[0-9]+:log-group:`
- CloudWatch Logs ARN

**Pattern**: `Type:\s*['"]?AWS::CloudWatch::|Type:\s*['"]?AWS::Logs::`
- CloudFormation CloudWatch resources

---

## Environment Variables

- `CLOUDWATCH_LOG_GROUP` - Log group name
- `CLOUDWATCH_LOG_STREAM` - Log stream name
- `CW_LOG_GROUP` - Alternative log group
- `AWS_EMF_NAMESPACE` - EMF namespace

## Detection Notes

- Metrics for performance monitoring
- Logs for application logging
- Alarms for alerting
- Dashboards for visualization
- Container Insights for ECS/EKS

---

## TIER 3: Configuration Extraction

### Log Group Extraction

**Pattern**: `(?:logGroupName|log[_-]?group|CLOUDWATCH_LOG_GROUP)\s*[=:]\s*['"]?([a-zA-Z0-9/_.-]+)['"]?`
- CloudWatch log group
- Extracts: `log_group`
- Example: `/aws/lambda/my-function`
