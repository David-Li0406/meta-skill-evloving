---
name: airflow-dag-patterns
description: Best practices and conventions for creating and maintaining Airflow DAGs, including task naming, flow patterns, and error handling.
version: 1.0.0
---

# Airflow DAG Patterns

## Main DAG Location

`dags/multi_sport_betting_workflow.py` - Unified workflow for all sports.

## Task Naming Convention

Format: `{action}_{sport}`

Examples:
- `download_games_nba`
- `update_elo_nhl`
- `identify_bets_mlb`
- `place_bets_nfl`

## Sports Configuration

Add/modify sports in `SPORTS_CONFIG`:

```python
SPORTS_CONFIG = {
    "nba": {
        "elo_module": "nba_elo_rating",
        "games_module": "nba_games",
        "kalshi_function": "fetch_nba_markets",
        "elo_threshold": 0.73,
    },
    # Add new sport here following same pattern
}
```

## Task Flow Pattern

```
download_games → load_to_db → update_elo → fetch_markets → identify_bets → place_bets
```

Each sport runs independently in parallel.

## Critical Rules

1. **NEVER trigger manual DAG runs** - Clear tasks and let Airflow schedule
2. **Use PythonOperator** for all tasks:
   ```python
   from airflow.providers.standard.operators.python import PythonOperator

   task = PythonOperator(
       task_id="update_elo_nba",
       python_callable=update_elo_ratings,
       op_kwargs={"sport": "nba"},
   )
   ```

3. **Handle failures gracefully** - Don't let one sport block others:
   ```python
   task = PythonOperator(
       task_id="download_games_nba",
       python_callable=download_games,
       retries=3,
       retry_delay=timedelta(minutes=5),
   )
   ```

## Adding a New Task

1. Define function in DAG file or import from plugins
2. Create PythonOperator with task_id following naming convention
3. Set dependencies with `>>` operator
4. Test DAG parsing: `python dags/multi_sport_betting_workflow.py`

## Common Imports

```python
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
```

## Default Args Pattern

```python
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "multi_sport_betting_workflow",
    default_args=default_args,
    schedule="0 10 * * *",  # 10 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    ...
```

## Files to Reference

- `dags/multi_sport_betting_workflow.py` - Main DAG
- `dags/portfolio_hourly_snapshot.py` - Simpler DAG example
