---
name: service-cost-analysis
description: "Cloud service and infrastructure cost analysis toolkit. Research current pricing, estimate costs across scenarios, calculate ROI projections, and identify cost optimization opportunities for software projects."
allowed-tools: [Read, Write, Edit, Bash, WebFetch, WebSearch]
---

# Service Cost Analysis

## Overview

Service cost analysis is a systematic process for estimating infrastructure and operational costs for software projects. Research current pricing, model costs across usage scenarios, calculate ROI projections, and identify optimization opportunities. Use this skill to make informed budget decisions backed by real pricing data.

## When to Use This Skill

This skill should be used when:
- Estimating infrastructure costs for new projects
- Comparing cloud provider pricing (AWS, GCP, Azure)
- Analyzing third-party service costs (SaaS, APIs)
- Creating cost projections across usage scenarios
- Calculating ROI and payback periods
- Identifying cost optimization opportunities

## Visual Enhancement with Project Diagrams

**When documenting cost analysis, include visualizations.**

Use the **project-diagrams** skill to generate:
- Cost breakdown charts
- Scenario comparison charts
- ROI projection graphs
- Cost optimization decision trees

```bash
python .claude/skills/project-diagrams/scripts/generate_schematic.py "diagram description" -o diagrams/output.png
```

---

## Cost Analysis Framework

### Cost Categories

| Category | Examples | Variability |
|----------|----------|-------------|
| **Compute** | VMs, containers, serverless | Usage-based |
| **Storage** | Object storage, block storage, databases | Capacity + operations |
| **Networking** | Data transfer, load balancers, CDN | Traffic-based |
| **Databases** | Managed databases, caching | Capacity + throughput |
| **Third-Party** | APIs, SaaS tools, services | Usually usage-based |
| **Development** | CI/CD, monitoring, logging | Often fixed + usage |
| **Personnel** | Development, operations, support | Fixed (but critical) |

### Research Protocol

**For every service, follow this protocol:**

1. **Find Official Pricing**
   - Use `WebFetch` or `WebSearch` to get current pricing
   - Look for pricing calculators
   - Note pricing model (per-hour, per-request, per-GB, etc.)

2. **Identify Cost Drivers**
   - What metrics drive cost?
   - Are there minimum commitments?
   - What are the tiered pricing breakpoints?

3. **Document Assumptions**
   - Usage estimates (requests, storage, users)
   - Growth projections
   - Geographic distribution

4. **Calculate Scenarios**
   - Low (conservative usage)
   - Mid (expected usage)
   - High (aggressive growth)

## Service Cost Specification Schema

```yaml
service_cost:
  # Identity
  service_name: "string"
  provider: "aws | gcp | azure | other"
  category: "compute | storage | database | networking | third_party | development"

  # Pricing
  pricing_model: "per_hour | per_request | per_gb | per_user | flat_rate | tiered"
  pricing_source: "URL to official pricing"
  pricing_date: "YYYY-MM-DD"

  # Cost Estimates
  monthly_cost:
    low: number
    mid: number
    high: number

  # Assumptions
  assumptions:
    - "string - assumption 1"
    - "string - assumption 2"

  # Usage Estimates
  usage:
    metric: "string (e.g., requests, GB, hours)"
    low: number
    mid: number
    high: number

  # Notes
  notes: "string - important considerations"
  optimization_opportunities:
    - "string - potential optimization"
```

## Cloud Provider Cost Analysis

### AWS Cost Analysis

**Common Services:**

| Service | Pricing Model | Key Cost Drivers |
|---------|--------------|------------------|
| EC2 | Per-hour + data transfer | Instance type, hours, data out |
| RDS | Per-hour + storage + IOPS | Instance type, storage, multi-AZ |
| S3 | Per-GB + requests | Storage class, requests, data transfer |
| Lambda | Per-request + duration | Invocations, memory, duration |
| ECS/Fargate | Per-vCPU-hour + memory-hour | Task size, hours running |
| CloudFront | Per-request + data transfer | Requests, data out, regions |

**AWS Pricing Research:**
```bash
# Use WebSearch to find current pricing
WebSearch: "AWS [service] pricing 2025"
WebFetch: "https://aws.amazon.com/[service]/pricing/"
```

**Example AWS Cost Specification:**

