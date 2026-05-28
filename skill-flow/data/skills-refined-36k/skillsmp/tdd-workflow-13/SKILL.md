---
name: tdd-workflow
description: >
  Anthropic Best Practices 기반 TDD 워크플로우. Red-Green-Refactor 강제.
version: 2.0.0

# 2025 Schema: 자동 트리거 조건
triggers:
  keywords:
    - "TDD"
    - "테스트 먼저"
    - "Red-Green"
    - "테스트 주도"
    - "test first"
  file_patterns:
    - "tests/**/*.py"
    - "**/*.spec.ts"
    - "**/*.test.ts"
    - "**/*.test.js"
  context:
    - "테스트 작성 요청"
    - "TDD 사이클 진행"
    - "Red Phase 시작"

# 2025 Schema: 스킬 기능 선언
capabilities:
  - validate_red_phase
  - run_tdd_cycle
  - generate_test_template
  - check_mock_usage

# 2025 Schema: 모델 선호도
model_preference: sonnet

# 기존 필드 유지
phase: [1, 2]
auto_trigger: true
dependencies:
  - debugger
token_budget: 1200
---

# TDD Workflow (Anthropic Best Practices)

Test-Driven Development 워크플로우입니다.

## Quick Start

```bash
# Red Phase 검증
python .claude/skills/tdd-workflow/scripts/validate_red_phase.py tests/test_feature.py

# TDD 자동 사이클 (최대 5회 반복)
python .claude/skills/tdd-workflow/scripts/tdd_auto_cycle.py tests/test_feature.py
```

## 핵심 규칙 (Anthropic Best Practices)

1. **NO IMPLEMENTATION BEFORE TESTS** - 테스트 먼저
2. **TESTS MUST FAIL FIRST** - Red Phase 필수
3. **NO MOCK IMPLEMENTATIONS** - 내부 함수 Mock 금지
4. **EXPLICIT TDD DECLARATION** - Claude에게 "This is TDD" 명시

## Phase Gates

### 🔴 RED Phase (테스트 실패 확인)

```bash
# 1. 테스트 파일만 작성 (구현 없음)
# 2. pytest 실행 → MUST FAIL
pytest tests/test_feature.py -v

# 3. 실패 검증
python scripts/validate_red_phase.py tests/test_feature.py

# 4. 커밋
git commit -m "test: Add feature test (RED) 🔴"
```

**Claude 프롬프트**:
```
This is TEST-DRIVEN DEVELOPMENT (RED phase).
Rules:
1. Write ONLY the test file
2. Do NOT create implementation files
3. Do NOT use mock implementations
4. Run tests and CONFIRM they fail
```

### 🟢 GREEN Phase (최소 구현)

```bash
# 1. 최소 구현
# 2. pytest 실행 → PASS
pytest tests/test_feature.py -v

# 3. 커밋
git commit -m "feat: Implement feature (GREEN) 🟢"
```

**Claude 프롬프트**:
```
This is TEST-DRIVEN DEVELOPMENT (GREEN phase).
Rules:
1. Write MINIMAL implementation to pass tests
2. Do NOT add extra features
3. Focus on making tests pass
```

### ♻️ REFACTOR Phase (개선)

```bash
# 1. 코드 개선 (테스트 변경 없음)
# 2. pytest 실행 → 여전히 PASS
pytest tests/test_feature.py -v

# 3. 커밋
git commit -m "refactor: Improve feature ♻️"
```

## Extended Thinking

| 복잡도 | Mode | 예시 |
|--------|------|------|
| 단순 CRUD | (none) | `login()` |
| 비즈니스 로직 | `think` | 결제 플로우 |
| 상태 머신 | `think hard` | 주문 상태 |
| 분산 시스템 | `ultrathink` | 캐시 일관성 |

**사용법**:
```
/tdd cache-system --ultrathink

"Ultrathink this TDD scenario:
- 3-node cluster
- Network partition handling
- Race conditions"
```

## Mock 사용 규칙

### ✅ 허용

```python
# 외부 API
@patch('requests.get')
def test_fetch(mock_get): ...

# 외부 서비스
@patch('boto3.client')
def test_upload(mock_s3): ...
```

### ❌ 금지

```python
# 내부 함수 Mock
@patch('src.auth.verify_password')  # 직접 구현 필요
def test_login(mock_verify): ...
```

### 경고 임계값

- Mock 비율 > 30% → 경고
- 내부 함수 Mock → 에러

## 자동화 스크립트

### validate_red_phase.py

```bash
python scripts/validate_red_phase.py tests/test_feature.py

# 검증:
# 1. 구현 파일 없음 확인
# 2. 테스트 실행 → MUST FAIL
# 3. 실패 원인이 예상된 에러인지 확인
```

### tdd_auto_cycle.py

```bash
python scripts/tdd_auto_cycle.py tests/test_feature.py --max-iterations 5

# 동작:
# 1. pytest 실행
# 2. 실패 분석
# 3. 자동 수정 제안
# 4. 재테스트
# 5. 5회 실패 시 → /issue-failed
```

## 테스트 템플릿

### pytest (Python)

```python
# assets/test-templates/pytest_template.py
import pytest

class TestFeature:
    def test_success_case(self):
        # Given
        input_data = {...}

        # When
        result = feature_function(input_data)

        # Then
        assert result == expected

    def test_failure_case(self):
        with pytest.raises(ValueError):
            feature_function(invalid_input)

    def test_edge_case(self):
        # Edge case handling
        pass
```

### Jest (TypeScript)

```typescript
// assets/test-templates/jest_template.ts
describe('Feature', () => {
  it('should handle success case', () => {
    // Given
    const input = {...};

    // When
    const result = featureFunction(input);

    // Then
    expect(result).toBe(expected);
  });

  it('should throw on invalid input', () => {
    expect(() => featureFunction(invalid)).toThrow();
  });
});
```

## 관련 도구

| 도구 | 용도 |
|------|------|
| `scripts/validate_red_phase.py` | Red Phase 검증 |
| `scripts/tdd_auto_cycle.py` | TDD 자동 반복 |
| `assets/test-templates/` | 테스트 템플릿 |
| `/tdd` | 기존 Command (deprecated) |

---

> 참조: [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
