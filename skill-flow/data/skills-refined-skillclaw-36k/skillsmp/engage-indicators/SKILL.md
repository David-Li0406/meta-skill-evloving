---
name: engage-indicators
description: Manage indicators and metrics in the Engage Analytics dbt project. Use when working with healthcare analytics indicators, adding new metrics, creating questionnaire response models, or understanding the metrics architecture. Triggers on requests involving indicator creation, metric definitions, questionnaire data models, PHQ-9/GAD-7 scores, mwTool eligibility, or dbt model development for Engage.
---

# Engage Indicators

Manage indicators and metrics in the Engage Analytics dbt project at `/Volumes/Biliba/github/engage-analytics/dbt`.

## How can I help?

**Ask the user which task they need help with:**

1. **Get Started (New User Setup)** - Install prerequisites, configure dbt, set up database connection
2. **Add a New Questionnaire** - Generate models for a new form added to the app
3. **Update Anonymization** - Mark fields as PII/non-PII in questionnaire metadata
4. **Create a New Metric** - Add a new indicator to the metrics catalog
5. **Modify an Existing Metric** - Change how an existing metric is calculated
6. **Export Data to S3** - Export anonymized or PII data to S3 buckets
7. **Understand Existing Indicators** - Query and explore current metrics in the system

## Getting Started (New User Setup)

### Prerequisites

1. **Install uv** (Python package manager):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Install direnv** (optional, for auto-loading env vars):
```bash
# macOS
brew install direnv

# Add to shell (bash)
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc

# Add to shell (zsh)
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
```

### dbt Setup

```bash
cd /Volumes/Biliba/github/engage-analytics/dbt

# Install dbt-postgres via uv
uv tool install dbt-postgres

# Install dbt package dependencies
uv run dbt deps --profiles-dir .
```

### Database Configuration

Create environment variables for database connection. Choose one method:

**Option A: Using direnv** (recommended)
```bash
cd /Volumes/Biliba/github/engage-analytics/dbt
cp .envrc.example .envrc  # or edit existing .envrc
direnv allow
```

**Option B: Manual export**
```bash
export DBT_HOST=localhost
export DBT_PORT=5432
export DBT_USER=postgres
export DBT_PASSWORD=your_password
export DBT_DATABASE=airbyte
export DBT_SCHEMA=engage_analytics
```

Edit values to match your PostgreSQL instance.

### Verify Setup

```bash
cd /Volumes/Biliba/github/engage-analytics/dbt

# Test database connection
uv run dbt debug --profiles-dir .

# Run all models
uv run dbt run --profiles-dir .
```

### Data Export Setup (Optional)

If you need to export data to S3:

```bash
cd /Volumes/Biliba/github/engage-analytics/dataexport

# Install Python dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your database and AWS credentials
```

## Quick Reference

- **Indicator specs**: `indicators/engage-indicators.csv`
- **Metrics catalog**: `macros/metrics.sql`
- **Metrics fact table**: `engage_analytics.fct_metrics_long`
- **Project docs**: `docs/metrics.md`

**Scripts** (in repo root):
- `model_generator.py` - Generate questionnaire models (named + anon)
- `metadata_manager.py` - Manage questionnaire metadata
- `run_dbt.sh` - Run dbt commands with env vars

**Data export** (in `dataexport/`):
- `run_export.sh` - Refresh dbt + export to S3
- `export_to_s3.py` - Direct S3 export

For full project structure, see [references/project-structure.md](references/project-structure.md).
For indicator-to-metric mapping, see [references/indicator-mapping.md](references/indicator-mapping.md).

## Core Capabilities

### 1. Understand Existing Indicators

Query current metrics:
```sql
SELECT metric_id, description, max(value) as latest_value
FROM engage_analytics.fct_metrics_long
GROUP BY 1, 2 ORDER BY 1;
```

Check indicator coverage in `docs/metrics.md` - maps all 32 CSV indicators to 64 dbt metrics.

### 2. Create New Indicator

**Guided workflow - ask user these questions:**

1. **What is the indicator name and description?**
2. **What domain?** (System Use, Programmatic, Treatment, Follow-up, Adoption)
3. **What module?** (mwTool, IPC, SBIRT, SPI, FWS, Planning Next Steps, All)
4. **What is the data source?**
   - Questionnaire ID (e.g., `Questionnaire/1613532`)
   - Task code (e.g., `040` for follow-up)
   - Existing model (e.g., `patient`, `practitioners`)
5. **What linkId or field contains the data?** (for questionnaire-based)
6. **What is the data type?** (Count, Percent)
7. **For percent metrics: what is the numerator and denominator?**
8. **What disaggregation?** (by organization, by practitioner, by month)

**Implementation steps:**

A. **If new source model needed**, create in `models/metrics/`:
```sql
-- models/metrics/new_metric_source.sql
-- ABOUTME: [What this model does]
-- ABOUTME: [What indicator it supports]

{{ config(materialized='view') }}

select
    subject_patient_id,
    organization_id,
    -- metric-specific fields
from {{ ref('source_model') }}
where conditions
```

B. **Add to metrics catalog** in `macros/metrics.sql`:
```yaml
- id: new_metric_name
  unit: count  # or percent
  grain: day
  entity_keys: [organization_id]
  source_model: new_metric_source
  expression: "count(distinct subject_patient_id)"  # for count
  # OR for percent:
  # numerator: "count(distinct case when condition then subject_patient_id end)"
  # denominator: "nullif(count(distinct subject_patient_id), 0)"
  description: "Human-readable description"
  version: v1
```

