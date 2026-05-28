---
name: cost-gcp
description: Estimate GCP infrastructure costs for any stack using live pricing data. Use when user asks about Google Cloud pricing, cost estimation for Cloud Run, GKE, Cloud SQL, Compute Engine, or any GCP service combination.
---

# GCP Cost & Ops Evaluator

Estimate costs and operational overhead for GCP-based infrastructure using real-time pricing data.

## Before Answering GCP Cost Questions

**IMPORTANT**: Always verify tool availability before providing cost estimates.

### Step 1: Check Available Tools

Check if the following tools are available:

**GCP MCP Tools** (preferred):
- `mcp__gcp-mcp__search_documentation` - Search GCP docs
- `mcp__gcp-mcp__read_documentation` - Read specific pricing pages

**gcloud CLI** (alternative):
- `gcloud billing` - Billing and pricing commands
- `gcloud services` - Service information

**Pricing API**:
- Cloud Billing Catalog API

### Step 2: If Tools Are Unavailable

If GCP MCP or CLI tools are not accessible, help the user set them up:

**Option A: GCP MCP Server**
Requirements: Python/uvx + GCP credentials
```bash
# Install GCP MCP (if available)
uvx mcp-server-gcp

# Or use the documentation MCP
uvx mcp-server-gcp-docs
```

**Option B: gcloud CLI**
```bash
# Install gcloud CLI
# macOS
brew install google-cloud-sdk

# Or download from https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

**Option C: Enable Billing API**
```bash
# Enable Cloud Billing API
gcloud services enable cloudbilling.googleapis.com

# List billing accounts
gcloud billing accounts list
```

Ask the user which option fits their environment before proceeding.

### Step 3: Fallback to Web Search

If no tools are available and user cannot install them, use web search to fetch current pricing from:
- https://cloud.google.com/pricing
- GCP Pricing Calculator: https://cloud.google.com/products/calculator

## How to Get Live Pricing

### Using gcloud CLI

```bash
# List available SKUs for a service
gcloud services list --available | grep -i compute

# Get billing information
gcloud billing accounts list

# Export billing to BigQuery for analysis
gcloud billing accounts describe ACCOUNT_ID
```

### Using Cloud Billing Catalog API

```bash
# List all services
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://cloudbilling.googleapis.com/v1/services"

# List SKUs for Compute Engine
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://cloudbilling.googleapis.com/v1/services/6F81-5844-456A/skus"

# Common Service IDs:
# Compute Engine: 6F81-5844-456A
# Cloud SQL: 9662-B51E-5089
# Cloud Run: 152E-C115-5142
# Cloud Storage: 95FF-2EF5-5EA1
# GKE: 6F81-5844-456A (uses Compute)
```

### Using Pricing Calculator API

```bash
# Use the GCP Pricing Calculator for estimates
# https://cloud.google.com/products/calculator

# Export estimates via URL sharing
```

## Standalone Usage

Can be invoked directly for cost estimation:
- "How much would Cloud Run + Cloud SQL cost?"
- "Estimate GCP costs for a Python API"
- "Compare GKE Autopilot vs Standard pricing"

## Cost Estimation Process

1. **Identify services** needed for the stack
2. **Query live pricing** using available tools
3. **Factor in sustained use discounts** (automatic)
4. **Calculate baseline** costs (minimum viable)
5. **Estimate at scale** (10x baseline load)
6. **Identify cost drivers** and optimization opportunities

## Service Categories & Tools

### Compute Services

| Service | Pricing Method |
|---------|---------------|
| Compute Engine | `cloudbilling.googleapis.com` (6F81-5844-456A) |
| Cloud Run | `cloudbilling.googleapis.com` (152E-C115-5142) |
| Cloud Functions | Billing Catalog API |
| GKE | Cluster fee ($0.10/hr) + node costs |
| App Engine | Billing Catalog API |

### Database Services

| Service | Pricing Method |
|---------|---------------|
| Cloud SQL | `cloudbilling.googleapis.com` (9662-B51E-5089) |
| Cloud Spanner | Billing Catalog API |
| Firestore | Billing Catalog API |
| Memorystore | Billing Catalog API |
| AlloyDB | Billing Catalog API |

### Storage & Networking

| Service | Pricing Method |
|---------|---------------|
| Cloud Storage | `cloudbilling.googleapis.com` (95FF-2EF5-5EA1) |
| Cloud CDN | Billing Catalog API |
| Cloud Load Balancing | Billing Catalog API |
| Cloud NAT | Billing Catalog API |

## Output Contract

```yaml
gcp_cost_estimate:
  description: "<what's being estimated>"
  region: "<GCP region>"
  pricing_source: "<mcp|cli|api|web|calculator>"
  pricing_date: "<when pricing was fetched>"

  components:
    - service: "<service name>"
      config: "<configuration>"
      monthly_cost: "<$X>"
      sustained_use_discount: "<X%>"
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

  discounts_applied:
    - type: "<sustained-use|committed-use|free-tier>"
      amount: "<$X or X%>"

  savings_opportunities:
    - type: "<committed-use|preemptible|spot>"
      potential_savings: "<X%>"
      commitment: "<1yr|3yr>"

  ops_overhead: "<low|medium|high>"
  required_gcp_knowledge: "<basic|intermediate|advanced>"

  optimization_tips:
    - "<tip 1>"
    - "<tip 2>"
```

## Cost Optimization Strategies

Query these using GCP tools:

### Committed Use Discounts
```bash
# List committed use discounts
gcloud compute commitments list

# Create a commitment (save 57% for 1yr, 70% for 3yr)
gcloud compute commitments create my-commitment \
  --region=us-central1 \
  --resources=vcpu=4,memory=16GB \
  --plan=twelve-month
```

### Preemptible/Spot VMs
```bash
# Create preemptible VM (up to 80% savings)
gcloud compute instances create my-vm \
  --preemptible \
  --machine-type=e2-medium

# Or use Spot VMs
gcloud compute instances create my-vm \
  --provisioning-model=SPOT \
  --machine-type=e2-medium
```

### Recommender API
```bash
# Get cost recommendations
gcloud recommender recommendations list \
  --project=PROJECT_ID \
  --location=global \
  --recommender=google.compute.instance.MachineTypeRecommender

# Get idle resource recommendations
gcloud recommender recommendations list \
  --recommender=google.compute.instance.IdleResourceRecommender
```

### Budget Alerts
```bash
# Create budget alert
gcloud billing budgets create \
  --billing-account=ACCOUNT_ID \
  --display-name="Monthly Budget" \
  --budget-amount=1000USD \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90
```

## GCP-Specific Pricing Notes

- **Sustained use discounts**: Automatic 30% off for consistent monthly usage
- **Committed use**: 57% (1yr) or 70% (3yr) savings
- **Preemptible/Spot**: Up to 80% off for fault-tolerant workloads
- **Free tier**: Many services have always-free tier
- **Per-second billing**: Most services bill per-second (1 min minimum)
- **Network egress**: Free within same zone, charges between zones/regions

## GCP vs AWS Cost Comparison Tips

When comparing to AWS:
- Cloud Run often cheaper than App Runner for variable traffic
- Cloud SQL slightly cheaper than RDS at baseline
- GCP sustained use discounts are automatic (AWS requires RIs)
- Secret Manager is significantly cheaper than AWS Secrets Manager
- Check data transfer costs - can vary significantly
