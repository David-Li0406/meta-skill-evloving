---
name: database-schema-validator
description: Validates SQL schema files for compliance with internal safety and naming policies.
---

# Database Schema Validator Skill

This skill ensures that all SQL files provided by the user comply with our strict database standards.

## Policies Enforced
1. **PostgreSQL/DuckDB 구분**: 각 엔진에 맞는 예약어 및 문법을 확인합니다.
2. **Naming**: 테이블명은 `snake_case`를 사용합니다.
3. **Structure**: 정답용 테이블(grading 스키마)은 원본 데이터와 컬럼 구조가 동일해야 합니다.

## Instructions

1. **스키마 검증 유틸리티 활용**:
   `scripts/check_schema.py`를 호출하여 테이블 구조를 확인합니다.
   
   ```bash
   python scripts/check_schema.py <table_name>
   ```

2. **DuckDB 스키마 확인**:
   `sql/init_duckdb.sql` 파일을 읽어 대규모 이벤트 로그 테이블 구조를 대조합니다.

