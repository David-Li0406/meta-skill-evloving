# CI/CD Deployments

## Quick Status Checks
```bash
gh run list --repo OWNER/REPO --branch BRANCH_NAME --limit 5
gh run view <RUN_ID> --repo OWNER/REPO --json status,conclusion,startedAt,completedAt
gh run view <RUN_ID> --repo OWNER/REPO --log
gh run view <RUN_ID> --repo OWNER/REPO --log-failed
gh run watch <RUN_ID> --repo OWNER/REPO
```

## Monitoring Deployment Status

### Check Latest Run Status
```bash
gh run list --repo OWNER/REPO --branch BRANCH_NAME --limit 1 --json databaseId,status,conclusion,displayTitle
gh run view <RUN_ID> --repo OWNER/REPO --json jobs | \
  jq '.jobs[0] | {status: .status, conclusion: .conclusion, started: .startedAt, completed: .completedAt}'
```

### Watch Deployment Progress
```bash
gh run watch <RUN_ID> --repo OWNER/REPO

(RUN_ID=<RUN_ID>
while true; do
  run_info=$(gh run view $RUN_ID --repo OWNER/REPO --json status,conclusion 2>/dev/null)
  status=$(echo "$run_info" | jq -r '.status')
  conclusion=$(echo "$run_info" | jq -r '.conclusion // ""')
  echo "$(date +%H:%M:%S) $status ($conclusion)"
  [ "$status" == "completed" ] && break
  sleep 30
done) | tail -n 5
```

### Check Current Step
```bash
gh run view <RUN_ID> --repo OWNER/REPO --json jobs | \
  jq -r '.jobs[0].steps[] | select(.status != "completed") | "\(.name): \(.status)"' | head -3
```

## Failed Deployments

### View Failed Steps Only
```bash
gh run view <RUN_ID> --repo OWNER/REPO --log-failed
gh run list --repo OWNER/REPO --branch BRANCH_NAME --limit 1 --json databaseId,conclusion | \
  jq -r 'select(.[0].conclusion == "failure") | .[0].databaseId'
```

### Filter Logs by Step Name
```bash
gh run view <RUN_ID> --repo OWNER/REPO --log | grep "STEP_NAME" | tail -30
gh run view <RUN_ID> --repo OWNER/REPO --log | grep -A 50 "Deploy Infrastructure" | tail -30
```

## Comparing Run Timing

### Get Run Durations
```bash
gh run list --repo OWNER/REPO --branch BRANCH_NAME --limit 2 --json databaseId | \
  jq -r '.[].databaseId' | \
  xargs -I {} gh run view {} --repo OWNER/REPO --json jobs | \
  jq '.jobs[0] | {started: .startedAt, completed: .completedAt}'
```


## Combined CI + AWS Monitoring
```bash
(RUN_ID=<RUN_ID>
for i in {1..20}; do
  echo "$(date +%H:%M:%S) #$i"
  ci_info=$(gh run view $RUN_ID --repo OWNER/REPO --json status,conclusion 2>/dev/null)
  ci_status=$(echo "$ci_info" | jq -r '.status // "unknown"')
  ci_conclusion=$(echo "$ci_info" | jq -r '.conclusion // ""')
  eb_info=$(aws elasticbeanstalk describe-environments \
    --application-name APP_NAME \
    --environment-names ENV_NAME \
    --region REGION \
    --query 'Environments[0].[Status,Health,VersionLabel]' \
    --output text 2>/dev/null || echo "NOT_FOUND")
  cf_status=$(aws cloudformation describe-stacks \
    --stack-name STACK_NAME \
    --region REGION \
    --query 'Stacks[0].StackStatus' \
    --output text 2>/dev/null || echo "NOT_FOUND")
  echo "CI: $ci_status ($ci_conclusion) | EB: $eb_info | CF: $cf_status"
  [ "$ci_status" == "completed" ] && break
  sleep 60
done) | tail -n 10
```
