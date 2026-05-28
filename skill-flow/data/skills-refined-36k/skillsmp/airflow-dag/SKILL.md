---
name: airflow-dag
description: Apache Airflow DAG development with TaskFlow API, Google Cloud operators (BigQuery, GCS), dbt integration, and dynamic DAG generation. Use when creating or modifying Airflow DAGs, implementing data pipeline orchestration, setting up cross-DAG dependencies with ExternalTaskSensor, adding deferrable operators, or configuring error handling and retries.
---

# Airflow DAG Development Skill

Write Airflow DAGs following best practices for recommendation systems.

## DAG Template

```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

default_args = {
    "owner": "data-team",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=2),
}

@dag(
    dag_id="recommendation_{pipeline_name}_daily",
    description="Description of the DAG purpose",
    schedule="0 2 * * *",  # Daily at 2 AM
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["recommendation", "daily"],
    default_args=default_args,
)
def recommendation_pipeline():
    """DAG docstring explaining the pipeline flow."""
    
    @task
    def extract_data(**context):
        """Extract data from source."""
        pass
    
    @task
    def transform_data(data, **context):
        """Transform extracted data."""
        pass
    
    @task
    def load_data(transformed_data, **context):
        """Load data to destination."""
        pass
    
    # Define task dependencies
    data = extract_data()
    transformed = transform_data(data)
    load_data(transformed)

dag_instance = recommendation_pipeline()
```

## Best Practices

### 1. Use Google Cloud Operators
```python
# BigQuery Insert Job
run_query = BigQueryInsertJobOperator(
    task_id="run_feature_query",
    configuration={
        "query": {
            "query": "{% include 'sql/features/user_features.sql' %}",
            "useLegacySql": False,
            "destinationTable": {
                "projectId": "{{ var.value.gcp_project }}",
                "datasetId": "recommendation",
                "tableId": "user_features_{{ ds_nodash }}",
            },
            "writeDisposition": "WRITE_TRUNCATE",
        }
    },
    location="asia-southeast1",
)
```

### 2. Deferrable Operators for Long-running Tasks
```python
from airflow.providers.google.cloud.sensors.bigquery import BigQueryTableExistenceSensor

wait_for_table = BigQueryTableExistenceSensor(
    task_id="wait_for_source_table",
    project_id="{{ var.value.gcp_project }}",
    dataset_id="raw_data",
    table_id="user_events_{{ ds_nodash }}",
    deferrable=True,  # Release worker while waiting
    poke_interval=60,
    timeout=3600,
)
```

### 3. Error Handling with Callbacks
```python
def on_failure_callback(context):
    """Send alert on task failure."""
    task_instance = context["task_instance"]
    dag_id = context["dag"].dag_id
    # Send to Slack/PagerDuty
    
@dag(
    ...,
    on_failure_callback=on_failure_callback,
)
```

### 4. Dynamic Task Generation
```python
from airflow.utils.task_group import TaskGroup

product_categories = ["clothing", "accessories", "shoes"]

with TaskGroup(group_id="process_categories") as category_group:
    for category in product_categories:
        BigQueryInsertJobOperator(
            task_id=f"process_{category}",
            configuration={...},
        )
```

## Error Handling & Retry Strategies

### Smart Retry with Error Classification
```python
from airflow.exceptions import AirflowFailException
from datetime import timedelta

def classify_and_retry(context):
    """Intelligent retry logic based on error type."""
    exception = context.get('exception')
    task_instance = context['task_instance']

    # Transient errors - retry immediately
    if isinstance(exception, (TimeoutError, ConnectionError)):
        return timedelta(seconds=30)

    # Rate limit errors - exponential backoff
    elif 'quota' in str(exception).lower() or 'rate limit' in str(exception).lower():
        backoff = timedelta(minutes=5 * (task_instance.try_number ** 2))
        return backoff

    # Permanent errors - don't retry
    elif 'not found' in str(exception).lower() or 'invalid' in str(exception).lower():
        raise AirflowFailException(f"Permanent failure: {exception}")

    # Default retry
    return timedelta(minutes=5)

@task(retry_delay_callable=classify_and_retry, retries=5)
def resilient_task(**context):
    """Task with smart retry logic."""
    # Task implementation
    pass
```

