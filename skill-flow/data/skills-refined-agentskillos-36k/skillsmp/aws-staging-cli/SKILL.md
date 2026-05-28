---
name: aws-staging-cli
description: AWS CLI reference for Vessel staging environment (account 643610656178, ca-central-1). Use when troubleshooting staging infrastructure, checking logs, monitoring RDS/EC2/ECS, investigating slow queries, or debugging application errors. Covers CloudWatch Logs, RDS, EC2, ALB, Lambda, ECS, S3, SNS/SQS, Secrets Manager, WAF.
---

# AWS Staging CLI Reference

## Environment

- **Account**: 643610656178
- **Region**: ca-central-1
- **Role**: Developer

## Key Resources

| Type | Name/ID | Notes |
|------|---------|-------|
| Log Group | `/vessel/apps` | Main app logs (JSON), 19+ GB |
| Log Group | `/vessel/llm` | LLM service logs |
| RDS | `vessel-staging` | Main database |
| RDS | `discovery-staging` | Discovery database |
| EC2 | `i-02e16bc2983c9c49c` | app-server (c6g.large) |
| EC2 | `i-0be15186fed003ac6` | app-server (c6g.large) |
| ALB | `alb-vessel-apps-staging` | Main ALB |
| ECS Cluster | `tools-cluster-staging` | Fargate cluster |
| ECS Service | `n8n-staging` | n8n service |

## Common Workflows

### Investigate Application Errors
```bash
# Tail live errors
aws logs tail /vessel/apps --follow --filter-pattern '{ $.level >= 40 }'

# Last hour errors
START_TIME=$(($(date +%s) - 3600))000
aws logs filter-log-events --log-group-name /vessel/apps \
  --filter-pattern '{ $.level >= 40 }' --start-time $START_TIME \
  | jq -r '.events[].message | fromjson | "\(.time) | \(.err.message // .msg)"'
```

### Find Slow Requests
```bash
# Requests > 1s (excluding long polls)
START_TIME=$(($(date +%s) - 3600))000
aws logs filter-log-events --log-group-name /vessel/apps \
  --filter-pattern '{ $.responseTime > 1000 }' --start-time $START_TIME --max-items 500 \
  | jq -r '.events[].message | fromjson | select(.request.url | (contains("LongPoll") or contains("longpoll")) | not) | "\(.responseTime)ms - \(.request.url // "unknown")"' \
  | sort -rn | head -10
```

### Check Database Health
```bash
# RDS status
aws rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceStatus]' --output table

# DB CPU (last hour)
aws cloudwatch get-metric-statistics --namespace AWS/RDS --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=vessel-staging \
  --start-time $(date -u -v-1H -I) --end-time $(date -u -I) --period 300 --statistics Average,Maximum

# Slow queries in PostgreSQL logs
aws logs tail /aws/rds/instance/vessel-staging/postgresql --follow --filter-pattern 'duration'
```

### Check Alarms
```bash
# All alarms in ALARM state
aws cloudwatch describe-alarms --state-value ALARM --output table
```

### SSH to Instance
```bash
aws ssm start-session --target i-02e16bc2983c9c49c
```

### Force ECS Redeployment
```bash
aws ecs update-service --cluster tools-cluster-staging --service n8n-staging --force-new-deployment
```

## Log JSON Structure

`/vessel/apps` logs are JSON with key fields:
- `level`: 30=info, 40=warn, 50=error
- `responseTime`: Request duration (ms)
- `requestId`: Unique request ID
- `name`: Service name (http, worker, discovery-mcp)
- `request.url`: Endpoint
- `msg`: Human-readable message

## Troubleshooting

### SSO Expired
```bash
aws sso login
```

### zsh Timestamp Issues
Calculate timestamp first:
```bash
START_TIME=$(($(date +%s) - 3600))000
aws logs filter-log-events --log-group-name /vessel/apps --start-time $START_TIME ...
```

## Full Reference

See [references/cli-commands.md](references/cli-commands.md) for complete command reference including: CloudWatch Logs Insights queries, RDS metrics, EC2 commands, ALB/target groups, Lambda, ECS, S3, SNS/SQS, Secrets Manager, WAF, VPC/networking.
