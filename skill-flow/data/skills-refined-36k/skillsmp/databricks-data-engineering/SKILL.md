---
name: databricks-data-engineering
description: Production data engineering pipelines following medallion architecture (Bronze/Silver/Gold layers) with data ingestion, transformation, quality checks, Delta Lake optimization, and orchestration. Use when building ETL pipelines, medallion architecture, data lakes, or data transformation workflows.
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

# Databricks Data Engineering Pipelines

Build production-grade data pipelines following medallion architecture (Bronze/Silver/Gold) with data quality checks, Delta Lake optimization, and multi-layer transformations.

## When to Use This Skill

- Building ETL/ELT data pipelines
- Implementing medallion architecture
- Data lake transformations
- Data quality and validation workflows
- Incremental data processing
- Batch data pipelines
- Real-time streaming (structured streaming)

## Medallion Architecture

The medallion architecture organizes data into three layers of increasing quality:

```
Bronze Layer (Raw/Landing)
    ↓
Silver Layer (Cleaned/Validated)
    ↓
Gold Layer (Business/Aggregated)
```

### Bronze Layer (Raw Ingestion)
- **Purpose**: Ingest raw data with minimal transformation
- **Pattern**: Append-only, preserve source format
- **Transformations**: Type casting, timestamp addition
- **Storage**: Delta Lake tables
- **Schema**: Flexible, can evolve

### Silver Layer (Cleaned Data)
- **Purpose**: Cleaned, validated, and conformed data
- **Pattern**: Deduplication, quality checks, schema enforcement
- **Transformations**: Data quality rules, null handling, type validation
- **Storage**: Delta Lake tables (optimized)
- **Schema**: Strict, well-defined

### Gold Layer (Business-Ready)
- **Purpose**: Aggregated, business-ready datasets
- **Pattern**: Joins, aggregations, business logic
- **Transformations**: Metrics, KPIs, analytics-ready views
- **Storage**: Delta Lake tables (highly optimized)
- **Schema**: Denormalized for analytics

## Complete Data Pipeline Workflow

### Phase 1: Schema Setup

Use `databricks-unity-catalog` skill to create medallion schemas:

```python
catalog = "de_prod"

# Bronze - raw data
create_schema(
    catalog_name=catalog,
    schema_name="bronze",
    comment="Raw ingested data. Minimal transformation. Append-only. 90-day retention."
)

# Silver - cleaned data
create_schema(
    catalog_name=catalog,
    schema_name="silver",
    comment="Cleaned and validated data. Deduplicated, quality-checked. 1-year retention."
)

# Gold - business aggregates
create_schema(
    catalog_name=catalog,
    schema_name="gold",
    comment="Business-ready aggregates. Optimized for analytics. 3-year retention."
)
```

### Phase 2: Bronze Layer Development

Use `databricks-testing` skill to test ingestion logic:

```python
databricks_command(
    cluster_id="0123-456789-abc123",
    language="python",
    code="""
from pyspark.sql import functions as F

# Ingest raw data
raw_df = (
    spark.read
    .format("json")  # or csv, parquet, etc.
    .option("inferSchema", "true")
    .load("/mnt/source/events/*.json")
)

# Add ingestion metadata
bronze_df = (
    raw_df
    .withColumn("ingestion_timestamp", F.current_timestamp())
    .withColumn("ingestion_date", F.current_date())
    .withColumn("source_file", F.input_file_name())
)

print(f"Ingested {bronze_df.count()} records")

# Save to bronze
bronze_df.write \\
    .format("delta") \\
    .mode("append") \\
    .saveAsTable("de_prod.bronze.raw_events")

print("Bronze ingestion complete")
"""
)
```

### Phase 3: Silver Layer Development

Use `databricks-testing` skill to test cleaning logic:

**Complete Silver Layer Notebook:**