### SLA Monitoring
```python
from airflow.models import DAG
from datetime import timedelta

def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    """Alert when SLA is missed."""
    message = f"SLA missed for tasks: {[t.task_id for t in task_list]}"
    # Send to monitoring system
    print(message)

@dag(
    dag_id="recommendation_train_daily",
    default_args={
        "sla": timedelta(hours=4),  # Task should complete within 4 hours
        "on_failure_callback": on_failure_callback,
    },
    sla_miss_callback=sla_miss_callback,
)
def pipeline_with_sla():
    pass
```

## Performance Optimization

### Resource Pool Management
```python
from airflow.models import Pool
from airflow.decorators import task

# Limit concurrent BigQuery jobs to prevent quota exhaustion
@task(pool="bigquery_pool", pool_slots=2)
def query_bigquery(**context):
    """Execute BigQuery job with resource limits."""
    from google.cloud import bigquery

    client = bigquery.Client()
    query = "SELECT * FROM `project.dataset.table` LIMIT 1000"
    query_job = client.query(query)
    return list(query_job.result())

# Create pool via Airflow UI or CLI:
# airflow pools set bigquery_pool 5 "BigQuery job pool"
```

### Task Parallelism Optimization
```python
from airflow.utils.task_group import TaskGroup

@dag(
    max_active_tasks=16,  # Limit concurrent tasks
    max_active_runs=1,     # Prevent overlapping DAG runs
)
def optimized_pipeline():
    """Pipeline with optimized parallelism."""

    with TaskGroup(group_id="parallel_processing") as process_group:
        # Process partitions in parallel
        partitions = [f"2024-01-{day:02d}" for day in range(1, 32)]

        for partition in partitions[:10]:  # Limit to 10 parallel tasks
            @task(task_id=f"process_{partition.replace('-', '_')}")
            def process_partition(partition_date: str):
                # Process single partition
                return partition_date

            process_partition(partition)
```

## Troubleshooting Common Issues

### DAG Import Failures
```python
# Check DAG import errors
from airflow.models import DagBag

dag_bag = DagBag(dag_folder='/path/to/dags', include_examples=False)

if dag_bag.import_errors:
    for dag_id, error in dag_bag.import_errors.items():
        print(f"DAG {dag_id} failed to import: {error}")
else:
    print(f"Successfully loaded {len(dag_bag.dags)} DAGs")
```

### XCom Size Limits
```python
from airflow.decorators import task
import json

@task
def large_data_handler(**context):
    """Handle large data without XCom limits."""
    from google.cloud import storage

    # Instead of returning large data via XCom, use GCS
    large_data = {"results": [i for i in range(1000000)]}

    # Upload to GCS
    client = storage.Client()
    bucket = client.bucket("airflow-temp-data")
    blob = bucket.blob(f"temp/{context['ds']}/data.json")
    blob.upload_from_string(json.dumps(large_data))

    # Return only the GCS path
    return f"gs://airflow-temp-data/temp/{context['ds']}/data.json"

@task
def process_large_data(gcs_path: str):
    """Read large data from GCS."""
    from google.cloud import storage
    import json

    client = storage.Client()
    bucket_name, blob_name = gcs_path.replace("gs://", "").split("/", 1)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    data = json.loads(blob.download_as_string())
    # Process data
    return len(data["results"])
```

### Debugging with Cloud Logging
```python
import logging
from airflow.decorators import task

# Configure structured logging
logger = logging.getLogger(__name__)

@task
def task_with_logging(**context):
    """Task with structured logging for Cloud Logging."""

    # Add context to logs
    logger.info(
        "Processing data",
        extra={
            "dag_id": context["dag"].dag_id,
            "task_id": context["task"].task_id,
            "execution_date": str(context["ds"]),
            "custom_metric": 123,
        }
    )

    try:
        # Task logic
        result = {"status": "success"}
        logger.info(f"Task completed: {result}")
        return result
    except Exception as e:
        logger.error(
            f"Task failed: {e}",
            exc_info=True,
            extra={"error_type": type(e).__name__}
        )
        raise
```

## Advanced Dependency Patterns

