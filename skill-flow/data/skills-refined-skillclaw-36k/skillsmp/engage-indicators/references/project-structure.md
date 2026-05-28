# Engage Analytics dbt Project Structure

## Directory Layout

```
dbt/
├── models/
│   ├── staging/           # Raw FHIR data extraction (stg_*)
│   ├── intermediate/      # Business logic (int_*)
│   ├── marts/
│   │   ├── qr_named/      # 71 questionnaire response models
│   │   ├── qr_anon/       # 34 anonymized versions
│   │   └── resources/     # patient, encounter, practitioner
│   └── metrics/           # Analytical KPIs (23+ models)
├── macros/
│   ├── metrics.sql        # Metrics catalog (YAML definitions)
│   ├── qr_wide_readable.sql
│   ├── create_anonymized_qr_view.sql
│   └── meta_tag_pivot.sql
├── data/
│   └── questionnaire_metadata.csv  # Column mappings + anon flags
├── indicators/
│   ├── engage-indicators.csv       # Indicator specifications
│   └── engage-indicators.xlsx
└── docs/
    └── metrics.md                   # Metrics documentation
```

## Data Flow

```
Raw FHIR (Airbyte) → Staging (stg_*) → Intermediate (int_*) → Marts (qr_*, patient, etc.) → Metrics
```

## Database Schemas

- `engage_analytics_engage_analytics_stg` - Staging
- `engage_analytics_engage_analytics_int` - Intermediate
- `engage_analytics_engage_analytics_mart` - Marts
- `engage_analytics` - Metrics

## Key Files

### Metrics Definition: `macros/metrics.sql`
Contains YAML catalog of all metrics with:
- `id`: Metric identifier
- `unit`: count or percent
- `source_model`: Model to query
- `expression`: SQL for count metrics
- `numerator`/`denominator`: SQL for percent metrics
- `description`: Human-readable description

### Questionnaire Metadata: `data/questionnaire_metadata.csv`
Maps questionnaire linkIds to column names:
- `table`: Target model name
- `column`: Output column name
- `linkid`: FHIR questionnaire linkId
- `anon`: TRUE/FALSE for PII masking

### Indicator Specs: `indicators/engage-indicators.csv`
Columns for defining new indicators:
- Status, Domain, Module
- Indicator/Metric name
- Description
- Questionnaire ID/Task ID
- Questionnaire Link id
- Data type (Count, Percent)
- Numerator, Denominator
- Indicator formula

## Running dbt

```bash
cd /path/to/engage-analytics/dbt
source .envrc  # or set DBT_* env vars

# Run all models
uv run dbt run --profiles-dir .

# Run specific model
uv run dbt run --profiles-dir . --select model_name

# Run with dependencies
uv run dbt run --profiles-dir . --select +model_name

# Load seed data
uv run dbt seed --profiles-dir .
```

## Environment Variables

- `DBT_HOST` - Database host
- `DBT_PORT` - Database port (default 5434)
- `DBT_USER` - Database user
- `DBT_PASSWORD` - Database password
- `DBT_DATABASE` - Database name (airbyte)
