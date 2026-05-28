---
name: databricks-bundle-deploy
description: Package and deploy Databricks Asset Bundles with proper parameterization, multi-environment support, and serverless compute. Handles project structure, databricks.yml generation, validation, and deployment. Use when packaging tested code for production, deploying pipelines, or managing multi-environment deployments.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
model: claude-sonnet-4-5-20250929
user-invocable: true
---

# Databricks Asset Bundle Deployment

Package tested code into Databricks Asset Bundles (DABs) and deploy to multiple environments (dev/staging/prod) with proper parameterization and governance.

## When to Use This Skill

- Packaging tested code for deployment (after `databricks-testing`)
- Creating production-ready pipeline projects
- Deploying to dev/staging/prod environments
- Setting up multi-environment CI/CD
- Managing notebook deployments
- Scheduling jobs in Databricks

## Core Concepts

### Databricks Asset Bundles (DABs)

DABs are the standard way to package and deploy Databricks workflows:
- Infrastructure as code for Databricks
- Version control friendly (Git)
- Multi-environment support (dev/staging/prod)
- Automated validation and deployment
- Consistent project structure

### Two-Phase Workflow

**Phase 1: Test & Iterate** (using `databricks-testing` skill)
- Test code on cluster via MCP
- Debug and fix errors
- Iterate until working

**Phase 2: Package & Deploy** (this skill)
- Create DAB project structure
- Generate databricks.yml and job definitions
- Validate bundle
- Deploy to environment
- (Optional) Run deployed job

## Standard Project Structure

```
project_name/
├── databricks.yml              # Bundle configuration (REQUIRED)
├── resources/                  # Job/pipeline definitions (REQUIRED)
│   └── job.yml                # Job definition
├── src/                       # Source code (RECOMMENDED)
│   └── project_name/
│       └── notebooks/
│           ├── 01_data_prep.py
│           ├── 02_transform.py
│           └── 03_output.py
└── tests/                     # Unit tests (OPTIONAL)
    └── test_transformations.py
```

### Key Files

**databricks.yml** - Bundle configuration:
- Bundle name and variables
- Environment targets (dev/staging/prod)
- References to resources

