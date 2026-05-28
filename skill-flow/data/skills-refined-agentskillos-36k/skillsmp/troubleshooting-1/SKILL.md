---
name: troubleshooting
description: Diagnosis and resolution guides for common issues in the system, including Airflow failures, database connection errors, API authentication, and data integrity problems.
version: 1.0.0
---

# Troubleshooting

## Airflow DAG Parsing Errors

**Symptom:** DAG not appearing in Airflow UI

```bash
# Test DAG parsing locally
python dags/multi_sport_betting_workflow.py

# Check Airflow logs
docker logs $(docker ps -qf "name=scheduler") 2>&1 | grep -i error
```

**Common causes:**
- Import errors in plugins (missing dependencies)
- Syntax errors in DAG file
- Circular imports

**Fix:** Ensure plugins directory is in Python path:
```python
plugins_dir = Path(__file__).parent.parent / "plugins"
if str(plugins_dir) not in sys.path:
    sys.path.insert(0, str(plugins_dir))
```

## Database Connection Issues

**Symptom:** `connection refused` or `authentication failed`

```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Test connection
psql -h localhost -U airflow -d airflow -c "SELECT 1"
```

**Environment variables:**
```bash
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_USER=airflow
export POSTGRES_PASSWORD=airflow
export POSTGRES_DB=airflow
```

## Kalshi API Authentication

**Symptom:** `401 Unauthorized` or `Invalid API key`

**Check credentials:**
```python
with open("kalshkey") as f:
    api_key = f.readline().strip()
    private_key = f.read()

print(f"API Key length: {len(api_key)}")
print(f"Private key starts with: {private_key[:50]}")
```

**Common issues:**
- Extra whitespace in kalshkey file
- Expired API key
- Wrong environment (demo vs production)

## Team Name Mismatches

**Symptom:** Bets not matching, empty results

```python
from naming_resolver import NamingResolver

resolver = NamingResolver()

# Debug team name resolution
print(resolver.resolve("LAL", "nba"))
print(resolver.resolve("Lakers", "nba"))
print(resolver.resolve("Los Angeles Lakers", "nba"))
```

**Fix:** Add missing mappings to `naming_resolver.py`:
```python
NBA_ALIASES = {
    "LA Lakers": "Los Angeles Lakers",
    "LAL": "Los Angeles Lakers",
    # Add missing aliases
}
```

## Data Pipeline Failures

**Symptom:** Missing games, stale data

```bash
# Check last successful run
docker exec $(docker ps -qf "name=scheduler") \
  airflow dags list-runs -d multi_sport_betting_workflow --limit 5
```

**Debug data freshness:**
```python
from db_manager import default_db

df = default_db.fetch_df("""
    SELECT sport, MAX(game_date) as latest
    FROM unified_games
    GROUP BY sport
""")
print(df)
```

## Task Failures

**Get task logs:**
```bash
docker exec $(docker ps -qf "name=scheduler") \
  airflow tasks logs multi_sport_betting_workflow download_games_nba 2024-01-15
```

**Clear failed task:**
```bash
docker exec $(docker ps -qf "name=scheduler") \
  airflow tasks clear multi_sport_betting_workflow -t download_games_nba -s 2024-01-15 -e 2024-01-15
```

## Memory Issues

**Symptom:** OOM errors, slow performance

```python
# Process data in chunks
for chunk in pd.read_sql(query, engine, chunksize=10000):
    process(chunk)
```

## Import Errors

**Symptom:** `ModuleNotFoundError`

```bash
# Check if module exists
ls plugins/ | grep module_name

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

## Files to Reference

- `TROUBLESHOOTING.md` - Additional troubleshooting
- `docker-compose.yaml` - Service configuration
- `logs/` - Airflow logs directory
