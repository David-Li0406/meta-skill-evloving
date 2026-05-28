# Transformer

코드 변환 전략 및 Babel 선택적 통합 가이드.

---

## Metro 호환 변환 순서

Metro의 변환 파이프라인을 따르되, 각 도구가 가장 잘하는 작업을 담당:

```
1. Hermes Parser Plugin - Flow + JSX 파싱 (Babel only)
2. Flow Enum Transform   - Flow enum 처리 (Babel only)
3. Flow Type Stripping   - Flow 타입 제거 (Babel only)
4. ESM → CJS Conversion  - 모듈 변환 (SWC - fast)
5. JSX Transformation    - JSX 변환 (SWC - fast)
```

### 현재 구현

```typescript
// Step 1-3: Babel + Hermes (Flow 처리 - Babel만 가능)
async function stripFlowTypesWithBabel(code: string, filePath?: string): Promise<string> {
  const babel = await import('@babel/core');
  const hermesParserPlugin = await import('babel-plugin-syntax-hermes-parser');
  const flowPlugin = await import('@babel/plugin-transform-flow-strip-types');

  const result = await babel.transformAsync(code, {
    filename: filePath || 'file.js',
    plugins: [[hermesParserPlugin.default, { parseLangTypes: 'flow' }], [flowPlugin.default]],
    babelrc: false,
    configFile: false,
  });
  return result?.code || code;
}

// Step 4: SWC (ESM → CJS - 빠름)
async function convertEsmToCjsWithSwc(code: string, filePath: string): Promise<string> {
  const swc = await import('@swc/core');
  const result = await swc.transform(code, {
    module: { type: 'commonjs' },
    // ...
  });
  return result.code;
}

// Step 5: SWC (JSX 변환 - 빠름)
async function transformJsxWithSwc(code: string, filePath: string): Promise<string> {
  const swc = await import('@swc/core');
  const result = await swc.transform(code, {
    filename: filePath,
    jsc: {
      parser: {
        syntax: 'typescript',
        tsx: true,
      },
      transform: {
        react: {
          runtime: 'automatic',
        },
      },
    },
  });
  return result.code;
}
```

### 도구별 역할

| 단계 | 도구           | 역할                | 이유                                |
| ---- | -------------- | ------------------- | ----------------------------------- |
| 1-3  | Babel + Hermes | Flow 파싱/타입 제거 | Hermes parser만 Flow 구문 처리 가능 |
| 4    | SWC            | ESM → CJS 변환      | Babel보다 빠름                      |
| 5    | SWC            | JSX 변환            | 빠른 JSX 변환                       |

---

## 점진적 Babel 제거 계획

현재 Flow 처리를 위해 Babel을 사용하지만, 장기적으로 Babel 의존성을 최소화할 계획:

### Phase 1 (현재): Flow 파일용 Babel

- React Native 코어 및 라이브러리의 Flow 코드 처리
- `babel-plugin-syntax-hermes-parser` + `@babel/plugin-transform-flow-strip-types`
- SWC로 나머지 변환

### Phase 2: Hermes Parser 직접 통합

- **목표**: Babel 없이 Hermes Parser를 직접 사용하여 Flow 타입 제거
- **방법**: Hermes Parser AST를 직접 조작하여 Flow 타입 제거 구현
- **참고**: https://github.com/facebook/hermes/tree/main/lib/Parser
- **장점**:
  - Babel 의존성 제거 가능
  - 더 빠른 파싱 성능 (Hermes는 C++ 기반)
  - React Native의 공식 파서 사용으로 호환성 향상
- **구현 계획**:
  1. Hermes Parser로 Flow 코드 파싱 (이미 `hermes-parser` npm 패키지 사용 중)
  2. AST를 순회하며 Flow 타입 어노테이션 제거
  3. Flow enum을 런타임 호출로 변환
  4. 깨끗한 JavaScript 코드 생성

### Phase 3: SWC Flow 지원 대기 (대안)

- SWC가 Flow 파싱을 지원하면 Babel 제거 가능
- 현재 SWC는 TypeScript만 지원
- 관련 이슈: SWC Flow 지원 상태 확인 필요
- **참고**: Phase 2 (Hermes Parser 직접 통합)가 우선순위가 더 높음