```yaml
service_costs:
  - service_name: "AWS RDS PostgreSQL"
    provider: "aws"
    category: "database"
    pricing_model: "per_hour"
    pricing_source: "https://aws.amazon.com/rds/postgresql/pricing/"
    pricing_date: "2025-01-06"

    monthly_cost:
      low: 50      # db.t3.micro, 20GB, single-AZ
      mid: 250     # db.t3.medium, 100GB, multi-AZ
      high: 800    # db.r5.large, 500GB, multi-AZ, provisioned IOPS

    assumptions:
      - "US East (N. Virginia) region"
      - "Reserved instances not applied (on-demand pricing)"
      - "Low: Development environment"
      - "Mid: Production with moderate traffic"
      - "High: Production with high availability requirements"

    usage:
      metric: "instance hours + storage GB"
      low: "730 hours db.t3.micro + 20GB"
      mid: "730 hours db.t3.medium + 100GB + multi-AZ"
      high: "730 hours db.r5.large + 500GB + multi-AZ + 3000 PIOPS"

    notes: |
      Consider Aurora for better scalability above 500GB.
      Reserved instances can reduce costs by 30-60%.
      Multi-AZ doubles compute cost but is recommended for production.

    optimization_opportunities:
      - "Reserved instances for predictable workloads"
      - "Aurora Serverless for variable workloads"
      - "Read replicas instead of larger instance"
```

### GCP Cost Analysis

**Common Services:**

| Service | Pricing Model | Key Cost Drivers |
|---------|--------------|------------------|
| Compute Engine | Per-second (min 1 min) | Machine type, sustained use |
| Cloud SQL | Per-hour + storage | Instance type, HA configuration |
| Cloud Storage | Per-GB + operations | Storage class, operations |
| Cloud Functions | Per-invocation + compute time | Invocations, memory, duration |
| Cloud Run | Per-request + vCPU-second | Requests, CPU, memory |
| BigQuery | Per-TB scanned + storage | Query bytes, storage |

**GCP Pricing Research:**
```bash
WebSearch: "GCP [service] pricing 2025"
WebFetch: "https://cloud.google.com/[service]/pricing"
```

### Azure Cost Analysis

**Common Services:**

| Service | Pricing Model | Key Cost Drivers |
|---------|--------------|------------------|
| Virtual Machines | Per-hour | VM size, hours, data transfer |
| Azure SQL | DTU or vCore model | Compute tier, storage |
| Blob Storage | Per-GB + operations | Access tier, redundancy |
| Azure Functions | Per-execution + duration | Executions, memory |
| Container Apps | Per-vCPU-second | vCPU, memory, requests |
| Cosmos DB | RU/s + storage | Provisioned RUs, storage |

### Third-Party Service Costs

**Common Categories:**

| Category | Examples | Typical Pricing |
|----------|----------|-----------------|
| Authentication | Auth0, Clerk, Firebase Auth | Per-MAU |
| Payments | Stripe, PayPal | % of transaction |
| Email | SendGrid, Postmark, SES | Per-email |
| Search | Algolia, Elasticsearch Cloud | Per-search + records |
| Monitoring | Datadog, New Relic | Per-host + features |
| Error Tracking | Sentry, Bugsnag | Per-event |
| Analytics | Mixpanel, Amplitude | Per-MTU |

**Example Third-Party Cost:**

```yaml
service_costs:
  - service_name: "Stripe Payment Processing"
    provider: "stripe"
    category: "third_party"
    pricing_model: "per_transaction"
    pricing_source: "https://stripe.com/pricing"
    pricing_date: "2025-01-06"

    monthly_cost:
      low: 150      # $5,000 GMV
      mid: 750      # $25,000 GMV
      high: 3000    # $100,000 GMV

    assumptions:
      - "Standard pricing: 2.9% + $0.30 per transaction"
      - "Average transaction: $50"
      - "Low: 100 transactions/month"
      - "Mid: 500 transactions/month"
      - "High: 2000 transactions/month"

    notes: |
      Volume discounts available above $100K/month.
      Additional fees for international cards (+1.5%).
      Subscription billing may have different rates.
```

## Cost Estimation Templates

### Monthly Cost Summary

```yaml
monthly_cost_summary:
  project: "[Project Name]"
  date: "YYYY-MM-DD"
  currency: "USD"

  scenarios:
    low:
      description: "MVP / Development"
      users: "< 100"
      total: 0
    mid:
      description: "Initial Production"
      users: "1,000 - 10,000"
      total: 0
    high:
      description: "Scale / Growth"
      users: "> 10,000"
      total: 0

  by_category:
    compute:
      services: []
      low: 0
      mid: 0
      high: 0
    storage:
      services: []
      low: 0
      mid: 0
      high: 0
    database:
      services: []
      low: 0
      mid: 0
      high: 0
    networking:
      services: []
      low: 0
      mid: 0
      high: 0
    third_party:
      services: []
      low: 0
      mid: 0
      high: 0
    development:
      services: []
      low: 0
      mid: 0
      high: 0

  totals:
    monthly:
      low: 0
      mid: 0
      high: 0
    annual:
      low: 0
      mid: 0
      high: 0
```

