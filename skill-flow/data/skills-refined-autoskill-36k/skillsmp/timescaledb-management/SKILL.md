---
name: timescaledb-management
description: Guidelines for managing TimescaleDB hypertables, continuous aggregates, and migrations. Use this when creating new tables or modifying time-series data schemas.
---

When managing database migrations for the Cycle Navigator Dashboard, follow these mandatory steps:

1. **Mandatory Backup**: Always back up the production database before any migration.  
   - **Linux (Bash)**: `pg_dump -h localhost -U cycle_user cycle_navigator > backup_$(date +%Y%m%d).sql`  
   - **Linux (Fish)**: `pg_dump -h localhost -U cycle_user cycle_navigator > backup_(date +%Y%m%d).sql`  
   - **Windows (PowerShell)**: `pg_dump -h localhost -U cycle_user cycle_navigator > backup_$(Get-Date -Format 'yyyyMMdd').sql`  
   - **Windows (CMD)**: `pg_dump -h localhost -U cycle_user cycle_navigator > backup_%date:~10,4%%date:~4,2%%date:~7,2%.sql`  

2. **Pre-Migration Checks**: Run the check script to verify compatibility before applying migrations. This script checks for schema conflicts, data type mismatches, and TimescaleDB extension availability.  
   Prerequisites: Ensure Python 3.x is installed and dependencies are met (run `pip install -r requirements.txt` if needed).  
   Command: `python3 scripts/run_timescale_migrations.py --check-only` (use `python` on Windows if aliased).  
   If checks fail, review the output for issues and resolve before proceeding.  

3. **Hypertable Conversion**: Converting a table to a hypertable is **irreversible**. Verify the `chunk_time_interval` before conversion (standard is '1 month' for FRED data due to lower update frequency, and '7 days' for crypto data due to high-frequency volatility).  
   Command: `python3 scripts/run_timescale_migrations.py --convert-table <table_name> --chunk-interval <interval>`  
   After conversion, run `SELECT * FROM timescaledb_information.hypertables;` to confirm the hypertable exists and chunk settings are correct.

4. **Compression Policy**: Ensure new hypertables include a compression policy to optimize storage and query performance. The standard is 90 days for macro data (slower update cadence) and 30 days for crypto data (high-frequency updates).  
   Command: `python3 scripts/run_timescale_migrations.py --compress-table <table_name> --compress-after <days>`  
   Verify with: `SELECT * FROM timescaledb_information.compression_settings WHERE hypertable_name = '<table_name>';`

5. **Continuous Aggregates**: When pre-calculating metrics, use materialized views with a refresh policy to reduce query latency. Use hourly refreshes for crypto data (high-frequency volatility) and daily refreshes for macro data (slower update cadence).  
   Command: `python3 scripts/run_timescale_migrations.py --create-aggregate <aggregate_name> --source-table <table_name> --refresh-interval <interval>`  
   Example metrics: OHLCV candles, moving averages, volatility indices.  
   Verify with: `SELECT * FROM timescaledb_information.continuous_aggregates WHERE view_name = '<aggregate_name>';`