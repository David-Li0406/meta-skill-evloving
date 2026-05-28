# Troubleshooting Common Issues

This guide covers common Airflow DAG issues and their solutions.

## DAG Import Failures

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

## XCom Size Limits

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

## Debugging with Cloud Logging

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

## Task Timeout Issues

```python
from datetime import timedelta

@task(execution_timeout=timedelta(minutes=30))
def long_running_task(**context):
    """Task with explicit timeout."""
    # Task logic here
    pass
```

## Memory Issues in Workers

```python
# Use KubernetesPodOperator for memory-intensive tasks
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

heavy_compute = KubernetesPodOperator(
    task_id="heavy_compute",
    name="heavy-compute-pod",
    namespace="airflow",
    image="gcr.io/project/heavy-compute:latest",
    cmds=["python", "script.py"],
    resources={
        "request_memory": "4Gi",
        "limit_memory": "8Gi",
        "request_cpu": "2",
        "limit_cpu": "4",
    },
)
```

## Scheduler Lag

Check scheduler performance metrics and consider:

- Increasing scheduler resources
- Reducing DAG file parsing frequency
- Using `dag_file_processor_timeout` appropriately
- Minimizing top-level code in DAG files

## Best Practices

- Always use `execution_timeout` to prevent hanging tasks
- Use GCS for large data instead of XCom
- Implement structured logging for better debugging
- Monitor Cloud Logging for error patterns
- Use appropriate resource limits for heavy tasks
- Keep DAG files lightweight (avoid heavy imports at top level)