### Cross-DAG Dependencies
```python
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import timedelta

@dag(dag_id="recommendation_serve_daily")
def serving_pipeline():
    """Pipeline that depends on upstream feature pipeline."""

    # Wait for upstream DAG to complete
    wait_for_features = ExternalTaskSensor(
        task_id="wait_for_feature_pipeline",
        external_dag_id="recommendation_features_daily",
        external_task_id="validate_features",
        allowed_states=["success"],
        failed_states=["failed", "skipped"],
        mode="reschedule",  # Don't block worker
        poke_interval=60,
        timeout=7200,
        # Handle execution date offset if schedules differ
        execution_delta=timedelta(hours=1),
    )

    @task
    def serve_recommendations():
        """Serve recommendations after features are ready."""
        pass

    wait_for_features >> serve_recommendations()
```

### Conditional Branching
```python
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator

def decide_processing_path(**context):
    """Decide which path to take based on data volume."""
    from google.cloud import bigquery

    client = bigquery.Client()
    query = f"""
    SELECT COUNT(*) as row_count
    FROM `project.raw.user_events`
    WHERE DATE(event_timestamp) = '{context['ds']}'
    """
    result = list(client.query(query).result())[0]

    if result.row_count > 1000000:
        return "heavy_processing"
    else:
        return "light_processing"

@dag(dag_id="conditional_pipeline")
def conditional_dag():
    """Pipeline with conditional execution."""

    branch = BranchPythonOperator(
        task_id="decide_path",
        python_callable=decide_processing_path,
    )

    heavy_task = EmptyOperator(task_id="heavy_processing")
    light_task = EmptyOperator(task_id="light_processing")
    join = EmptyOperator(task_id="join", trigger_rule="none_failed_min_one_success")

    branch >> [heavy_task, light_task] >> join
```

### Dynamic Task Mapping (Airflow 2.3+)
```python
from airflow.decorators import task

@dag(dag_id="dynamic_mapping_example")
def dynamic_pipeline():
    """Pipeline with dynamic task mapping."""

    @task
    def get_partitions(**context):
        """Get list of partitions to process."""
        return [f"2024-01-{day:02d}" for day in range(1, 32)]

    @task
    def process_partition(partition: str):
        """Process a single partition."""
        print(f"Processing {partition}")
        return f"Completed {partition}"

    # Dynamic mapping - creates task for each partition
    partitions = get_partitions()
    process_partition.expand(partition=partitions)

dag_instance = dynamic_pipeline()
```

## dbt Integration Patterns

### DbtCloudRunJobOperator

```python
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator

run_dbt_job = DbtCloudRunJobOperator(
    task_id="run_dbt_transformation",
    job_id="{{ var.value.dbt_job_id }}",
    check_interval=60,
    timeout=3600,
    deferrable=True,  # Use triggerer for efficiency
)
```

### dbt Core with BashOperator

```python
from airflow.operators.bash import BashOperator

dbt_run = BashOperator(
    task_id="dbt_run",
    bash_command="""
    cd /path/to/dbt/project &&
    dbt run --models {{ params.models }} --target prod
    """,
    params={"models": "user_features product_features"},
    env={
        "DBT_PROFILES_DIR": "/path/to/profiles",
        "GCP_PROJECT": "{{ var.value.gcp_project }}",
    },
)

dbt_test = BashOperator(
    task_id="dbt_test",
    bash_command="cd /path/to/dbt/project && dbt test --target prod",
)

dbt_run >> dbt_test
```

### Incremental dbt Models in Airflow

```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id="dbt_incremental_pipeline",
    schedule="0 * * * *",  # Hourly
    start_date=datetime(2024, 1, 1),
    catchup=False,
)
def dbt_incremental():
    """Run dbt incremental models hourly."""

    @task
    def check_source_freshness():
        """Check source data freshness before dbt run."""
        import subprocess
        result = subprocess.run(
            ["dbt", "source", "freshness"],
            cwd="/path/to/dbt/project",
            capture_output=True,
        )
        if result.returncode != 0:
            raise Exception(f"Source freshness check failed: {result.stderr}")

    run_dbt = BashOperator(
        task_id="dbt_run_incremental",
        bash_command="""
        cd /path/to/dbt/project &&
        dbt run --select state:modified+ --defer --state prod-run-artifacts/
        """,
    )

    check_source_freshness() >> run_dbt

dag_instance = dbt_incremental()
```

