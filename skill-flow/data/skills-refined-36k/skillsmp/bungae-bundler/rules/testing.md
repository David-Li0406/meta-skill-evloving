# Testing Guide

Bungae 프로젝트의 테스트 코드 작성 가이드. Metro의 테스트 구조를 참고하여 동일한 패턴을 유지합니다.

## 테스트 구조 원칙

Metro와 동일한 테스트 구조를 유지하여 일관성과 유지보수성을 확보합니다.

### 1. 파일 네이밍 규칙

**Metro 스타일**: `*-test.ts` 또는 `*.test.ts`

```
src/
├── resolver/
│   ├── index.ts
│   └── __tests__/
│       └── index-test.ts      ✅ Metro 스타일
│       └── index.test.ts       ✅ 대안 (일반적)
```

**예시**:

- `resolver-test.ts` 또는 `resolver.test.ts`
- `transformer-test.ts` 또는 `transformer.test.ts`
- `serializer-test.ts` 또는 `serializer.test.ts`

### 2. 디렉토리 구조

각 소스 모듈과 동일한 디렉토리 구조에 `__tests__` 폴더를 생성:

```
packages/bungae/src/
├── resolver/
│   ├── index.ts
│   └── __tests__/
│       └── index-test.ts
├── transformer/
│   ├── index.ts
│   └── __tests__/
│       └── index-test.ts
└── serializer/
    ├── index.ts
    └── __tests__/
        └── index-test.ts
```

**통합 테스트**: 복잡한 시나리오는 별도의 `integration_tests` 폴더에 분리

```
packages/bungae/src/
├── integration_tests/
│   └── __tests__/
│       ├── build-test.ts
│       ├── bundle-test.ts
│       └── server-test.ts
```

### 3. 테스트 코드 구조

#### 기본 패턴 (Metro 스타일)

```typescript
/**
 * Copyright (c) ...
 *
 * @format
 */

import { describe, test, expect, beforeEach } from 'bun:test';
import { functionToTest } from '../index';

describe('ModuleName', () => {
  beforeEach(() => {
    // 테스트 전 초기화
  });

  test('should work for the simple case', () => {
    const result = functionToTest('input');
    expect(result).toBe('expected');
  });

  test('should handle edge cases', async () => {
    await expect(functionToTest('invalid')).rejects.toThrow(Error);
  });
});
```

#### 복잡한 테스트 예시 (Metro 스타일)

```typescript
describe('getAsset', () => {
  beforeEach(() => {
    // 파일 시스템 초기화
    fs.reset();
    fs.mkdirSync('/root/imgs', { recursive: true });
  });

  test('should work for the simple case', () => {
    writeImages({ 'b.png': 'b image', 'b@2x.png': 'b2 image' });

    return Promise.all([
      getAssetStr('imgs/b.png', '/root', [], null, ['png']),
      getAssetStr('imgs/b@1x.png', '/root', [], null, ['png']),
    ]).then((resp) => resp.forEach((data) => expect(data).toBe('b image')));
  });

  test('should work for the simple case with platform ext', async () => {
    writeImages({
      'b.ios.png': 'b ios image',
      'b.android.png': 'b android image',
    });

    expect(
      await Promise.all([
        getAssetStr('imgs/b.png', '/root', [], 'ios', ['png']),
        getAssetStr('imgs/b.png', '/root', [], 'android', ['png']),
      ]),
    ).toEqual(['b ios image', 'b android image']);
  });
});
```

### 4. 테스트 프레임워크

**Bun 내장 테스트 프레임워크 사용**:

```typescript
import { describe, test, expect, beforeEach, afterEach } from 'bun:test';
```

**주요 API**:

- `describe(name, fn)`: 테스트 그룹
- `test(name, fn)` 또는 `it(name, fn)`: 개별 테스트
- `expect(value)`: 어설션
- `beforeEach(fn)`: 각 테스트 전 실행
- `afterEach(fn)`: 각 테스트 후 실행

### 5. Mock 사용

#### 파일 시스템 Mock

```typescript
// Metro 스타일: metro-memory-fs 사용
jest.mock('fs', () => new (require('metro-memory-fs'))());

// Bun에서는 Bun의 내장 기능 사용
import { mkdir, writeFile } from 'fs/promises';
// 또는 테스트용 메모리 파일 시스템 구현
```

