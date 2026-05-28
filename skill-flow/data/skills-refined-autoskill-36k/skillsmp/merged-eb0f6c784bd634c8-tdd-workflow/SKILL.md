---
name: tdd-workflow
description: Use this skill to enforce a Test-Driven Development (TDD) workflow, following the Red-Green-Refactor methodology.
---

# TDD Workflow Skill

이 스킬은 TDD(Test-Driven Development) 워크플로우를 강제합니다. 이 과정은 RED-GREEN-REFACTOR의 세 단계를 포함합니다.

## 워크플로우

### 1. RED 단계 - 실패하는 테스트 먼저 작성

```bash
# Backend (pytest)
poetry run pytest apps/{app}/tests/test_{feature}.py -v

# Frontend (vitest)
pnpm test -- {feature}.test.tsx
```

**반드시 테스트가 FAIL 상태임을 확인한 후 다음 단계로 진행합니다.**

### 2. GREEN 단계 - 최소한의 구현

테스트를 통과하기 위한 최소한의 코드만 작성합니다.
- 과도한 추상화 금지
- 불필요한 기능 추가 금지
- 테스트 통과만을 목표로 함

```bash
# 테스트 실행하여 PASS 확인
poetry run pytest apps/{app}/tests/test_{feature}.py -v
```

### 3. REFACTOR 단계 - 코드 개선

테스트가 통과한 상태에서 코드를 개선합니다.
- 중복 제거
- 가독성 향상
- 성능 최적화

```bash
# 리팩토링 후에도 테스트 PASS 유지 확인
poetry run pytest apps/{app}/tests/test_{feature}.py -v
```

## 핵심 규칙

1. **NO IMPLEMENTATION BEFORE TESTS** - 테스트 먼저
2. **TESTS MUST FAIL FIRST** - Red Phase 필수
3. **NO MOCK IMPLEMENTATIONS** - 내부 함수 Mock 금지
4. **EXPLICIT TDD DECLARATION** - "This is TDD" 명시

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

### 🟢 GREEN Phase (최소 구현)

```bash
# 1. 최소 구현
# 2. pytest 실행 → PASS
pytest tests/test_feature.py -v

# 3. 커밋
git commit -m "feat: Implement feature (GREEN) 🟢"
```

### ♻️ REFACTOR Phase (개선)

```bash
# 1. 코드 개선 (테스트 변경 없음)
# 2. pytest 실행 → 여전히 PASS
pytest tests/test_feature.py -v

# 3. 커밋
git commit -m "refactor: Improve feature ♻️"
```

## 체크리스트

- [ ] 테스트 먼저 작성했는가?
- [ ] 테스트가 실패하는 것을 확인했는가?
- [ ] 최소한의 코드로 테스트를 통과시켰는가?
- [ ] 리팩토링 후에도 테스트가 통과하는가?

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

---

> 참조: [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)