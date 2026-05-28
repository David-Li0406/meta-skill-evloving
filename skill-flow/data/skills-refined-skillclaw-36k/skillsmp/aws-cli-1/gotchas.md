# AWS CLI Gotchas & Patterns

> **Subagents: Review before running AWS commands.** These gotchas cause silent failures or unexpected behavior and are NOT discoverable via `aws help`.

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `Unable to locate credentials` | No profile or expired session | `aws configure` or `aws sso login --profile <p>` |
| `ExpiredTokenException` | Session token expired | Refresh SSO/credentials |
| `AccessDenied` | Missing IAM permissions | Check role/user policies |
| `NoSuchBucket` / `404` | Bucket doesn't exist or wrong region | Verify name and `--region` |
| `InvalidParameterValue` | Wrong parameter format | Check `aws <cmd> help` |
| `ThrottlingException` | Rate limit hit | Add retry, reduce frequency |

## Universal

- **Pager blocks scripts**: Set `AWS_PAGER=""` or use `--no-cli-pager`
- **`file://` vs `fileb://`**: Use `fileb://` for binary data (zips, keys, certificates)
- **JSON escaping**: Use single-quoted outer wrapper: `'{"key":"value"}'`

## S3

- **Non-us-east-1 buckets**: Require `--create-bucket-configuration LocationConstraint=<region>`
- **Cross-account copy**: Needs `--acl bucket-owner-full-control`
- **`aws s3` vs `aws s3api`**: High-level (cp/sync) vs low-level API access

## EC2

- **AMI owner IDs**: Amazon Linux=`amazon`, Ubuntu=`099720109477`
- **User data**: Use `--user-data file://script.sh`
- **Dry run**: `--dry-run` only works on EC2 commands

## Lambda

- **Invoke JSON payload**: Requires `--cli-binary-format raw-in-base64-out`
- **Log decoding**: `--query 'LogResult' --output text | base64 --decode`
- **Zip upload**: `--zip-file fileb://function.zip`

## IAM

- **Deletion prerequisites**: Remove all attached policies, keys, group memberships first
- **Access key secret**: Shown only once at creation - save immediately
- **Trust policies**: Required for roles, defines who can assume the role

## ECS/EKS

- **Network config**: `awsvpcConfiguration={subnets=[...],securityGroups=[...],assignPublicIp=ENABLED}`
- **ECS Exec prerequisites**: Requires SSM plugin, task role perms, `--enable-execute-command`
- **Delete order (EKS)**: Node groups/Fargate profiles before cluster
- **Upgrade order (EKS)**: Control plane -> Add-ons -> Node groups

## CloudFormation

- **Capabilities**: `--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND`
- **CI/CD safety**: `--no-fail-on-empty-changeset` prevents failures on no changes
- **Recovery**: `continue-update-rollback --resources-to-skip <resource-id>`

## DynamoDB

- **Type-prefixed JSON**: Values need `{"S":"string"}`, `{"N":"123"}`, `{"BOOL":true}`
- **Expression placeholders**: Use `#name` and `:value` for reserved words

## Route53

- **Trailing dots**: Domain names in queries need trailing dot (`example.com.`)
- **Alias zone IDs**: CloudFront=`Z2FDTNDATAQYW2`, S3 varies by region

## CloudWatch

- **Epoch milliseconds**: Many timestamp flags need ms, not seconds
- **Insights is async**: `start-query` returns query ID -> wait -> `get-query-results`
- **Log tail**: `aws logs tail <group> --since 1h --follow`
