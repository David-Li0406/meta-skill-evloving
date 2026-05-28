# Bundling Process

3단계 번들링 파이프라인 구현 가이드.

```
Entry File → [Resolution] → [Transformation] → [Serialization] → Bundle
```

---

## 1. Resolution (모듈 해석)

모듈 import/require 경로를 실제 파일 경로로 해석.

### Bun의 Resolution 현황

**내장 기능**:

- `Bun.build()`가 내부적으로 모듈 해석 수행
- Node.js 표준 모듈 해석 알고리즘 지원
- `package.json`의 `exports`, `main`, `module` 필드 지원
- `node_modules` 계층적 탐색 지원

**한계**:

- React Native 플랫폼 확장자 (`.ios.js`, `.android.js`, `.native.js`) **미지원**
- GitHub Issue #21380에서 요청 중이지만 아직 구현 안 됨

**해결 방법**: Bun Plugin으로 플랫폼 확장자 처리 추가

### 구현 전략

**✅ Bun.build() 기본 해석 활용 + Plugin으로 플랫폼 확장자 처리**

```typescript
import type { BunPlugin } from 'bun';

const platformResolverPlugin: BunPlugin = {
  name: 'bungae-platform-resolver',
  setup(build) {
    const platform = build.config.platform || 'ios';
    const sourceExts = ['.tsx', '.ts', '.jsx', '.js'];

    build.onResolve({ filter: /.*/ }, (args) => {
      // 플랫폼별 확장자 시도
      const platformExts = [
        `.${platform}.tsx`,
        `.${platform}.ts`,
        `.${platform}.jsx`,
        `.${platform}.js`,
        '.native.tsx',
        '.native.ts',
        '.native.jsx',
        '.native.js',
      ];

      // 기본 확장자
      const defaultExts = sourceExts;

      // 시도 순서: platform → native → default
      for (const ext of [...platformExts, ...defaultExts]) {
        const candidate = args.path + ext;
        if (await Bun.file(candidate).exists()) {
          return { path: candidate };
        }
      }

      // Bun의 기본 해석에 위임
      return undefined;
    });
  },
};

await Bun.build({
  entrypoints: ['./index.ts'],
  plugins: [platformResolverPlugin],
  // Bun이 나머지 해석을 자동으로 처리
});
```

### 지원 기능

| 기능               | Bun 내장 | Bungae 추가 |
| ------------------ | -------- | ----------- |
| 상대 경로          | ✅       | -           |
| npm 패키지         | ✅       | -           |
| 스코프 패키지      | ✅       | -           |
| 플랫폼별 확장자    | ❌       | ✅ Plugin   |
| Package exports    | ✅       | -           |
| react-native field | ❌       | ✅ Plugin   |

### 해석 우선순위

```typescript
// platform: 'ios' 일 때
const extensions = [
  '.ios.tsx',
  '.ios.ts',
  '.ios.jsx',
  '.ios.js', // 플랫폼 특정
  '.native.tsx',
  '.native.ts',
  '.native.jsx',
  '.native.js', // 네이티브 공통
  '.tsx',
  '.ts',
  '.jsx',
  '.js', // 기본
  '.json',
];
```

### 참고 코드

- Bun Plugin API: https://bun.sh/docs/bundler/plugins
- Metro Resolver: `reference/metro/packages/metro-resolver/src/resolve.js`
- GitHub Issue: https://github.com/oven-sh/bun/issues/21380

---

## 2. Transformation (코드 변환)

소스 코드를 RN 런타임이 실행 가능한 형태로 변환.

### 기본: Bun 내장 트랜스파일러

```typescript
const transpiler = new Bun.Transpiler({
  loader: 'tsx',
  target: 'browser',
});

const output = transpiler.transformSync(sourceCode);
```

### Babel 선택적 통합

`rules/transformer.md` 참조.

### 참고 코드

- `reference/metro/packages/metro-transform-worker/`

---

## 3. Serialization (번들 직렬화)

변환된 모듈들을 하나의 번들 파일로 합침.

### 번들 형식

| 형식                 | 용도    | 특징                       |
| -------------------- | ------- | -------------------------- |
| Plain Bundle         | 기본    | 모든 모듈을 하나의 JS 파일 |
| RAM Bundle (Indexed) | iOS     | 바이너리 형식, 빠른 로딩   |
| RAM Bundle (File)    | Android | 모듈별 파일 분리           |

### Plain Bundle 구조

```javascript
// 1. Polyfills
(function () {
  /* polyfill */
})();

// 2. Module definitions
__d(
  function (require, module, exports) {
    // module 0
  },
  0,
  [1, 2],
);

__d(
  function (require, module, exports) {
    // module 1
  },
  1,
  [],
);

// 3. Entry execution
__r(0);
```

### 런타임 함수

```typescript
// __d: define module
function __d(factory, moduleId, dependencyIds) { ... }

// __r: require module (entry point)
function __r(moduleId) { ... }
```

### 참고 코드

- `reference/metro/packages/metro/src/DeltaBundler/Serializers/`
