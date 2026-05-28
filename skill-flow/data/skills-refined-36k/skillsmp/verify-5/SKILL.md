---
name: verify
description: Run backend tests and frontend build/lint checks. Use when verifying code changes, before committing, or when user says "verify", "check", "테스트", "검증해줘".
---

# Verify Project

QueryCraft 프로젝트의 전체 정합성을 검증합니다.

## Instructions

1. **통합 검증 실행**:
   - `scripts/run_task.py verify`를 호출하거나 다음 개별 명령을 수행합니다.

2. **개별 검증 단계**:
   - **Backend Tests**:
     ```bash
     export PYTHONPATH=$PYTHONPATH:$(pwd)
     pytest tests/test_grader.py tests/test_duckdb_engine.py -v
     ```
   - **Frontend Build & Lint**:
     ```bash
     cd frontend && npm run build && npm run lint
     ```

3. **결과 보고**:
   - 테스트 통과 여부 및 빌드 성공 여부를 요약하여 보고합니다.
   - 실패 시 로그에서 핵심 에러 메세지를 추출하여 해결 방안을 제안합니다.

## Best Practices

- 코드 수정 후 커밋하기 전에 반드시 이 스킬을 사용하여 사이드 이펙트를 확인하세요.
- PR을 올리기 전 최종 확인 단계로 사용합니다.
