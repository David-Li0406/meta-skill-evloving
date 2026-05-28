---
name: db-explorer
description: Explore PostgreSQL and DuckDB schemas, tables, and sample data. Use when investigating data issues, checking table structures, or when user asks "DB 구조 알려줘", "데이터 확인해줘".
---

# Database Explorer

QueryCraft가 사용하는 하이브리드 데이터베이스 시스템(PostgreSQL + DuckDB)을 탐색합니다.

## Instructions

1. **스키마 및 테이블 목록 조회**:
   - `scripts/run_task.py list`를 통해 명령어를 확인하거나 `psql`, `duckdb` CLI를 우회적으로 활용합니다.
   
   - **PostgreSQL 테이블 목록**:
     ```bash
     export PYTHONPATH=$PYTHONPATH:$(pwd)
     python -c "from backend.engine.postgres_engine import PostgresEngine; from backend.config.db import PostgresEnv; pg=PostgresEngine(PostgresEnv().dsn()); print(pg.fetch_df('SELECT table_name FROM information_schema.tables WHERE table_schema=\'public\''))"
     ```

2. **특정 테이블 스키마 확인**:
   - `scripts/check_schema.py` 유틸리티를 사용합니다.
     ```bash
     python scripts/check_schema.py <table_name>
     ```

3. **샘플 데이터 조회**:
   - 테이블의 실시간 데이터를 확인할 때 사용합니다.
     ```bash
     export PYTHONPATH=$PYTHONPATH:$(pwd)
     python -c "from backend.engine.postgres_engine import PostgresEngine; from backend.config.db import PostgresEnv; pg=PostgresEngine(PostgresEnv().dsn()); print(pg.fetch_df('SELECT * FROM <table_name> LIMIT 5'))"
     ```

## Key Databases

- **PostgreSQL**: 사용자 정보, 제출 이력, 정답지(grading 스키마)
- **DuckDB**: 대규모 이벤트 로그 (PA 분석용), `data/pa_lab.duckdb`

## Best Practices

- 쿼리 실행 전 항상 `LIMIT`을 사용하여 대량 데이터 출력을 방지하세요.
- 비즈니스 프로필(commerce, saas 등)에 따라 테이블명이 달라질 수 있으므로 먼저 목록을 확인하는 것이 좋습니다.