### ROI Analysis Template

```yaml
roi_analysis:
  project: "[Project Name]"

  investment:
    development_cost: 0
    infrastructure_setup: 0
    training_and_onboarding: 0
    total_initial_investment: 0

  ongoing_costs:
    monthly_infrastructure: 0
    monthly_third_party: 0
    monthly_personnel: 0
    total_monthly_operating: 0
    annual_operating: 0

  revenue_projections:
    year_1:
      monthly_revenue: 0
      growth_rate: "% per month"
      annual_revenue: 0
    year_2:
      annual_revenue: 0
    year_3:
      annual_revenue: 0

  metrics:
    payback_period_months: 0
    year_1_roi: "percentage"
    year_3_roi: "percentage"
    break_even_users: 0

  assumptions:
    - "Revenue assumption 1"
    - "Cost assumption 2"
    - "Growth assumption 3"
```

## Cost Optimization Strategies

### Compute Optimization

| Strategy | Savings | When to Use |
|----------|---------|-------------|
| Reserved Instances | 30-60% | Predictable, steady workloads |
| Spot/Preemptible | 60-90% | Fault-tolerant, batch jobs |
| Right-sizing | 20-40% | Over-provisioned resources |
| Auto-scaling | Variable | Variable traffic patterns |
| Serverless | Variable | Sporadic, unpredictable loads |

### Storage Optimization

| Strategy | Savings | When to Use |
|----------|---------|-------------|
| Tiered Storage | 40-80% | Infrequently accessed data |
| Lifecycle Policies | Variable | Data with known access patterns |
| Compression | 20-50% | Compressible data types |
| Deduplication | Variable | Redundant data |

### Database Optimization

| Strategy | Savings | When to Use |
|----------|---------|-------------|
| Reserved Capacity | 30-60% | Predictable workloads |
| Read Replicas | Variable | Read-heavy workloads |
| Serverless | Variable | Variable traffic |
| Query Optimization | 20-50% | Pay-per-query models |

### Third-Party Optimization

| Strategy | Savings | When to Use |
|----------|---------|-------------|
| Annual Contracts | 10-30% | Committed usage |
| Volume Discounts | Variable | High volume |
| Alternative Providers | Variable | Comparable services |
| Self-hosting | Variable | High volume, DevOps capacity |

## Cost Analysis Report Structure

```markdown
# Cost Analysis Report: [Project Name]

## Executive Summary
- Total estimated monthly cost: $X - $Y
- Primary cost drivers: [List top 3]
- Key optimization opportunities: [List top 3]

## Cost Breakdown by Category

### Compute ($X/month)
[Service details and cost justification]

### Storage ($X/month)
[Service details and cost justification]

### Database ($X/month)
[Service details and cost justification]

### Third-Party Services ($X/month)
[Service details and cost justification]

## Scenario Analysis

### Low Scenario (MVP)
- Users: X
- Monthly cost: $Y
- Suitable for: [Use case]

### Mid Scenario (Production)
- Users: X
- Monthly cost: $Y
- Suitable for: [Use case]

### High Scenario (Scale)
- Users: X
- Monthly cost: $Y
- Suitable for: [Use case]

## ROI Analysis
[If applicable]

## Optimization Recommendations
1. [Recommendation with potential savings]
2. [Recommendation with potential savings]
3. [Recommendation with potential savings]

## Assumptions and Risks
- [Key assumption 1]
- [Key assumption 2]
- [Cost risk 1]

## References
- [Pricing source 1]
- [Pricing source 2]
```

## Quality Checklist

Before completing cost analysis:

- [ ] All major services identified
- [ ] Current pricing verified from official sources
- [ ] Pricing dates documented
- [ ] Usage assumptions documented
- [ ] Three scenarios calculated (low/mid/high)
- [ ] Cost optimization opportunities identified
- [ ] ROI calculated (if applicable)
- [ ] Total monthly and annual costs calculated
- [ ] Primary cost drivers identified

## Best Practices

### Do's
- Always cite official pricing sources
- Include pricing date (pricing changes frequently)
- Document all assumptions explicitly
- Consider all cost categories (don't forget networking)
- Calculate both monthly and annual costs
- Identify optimization opportunities proactively

### Don'ts
- Don't use outdated pricing data
- Don't forget data transfer costs (often overlooked)
- Don't ignore startup vs. steady-state costs
- Don't assume linear scaling of costs
- Don't forget development and operational tooling
- Don't skip personnel costs in TCO analysis
