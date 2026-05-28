# AWS Staging CLI Commands Reference

## CloudWatch Logs

### Basic Operations
```bash
# List all log groups
aws logs describe-log-groups

# Tail logs (live)
aws logs tail /vessel/apps --follow --format short

# Search logs (time-based)
aws logs tail /vessel/apps --since 1h --filter-pattern "ERROR"
aws logs tail /vessel/apps --since 30m --filter-pattern '{ $.level = "error" }'
```

### Key Log Groups
- `/vessel/apps` - Main application logs (19+ GB)
- `/vessel/llm` - LLM service logs
- `/vessel/vpc-flow-logs` - VPC flow logs
- `/aws/rds/instance/vessel-staging/postgresql` - Main DB logs
- `/aws/rds/instance/discovery-staging/postgresql` - Discovery DB logs
- `/aws/rds/proxy/discovery-proxy-staging` - RDS proxy logs
- `/aws/lambda/*-staging` - Lambda function logs
- `aws-waf-logs-vessel-apps-staging-web-acl` - WAF logs

### CloudWatch Logs Insights
```bash
# Start query
aws logs start-query \
  --log-group-name /vessel/apps \
  --start-time $(expr $(date +%s) - 3600) \
  --end-time $(date +%s) \
  --query-string 'fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc | limit 20'

# Get results
aws logs get-query-results --query-id <query-id>

# Slow API endpoints
aws logs start-query \
  --log-group-name /vessel/apps \
  --start-time $(expr $(date +%s) - 3600) \
  --end-time $(date +%s) \
  --query-string 'fields @timestamp, responseTime, request.url, requestId
| filter responseTime > 1000
| sort responseTime desc
| limit 50'

# Top slowest endpoints (aggregated)
aws logs start-query \
  --log-group-name /vessel/apps \
  --start-time $(expr $(date +%s) - 3600) \
  --end-time $(date +%s) \
  --query-string 'fields request.url as endpoint
| stats avg(responseTime) as avg_ms, max(responseTime) as max_ms, count() as request_count by endpoint
| filter avg_ms > 500
| sort avg_ms desc
| limit 20'

# Average response times by service
aws logs start-query \
  --log-group-name /vessel/apps \
  --start-time $(expr $(date +%s) - 3600) \
  --end-time $(date +%s) \
  --query-string 'fields name
| stats avg(responseTime) as avg_ms, percentile(responseTime, 95) as p95_ms, count() by name
| sort avg_ms desc'

# Count by status code
aws logs start-query \
  --log-group-name /vessel/apps \
  --start-time $(expr $(date +%s) - 3600) \
  --end-time $(date +%s) \
  --query-string 'fields response.statusCode
| stats count() by response.statusCode'
```

### Filter Log Events
```bash
START_TIME=$(($(date +%s) - 3600))000

# Filter by pattern
aws logs filter-log-events \
  --log-group-name /vessel/apps \
  --filter-pattern "ERROR" \
  --start-time $START_TIME \
  --max-items 50

# Slow requests (> 1s)
aws logs filter-log-events \
  --log-group-name /vessel/apps \
  --filter-pattern '{ $.responseTime > 1000 }' \
  --start-time $START_TIME \
  | jq -r '.events[].message | fromjson | "\(.time) | \(.responseTime)ms | \(.request.url) | \(.requestId)"'

# Slow requests excluding long polls
aws logs filter-log-events \
  --log-group-name /vessel/apps \
  --filter-pattern '{ $.responseTime > 500 }' \
  --start-time $START_TIME \
  --max-items 500 \
  | jq -r '.events[].message | fromjson | select(.request.url | (contains("LongPoll") or contains("longpoll")) | not) | "\(.responseTime)ms - \(.request.url // "unknown")"' \
  | sort -rn | head -10

# Discovery database MCP calls
aws logs filter-log-events \
  --log-group-name /vessel/apps \
  --filter-pattern '{ $.methodName = "queryDiscoveryDatabase" }' \
  --start-time $START_TIME \
  | jq -r '.events[].message | fromjson | "\(.tokenCount) tokens | \(.sql[:100])"' | sort -rn

# All errors (level >= 40)
aws logs filter-log-events \
  --log-group-name /vessel/apps \
  --filter-pattern '{ $.level >= 40 }' \
  --start-time $START_TIME \
  | jq -r '.events[].message | fromjson | "\(.time) | \(.err.message // .msg)"'

# Twirp RPC calls > 500ms
aws logs filter-log-events \
  --log-group-name /vessel/apps \
  --filter-pattern '/twirp' \
  --start-time $(($(date +%s) - 1800))000 \
  | jq -r '.events[].message | fromjson | select(.responseTime > 500) | "\(.responseTime)ms - \(.request.url)"'
```

