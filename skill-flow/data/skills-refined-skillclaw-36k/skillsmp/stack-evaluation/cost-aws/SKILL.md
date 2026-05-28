---
description: Estimate AWS infrastructure costs for any stack using live pricing data. Use when user asks about AWS pricing, cost estimation for EC2, Lambda, ECS, RDS, DynamoDB, CloudFront, Aurora, S3, or any AWS service combination.
name: cost-aws
---

# AWS Cost & Ops Evaluator

Estimate costs and operational overhead for AWS-based infrastructure using real-time pricing data.

## Before Answering AWS Cost Questions

**IMPORTANT**: Always verify tool availability before providing cost estimates.

### Step 1: Check Available Tools

Check if the following tools are available:

**AWS MCP Tools** (preferred):

- `mcp__aws-mcp__aws___search_documentation` - Search AWS docs
- `mcp__aws-mcp__aws___read_documentation` - Read specific pricing pages
- `mcp__aws-mcp__aws___get_regional_availability` - Check service availability

**AWS CLI** (alternative):

- `aws pricing get-products` - Query AWS Price List API
- `aws ce get-cost-and-usage` - Get actual usage costs (if account connected)

### Step 2: If Tools Are Unavailable

If AWS MCP or CLI tools are not accessible, help the user set them up:

**Option A: AWS MCP Server (Full Access)**
Requirements: Python/uvx + AWS credentials

```bash
# Install AWS MCP
uvx mcp-server-aws

# Configure in Claude settings or MCP config
```

**Option B: AWS Documentation MCP (No Auth Required)**
For pricing lookups without AWS account:

```bash
# Install documentation-only MCP
uvx mcp-server-aws-docs
```

**Option C: AWS CLI**

```bash
# Install AWS CLI
brew install awscli  # macOS
# or: pip install awscli

# Configure credentials
aws configure
```

Ask the user which option fits their environment before proceeding.

### Step 3: Fallback to Web Search

If no tools are available and user cannot install them, use web search to fetch current pricing from:

- https://aws.amazon.com/pricing/
- AWS Pricing Calculator: https://calculator.aws/

## How to Get Live Pricing

### Using AWS MCP Tools

```sh
# Search for EC2 pricing documentation
mcp__aws-mcp__aws___search_documentation("EC2 pricing on-demand")

# Read specific pricing page
mcp__aws-mcp__aws___read_documentation("/ec2/pricing/on-demand")

# Check regional availability
mcp__aws-mcp__aws___get_regional_availability("aurora-serverless-v2")
```

### Using AWS CLI

```bash
# Get EC2 pricing for specific instance type
aws pricing get-products \
  --service-code AmazonEC2 \
  --filters "Type=TERM_MATCH,Field=instanceType,Value=t3.micro" \
            "Type=TERM_MATCH,Field=location,Value=US East (N. Virginia)" \
  --region us-east-1

# Get RDS pricing
aws pricing get-products \
  --service-code AmazonRDS \
  --filters "Type=TERM_MATCH,Field=instanceType,Value=db.t3.micro"

# Get actual costs (requires Cost Explorer access)
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost
```

### Using AWS Pricing Calculator API

```bash
# Use the AWS Pricing Calculator for estimates
# https://calculator.aws/#/estimate

# Or use the Bulk API for programmatic access
curl "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json"
```

## Standalone Usage

Can be invoked directly for cost estimation:

- "How much would ECS Fargate + Aurora cost?"
- "Estimate AWS costs for a Node.js API with PostgreSQL"
- "Compare Lambda vs App Runner pricing"

## Cost Estimation Process

1. **Identify services** needed for the stack
2. **Query live pricing** using available tools
3. **Calculate baseline** costs (minimum viable)
4. **Estimate at scale** (10x baseline load)
5. **Identify cost drivers** and optimization opportunities

## Service Categories & Tools

### Compute Services

| Service | Pricing Tool/Command |
|---------|---------------------|
| EC2 | `aws pricing get-products --service-code AmazonEC2` |
| Lambda | `aws pricing get-products --service-code AWSLambda` |
| ECS/Fargate | `aws pricing get-products --service-code AmazonECS` |
| EKS | $0.10/hr cluster + compute costs |
| App Runner | `aws pricing get-products --service-code AWSAppRunner` |

### Database Services

| Service | Pricing Tool/Command |
|---------|---------------------|
| RDS | `aws pricing get-products --service-code AmazonRDS` |
| Aurora | `aws pricing get-products --service-code AmazonRDS` (engine=aurora) |
| DynamoDB | `aws pricing get-products --service-code AmazonDynamoDB` |
| ElastiCache | `aws pricing get-products --service-code AmazonElastiCache` |

### Storage & Networking

| Service | Pricing Tool/Command |
|---------|---------------------|
| S3 | `aws pricing get-products --service-code AmazonS3` |
| CloudFront | `aws pricing get-products --service-code AmazonCloudFront` |
| ALB/NLB | `aws pricing get-products --service-code AWSELB` |
| NAT Gateway | `aws pricing get-products --service-code AmazonEC2` (NAT) |

## Output Contract

```yaml
aws_cost_estimate:
  description: "<what's being estimated>"
  region: "<AWS region>"
  pricing_source: "<mcp|cli|web|calculator>"
  pricing_date: "<when pricing was fetched>"

  components:
    - service: "<service name>"
      config: "<configuration>"
      monthly_cost: "<$X>"
      pricing_model: "<on-demand|reserved|spot>"
      notes: "<any notes>"

  baseline_monthly:
    compute: "<$X>"
    database: "<$X>"
    storage: "<$X>"
    networking: "<$X>"
    other: "<$X>"
    total: "<$X>"

  at_10x_scale:
    compute: "<$X>"
    database: "<$X>"
    networking: "<$X>"
    total: "<$X>"

  cost_drivers:
    - "<primary cost driver>"
    - "<secondary driver>"

  savings_opportunities:
    - type: "<reserved|savings-plan|spot>"
      potential_savings: "<X%>"
      commitment: "<1yr|3yr>"

  ops_overhead: "<low|medium|high>"
  required_aws_knowledge: "<basic|intermediate|advanced>"

  optimization_tips:
    - "<tip 1>"
    - "<tip 2>"
```

## Cost Optimization Strategies

Query these using AWS tools:

### Reserved Instances / Savings Plans

```bash
# Check RI recommendations
aws ce get-reservation-purchase-recommendation \
  --service AmazonEC2 \
  --lookback-period-in-days SIXTY_DAYS

# Check Savings Plans recommendations
aws ce get-savings-plans-purchase-recommendation \
  --savings-plans-type COMPUTE_SP \
  --lookback-period-in-days SIXTY_DAYS
```

### Right-sizing

```bash
# Get Compute Optimizer recommendations
aws compute-optimizer get-ec2-instance-recommendations
aws compute-optimizer get-ecs-service-recommendations
```

### Cost Anomaly Detection

```bash
# Set up cost anomaly detection
aws ce create-anomaly-monitor \
  --anomaly-monitor '{"MonitorName":"MyMonitor","MonitorType":"DIMENSIONAL"}'
```

## Pricing Notes

- Prices vary by region (us-east-1 typically cheapest)
- Always verify current pricing - AWS updates frequently
- Consider data transfer costs (often overlooked)
- Free tier limits reset monthly
- Spot pricing fluctuates - check current rates
