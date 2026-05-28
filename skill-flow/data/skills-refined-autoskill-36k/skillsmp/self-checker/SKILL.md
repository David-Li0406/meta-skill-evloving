---
name: self-checker
description: Automatically validates AI-generated code/tests and retries fixes up to 3 times on failure. Use this after code generation or when tests fail.
---

# Self Checker

## Role
AI 생성 결과물의 품질을 자동으로 검증하고 개선하는 자가 점검 전담 역할

## Goal
- 생성된 코드를 실제로 실행하여 런타임 에러 사전 발견
- 테스트 실패 시 원인 분석 후 자동 수정
- 최대 3회 재시도로 성공률 60% → 85%+ 향상

## Responsibilities

### 1. 코드 실행 검증
```bash
# Python
python -m py_compile src/**/*.py
python -m pylint src/ --errors-only

# JavaScript/TypeScript
npm run build --dry-run
tsc --noEmit

# 서버 헬스체크
timeout 10s uvicorn main:app &
sleep 3
curl -f http://localhost:8000/health
```

### 2. 테스트 실패 분석

```python
def analyze_test_failure(log_output):
    """
    테스트 실패 로그를 분석하여 원인 분류
    
    Returns:
        {
            'error_type': 'SYNTAX' | 'LOGIC' | 'API' | 'DB' | 'IMPORT',
            'file': 'src/api/users.py',
            'line': 45,
            'message': 'NameError: name "User" is not defined',
            'suggested_fix': 'Import User model: from models import User'
        }
    """
    import re
    
    patterns = {
        'SYNTAX': r'SyntaxError|IndentationError',
        'IMPORT': r'ImportError|ModuleNotFoundError|NameError',
        'LOGIC': r'AssertionError|ValueError|KeyError',
        'API': r'ConnectionError|HTTPError|TimeoutError',
        'DB': r'OperationalError|IntegrityError'
    }
    
    for error_type, pattern in patterns.items():
        if re.search(pattern, log_output):
            return {'error_type': error_type, ...}
```

### 3. 자동 수정 전략

```python
def auto_fix_loop(max_retries=3):
    for attempt in range(1, max_retries + 1):
        print(f"===== 시도 {attempt}/{max_retries} =====")
        
        result = run_tests()
        if result['success']:
            return True
        
        analysis = analyze_test_failure(result['log'])
        
        # 에러 타입별 수정
        if analysis['error_type'] == 'SYNTAX':
            fix_syntax_error(analysis)
        elif analysis['error_type'] == 'IMPORT':
            fix_import_error(analysis)
        elif analysis['error_type'] == 'LOGIC':
            call_skill('backend-developer', f"Fix {analysis['file']}")
        elif analysis['error_type'] in ['API', 'DB']:
            call_skill('architecture-designer', "Review config")
        
        time.sleep(2)
    
    generate_failure_report(result['log'])
    return False
```

### 4. 에러 유형별 처리

| 에러 타입 | 자동 수정 방법 | 호출 Skill |
|-----------|----------------|------------|
| SYNTAX | 파서 에러 기반 즉시 수정 | self-checker |
| IMPORT | 누락된 import 추가 | self-checker |
| LOGIC | 함수 로직 재작성 | backend/frontend-developer |
| API | 엔드포인트 재확인 | backend-developer |
| DB | 스키마 재확인 | architecture-designer |

## Input Requirements

- 실행할 코드 경로
- 테스트 실패 로그 (선택)
- `.agent/artifacts/architecture.md`
- `.agent/artifacts/api-spec.md`

## Output

- `.agent/artifacts/self-check-report.md`
- `.agent/artifacts/failed-issues.md` (3회 실패 시)

## Constraints

- 재시도 한도: 최대 3회
- 각 시도 토큰: 10-15K
- 총 토큰 한도: 50K
- 타임아웃: 각 테스트 최대 5분

## Tools

- `scripts/run-tests.sh`
- `scripts/analyze-error.py`
- `scripts/health-check.sh`
