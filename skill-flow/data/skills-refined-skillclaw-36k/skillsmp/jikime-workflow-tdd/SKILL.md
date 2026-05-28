---
name: jikime-workflow-tdd
description: Test-Driven Development workflow for new feature development. RED-GREEN-REFACTOR cycle for building new functionality with test-first approach.
version: 1.0.0
tags: ["workflow", "tdd", "testing", "red-green-refactor", "test-first"]
triggers:
  keywords: ["TDD", "test-driven", "RED-GREEN", "test first", "테스트 주도"]
  phases: ["run"]
  agents: ["test-guide"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2000
user-invocable: false
context: fork
agent: test-guide
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
---

# JikiME TDD Workflow Skill

Test-Driven Development workflow for new feature development.

## Overview

TDD(Test-Driven Development) 방법론을 사용한 새로운 기능 개발 워크플로우입니다.
테스트를 먼저 작성하고, 테스트를 통과하는 최소한의 코드를 구현합니다.

## Core Cycle

```
RED → GREEN → REFACTOR
```

### 1. RED (실패하는 테스트 작성)
- 기능 요구사항을 테스트로 표현
- 테스트 실행 → 반드시 실패해야 함
- 실패 메시지가 명확해야 함

### 2. GREEN (테스트 통과)
- 테스트를 통과하는 **최소한의** 코드 작성
- 완벽한 코드 X, 동작하는 코드 O
- 하드코딩도 OK (일단 통과가 목표)

### 3. REFACTOR (리팩토링)
- 테스트가 통과하는 상태 유지
- 코드 품질 개선
- 중복 제거, 가독성 향상

## TDD Principles

### Three Laws of TDD
1. 실패하는 테스트 없이 프로덕션 코드를 작성하지 않는다
2. 실패하기에 충분한 만큼만 테스트를 작성한다
3. 테스트를 통과하기에 충분한 만큼만 프로덕션 코드를 작성한다

### FIRST Principles
- **F**ast: 테스트는 빨라야 한다
- **I**ndependent: 테스트는 서로 독립적이어야 한다
- **R**epeatable: 어떤 환경에서도 반복 가능해야 한다
- **S**elf-validating: 테스트는 스스로 성공/실패를 판단해야 한다
- **T**imely: 테스트는 프로덕션 코드 직전에 작성해야 한다

## Test Structure

### AAA Pattern
```typescript
describe('OrderService', () => {
  it('should calculate total with discount', () => {
    // Arrange: 테스트 데이터 준비
    const order = new Order([
      { product: 'A', price: 100 },
      { product: 'B', price: 200 }
    ]);
    const discount = 0.1; // 10%

    // Act: 테스트 대상 실행
    const total = orderService.calculateTotal(order, discount);

    // Assert: 결과 검증
    expect(total).toBe(270);
  });
});
```

### Given-When-Then (BDD Style)
```typescript
describe('User Registration', () => {
  describe('given valid user data', () => {
    const validUser = { email: 'test@example.com', password: 'secure123' };

    describe('when registering', () => {
      it('then creates user account', async () => {
        const result = await userService.register(validUser);
        expect(result.success).toBe(true);
      });
    });
  });
});
```

## Test Types & Coverage

### Testing Pyramid
```
        /  E2E  \        ← 적게 (10%)
       /  통합   \       ← 중간 (20%)
      /   단위    \      ← 많이 (70%)
```

### Coverage Targets
| Type | Target | Focus |
|------|--------|-------|
| Unit Tests | 80%+ | Business Logic |
| Integration Tests | 70%+ | API, DB |
| E2E Tests | Critical Paths | User Flows |

## Test Doubles

### Types
```typescript
// Dummy: 사용되지 않는 인자
const dummyLogger = {} as Logger;

// Stub: 미리 정의된 응답 반환
const stubUserRepo = {
  findById: () => ({ id: 1, name: 'Test User' })
};

// Mock: 호출 검증
const mockEmailService = {
  send: jest.fn()
};
expect(mockEmailService.send).toHaveBeenCalledWith(expectedEmail);

// Fake: 단순화된 실제 구현
class FakeUserRepository implements UserRepository {
  private users = new Map<number, User>();
  async save(user: User) { this.users.set(user.id, user); }
  async findById(id: number) { return this.users.get(id); }
}

// Spy: 실제 객체의 일부 메서드만 감시
jest.spyOn(realService, 'processPayment');
```

## Example TDD Session

### Feature: Add item to cart

```typescript
// Step 1: RED - 실패하는 테스트
describe('ShoppingCart', () => {
  it('should add item to empty cart', () => {
    const cart = new ShoppingCart();
    cart.addItem({ id: 1, name: 'Product A', price: 100 });
    expect(cart.items).toHaveLength(1);
  });
});
// ❌ FAIL: ShoppingCart is not defined

// Step 2: GREEN - 최소한의 구현
class ShoppingCart {
  items: Item[] = [];
  addItem(item: Item) {
    this.items.push(item);
  }
}
// ✅ PASS

// Step 3: REFACTOR - 개선
class ShoppingCart {
  private _items: Item[] = [];

  get items(): readonly Item[] {
    return [...this._items]; // 불변성 보장
  }

  addItem(item: Item): void {
    this.validateItem(item);
    this._items.push(item);
  }

  private validateItem(item: Item): void {
    if (item.price < 0) throw new Error('Invalid price');
  }
}
// ✅ PASS (리팩토링 후에도 테스트 통과)
```

## Integration with Commands

| Command | TDD Usage |
|---------|-----------|
| `/jikime:test --tdd` | TDD 모드로 테스트 실행 |
| `/jikime:test --coverage` | 커버리지 리포트 |
| `/jikime:test --watch` | 워치 모드 |

## DDD vs TDD 사용 시점

| Scenario | Use |
|----------|-----|
| 레거시 코드 마이그레이션 | DDD |
| 기존 코드 리팩토링 | DDD |
| 새로운 기능 개발 | TDD |
| 버그 수정 | TDD (regression test) |
| API 추가 | TDD |

## Best Practices

1. **작은 단계로**: 한 번에 하나의 테스트만
2. **의도 표현**: 테스트 이름에 의도를 명확히
3. **빠른 피드백**: 테스트 실행 시간 최소화
4. **격리된 테스트**: 테스트 간 의존성 제거
5. **실패 먼저**: 테스트가 실패하는 것 확인 후 구현
6. **리팩토링 시간 확보**: GREEN 후 REFACTOR 단계 생략 금지