## RDS & Databases

### Instances
- `vessel-staging` - Main database
- `discovery-staging` - Discovery database
- `n8n-staging` - n8n database

### Commands
```bash
# List DB instances
aws rds describe-db-instances \
  --query 'DBInstances[*].[DBInstanceIdentifier,Engine,DBInstanceStatus,Endpoint.Address]' \
  --output table

# Get connection info
aws rds describe-db-instances \
  --db-instance-identifier vessel-staging \
  --query 'DBInstances[0].Endpoint' \
  --output json

# CPU metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=vessel-staging \
  --start-time $(date -u -v-1H -I) \
  --end-time $(date -u -I) \
  --period 300 \
  --statistics Average,Maximum

# Connection count
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name DatabaseConnections \
  --dimensions Name=DBInstanceIdentifier,Value=vessel-staging \
  --start-time $(date -u -v-1H -I) \
  --end-time $(date -u -I) \
  --period 300 \
  --statistics Average,Maximum

# RDS proxy info
aws rds describe-db-proxies --db-proxy-name discovery-proxy-staging

# View RDS logs
aws logs tail /aws/rds/instance/vessel-staging/postgresql --follow
aws logs tail /aws/rds/instance/discovery-staging/postgresql --follow --filter-pattern 'duration'
aws logs tail /aws/rds/proxy/discovery-proxy-staging --since 1h --follow
```

## EC2 Instances

### Instances
- `i-02e16bc2983c9c49c` - app-server (c6g.large)
- `i-0be15186fed003ac6` - app-server (c6g.large)
- `i-00bf3df146f044955` - proxy (t4g.nano)
- `i-0ac17d09aa65c7dc9` - Airbyte (c6g.xlarge)

### Commands
```bash
# List instances
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,PrivateIpAddress,Tags[?Key==`Name`].Value|[0]]' \
  --output table

# Check CPU
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-02e16bc2983c9c49c \
  --start-time $(date -u -v-1H -I) \
  --end-time $(date -u -I) \
  --period 300 \
  --statistics Average,Maximum

# SSH via Session Manager
aws ssm start-session --target i-02e16bc2983c9c49c

# Console output
aws ec2 get-console-output --instance-id i-02e16bc2983c9c49c

# Instance status
aws ec2 describe-instance-status --query 'InstanceStatuses[*].[InstanceId,InstanceStatus.Status,SystemStatus.Status]' --output table
```

## Load Balancers & Target Groups

### ALBs
- `alb-vessel-apps-staging` - Main application ALB

### Target Groups
- `caddy-*` - Port 80, health: /health
- `n8n-*` - Port 5678, health: /healthz
- `proxy-*` - Port 5432 (TCP)

### Commands
```bash
# List ALBs
aws elbv2 describe-load-balancers --query 'LoadBalancers[*].[LoadBalancerName,DNSName,State.Code]' --output table

# Target groups
aws elbv2 describe-target-groups --output table

# Target health
aws elbv2 describe-target-health --target-group-arn <arn>

# Response time metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApplicationELB \
  --metric-name TargetResponseTime \
  --dimensions Name=LoadBalancer,Value=app/alb-vessel-apps-staging/<id> \
  --start-time $(date -u -v-1H -I) \
  --end-time $(date -u -I) \
  --period 300 \
  --statistics Average,Maximum
```

## Lambda Functions

### Functions
- `sync-rds-proxy-staging`
- `slack-alarm-router-staging`
- `sms-alarm-router-staging`

### Commands
```bash
# List functions
aws lambda list-functions --query 'Functions[*].[FunctionName,Runtime]' --output table

# Invoke
aws lambda invoke --function-name sync-rds-proxy-staging --payload '{}' response.json

# Tail logs
aws logs tail /aws/lambda/sync-rds-proxy-staging --follow

# Recent errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/sync-rds-proxy-staging \
  --filter-pattern "ERROR" \
  --start-time $(($(date +%s) - 3600))000
```

