---
name: test-writer
description: 테스트 코드 작성 시 따라야 할 규칙과 패턴을 정의합니다
license: MIT
compatibility: opencode
metadata:
  category: testing
  language: javascript
---

# 테스트 작성 가이드라인

테스트 코드를 작성할 때 다음 원칙과 패턴을 따릅니다.

## 1. 테스트 원칙

### FIRST 원칙
- **F**ast: 빠르게 실행되어야 함
- **I**ndependent: 다른 테스트에 의존하지 않음
- **R**epeatable: 어떤 환경에서도 같은 결과
- **S**elf-validating: 성공/실패가 명확
- **T**imely: 프로덕션 코드와 함께 작성

### AAA 패턴
모든 테스트는 다음 구조를 따릅니다:

```javascript
test('should do something', () => {
  // Arrange - 테스트 준비
  const input = createTestData();
  
  // Act - 실행
  const result = functionToTest(input);
  
  // Assert - 검증
  expect(result).toBe(expectedValue);
});
```

## 2. 테스트 명명 규칙

### 형식
```
should [expected behavior] when [condition]
```

### 예시
```javascript
// Good
'should return user when valid id is provided'
'should throw error when email is invalid'
'should return empty array when no items exist'

// Bad
'test1'
'user test'
'it works'
```

## 3. 테스트 종류별 가이드

### 단위 테스트 (Unit Test)
- 하나의 함수/메서드만 테스트
- 외부 의존성은 모킹
- 빠른 실행 속도

```javascript
describe('UserService', () => {
  describe('createUser', () => {
    test('should create user with valid data', () => {
      // ...
    });
    
    test('should throw error when email is invalid', () => {
      // ...
    });
  });
});
```

### 통합 테스트 (Integration Test)
- 여러 컴포넌트 간 상호작용 테스트
- 실제 의존성 사용 (DB, API 등)
- 단위 테스트보다 느림

### E2E 테스트
- 사용자 시나리오 전체 테스트
- 실제 환경과 유사하게 설정
- 가장 느리지만 신뢰도 높음

## 4. 모킹 가이드

### 언제 모킹하는가?
- 외부 API 호출
- 데이터베이스 접근
- 시간 의존적 코드
- 랜덤 값

### 모킹 예시
```javascript
// 함수 모킹
jest.mock('./api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: 1, name: 'Test' })
}));

// 시간 모킹
jest.useFakeTimers();
jest.setSystemTime(new Date('2024-01-01'));
```

## 5. 테스트 커버리지

### 목표 커버리지
- 라인 커버리지: 80% 이상
- 브랜치 커버리지: 70% 이상
- 핵심 비즈니스 로직: 90% 이상

### 커버리지보다 중요한 것
- 의미 있는 테스트인가?
- 실제 버그를 잡을 수 있는가?
- 유지보수가 용이한가?

## 6. 테스트 안티패턴

### 피해야 할 것들
- ❌ 구현 세부사항 테스트
- ❌ 하나의 테스트에서 여러 기능 검증
- ❌ 테스트 간 의존성
- ❌ 매직 넘버/스트링
- ❌ 불안정한 테스트 (가끔 실패)

### 좋은 테스트
- ✅ 동작(behavior) 테스트
- ✅ 하나의 테스트, 하나의 개념
- ✅ 독립적으로 실행 가능
- ✅ 의미 있는 변수명과 상수
- ✅ 항상 같은 결과

## 7. 테스트 파일 구조

```
src/
├── userService.js
└── __tests__/
    └── userService.test.js

# 또는

src/
├── userService.js
└── userService.test.js
```

## 8. 테스트 작성 순서

1. 가장 간단한 성공 케이스
2. 엣지 케이스들
3. 에러 케이스들
4. 경계값 테스트