```python
# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Layer - Data Cleaning & Validation
# MAGIC
# MAGIC Transforms bronze data into cleaned, validated silver tables

# COMMAND ----------
# Widget parameterization
try:
    catalog = dbutils.widgets.get("catalog")
except:
    catalog = "de_dev"

try:
    bronze_schema = dbutils.widgets.get("bronze_schema")
except:
    bronze_schema = "bronze"

try:
    silver_schema = dbutils.widgets.get("silver_schema")
except:
    silver_schema = "silver"

try:
    batch_date = dbutils.widgets.get("batch_date")
except:
    from datetime import date
    batch_date = str(date.today())

print(f"Processing silver layer:")
print(f"  Catalog: {catalog}")
print(f"  Bronze schema: {bronze_schema}")
print(f"  Silver schema: {silver_schema}")
print(f"  Batch date: {batch_date}")

# COMMAND ----------
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Read from bronze (incremental)
bronze_df = spark.read.table(f"{catalog}.{bronze_schema}.raw_events") \\
    .filter(F.col("ingestion_date") == batch_date)

print(f"Bronze records for {batch_date}: {bronze_df.count()}")

# COMMAND ----------
# Data quality checks BEFORE cleaning
print("Data Quality Report - Before Cleaning:")
print(f"  Total records: {bronze_df.count()}")
print(f"  Null event_id: {bronze_df.filter(F.col('event_id').isNull()).count()}")
print(f"  Null timestamp: {bronze_df.filter(F.col('timestamp').isNull()).count()}")
print(f"  Duplicate event_id: {bronze_df.groupBy('event_id').count().filter(F.col('count') > 1).count()}")

# Record initial count for tracking
initial_count = bronze_df.count()

# COMMAND ----------
# Cleaning transformations
silver_df = (
    bronze_df

    # Remove records with null in critical fields
    .filter(F.col("event_id").isNotNull())
    .filter(F.col("timestamp").isNotNull())
    .filter(F.col("user_id").isNotNull())

    # Deduplicate - keep latest by timestamp
    .withColumn("row_num", F.row_number().over(
        Window.partitionBy("event_id").orderBy(F.col("timestamp").desc())
    ))
    .filter(F.col("row_num") == 1)
    .drop("row_num")

    # Type casting and validation
    .withColumn("amount", F.col("amount").cast("double"))
    .withColumn("quantity", F.col("quantity").cast("int"))
    .withColumn("timestamp", F.col("timestamp").cast("timestamp"))

    # Remove invalid values
    .filter(F.col("amount") >= 0)  # No negative amounts
    .filter(F.col("quantity") > 0)  # Quantity must be positive

    # Add silver layer metadata
    .withColumn("silver_processed_at", F.current_timestamp())
    .withColumn("silver_processing_date", F.current_date())

    # Drop ingestion metadata (not needed in silver)
    .drop("source_file", "ingestion_timestamp", "ingestion_date")
)

# COMMAND ----------
# Data quality checks AFTER cleaning
final_count = silver_df.count()
removed_count = initial_count - final_count

print(f"\\nData Quality Report - After Cleaning:")
print(f"  Clean records: {final_count}")
print(f"  Removed records: {removed_count} ({removed_count/initial_count*100:.2f}%)")

# Validation assertions
assert silver_df.filter(F.col("event_id").isNull()).count() == 0, "Null event_ids remain"
assert silver_df.filter(F.col("timestamp").isNull()).count() == 0, "Null timestamps remain"
assert silver_df.groupBy("event_id").count().filter(F.col("count") > 1).count() == 0, "Duplicates remain"

print("✓ All quality checks passed")

# COMMAND ----------
# Write to silver (merge for idempotency)
from delta.tables import DeltaTable

silver_table = f"{catalog}.{silver_schema}.clean_events"

# Check if table exists
if spark.catalog.tableExists(silver_table):
    # Merge into existing table (upsert pattern)
    deltaTable = DeltaTable.forName(spark, silver_table)

    deltaTable.alias("target").merge(
        silver_df.alias("source"),
        "target.event_id = source.event_id"
    ).whenMatchedUpdateAll() \\
     .whenNotMatchedInsertAll() \\
     .execute()

    print(f"Merged {final_count} records into {silver_table}")
else:
    # Create table
    silver_df.write \\
        .format("delta") \\
        .mode("overwrite") \\
        .saveAsTable(silver_table)

    print(f"Created {silver_table} with {final_count} records")

# COMMAND ----------
# Optimize Delta table
spark.sql(f"OPTIMIZE {silver_table}")
print(f"✓ Optimized {silver_table}")

# Update statistics
spark.sql(f"ANALYZE TABLE {silver_table} COMPUTE STATISTICS")
print(f"✓ Updated statistics for {silver_table}")

# COMMAND ----------
# Z-order for query optimization (optional)
spark.sql(f"OPTIMIZE {silver_table} ZORDER BY (event_id, timestamp)")
print(f"✓ Z-ordered {silver_table}")

# COMMAND ----------
print(f"\\n{'='*50}")
print("Silver layer processing complete!")
print(f"  Input (Bronze): {initial_count} records")
print(f"  Output (Silver): {final_count} records")
print(f"  Quality: {final_count/initial_count*100:.2f}% retention")
print(f"{'='*50}")
```