## Data Lineage Tracking

### OpenLineage Integration

```python
from airflow import DAG
from airflow.providers.openlineage.plugins.adapter import OpenLineageAdapter
from airflow.decorators import task

# OpenLineage is automatically enabled in Airflow 2.7+
# Configure via environment variables:
# OPENLINEAGE_URL=http://marquez:5000
# OPENLINEAGE_NAMESPACE=recommendation_pipeline

@dag(dag_id="lineage_tracked_pipeline")
def pipeline_with_lineage():
    """Pipeline with automatic lineage tracking."""

    @task
    def extract_data(**context):
        """Extract data - lineage tracked automatically."""
        from google.cloud import bigquery

        client = bigquery.Client()
        query = """
        SELECT * FROM `project.raw.user_events`
        WHERE DATE(event_timestamp) = CURRENT_DATE()
        """
        # OpenLineage captures: source table, query, destination
        df = client.query(query).to_dataframe()
        return df.to_json()

    extract_data()
```

### Custom Lineage Metadata

```python
from airflow.lineage.entities import File, Table
from airflow.operators.bash import BashOperator

# Add lineage metadata to tasks
process_data = BashOperator(
    task_id="process_data",
    bash_command="python process.py",
    inlets=[
        Table(
            database="bigquery",
            cluster="gcp-project",
            name="raw.user_events",
        )
    ],
    outlets=[
        Table(
            database="bigquery",
            cluster="gcp-project",
            name="features.user_features",
        )
    ],
)
```

## Dynamic DAG Generation

For advanced dynamic DAG patterns (YAML-based factories, database-driven generation, Jinja2 templates), see [reference/dynamic-dags.md](reference/dynamic-dags.md).

### Quick Example - Generate DAGs from Config

```python
import yaml
from pathlib import Path
from airflow import DAG
from datetime import datetime

config_dir = Path(__file__).parent / "configs"

for config_file in config_dir.glob("*.yaml"):
    with open(config_file) as f:
        config = yaml.safe_load(f)
        # Create DAG from config
        dag = DAG(
            dag_id=config["dag_id"],
            schedule=config["schedule"],
            start_date=datetime.fromisoformat(config["start_date"]),
            catchup=False,
        )
        globals()[config["dag_id"]] = dag
```

## Cost Optimization

For detailed cost optimization patterns (cost-aware operators, query caching, cost tracking), see [reference/cost-tracking.md](reference/cost-tracking.md).

### Quick Cost Control Example
```python
from airflow.decorators import task
from google.cloud import bigquery

@task
def cost_controlled_query(sql: str, max_cost_usd: float = 10.0, **context):
    """Execute BigQuery query with cost control."""
    client = bigquery.Client()

    # Dry run to estimate cost
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=True)
    dry_run_job = client.query(sql, job_config=job_config)

    estimated_cost = (dry_run_job.total_bytes_processed / 1e12) * 5
    if estimated_cost > max_cost_usd:
        raise AirflowException(f"Query too expensive: ${estimated_cost:.2f}")

    return list(client.query(sql).result())
```

## Troubleshooting

For detailed troubleshooting guides (DAG import failures, XCom limits, debugging, memory issues), see [reference/troubleshooting.md](reference/troubleshooting.md).

## Coding Conventions

- Task IDs: `{verb}_{noun}` (e.g., `extract_user_events`)
- DAG IDs: `{domain}_{action}_{frequency}` (e.g., `recommendation_train_daily`)
- Use Jinja templating for dynamic values
- Always set `execution_timeout` to prevent hanging tasks
- Document DAG purpose in docstring
- Use deferrable operators for long-running tasks

## Advanced Topics

For detailed guidance on specialized patterns:

- **Cost Optimization**: See [reference/cost-tracking.md](reference/cost-tracking.md) for cost-aware operators and query caching
- **Troubleshooting**: See [reference/troubleshooting.md](reference/troubleshooting.md) for DAG import failures, XCom limits, and debugging
