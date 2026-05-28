---
name: design-tests
description: |
  구현 전 테스트 케이스 설계 (TDD 준비). Use when (1) 구현 전 테스트 설계,
  (2) Acceptance Criteria 기반 테스트 케이스, (3) TDD 테스트 스켈레톤 생성.
tools: [Read, Write]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: design-tests 호출` 메시지를 첫 줄에 출력하세요.

# design-tests Skill

> 구현 전 테스트 케이스 설계 및 TDD 스켈레톤 생성

## Purpose

Epic/Task의 Acceptance Criteria를 기반으로 테스트 케이스를 설계하고, TDD 방식으로 개발할 수 있도록 테스트 스켈레톤을 생성합니다.

## Workflow

```
Epic/Task 분석
    ↓
1. Acceptance Criteria 추출
2. 테스트 시나리오 설계
3. 테스트 케이스 문서 생성
4. 테스트 스켈레톤 코드 생성
    ↓
완료
```

## Input

```yaml
spec_path: "docs/spec/epic-123/"  # Speckit 문서 경로
# 또는
task_url: "https://github.com/.../issues/456"  # Task Issue URL
```

## Output

```markdown
[SEMO] Skill: design-tests 완료

✅ 테스트 케이스 설계 완료

**생성된 파일**:
- docs/test/test-cases.md (테스트 케이스 문서)
- __tests__/feature.test.ts (테스트 스켈레톤)

| 테스트 유형 | 케이스 수 |
|------------|----------|
| Unit | 12개 |
| Integration | 5개 |
| E2E | 3개 |
```

## Test Case 문서 템플릿

```markdown
# 테스트 케이스 설계

> Epic: {epic_title}
> 작성일: {date}

## 1. 개요

### 테스트 범위

- **포함**: {included_scope}
- **제외**: {excluded_scope}

### 테스트 전략

| 유형 | 도구 | 대상 |
|------|------|------|
| Unit | Vitest | 비즈니스 로직, 유틸리티 |
| Integration | Vitest + MSW | API 연동, 서비스 계층 |
| E2E | Playwright | 사용자 시나리오 |

## 2. Acceptance Criteria → 테스트 케이스 매핑

### AC-1: {acceptance_criteria_1}

| TC ID | 테스트 케이스 | 유형 | 우선순위 |
|-------|--------------|------|----------|
| TC-1.1 | {test_case_1} | Unit | High |
| TC-1.2 | {test_case_2} | Integration | High |
| TC-1.3 | {test_case_3} | E2E | Medium |

### AC-2: {acceptance_criteria_2}

| TC ID | 테스트 케이스 | 유형 | 우선순위 |
|-------|--------------|------|----------|
| TC-2.1 | {test_case_4} | Unit | High |
| TC-2.2 | {test_case_5} | Integration | Medium |

## 3. 상세 테스트 케이스

### TC-1.1: {test_case_name}

**설명**: {description}

**사전 조건**:
- {precondition_1}
- {precondition_2}

**테스트 단계**:
1. {step_1}
2. {step_2}
3. {step_3}

**예상 결과**:
- {expected_result}

**테스트 데이터**:
```json
{
  "input": {...},
  "expected": {...}
}
```

## 4. 테스트 커버리지 목표

| 영역 | 목표 | 현재 |
|------|------|------|
| 비즈니스 로직 | 80% | 0% |
| API 계층 | 70% | 0% |
| UI 컴포넌트 | 60% | 0% |
| E2E 시나리오 | 100% | 0% |

## 5. 테스트 우선순위

### P0 (필수)
- [ ] TC-1.1: {critical_test_1}
- [ ] TC-2.1: {critical_test_2}

### P1 (중요)
- [ ] TC-1.2: {important_test_1}
- [ ] TC-1.3: {important_test_2}

### P2 (권장)
- [ ] TC-2.2: {nice_to_have_test}
```

## Test Skeleton 템플릿

### Unit Test (Vitest)

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { FeatureService } from '@/domains/feature/services/FeatureService';

describe('FeatureService', () => {
  let service: FeatureService;

  beforeEach(() => {
    service = new FeatureService();
  });

  // AC-1: {acceptance_criteria_1}
  describe('AC-1: {ac_summary}', () => {
    it('TC-1.1: {test_case_1}', () => {
      // Arrange
      const input = {};

      // Act
      const result = service.method(input);

      // Assert
      expect(result).toEqual(/* expected */);
    });

    it('TC-1.2: {test_case_2}', () => {
      // TODO: Implement
      expect.fail('Not implemented');
    });
  });

  // AC-2: {acceptance_criteria_2}
  describe('AC-2: {ac_summary}', () => {
    it('TC-2.1: {test_case_3}', () => {
      // TODO: Implement
      expect.fail('Not implemented');
    });
  });
});
```

### Integration Test (API)

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { setupServer } from 'msw/node';
import { handlers } from '@/mocks/handlers';

describe('Feature API Integration', () => {
  const server = setupServer(...handlers);

  beforeAll(() => server.listen());
  afterAll(() => server.close());

  describe('POST /api/feature', () => {
    it('TC-1.2: {integration_test_1}', async () => {
      // Arrange
      const request = {};

      // Act
      const response = await fetch('/api/feature', {
        method: 'POST',
        body: JSON.stringify(request),
      });

      // Assert
      expect(response.ok).toBe(true);
    });
  });
});
```

### E2E Test (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature E2E', () => {
  // AC-1: {acceptance_criteria_1}
  test('TC-1.3: {e2e_test_1}', async ({ page }) => {
    // Arrange
    await page.goto('/feature');

    // Act
    await page.click('[data-testid="action-button"]');

    // Assert
    await expect(page.locator('[data-testid="result"]')).toBeVisible();
  });
});
```

## 완료 메시지

```markdown
[SEMO] Skill: design-tests 완료

✅ **테스트 케이스 설계 완료**

| 항목 | 값 |
|------|-----|
| AC 수 | {ac_count}개 |
| 테스트 케이스 | {tc_count}개 |
| Unit | {unit_count}개 |
| Integration | {integration_count}개 |
| E2E | {e2e_count}개 |

**생성된 파일**:
- docs/test/test-cases.md
- __tests__/feature.test.ts
- __tests__/feature.integration.test.ts
- e2e/feature.spec.ts

다음 단계: `skill:write-code` 실행 (TDD 방식 개발)
```

## Related Skills

- `write-test` - 테스트 코드 작성
- `write-code` - 코드 작성
- `generate-spec` - 명세 생성
