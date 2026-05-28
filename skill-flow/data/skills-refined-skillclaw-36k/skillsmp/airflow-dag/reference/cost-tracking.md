# Cost Optimization for GCP

This guide provides patterns for tracking and optimizing BigQuery costs in Airflow DAGs.

## Cost-Aware BigQuery Operator

```python
from airflow.decorators import task
from airflow.exceptions import AirflowException
from google.cloud import bigquery

@task
def cost_controlled_query(sql: str, max_cost_usd: float = 10.0, **context):
    """Execute BigQuery query with cost control."""

    client = bigquery.Client()

    # Dry run to estimate cost
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=True)
    dry_run_job = client.query(sql, job_config=job_config)

    bytes_processed = dry_run_job.total_bytes_processed
    estimated_cost = (bytes_processed / 1e12) * 5  # $5 per TB

    context["task_instance"].xcom_push(
        key="estimated_cost",
        value=estimated_cost
    )

    if estimated_cost > max_cost_usd:
        raise AirflowException(
            f"Query too expensive: ${estimated_cost:.2f} exceeds ${max_cost_usd} limit"
        )

    # Execute actual query
    job_config = bigquery.QueryJobConfig(use_query_cache=True)
    query_job = client.query(sql, job_config=job_config)
    results = list(query_job.result())

    # Log actual cost
    actual_bytes = query_job.total_bytes_processed
    actual_cost = (actual_bytes / 1e12) * 5

    context["task_instance"].log.info(
        f"Query cost: ${actual_cost:.4f} (processed {actual_bytes / 1e9:.2f} GB)"
    )

    return results
```

## Query Result Caching

```python
from google.cloud import bigquery

@task
def cached_query(**context):
    """Execute query with result caching."""

    client = bigquery.Client()

    job_config = bigquery.QueryJobConfig(
        use_query_cache=True,  # Use cached results if available
        use_legacy_sql=False,
    )

    query = """
    SELECT user_id, COUNT(*) as events
    FROM `project.raw.user_events`
    WHERE DATE(event_timestamp) = CURRENT_DATE()
    GROUP BY user_id
    """

    query_job = client.query(query, job_config=job_config)

    # Check if results came from cache
    if query_job.cache_hit:
        context["task_instance"].log.info("Results retrieved from cache (no cost)")
    else:
        bytes_billed = query_job.total_bytes_billed
        cost = (bytes_billed / 1e12) * 5
        context["task_instance"].log.info(f"Query cost: ${cost:.4f}")

    return list(query_job.result())
```

## Cost Tracking

```python
from airflow.decorators import task
from google.cloud import bigquery
from datetime import datetime

@task
def track_dag_costs(dag_id: str, **context):
    """Track BigQuery costs for this DAG run."""

    client = bigquery.Client()

    # Query job history for this DAG run
    query = f"""
    SELECT
        job_id,
        user_email,
        total_bytes_billed,
        (total_bytes_billed / POW(10, 12)) * 5 as cost_usd,
        creation_time
    FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
    WHERE DATE(creation_time) = '{context['ds']}'
        AND state = 'DONE'
        AND job_type = 'QUERY'
        AND user_email = '{client.get_service_account_email()}'
    ORDER BY creation_time DESC
    """

    results = list(client.query(query).result())
    total_cost = sum(row.cost_usd for row in results)

    # Store cost metric
    context["task_instance"].xcom_push(key="dag_cost_usd", value=total_cost)
    context["task_instance"].log.info(
        f"Total BigQuery cost for {dag_id}: ${total_cost:.2f}"
    )

    return total_cost
```

## Cost Budget Alerts

```python
from airflow.decorators import task
from airflow.exceptions import AirflowException

@task
def enforce_daily_budget(max_daily_cost_usd: float = 100.0, **context):
    """Enforce daily cost budget for BigQuery usage."""

    from google.cloud import bigquery

    client = bigquery.Client()

    query = f"""
    SELECT
        SUM((total_bytes_billed / POW(10, 12)) * 5) as total_cost_usd
    FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
    WHERE DATE(creation_time) = CURRENT_DATE()
        AND job_type = 'QUERY'
        AND state = 'DONE'
    """

    result = list(client.query(query).result())[0]
    daily_cost = result.total_cost_usd or 0.0

    context["task_instance"].log.info(f"Daily cost so far: ${daily_cost:.2f}")

    if daily_cost > max_daily_cost_usd:
        raise AirflowException(
            f"Daily budget exceeded: ${daily_cost:.2f} > ${max_daily_cost_usd}"
        )

    return daily_cost
```

## Best Practices

- Always use dry_run for cost estimation before executing expensive queries
- Enable query result caching to avoid re-scanning data
- Set cost budgets and enforce them with pre-flight checks
- Track costs per DAG run to identify expensive pipelines
- Use partitioned tables and filter on partition columns
- Monitor INFORMATION_SCHEMA.JOBS to analyze query patterns