### Phase 4: Gold Layer Development

Use `databricks-testing` skill to test aggregation logic:

**Complete Gold Layer Notebook:**

```python
# Databricks notebook source
# MAGIC %md
# MAGIC # Gold Layer - Business Aggregates
# MAGIC
# MAGIC Creates business-ready aggregated datasets for analytics

# COMMAND ----------
# Widget parameterization
try:
    catalog = dbutils.widgets.get("catalog")
except:
    catalog = "de_dev"

try:
    silver_schema = dbutils.widgets.get("silver_schema")
except:
    silver_schema = "silver"

try:
    gold_schema = dbutils.widgets.get("gold_schema")
except:
    gold_schema = "gold"

print(f"Processing gold layer:")
print(f"  Catalog: {catalog}")
print(f"  Silver schema: {silver_schema}")
print(f"  Gold schema: {gold_schema}")

# COMMAND ----------
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Read from silver
silver_df = spark.table(f"{catalog}.{silver_schema}.clean_events")
print(f"Silver records: {silver_df.count()}")

# COMMAND ----------
# Daily aggregations by user
daily_user_metrics = (
    silver_df
    .withColumn("event_date", F.to_date("timestamp"))
    .groupBy("event_date", "user_id")
    .agg(
        F.count("*").alias("event_count"),
        F.sum("amount").alias("total_amount"),
        F.avg("amount").alias("avg_amount"),
        F.sum("quantity").alias("total_quantity"),
        F.countDistinct("event_id").alias("unique_events"),
        F.min("timestamp").alias("first_event_time"),
        F.max("timestamp").alias("last_event_time")
    )
    .withColumn("gold_created_at", F.current_timestamp())
)

print(f"Daily user metrics: {daily_user_metrics.count()} records")

# COMMAND ----------
# Weekly aggregations
weekly_metrics = (
    silver_df
    .withColumn("week_start", F.date_trunc("week", "timestamp"))
    .groupBy("week_start")
    .agg(
        F.count("*").alias("total_events"),
        F.countDistinct("user_id").alias("active_users"),
        F.sum("amount").alias("weekly_revenue"),
        F.avg("amount").alias("avg_transaction_value")
    )
    .withColumn("gold_created_at", F.current_timestamp())
)

print(f"Weekly metrics: {weekly_metrics.count()} records")

# COMMAND ----------
# User lifetime metrics (SCD Type 1)
user_lifetime_metrics = (
    silver_df
    .groupBy("user_id")
    .agg(
        F.count("*").alias("lifetime_events"),
        F.sum("amount").alias("lifetime_value"),
        F.avg("amount").alias("avg_order_value"),
        F.min("timestamp").alias("first_purchase_date"),
        F.max("timestamp").alias("last_purchase_date"),
        F.countDistinct(F.to_date("timestamp")).alias("purchase_days")
    )
    .withColumn(
        "days_since_last_purchase",
        F.datediff(F.current_date(), F.col("last_purchase_date"))
    )
    .withColumn(
        "customer_lifetime_days",
        F.datediff(F.col("last_purchase_date"), F.col("first_purchase_date"))
    )
    .withColumn("gold_created_at", F.current_timestamp())
)

print(f"User lifetime metrics: {user_lifetime_metrics.count()} users")

# COMMAND ----------
# Save gold tables
daily_user_metrics.write \\
    .format("delta") \\
    .mode("overwrite") \\
    .option("overwriteSchema", "true") \\
    .saveAsTable(f"{catalog}.{gold_schema}.daily_user_metrics")

weekly_metrics.write \\
    .format("delta") \\
    .mode("overwrite") \\
    .option("overwriteSchema", "true") \\
    .saveAsTable(f"{catalog}.{gold_schema}.weekly_metrics")

user_lifetime_metrics.write \\
    .format("delta") \\
    .mode("overwrite") \\
    .option("overwriteSchema", "true") \\
    .saveAsTable(f"{catalog}.{gold_schema}.user_lifetime_metrics")

print("✓ Gold tables created")

# COMMAND ----------
# Optimize all gold tables
for table in ["daily_user_metrics", "weekly_metrics", "user_lifetime_metrics"]:
    full_table = f"{catalog}.{gold_schema}.{table}"
    spark.sql(f"OPTIMIZE {full_table}")
    spark.sql(f"ANALYZE TABLE {full_table} COMPUTE STATISTICS")
    print(f"✓ Optimized {full_table}")

# COMMAND ----------
print(f"\\n{'='*50}")
print("Gold layer processing complete!")
print(f"  Daily user metrics: {daily_user_metrics.count()} records")
print(f"  Weekly metrics: {weekly_metrics.count()} records")
print(f"  User lifetime metrics: {user_lifetime_metrics.count()} users")
print(f"{'='*50}")
```

