---
name: cost-optimization
description: "Cloud cost optimization and FinOps practices. Use when analyzing cloud costs, implementing savings strategies, or optimizing resource usage."
---

# Cloud Cost Optimization

FinOps practices for managing and optimizing cloud spending.

## When to Use

- Analyzing and reducing cloud costs
- Implementing cost allocation and tagging
- Right-sizing resources
- Choosing commitment options
- Setting up cost alerts and budgets

## Cost Optimization Framework

### The Three Pillars

| Pillar | Actions |
|--------|---------|
| **See** | Tagging, allocation, visibility |
| **Save** | Right-sizing, commitments, spot |
| **Plan** | Forecasting, budgeting, governance |

## Tagging Strategy

### Required Tags

```hcl
locals {
  required_tags = {
    Environment = var.environment
    Project     = var.project
    Owner       = var.owner
    CostCenter  = var.cost_center
    ManagedBy   = "terraform"
    Application = var.application
  }
}

resource "aws_instance" "example" {
  # ...
  tags = merge(local.required_tags, {
    Name = "${var.project}-web"
    Role = "webserver"
  })
}
```

### Tag Policy (AWS)

```json
{
  "tags": {
    "Environment": {
      "tag_key": { "@@assign": "Environment" },
      "tag_value": {
        "@@assign": ["production", "staging", "development"]
      },
      "enforced_for": {
        "@@assign": ["ec2:instance", "rds:db", "s3:bucket"]
      }
    },
    "CostCenter": {
      "tag_key": { "@@assign": "CostCenter" },
      "enforced_for": {
        "@@assign": ["*"]
      }
    }
  }
}
```

## Right-Sizing

### Identify Over-Provisioned Resources

```sql
-- AWS Cost Explorer query
SELECT
  line_item_resource_id,
  product_instance_type,
  AVG(line_item_usage_amount) as avg_usage,
  MAX(line_item_usage_amount) as max_usage
FROM cost_and_usage_report
WHERE line_item_product_code = 'AmazonEC2'
GROUP BY 1, 2
HAVING avg_usage < max_usage * 0.3  -- Under 30% utilized
```

### Right-Sizing Recommendations

| Current | Recommendation | Savings |
|---------|---------------|---------|
| m5.xlarge (4 vCPU, 16GB) | m5.large (2 vCPU, 8GB) | ~50% |
| r5.2xlarge (8 vCPU, 64GB) | r5.xlarge (4 vCPU, 32GB) | ~50% |
| Provisioned IOPS SSD | General Purpose SSD | ~60% |

### Terraform Right-Sizing

```hcl
variable "instance_sizes" {
  type = map(string)
  default = {
    development = "t3.small"
    staging     = "t3.medium"
    production  = "m5.large"
  }
}

resource "aws_instance" "app" {
  instance_type = var.instance_sizes[var.environment]
}
```

## Commitment Discounts

### Comparison

| Type | Discount | Flexibility | Best For |
|------|----------|-------------|----------|
| On-Demand | 0% | Full | Variable workloads |
| Reserved (1yr) | 30-40% | Low | Steady-state |
| Reserved (3yr) | 50-60% | Low | Predictable long-term |
| Savings Plans | 20-30% | Medium | Flexible compute |
| Spot/Preemptible | 60-90% | None | Fault-tolerant |

### AWS Savings Plans

```hcl
resource "aws_ce_savings_plan_purchase_recommendation" "compute" {
  lookback_period_in_days = "SIXTY_DAYS"
  payment_option          = "NO_UPFRONT"
  savings_plan_type       = "COMPUTE_SP"
  term_in_years           = "ONE_YEAR"
}
```

### GCP Committed Use

```hcl
resource "google_compute_resource_policy" "commitment" {
  name   = "commitment-policy"
  region = var.region

  instance_schedule_policy {
    vm_start_schedule {
      schedule = "0 9 * * MON-FRI"
    }
    vm_stop_schedule {
      schedule = "0 18 * * MON-FRI"
    }
  }
}
```

## Spot/Preemptible Instances

### AWS Spot Instances

