---
name: Data Engineering
description: This skill should be used when the user asks to "create data pipeline", "ETL process", "data lake", "data warehouse", "Apache Spark", "Airflow DAG", "data streaming", "Kafka pipeline", "dbt models", "data quality", or needs help with data engineering and pipeline development.
version: 1.0.0
---

# Data Engineering

Comprehensive guidance for data pipelines, ETL processes, and data infrastructure.

## Data Pipeline Patterns

### Batch Processing (Apache Spark)

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ETL").getOrCreate()

# Extract
df = spark.read.parquet("s3://data-lake/raw/events/")

# Transform
transformed = df \
    .filter(df.event_type == "purchase") \
    .groupBy("user_id", "date") \
    .agg({"amount": "sum"})

# Load
transformed.write.mode("overwrite").parquet("s3://data-lake/processed/daily_purchases/")
```

### Stream Processing (Kafka + Flink)

```python
# Kafka consumer
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'events',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    group_id='my-group'
)

for message in consumer:
    process_event(message.value)
```

## Airflow DAGs

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'daily_etl',
    default_args=default_args,
    schedule_interval='0 6 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_data
    )

    transform = PythonOperator(
        task_id='transform',
        python_callable=transform_data
    )

    load = PythonOperator(
        task_id='load',
        python_callable=load_data
    )

    extract >> transform >> load
```

## dbt Models

```sql
-- models/staging/stg_orders.sql
{{ config(materialized='view') }}

SELECT
    id as order_id,
    user_id,
    created_at,
    total_amount
FROM {{ source('raw', 'orders') }}
WHERE created_at >= '2024-01-01'
```

## Data Quality

```python
from great_expectations.core import ExpectationSuite

suite = ExpectationSuite("orders_suite")
suite.add_expectation(
    expectation_type="expect_column_values_to_not_be_null",
    kwargs={"column": "order_id"}
)
suite.add_expectation(
    expectation_type="expect_column_values_to_be_between",
    kwargs={"column": "amount", "min_value": 0, "max_value": 10000}
)
```

## Additional Resources

### Reference Files
- **`references/data-patterns.md`** - Data pipeline patterns
- **`references/dbt-guide.md`** - dbt best practices