C. **Rebuild metrics**:
```bash
cd /Volumes/Biliba/github/engage-analytics/dbt
uv run dbt run --profiles-dir . --select new_metric_source fct_metrics_long
```

D. **Verify**:
```sql
SELECT * FROM engage_analytics.fct_metrics_long
WHERE metric_id = 'new_metric_name';
```

### 3. Add New Questionnaire

When a new form is added to the app:

A. **Find questionnaire ID** in raw data:
```sql
SELECT DISTINCT questionnaire_id
FROM engage_analytics_engage_analytics_stg.stg_questionnaire_response
ORDER BY 1;
```

B. **Extract metadata** using `metadata_manager.py`:
```bash
cd /Volumes/Biliba/github/engage-analytics/dbt
python3 metadata_manager.py extract --questionnaire-id NEW_ID
```
This extracts linkIds and adds them to `data/questionnaire_metadata.csv`.

C. **Review and edit metadata** in `data/questionnaire_metadata.csv`:
- Set `anon=TRUE` for PII fields (names, DOB, phone, address)
- Set `anon=FALSE` for non-PII fields
- Add readable `label` for each field

D. **Generate models** using `model_generator.py`:
```bash
# Generate both named and anonymized models
python3 model_generator.py all --table qr_new_form --questionnaire-id NEW_ID

# Or generate separately:
python3 model_generator.py named --table qr_new_form --questionnaire-id NEW_ID
python3 model_generator.py anon --table qr_new_form
```

E. **Build**:
```bash
uv run dbt seed --profiles-dir .  # Reload metadata
uv run dbt run --profiles-dir . --select qr_new_form qr_new_form_anon
```

**Manual model creation** (if scripts unavailable):

Named model (`models/marts/qr_named/qr_new_form.sql`):
```sql
{{ config(materialized='view') }}
{% set identifiers = ["Questionnaire/NEW_ID"] %}
{% if identifiers|length == 0 %}
  select null::text as placeholder where false
{% else %}
  {{ build_qr_wide_readable(identifiers, this.name) }}
{% endif %}
```

Anonymized model (`models/marts/qr_anon/qr_new_form_anon.sql`):
```sql
{{ config(materialized='view') }}
{{ create_anonymized_qr_view('qr_new_form', []) }}
```

### 4. Update Anonymization

Edit `data/questionnaire_metadata.csv`:
- Set `anon=TRUE` for PII fields (names, DOB, phone, address, SSN, Medicaid)
- Set `anon=FALSE` for non-PII fields

Rebuild anonymized view:
```bash
uv run dbt seed --profiles-dir .
uv run dbt run --profiles-dir . --select qr_*_anon
```

### 5. Test Metrics

Verify metric logic matches source data:
```sql
-- Get metric value
SELECT metric_id, organization_id, value
FROM engage_analytics.fct_metrics_long
WHERE metric_id = 'metric_name';

-- Verify against source
SELECT organization_id, count(distinct subject_patient_id)
FROM engage_analytics.source_model
GROUP BY 1;
```

### 6. Export Data to S3

The `dataexport/` directory contains tools for exporting data to S3 buckets.

**Full refresh + export** (recommended):
```bash
cd /Volumes/Biliba/github/engage-analytics/dataexport
./run_export.sh anon     # Anonymized data only
./run_export.sh pii      # PII data only
./run_export.sh          # Both (default)
```

This runs:
1. `dbt run` to refresh all models
2. `export_to_s3.py` to export and upload

**Direct export** (skip dbt refresh):
```bash
cd /Volumes/Biliba/github/engage-analytics/dataexport
uv run python export_to_s3.py --type anon
uv run python export_to_s3.py --type pii
uv run python export_to_s3.py --type both
uv run python export_to_s3.py --type both --delete-local  # Remove local files after upload
```

**Environment setup** - create `dataexport/.env` with:
```
# Database
DBT_HOST=localhost
DBT_PORT=5432
DBT_USER=postgres
DBT_PASSWORD=your_password
DBT_DATABASE=airbyte

# AWS
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# S3 Buckets
S3_BUCKET_ANON=engage-analytics-exports-anon
S3_BUCKET_PII=engage-analytics-exports-pii
```

**S3 file structure**:
```
s3://engage-analytics-exports-anon/
  └── 2024/01/12/
      └── engage_analytics_export_anon_20240112_143022.zip
```

**What gets exported**:
- **Anon**: `qr_*_anon` views, `patient_anon`, resource tables
- **PII**: `qr_*` views, `patient`, resource tables

## Common Patterns

### Eligibility from mwTool
```sql
-- Extract boolean from mwTool (Questionnaire/1613532)
(jsonb_path_query_first(items::jsonb,
  '$.**.item[*] ? (@.linkId == "flag-name").answer[0].valueBoolean'))::boolean
```

### Acceptance from Planning Next Steps
```sql
-- Check acceptance field
WHERE planning_next_steps_did_the_client_accept_X = 'true'
```

### Session Tracking
```sql
-- Count sessions by intervention type
SELECT intervention_type, count(distinct qr_id)
FROM engage_analytics.intervention_sessions
GROUP BY 1;
```

### Assessment Score Severity
- PHQ-9: Severe 20-27, Moderate 10-19, Mild 5-9, Minimal 0-4
- GAD-7: Severe 15-21, Moderate 10-14, Mild 5-9, Minimal 0-4