## ECS (Fargate)

### Resources
- Cluster: `tools-cluster-staging`
- Service: `n8n-staging`

### Commands
```bash
# List clusters
aws ecs list-clusters

# List services
aws ecs list-services --cluster tools-cluster-staging
aws ecs describe-services --cluster tools-cluster-staging --services n8n-staging

# List tasks
aws ecs list-tasks --cluster tools-cluster-staging --service-name n8n-staging

# Task logs
aws logs tail /aws/ecs/n8n-staging/n8n --follow

# Force new deployment
aws ecs update-service --cluster tools-cluster-staging --service n8n-staging --force-new-deployment
```

## CloudWatch Alarms

```bash
# List all
aws cloudwatch describe-alarms --query 'MetricAlarms[*].[AlarmName,StateValue]' --output table

# Alarms in ALARM state
aws cloudwatch describe-alarms --state-value ALARM --output table

# Alarm details
aws cloudwatch describe-alarms --alarm-names "rds-cpu-high-critical-vessel-staging"

# Alarm history
aws cloudwatch describe-alarm-history --alarm-name "rds-cpu-high-critical-vessel-staging" --max-records 10

# Set alarm state (testing)
aws cloudwatch set-alarm-state \
  --alarm-name "alarm-suppressor-staging" \
  --state-value ALARM \
  --state-reason "Testing"
```

## S3 Buckets

### Buckets
- `alb-vessel-apps-staging-logs-*`
- `deploy-logs*`
- `proxy-ci-bucket-staging`
- `vessel-cdn-content-staging-*`
- `vessel-investor-content-staging`

### Commands
```bash
aws s3 ls
aws s3 ls s3://vessel-cdn-content-staging-20230717154759242400000002/ --recursive
aws s3 cp s3://bucket-name/path/to/file.txt ./local-file.txt
aws s3 cp ./local-file.txt s3://bucket-name/path/to/file.txt
aws s3 sync ./local-dir s3://bucket-name/prefix/
```

## SNS & SQS

### Topics
- `alerts-staging`
- `blackhole-alerts-staging`
- `vessel-staging-db-alarm`

### Commands
```bash
# List SNS topics
aws sns list-topics

# Publish message
aws sns publish \
  --topic-arn arn:aws:sns:ca-central-1:643610656178:alerts-staging \
  --message "Test alert"

# List subscriptions
aws sns list-subscriptions-by-topic \
  --topic-arn arn:aws:sns:ca-central-1:643610656178:alerts-staging

# List SQS queues
aws sqs list-queues

# Receive messages
aws sqs receive-message \
  --queue-url https://sqs.ca-central-1.amazonaws.com/643610656178/blackhole-alerts-queue-staging \
  --max-number-of-messages 10
```

## Secrets Manager

```bash
aws secretsmanager list-secrets
aws secretsmanager get-secret-value --secret-id llm/auth --query SecretString --output text
```

## WAF

```bash
# List web ACLs
aws wafv2 list-web-acls --scope REGIONAL

# Get web ACL
aws wafv2 get-web-acl \
  --scope REGIONAL \
  --id 004c412c-16f7-44af-ac09-aa87f8aa207b \
  --name waf-vessel-apps-staging

# View WAF logs
aws logs tail aws-waf-logs-vessel-apps-staging-web-acl --follow
```

## VPC & Networking

- VPC: `vpc-0dc52b5bf43c3e9b5` (10.10.0.0/16)

```bash
# List VPCs
aws ec2 describe-vpcs --query 'Vpcs[*].[VpcId,CidrBlock]' --output table

# List subnets
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-0dc52b5bf43c3e9b5" --output table

# List security groups
aws ec2 describe-security-groups --filters "Name=vpc-id,Values=vpc-0dc52b5bf43c3e9b5" --output table

# VPC flow logs
aws logs tail /vessel/vpc-flow-logs --follow
```

## Time Range Reference

```bash
# Last 5 minutes
--start-time $(($(date +%s) - 300))000

# Last 30 minutes
--start-time $(($(date +%s) - 1800))000

# Last hour
--start-time $(($(date +%s) - 3600))000

# Last 2 hours
--start-time $(($(date +%s) - 7200))000

# Last 24 hours
--start-time $(($(date +%s) - 86400))000

# Specific range
--start-time 1764288000000 --end-time 1764295200000
```