**resources/*.yml** - Job/pipeline definitions:
- Task configurations
- Cluster settings (use serverless)
- Schedules and triggers
- Notebook paths and parameters

## Deployment Workflows

### Workflow 1: Create Bundle from Scratch

Package working code into new DAB project.

**Pattern:**
1. Create project directory structure
2. Generate `databricks.yml` with:
   - Bundle name
   - Variables (catalog, schema, etc.)
   - Targets (dev, staging, prod)
3. Create job definition in `resources/job.yml`
4. Move tested notebooks to `src/<project>/notebooks/`
5. Add parameterization (widgets) to notebooks
6. **Validate** (automatic, no confirmation)
7. **Deploy** (automatic, no confirmation)
8. **Ask before running** (requires user confirmation)

### Workflow 2: Validate and Deploy (AUTOMATIC)

After bundle creation, automatically validate and deploy.

**Pattern:**
```bash
# Step 1: Validate (AUTOMATIC - no confirmation needed)
databricks bundle validate -t dev

# If validation fails:
# - Show errors
# - Fix databricks.yml or resource files
# - Re-run validate

# Step 2: Deploy (AUTOMATIC - no confirmation needed)
databricks bundle deploy -t dev

# Reports:
# - Deployment success
# - Job name and ID
# - Workspace URL
```

**IMPORTANT:** These commands run automatically per CLAUDE.md rules.

### Workflow 3: Run Deployed Job (REQUIRES CONFIRMATION)

Execute the deployed job.

**Pattern:**
```bash
# IMPORTANT: ALWAYS ask user first
# "Do you want to run the deployed job '<job_name>' now?"

# Only if user confirms:
databricks bundle run <job_name> -t dev

# Monitor and report:
# - Run URL
# - Run status (RUNNING, SUCCESS, FAILED)
# - Result state
# - Error messages if failed
```

**IMPORTANT:** Never run jobs without explicit user confirmation per CLAUDE.md rules.

## Parameterization

### Required Parameterization Patterns

**Never hard-code values. Always use variables.**

**Bundle Variables (databricks.yml):**
```yaml
variables:
  catalog:
    description: "Unity Catalog name"
    default: "dev_catalog"

  schema:
    description: "Schema name"
    default: "default"

  project_name:
    description: "Project identifier"
```

**Environment-Specific Values (targets):**
```yaml
targets:
  dev:
    mode: development
    variables:
      catalog: "dev_catalog"
      schema: "dev_schema"

  prod:
    mode: production
    variables:
      catalog: "prod_catalog"
      schema: "prod_schema"
```

**Built-in Variables:**
- `${var.catalog}` - User-defined variable
- `${bundle.target}` - Current environment (dev/staging/prod)
- `${workspace.current_user.userName}` - Current user email
- `${workspace.file_path}` - Workspace file path

### Notebook Widget Parameterization

**All notebooks must use widgets with defaults:**

```python
# REQUIRED pattern for all notebook parameters
try:
    catalog = dbutils.widgets.get("catalog")
except:
    catalog = "dev_catalog"

try:
    schema = dbutils.widgets.get("schema")
except:
    schema = "default"

try:
    batch_date = dbutils.widgets.get("batch_date")
except:
    from datetime import date
    batch_date = str(date.today())
```

**Why try/except:**
- Allows local testing without widgets
- Provides sensible defaults
- Prevents errors in interactive mode

## Serverless Compute Guidelines

**DO:**
- Rely on serverless compute (no `new_cluster` in tasks)
- Use `%pip install` for Python dependencies
- Keep tasks small and focused
- Use Delta Lake for data persistence

**DON'T:**
- Define `new_cluster` in task configuration
- Install libraries via cluster init scripts
- Run long operations without checkpoints
- Use non-Delta formats for production data

**Example Task Configuration:**
```yaml
tasks:
  - task_key: data_prep
    notebook_task:
      notebook_path: ../src/project/notebooks/01_prep.py
      base_parameters:
        catalog: ${var.catalog}
    # NO new_cluster here - uses serverless by default
```

## Path Resolution Rules

**CRITICAL:** Paths in `resources/*.yml` resolve **relative to the resource file**.

```
project/
├── databricks.yml
├── resources/
│   └── job.yml          # Paths resolve from HERE
└── src/
    └── notebooks/
        └── notebook.py
```

**In resources/job.yml:**
```yaml
notebook_path: ../src/notebooks/notebook.py  # Relative to resources/
```

**Not:**
```yaml
notebook_path: src/notebooks/notebook.py  # Wrong - from project root
```

## Complete Bundle Examples

### Example 1: Simple Data Pipeline Bundle

**databricks.yml:**
```yaml
bundle:
  name: ${var.project_name}

variables:
  project_name:
    description: "Project identifier"
    default: "my_pipeline"

  catalog:
    description: "Unity Catalog name"
    default: "dev_catalog"

  schema:
    description: "Schema name"
    default: "pipeline_data"

targets:
  dev:
    mode: development
    workspace:
      host: ${DATABRICKS_HOST}
    variables:
      catalog: "dev_catalog"

  prod:
    mode: production
    workspace:
      host: ${DATABRICKS_HOST}
    variables:
      catalog: "prod_catalog"

resources:
  jobs:
    my_pipeline_job:
      name: ${var.project_name}_job_${bundle.target}

      tasks:
        - task_key: data_ingestion
          notebook_task:
            notebook_path: ../src/${var.project_name}/notebooks/01_ingest.py
            base_parameters:
              catalog: ${var.catalog}
              schema: ${var.schema}

        - task_key: data_transformation
          depends_on:
            - task_key: data_ingestion
          notebook_task:
            notebook_path: ../src/${var.project_name}/notebooks/02_transform.py
            base_parameters:
              catalog: ${var.catalog}
              schema: ${var.schema}

        - task_key: data_output
          depends_on:
            - task_key: data_transformation
          notebook_task:
            notebook_path: ../src/${var.project_name}/notebooks/03_output.py
            base_parameters:
              catalog: ${var.catalog}
              schema: ${var.schema}

      # Optional: Schedule
      schedule:
        quartz_cron_expression: "0 0 2 * * ?"  # Daily at 2am
        timezone_id: "UTC"

      # Optional: Email notifications
      email_notifications:
        on_failure:
          - ${workspace.current_user.userName}
```

**resources/job.yml:**
```yaml
# Alternative: Define job in separate file
# Reference from databricks.yml with: resources: {jobs: job.yml}

resources:
  jobs:
    my_pipeline_job:
      # Same content as above
```

### Example 2: ML Training Pipeline Bundle

**databricks.yml:**
```yaml
bundle:
  name: ml_training_pipeline

variables:
  catalog:
    description: "Unity Catalog for ML assets"
    default: "ml_dev"

  schema:
    description: "Schema for models and features"
    default: "churn_model"

  experiment_name:
    description: "MLflow experiment path"

targets:
  dev:
    mode: development
    variables:
      catalog: "ml_dev"
      experiment_name: "/Users/${workspace.current_user.userName}/experiments/churn_dev"

  prod:
    mode: production
    variables:
      catalog: "ml_prod"
      experiment_name: "/Shared/experiments/churn_prod"

resources:
  jobs:
    ml_training_job:
      name: ml_training_${bundle.target}

      tasks:
        - task_key: data_preparation
          notebook_task:
            notebook_path: ../src/ml_training/notebooks/01_data_prep.py
            base_parameters:
              catalog: ${var.catalog}
              schema: ${var.schema}

        - task_key: feature_engineering
          depends_on:
            - task_key: data_preparation
          notebook_task:
            notebook_path: ../src/ml_training/notebooks/02_features.py
            base_parameters:
              catalog: ${var.catalog}
              schema: ${var.schema}

        - task_key: model_training
          depends_on:
            - task_key: feature_engineering
          notebook_task:
            notebook_path: ../src/ml_training/notebooks/03_training.py
            base_parameters:
              catalog: ${var.catalog}
              schema: ${var.schema}
              experiment_name: ${var.experiment_name}

        - task_key: model_registration
          depends_on:
            - task_key: model_training
          notebook_task:
            notebook_path: ../src/ml_training/notebooks/04_register.py
            base_parameters:
              catalog: ${var.catalog}
              schema: ${var.schema}
```

### Example 3: Medallion Architecture Bundle

**databricks.yml:**
```yaml
bundle:
  name: medallion_pipeline

variables:
  catalog:
    description: "Unity Catalog name"
    default: "de_dev"

targets:
  dev:
    mode: development
    variables:
      catalog: "de_dev"

  prod:
    mode: production
    variables:
      catalog: "de_prod"

resources:
  jobs:
    medallion_job:
      name: medallion_pipeline_${bundle.target}

      tasks:
        # Bronze layer - raw ingestion
        - task_key: bronze_ingestion
          notebook_task:
            notebook_path: ../src/medallion/notebooks/bronze_ingest.py
            base_parameters:
              catalog: ${var.catalog}
              bronze_schema: "bronze"

        # Silver layer - cleaned/validated
        - task_key: silver_transformation
          depends_on:
            - task_key: bronze_ingestion
          notebook_task:
            notebook_path: ../src/medallion/notebooks/silver_transform.py
            base_parameters:
              catalog: ${var.catalog}
              bronze_schema: "bronze"
              silver_schema: "silver"

        # Gold layer - business aggregates
        - task_key: gold_aggregation
          depends_on:
            - task_key: silver_transformation
          notebook_task:
            notebook_path: ../src/medallion/notebooks/gold_aggregate.py
            base_parameters:
              catalog: ${var.catalog}
              silver_schema: "silver"
              gold_schema: "gold"

      schedule:
        quartz_cron_expression: "0 0 * * * ?"  # Hourly
        timezone_id: "UTC"
```

## Notebook Parameter Example

**Parameterized notebook (01_data_prep.py):**
```python
# Databricks notebook source
# MAGIC %md
# MAGIC # Data Preparation
# MAGIC
# MAGIC Loads and prepares data for transformation

# COMMAND ----------
# Widget parameterization with defaults
try:
    catalog = dbutils.widgets.get("catalog")
except:
    catalog = "dev_catalog"

try:
    schema = dbutils.widgets.get("schema")
except:
    schema = "pipeline_data"

try:
    batch_date = dbutils.widgets.get("batch_date")
except:
    from datetime import date
    batch_date = str(date.today())

print(f"Running with parameters:")
print(f"  Catalog: {catalog}")
print(f"  Schema: {schema}")
print(f"  Batch Date: {batch_date}")

# COMMAND ----------
from pyspark.sql import functions as F

# Load data using parameterized catalog/schema
df = spark.table(f"{catalog}.{schema}.source_data")

# Filter by batch date
df_filtered = df.filter(F.col("date") == batch_date)

print(f"Loaded {df_filtered.count()} records for {batch_date}")

# COMMAND ----------
# Save prepared data
output_table = f"{catalog}.{schema}.prepared_data"

df_filtered.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(output_table)

print(f"Saved to {output_table}")
```

## Deployment Commands

### Validate Bundle

```bash
# Validate bundle structure and configuration
databricks bundle validate -t dev

# Common validation errors:
# - Invalid YAML syntax
# - Missing required fields
# - Invalid notebook paths
# - Undefined variables
```

### Deploy Bundle

```bash
# Deploy to development environment
databricks bundle deploy -t dev

# Deploy to production environment
databricks bundle deploy -t prod

# What happens:
# - Bundle uploaded to workspace
# - Jobs created/updated
# - Notebooks synced
# - Resources configured
```

### Run Deployed Job

```bash
# IMPORTANT: Ask user first!
# "Do you want to run the job now?"

# If confirmed:
databricks bundle run my_job -t dev

# Monitor output for:
# - Run URL (for tracking)
# - Run status
# - Error messages
```

## Error Handling

### Validation Errors

**Error:** `Invalid notebook path: src/notebooks/01_prep.py`

**Cause:** Path doesn't account for relative resolution

**Fix:** Use `../src/notebooks/01_prep.py` (relative to resources/)

---

**Error:** `Variable 'catalog' is not defined`

**Cause:** Used `${var.catalog}` without defining in variables section

**Fix:** Add to databricks.yml:
```yaml
variables:
  catalog:
    description: "Unity Catalog name"
```

---

**Error:** `YAML syntax error at line 15`

**Cause:** Invalid YAML (indentation, missing quotes, etc.)

**Fix:** Check YAML syntax, ensure consistent indentation (2 spaces)

### Deployment Errors

**Error:** `Permission denied: cannot create job`

**Cause:** Insufficient workspace permissions

**Fix:** Check user has job creation permissions in workspace

---

**Error:** `Notebook not found: /Workspace/...`

**Cause:** Notebook doesn't exist at specified path

**Fix:** Verify notebook was created in src/ directory, check path in job definition

## Integration with Other Skills

### Receives From
- `databricks-testing` - Tested, working code
- `databricks-unity-catalog` - Schema and table names to use

### Used By
- `databricks-ml-pipeline` - Packages ML training pipelines
- `databricks-data-engineering` - Packages data pipelines

## Best Practices

### 1. Always Parameterize
- Never hard-code catalog/schema names
- Use variables for environment-specific values
- Use widgets in notebooks with try/except defaults

### 2. Use Serverless Compute
- Don't define new_cluster
- Rely on Databricks serverless
- Faster startup, better cost optimization

### 3. Validate Before Deploy
- Always run `databricks bundle validate` first
- Fix all validation errors
- Then deploy

### 4. Use Meaningful Names
- Job names: `project_name_job_${bundle.target}`
- Task keys: Descriptive (data_prep, model_training)
- Clear variable names

### 5. Document with Comments
- Add descriptions to all variables
- Comment complex job configurations
- Include README in project

### 6. Multi-Environment from Day 1
- Define dev, staging, prod targets upfront
- Use same bundle for all environments
- Only variables differ per environment

## Security Reminders

- Never embed tokens or secrets in databricks.yml
- Use environment variables for credentials
- Set proper job permissions
- Use service principals for production

## Summary

This skill packages and deploys Databricks Asset Bundles:
- **Create**: Generate project structure, databricks.yml, job definitions
- **Parameterize**: Variables for catalogs, schemas, environments
- **Validate**: Automatic validation (no confirmation)
- **Deploy**: Automatic deployment (no confirmation)
- **Run**: Manual job execution (requires user confirmation)
- **Multi-environment**: Support dev/staging/prod with same bundle

Use this skill after testing code with `databricks-testing` to deploy production-ready pipelines.