### Phase 5: Deployment

Use `databricks-bundle-deploy` skill to package medallion pipeline:

**databricks.yml:**
```yaml
bundle:
  name: medallion_pipeline

variables:
  catalog:
    description: "Unity Catalog name"
    default: "de_dev"

  bronze_schema:
    description: "Bronze layer schema"
    default: "bronze"

  silver_schema:
    description: "Silver layer schema"
    default: "silver"

  gold_schema:
    description: "Gold layer schema"
    default: "gold"

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
              bronze_schema: ${var.bronze_schema}

        # Silver layer - cleaned/validated
        - task_key: silver_transformation
          depends_on:
            - task_key: bronze_ingestion
          notebook_task:
            notebook_path: ../src/medallion/notebooks/silver_transform.py
            base_parameters:
              catalog: ${var.catalog}
              bronze_schema: ${var.bronze_schema}
              silver_schema: ${var.silver_schema}

        # Gold layer - business aggregates
        - task_key: gold_aggregation
          depends_on:
            - task_key: silver_transformation
          notebook_task:
            notebook_path: ../src/medallion/notebooks/gold_aggregate.py
            base_parameters:
              catalog: ${var.catalog}
              silver_schema: ${var.silver_schema}
              gold_schema: ${var.gold_schema}

      schedule:
        quartz_cron_expression: "0 0 * * * ?"  # Hourly
        timezone_id: "UTC"

      email_notifications:
        on_failure:
          - ${workspace.current_user.userName}
```

**Validate and deploy:**
```bash
databricks bundle validate -t dev
databricks bundle deploy -t dev

# Ask before running:
# "Do you want to run the pipeline now?"
```

## Data Engineering Best Practices

### 1. Idempotent Operations

Use merge (upsert) pattern for idempotency:

```python
from delta.tables import DeltaTable

deltaTable = DeltaTable.forName(spark, target_table)

deltaTable.alias("target").merge(
    source_df.alias("source"),
    "target.id = source.id"
).whenMatchedUpdateAll() \\
 .whenNotMatchedInsertAll() \\
 .execute()
```

### 2. Data Quality Checks

Add assertions at each layer:

```python
# Check for required fields
assert df.filter(F.col("id").isNull()).count() == 0, "Null IDs found"

# Check for duplicates
dup_count = df.groupBy("id").count().filter(F.col("count") > 1).count()
assert dup_count == 0, f"Found {dup_count} duplicates"

# Check data ranges
assert df.filter(F.col("amount") < 0).count() == 0, "Negative amounts found"
```

### 3. Delta Lake Optimization

