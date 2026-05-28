---
name: Cost Optimization
description: This skill should be used when the user asks to "reduce cloud costs", "optimize spending", "FinOps", "cost analysis", "right-sizing", "reserved instances", "spot instances", "cloud budget", "cost allocation", "resource optimization", or needs help with cloud cost management and optimization strategies.
version: 1.0.0
---

# Cost Optimization

Comprehensive guidance for cloud cost management, FinOps practices, and resource optimization.

## FinOps Framework

### Core Principles

1. **Visibility** - Know what you're spending
2. **Allocation** - Attribute costs to owners
3. **Optimization** - Reduce waste, improve efficiency
4. **Governance** - Set policies and budgets

### Cost Categories

| Category | Examples | Optimization Strategy |
|----------|----------|----------------------|
| Compute | EC2, VMs | Right-sizing, Reserved |
| Storage | S3, Disk | Tiering, Lifecycle |
| Network | Data transfer | CDN, Compression |
| Database | RDS, BigQuery | Reserved, Query optimization |

## AWS Cost Optimization

### Cost Explorer Analysis

```bash
# Get monthly costs by service
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-02-01 \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE

# Get costs with tags
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-02-01 \
  --granularity DAILY \
  --metrics "UnblendedCost" \
  --filter '{"Tags":{"Key":"Environment","Values":["production"]}}'
```

### Right-Sizing with Compute Optimizer

```bash
# Get EC2 recommendations
aws compute-optimizer get-ec2-instance-recommendations \
  --instance-arns arn:aws:ec2:us-east-1:123456789:instance/i-12345

# Export recommendations
aws compute-optimizer export-ec2-instance-recommendations \
  --s3-destination-config bucket=my-bucket,keyPrefix=optimizer
```

### Savings Plans & Reserved Instances

| Type | Commitment | Discount | Flexibility |
|------|------------|----------|-------------|
| On-Demand | None | 0% | Full |
| Savings Plans | 1-3 years | 30-72% | High |
| Reserved Instances | 1-3 years | 40-75% | Low |
| Spot Instances | None | Up to 90% | Lowest |

### S3 Cost Optimization

```bash
# Set up Intelligent Tiering
aws s3api put-bucket-intelligent-tiering-configuration \
  --bucket my-bucket \
  --id config-name \
  --intelligent-tiering-configuration '{
    "Id": "config-name",
    "Status": "Enabled",
    "Tierings": [
      {"Days": 90, "AccessTier": "ARCHIVE_ACCESS"},
      {"Days": 180, "AccessTier": "DEEP_ARCHIVE_ACCESS"}
    ]
  }'

# Lifecycle policy for old objects
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration file://lifecycle.json
```

## GCP Cost Optimization

### Billing Export Analysis

```sql
-- BigQuery: Top spending services
SELECT
  service.description,
  SUM(cost) as total_cost
FROM `project.dataset.billing_export`
WHERE invoice.month = '202401'
GROUP BY service.description
ORDER BY total_cost DESC
LIMIT 10;

-- Unused resources
SELECT
  resource.name,
  SUM(cost) as cost
FROM `project.dataset.billing_export`
WHERE usage.amount = 0
GROUP BY resource.name;
```

### Committed Use Discounts

```bash
# Create commitment
gcloud compute commitments create my-commitment \
  --region=us-central1 \
  --resources=vcpu=100,memory=200GB \
  --plan=twelve-month
```

### Preemptible VMs

```bash
# Create preemptible instance
gcloud compute instances create my-vm \
  --zone=us-central1-a \
  --machine-type=n2-standard-4 \
  --preemptible \
  --no-restart-on-failure
```

## Azure Cost Optimization

### Cost Management

```bash
# Get cost by resource group
az consumption usage list \
  --start-date 2024-01-01 \
  --end-date 2024-01-31 \
  --query "[?contains(instanceId, 'my-rg')]"

# Create budget alert
az consumption budget create \
  --budget-name monthly-budget \
  --amount 1000 \
  --category cost \
  --time-grain monthly \
  --start-date 2024-01-01 \
  --end-date 2024-12-31
```

### Azure Advisor Recommendations

```bash
# Get cost recommendations
az advisor recommendation list \
  --category Cost \
  --output table
```

## Kubernetes Cost Optimization

### Resource Requests/Limits

```yaml
# Right-sized resources
resources:
  requests:
    cpu: "100m"      # Based on actual usage
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "256Mi"
```

### Cluster Autoscaler

```yaml
# Scale down unused nodes
apiVersion: autoscaling.k8s.io/v1
kind: ClusterAutoscaler
spec:
  scaleDown:
    enabled: true
    delayAfterAdd: 10m
    delayAfterDelete: 10m
    unneededTime: 10m
```

### Spot/Preemptible Nodes

```yaml
# Node pool with spot instances
apiVersion: v1
kind: NodePool
spec:
  nodeLabels:
    workload-type: "batch"
  taints:
    - key: "spot"
      value: "true"
      effect: "NoSchedule"
  spotInstanceTypes:
    - m5.large
    - m5.xlarge
```

## Cost Monitoring

### Alerts and Budgets

```python
# AWS Budget alarm
import boto3

budgets = boto3.client('budgets')

budgets.create_budget(
    AccountId='123456789012',
    Budget={
        'BudgetName': 'monthly-budget',
        'BudgetLimit': {'Amount': '1000', 'Unit': 'USD'},
        'TimeUnit': 'MONTHLY',
        'BudgetType': 'COST'
    },
    NotificationsWithSubscribers=[{
        'Notification': {
            'NotificationType': 'ACTUAL',
            'ComparisonOperator': 'GREATER_THAN',
            'Threshold': 80
        },
        'Subscribers': [{
            'SubscriptionType': 'EMAIL',
            'Address': 'team@example.com'
        }]
    }]
)
```

### Cost Dashboard Metrics

| Metric | Description |
|--------|-------------|
| Daily spend | Current day's costs |
| MTD spend | Month-to-date total |
| Forecast | Predicted month-end cost |
| Variance | Actual vs budget |
| Cost per unit | Cost per request/user |

## Optimization Checklist

### Compute

- [ ] Right-size instances based on utilization
- [ ] Use Reserved/Savings Plans for steady workloads
- [ ] Use Spot for fault-tolerant workloads
- [ ] Auto-scale based on demand
- [ ] Shut down dev/test outside hours

### Storage

- [ ] Enable storage tiering
- [ ] Set lifecycle policies
- [ ] Delete unattached volumes
- [ ] Compress data before storage
- [ ] Use appropriate storage class

### Network

- [ ] Use CDN for static content
- [ ] Compress API responses
- [ ] Minimize cross-region traffic
- [ ] Use VPC endpoints
- [ ] Review NAT Gateway usage

### Database

- [ ] Use reserved capacity
- [ ] Optimize queries
- [ ] Right-size instances
- [ ] Use read replicas efficiently
- [ ] Archive old data

## Additional Resources

### Reference Files

- **`references/aws-cost-tools.md`** - AWS cost optimization tools
- **`references/finops-framework.md`** - Complete FinOps guide

### Example Files

- **`examples/cost-dashboard.json`** - Grafana cost dashboard
- **`examples/budget-alerts.tf`** - Terraform budget configuration