#### 함수 Mock

**Bun 테스트 프레임워크는 Jest와 호환되는 API를 제공합니다.**

**Bun의 `spyOn` 사용**:

```typescript
import { spyOn } from 'bun:test';

// 객체의 메서드를 spy로 감싸기
const spy = spyOn(module, 'functionName');

// 호출 검증
expect(spy).toHaveBeenCalled();
expect(spy).toHaveBeenCalledTimes(1);
expect(spy).toHaveBeenCalledWith('arg1', 'arg2');

// 반환값 설정
spy.mockReturnValue('mocked value');
spy.mockResolvedValue(Promise.resolve('async value'));
spy.mockImplementation((arg) => `custom: ${arg}`);

// 테스트 후 복원 (자동으로 복원됨)
```

**왜 `spyOn`을 사용해야 하는가?**

1. **호출 검증**: 함수가 예상대로 호출되었는지 확인
2. **인자 검증**: 전달된 인자가 올바른지 확인
3. **호출 횟수 검증**: 함수가 몇 번 호출되었는지 확인
4. **원래 구현 유지**: 실제 함수를 대체하지 않고 감시만 함
5. **Metro와의 일관성**: Metro가 Jest를 사용하므로, Bun의 Jest 호환 API로 동일한 패턴 유지

**예시: Metro 스타일과 동일한 패턴**:

```typescript
// Metro (Jest) 스타일
const spy = jest.spyOn(module, 'functionName');
expect(spy).toHaveBeenCalled();

// Bun 스타일 (동일한 API)
import { spyOn } from 'bun:test';
const spy = spyOn(module, 'functionName');
expect(spy).toHaveBeenCalled();
```

**참고**:

- Bun의 `spyOn`은 Jest의 `jest.spyOn`과 호환되는 API를 제공합니다.
- 공식 문서: https://bun.sh/guides/test/spy-on
- Mock 관련 문서: https://bun.sh/docs/test/mocks

### 6. 테스트 카테고리

#### Unit Tests (단위 테스트)

각 모듈의 개별 함수/클래스를 테스트:

```typescript
describe('CountingSet', () => {
  test('basic add/delete', () => {
    const set = new CountingSet();
    set.add('a');
    expect(set.has('a')).toBe(true);
    expect(set.size).toBe(1);
  });
});
```

#### Integration Tests (통합 테스트)

여러 모듈이 함께 동작하는 시나리오 테스트:

```typescript
describe('build', () => {
  test('should build a complete bundle', async () => {
    const result = await build({
      entry: './src/index.js',
      platform: 'ios',
    });
    expect(result.code).toBeDefined();
    expect(result.map).toBeDefined();
  });
});
```

### 7. 테스트 실행

#### Bun 테스트 실행

```bash
# 모든 테스트 실행
mise exec -- bun test

# 특정 파일만 실행
mise exec -- bun test src/__tests__/index-test.ts

# Watch 모드
mise exec -- bun test --watch

# Coverage
mise exec -- bun test --coverage
```

### 8. Metro와의 차이점

| 항목              | Metro           | Bungae             |
| ----------------- | --------------- | ------------------ |
| 테스트 프레임워크 | Jest            | Bun 내장 테스트    |
| 파일 확장자       | `.js`           | `.ts`              |
| Mock 라이브러리   | jest.mock       | Bun spyOn          |
| 파일 시스템       | metro-memory-fs | Bun 내장 또는 구현 |

### 9. 베스트 프랙티스

1. **명확한 테스트 이름**: `should work for the simple case` 같은 구체적인 이름 사용
2. **beforeEach 활용**: 각 테스트 전 상태 초기화
3. **비동기 테스트**: `async/await` 또는 Promise 반환
4. **에러 테스트**: `expect().rejects.toThrow()` 사용
5. **Mock 최소화**: 필요한 경우에만 Mock 사용
6. **통합 테스트 분리**: 복잡한 시나리오는 `integration_tests`에 분리

### 10. 참고 자료

- Metro 테스트 예시: `reference/metro/packages/metro/src/__tests__/`
- Metro 통합 테스트: `reference/metro/packages/metro/src/integration_tests/__tests__/`
- Bun 테스트 문서: https://bun.sh/docs/cli/test
