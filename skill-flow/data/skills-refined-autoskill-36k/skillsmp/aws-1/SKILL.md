---
name: aws
description: Use AWS CLI for read-only operations and debugging. Use when working with AWS services, checking status, reading logs, or querying resources.
disable-model-invocation: true
---
# AWS CLI Usage

## 🚨 CRITICAL RULE
**NEVER make AWS changes via CLI without explicit user approval each time.** Only use for read-only debugging and information gathering.

## Output Formats
- `--output table` - Human readable tables
- `--output text` - Plain text (good for scripts)
- `--output json` - Full JSON (pipe to jq)
- Use `--query` to filter fields and minimize output

## JSON Parsing Tips
```bash
# Use jq for complex JSON parsing
aws <service> <command> --output json | jq '.Field.Path'

# Use --query for simple filtering
aws <service> <command> --query 'Items[].PropertyName'
```

## Use Case References

For specific AWS service workflows, see:
- **CloudWatch Logs**: [cloudwatch.md](cloudwatch.md) - Reading application logs, log streams, time-based filtering
- **Elastic Beanstalk**: [elasticbeanstalk.md](elasticbeanstalk.md) - Environment health, deployment failures, instance issues
- **IAM & Permissions**: [iam.md](iam.md) - Role checks, policy inspection, permission debugging
