---
name: superset-dashboard-automation
description: Use this skill when you need to automate the creation of Apache Superset dashboards for finance, compliance, and operational analytics, saving costs compared to traditional BI tools.
---

# Skill body

## What This Skill Does

- **Auto-generate dashboards** for BIR compliance, finance SSC, and operational analytics.
- **Create datasets** using optimized SQL from Supabase or Odoo.
- **Build charts** with 20+ visualization types following best practices.
- **Apply templates** for common use cases to streamline dashboard creation.
- **Schedule refreshes** for automated data updates.

**Annual Savings**: $8,400 compared to a Tableau 10-user license.

## Quick Start

When asked to create dashboards:

1. **Identify data source**: Choose from Supabase, Odoo PostgreSQL, or CSV.
2. **Create dataset**: Write an optimized SQL query.
3. **Build charts**: Select the appropriate visualization type.
4. **Assemble dashboard**: Layout charts with necessary filters.
5. **Apply template**: Use pre-built templates for common scenarios.
6. **Schedule refreshes**: Set up automated data updates.

## Core Workflows

### Workflow 1: BIR Compliance Dashboard

1. Connect to the Supabase database.
2. Create dataset: `bir_filing_summary`.
3. Build charts:
   - 1601-C monthly trends (timeseries).
   - 2550Q status by agency (pivot table).
   - ATP expiry calendar (table).
   - Tax payable big number (KPI).
4. Apply filters: agency, period, status.
5. Set refresh schedule: daily at 6 AM.

### Workflow 2: Create Optimized Dataset

1. Write SQL query joining Odoo tables.
2. Add calculated columns.
3. Set proper column types.
4. Configure cache timeout.
5. Add metrics (SUM, AVG, COUNT).
6. Define dimensions (group by fields).
7. Test query performance.

### Workflow 3: Chart Best Practices

1. Select chart type: Pivot Table v2.
2. Configure:
   - Rows: Vendor name.
   - Columns: Aging buckets.
   - Metrics: Sum(amount).
   - Color scale: Red (overdue) to Green (current).
3. Add conditional formatting.
4. Set refresh interval.

## Deployment Options

### Option 1: App Platform (Managed, Zero Maintenance)

- Best for teams without DevOps who want zero maintenance.
- [Complete guide](deployment/digitalocean-spec.yaml).

### Option 2: Droplets (Self-hosted, Full Control)

- For teams needing flexibility and control.
- [Droplet Guide](deployment/droplet-guide.md).

### Corrected App Spec (DO Best Practices)

```yaml
name: superset
region: sgp  # Or your preferred region

services:
  - name: superset
    image:
      registry_type: DOCKER_HUB
      registry: apache
      repository: superset
      tag: "3.1.0"  # Pin to stable version (not 'latest')
    
    instance_size_slug: professional-xs  # Minimum 1GB RAM
    instance_count: 1
    http_port: 8088
    
    envs:
      # Required: Database connection
      - key: DATABASE_URL
        value: postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
        type: SECRET
        scope:
```