### Phase 4: 완전한 Babel 제거

- Flow 지원이 추가되면 전체 파이프라인을 SWC로 통합
- Babel은 특수 플러그인 필요 시에만 사용 (reanimated, styled-components 등)

### 현재 Babel이 필수인 경우

| 기능            | 이유                 | 대안               |
| --------------- | -------------------- | ------------------ |
| Flow 타입       | Hermes parser만 가능 | SWC Flow 지원 대기 |
| `import typeof` | Flow 전용 구문       | SWC Flow 지원 대기 |
| Flow enum       | Babel 플러그인 필요  | SWC Flow 지원 대기 |

---

## 기본 전략: Bun 트랜스파일러

Bun은 Zig로 작성된 네이티브 트랜스파일러를 내장.
Babel/SWC보다 훨씬 빠름.

### 지원 변환

- TypeScript → JavaScript
- TSX/JSX → JavaScript
- ES Modules 구문 처리

### 사용법

```typescript
const transpiler = new Bun.Transpiler({
  loader: 'tsx',
  target: 'browser',
  define: {
    'process.env.NODE_ENV': JSON.stringify('development'),
    __DEV__: 'true',
  },
});

const output = transpiler.transformSync(sourceCode);
```

---

## Babel 선택적 통합

특수 플러그인이 필요한 경우만 Babel 사용.

### 설정

```typescript
transformer: {
  // 기본: Bun
  default: 'bun',

  // Babel 필요한 패키지만 지정
  babel: {
    include: [
      '**/node_modules/react-native-reanimated/**',
      '**/node_modules/react-native-gesture-handler/**',
    ],
    plugins: [
      'react-native-reanimated/plugin',
    ],
    presets: [
      // 필요 시 추가
    ],
  },
}
```

---

## Babel이 필요한 케이스

### 1. react-native-reanimated

**이유**: `'worklet'` 디렉티브가 있는 함수를 UI 스레드용 코드로 분리

```javascript
// 변환 전
function MyComponent() {
  const style = useAnimatedStyle(() => {
    'worklet';
    return { opacity: sv.value };
  });
}

// 변환 후 (worklet 추출)
function MyComponent() {
  const style = useAnimatedStyle(_worklet_factory_1);
}
// _worklet_factory_1은 UI 스레드에서 실행
```

**플러그인**: `react-native-reanimated/plugin`

### 2. styled-components / Emotion

**이유**: 디버깅용 displayName, componentId 주입

```javascript
// 변환 전
const Button = styled.View`...`;

// 변환 후
const Button = styled.View.withConfig({
  displayName: 'Button',
  componentId: 'sc-abc123',
})`...`;
```

**플러그인**: `babel-plugin-styled-components`

### 3. Decorator 문법

**이유**: TypeScript/JavaScript 데코레이터 변환

```typescript
// MobX 등
@observable
class Store {
  @action doSomething() {}
}
```

**플러그인**: `@babel/plugin-proposal-decorators`

### 4. Flow 코드

**이유**: Bun은 Flow 타입을 지원하지 않음

```javascript
// @flow
function add(a: number, b: number): number {
  return a + b;
}
```

**프리셋**: `@babel/preset-flow`

---

## 구현 전략

```typescript
async function transform(filePath: string, code: string): Promise<string> {
  // 1. Babel 필요 여부 확인
  if (shouldUseBabel(filePath)) {
    return babelTransform(code, getBabelConfig(filePath));
  }

  // 2. 기본: Bun 트랜스파일러
  const transpiler = new Bun.Transpiler({ loader: getLoader(filePath) });
  return transpiler.transformSync(code);
}

function shouldUseBabel(filePath: string): boolean {
  const { include } = config.transformer.babel;
  return include.some((pattern) => minimatch(filePath, pattern));
}
```

---

## 성능 비교

| 트랜스파일러 | 상대 속도    | 사용 시점               |
| ------------ | ------------ | ----------------------- |
| Bun 내장     | 1x (기준)    | 대부분의 파일           |
| SWC          | ~2-3x 느림   | -                       |
| Babel        | ~10-20x 느림 | 특수 플러그인 필요 시만 |

**원칙**: Babel은 정말 필요한 파일에만 사용