Optimize tables after writes:

```python
# Compact small files
spark.sql(f"OPTIMIZE {table_name}")

# Update statistics
spark.sql(f"ANALYZE TABLE {table_name} COMPUTE STATISTICS")

# Z-order for query performance (optional)
spark.sql(f"OPTIMIZE {table_name} ZORDER BY (date_column, id_column)")
```

### 4. Incremental Processing

Process only new data:

```python
# Bronze - append new files
new_files_df = spark.read.json("/mnt/source/*.json") \\
    .filter(F.col("ingestion_date") == current_date)

# Silver - process today's bronze records
bronze_incremental = spark.read.table("bronze.events") \\
    .filter(F.col("ingestion_date") == current_date)
```

### 5. Schema Evolution

Handle schema changes gracefully:

```python
# Allow schema evolution in silver
silver_df.write \\
    .format("delta") \\
    .mode("append") \\
    .option("mergeSchema", "true") \\
    .saveAsTable(silver_table)
```

## Common Patterns

### Pattern: SCD Type 2 (Slowly Changing Dimension)

```python
# Add effective dates for historical tracking
from pyspark.sql import functions as F

scd2_df = (
    df
    .withColumn("effective_start_date", F.current_date())
    .withColumn("effective_end_date", F.lit("9999-12-31").cast("date"))
    .withColumn("is_current", F.lit(True))
)
```

### Pattern: Late-Arriving Data

```python
# Handle late data with merge
deltaTable.alias("target").merge(
    late_data.alias("source"),
    "target.id = source.id AND target.date = source.date"
).whenMatchedUpdate(
    condition="source.updated_at > target.updated_at",
    set={"*"}
).whenNotMatchedInsertAll() \\
 .execute()
```

### Pattern: Data Lineage Tracking

```python
# Add lineage metadata
df_with_lineage = (
    df
    .withColumn("source_system", F.lit("sales_db"))
    .withColumn("pipeline_run_id", F.lit(dbutils.widgets.get("run_id")))
    .withColumn("processed_timestamp", F.current_timestamp())
)
```

## Integration with Other Skills

### Uses
- `databricks-unity-catalog` - Creates medallion schemas (bronze, silver, gold)
- `databricks-testing` - Tests each layer's transformation logic
- `databricks-bundle-deploy` - Packages and deploys pipeline

### Workflow Summary

1. UC skill → Create bronze, silver, gold schemas
2. Testing skill → Test bronze ingestion
3. Testing skill → Test silver cleaning
4. Testing skill → Test gold aggregations
5. Bundle skill → Package medallion pipeline
6. Bundle skill → Deploy to environments

## Troubleshooting

### Issue: Small Files Problem

**Symptom:** Slow queries, many small files

**Solution:**
```python
# Optimize to compact files
spark.sql(f"OPTIMIZE {table_name}")

# Or set target file size
spark.conf.set("spark.databricks.delta.targetFileSize", "128mb")
```

### Issue: Schema Mismatch

**Symptom:** "Schema mismatch" error on append

**Solution:**
```python
# Enable schema merging
df.write.option("mergeSchema", "true").saveAsTable(table)

# Or overwrite schema
df.write.option("overwriteSchema", "true").mode("overwrite").saveAsTable(table)
```

### Issue: Duplicate Records

**Symptom:** Same record appears multiple times

**Solution:**
```python
# Deduplicate in silver layer
from pyspark.sql.window import Window

dedup_df = df.withColumn(
    "row_num",
    F.row_number().over(Window.partitionBy("id").orderBy(F.col("timestamp").desc()))
).filter(F.col("row_num") == 1).drop("row_num")
```

## Summary

This skill builds production data engineering pipelines:
- **Bronze**: Raw data ingestion with minimal transformation
- **Silver**: Cleaned, validated, deduplicated data
- **Gold**: Business-ready aggregates and metrics
- **Quality**: Data validation at each layer
- **Optimization**: Delta Lake compaction and Z-ordering
- **Idempotency**: Merge patterns for reliable pipelines

Use this skill to build scalable, production-grade data pipelines following medallion architecture best practices.