```hcl
resource "aws_spot_fleet_request" "workers" {
  iam_fleet_role  = aws_iam_role.spot_fleet.arn
  target_capacity = 10

  launch_specification {
    instance_type     = "m5.large"
    ami               = data.aws_ami.amazon_linux.id
    spot_price        = "0.05"

    tags = {
      Name = "spot-worker"
    }
  }

  launch_specification {
    instance_type     = "m5.xlarge"
    ami               = data.aws_ami.amazon_linux.id
    spot_price        = "0.10"
  }

  # Diversify across instance types
  allocation_strategy = "diversified"
}
```

### GCP Preemptible VMs

```hcl
resource "google_compute_instance" "worker" {
  name         = "worker"
  machine_type = "e2-standard-4"

  scheduling {
    preemptible         = true
    automatic_restart   = false
    on_host_maintenance = "TERMINATE"
  }
}
```

### Kubernetes Spot Nodes

```yaml
# EKS Node Group with Spot
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: my-cluster
  region: us-east-1

managedNodeGroups:
  - name: spot-workers
    instanceTypes: ["m5.large", "m5.xlarge", "m4.large"]
    spot: true
    minSize: 2
    maxSize: 20
    labels:
      lifecycle: spot
    taints:
      - key: lifecycle
        value: spot
        effect: NoSchedule
```

## Storage Optimization

### S3 Lifecycle Policies

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    id     = "archive"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"  # 45% cheaper
    }

    transition {
      days          = 90
      storage_class = "GLACIER"  # 68% cheaper
    }

    transition {
      days          = 180
      storage_class = "DEEP_ARCHIVE"  # 95% cheaper
    }

    expiration {
      days = 365
    }
  }
}
```

### EBS Optimization

```hcl
# Use gp3 instead of gp2 (20% cheaper, better performance)
resource "aws_ebs_volume" "data" {
  availability_zone = var.az
  size              = 100
  type              = "gp3"
  iops              = 3000   # Baseline included
  throughput        = 125    # Baseline included
}
```

## Budget Alerts

### AWS Budget

```hcl
resource "aws_budgets_budget" "monthly" {
  name         = "${var.project}-monthly"
  budget_type  = "COST"
  limit_amount = "1000"
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  cost_filter {
    name   = "TagKeyValue"
    values = ["user:Project$${var.project}"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.alert_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }
}
```

### GCP Budget

```hcl
resource "google_billing_budget" "project" {
  billing_account = var.billing_account
  display_name    = "${var.project} Budget"

  budget_filter {
    projects = ["projects/${var.project}"]
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = "1000"
    }
  }

  threshold_rules {
    threshold_percent = 0.5
  }

  threshold_rules {
    threshold_percent = 0.8
  }

  threshold_rules {
    threshold_percent = 1.0
    spend_basis       = "FORECASTED_SPEND"
  }

  all_updates_rule {
    pubsub_topic = google_pubsub_topic.budget.id
  }
}
```

## Cost Analysis Queries

### AWS Athena (Cost and Usage Report)

```sql
-- Daily cost by service
SELECT
  DATE(line_item_usage_start_date) as date,
  line_item_product_code as service,
  SUM(line_item_unblended_cost) as cost
FROM cost_report
WHERE MONTH(line_item_usage_start_date) = MONTH(CURRENT_DATE)
GROUP BY 1, 2
ORDER BY 1, 3 DESC;

-- Cost by tag
SELECT
  resource_tags_user_project as project,
  SUM(line_item_unblended_cost) as cost
FROM cost_report
WHERE MONTH(line_item_usage_start_date) = MONTH(CURRENT_DATE)
GROUP BY 1
ORDER BY 2 DESC;
```

## Quick Wins

| Action | Effort | Savings |
|--------|--------|---------|
| Delete unused resources | Low | 5-15% |
| Right-size instances | Medium | 20-40% |
| Use spot/preemptible | Medium | 60-90% |
| Reserved/Savings Plans | Low | 30-60% |
| S3 lifecycle policies | Low | 40-90% |
| Schedule dev environments | Low | 65% |

## Checklist

- [ ] Consistent tagging implemented
- [ ] Cost allocation reports enabled
- [ ] Budgets and alerts configured
- [ ] Unused resources identified
- [ ] Right-sizing analyzed
- [ ] Commitment options evaluated
- [ ] Storage tiering configured
- [ ] Dev environments scheduled

## Integration

Works with:
- `/aws`, `/gcp`, `/azure` - Cloud cost analysis
- `/terraform` - Cost-aware infrastructure
- `/devops` - Cost in CI/CD
