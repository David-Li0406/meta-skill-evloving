# Resolution (모듈 해석)

Bungae의 모듈 해석 구현 전략. Bun의 내장 기능을 최대한 활용하고, React Native 특화 기능만 추가합니다.

## Bun의 Resolution 현황

### 내장 기능

Bun은 이미 강력한 모듈 해석 기능을 제공합니다:

```typescript
// Bun.build()가 내부적으로 모듈 해석 수행
await Bun.build({
  entrypoints: ['./index.ts'],
  // Bun이 자동으로 다음을 처리:
  // - 상대 경로 해석
  // - node_modules 탐색
  // - package.json의 exports/main/module 필드
  // - TypeScript/JSX 확장자 자동 탐색
});
```

**지원되는 기능**:

- ✅ Node.js 표준 모듈 해석 알고리즘
- ✅ `package.json`의 `exports`, `main`, `module` 필드
- ✅ `node_modules` 계층적 탐색
- ✅ 상대 경로 (`./`, `../`)
- ✅ 스코프 패키지 (`@scope/package`)
- ✅ TypeScript/JSX 확장자 자동 탐색 (`.ts`, `.tsx`, `.js`, `.jsx`)

### 한계

**React Native 플랫폼 확장자 미지원**:

- ❌ `.ios.js`, `.android.js`, `.native.js` 확장자 인식 안 됨
- GitHub Issue: https://github.com/oven-sh/bun/issues/21380
- 아직 구현되지 않음

### import.meta.resolve() 제한

```typescript
// ⚠️ 런타임 전용 - 번들링 시점에 동작 안 함
const resolved = await import.meta.resolve('./module');
// 번들링 시점에는 사용할 수 없음
```

## 해결 방법: Bun Plugin

Bun의 Plugin 시스템을 활용하여 플랫폼 확장자만 추가 처리합니다.

### Platform Resolver Plugin 구현

```typescript
import type { BunPlugin } from 'bun';
import { existsSync } from 'fs';

interface PlatformResolverOptions {
  platform: 'ios' | 'android' | 'web';
  sourceExts: string[];
  preferNativePlatform?: boolean;
}

export function createPlatformResolverPlugin(options: PlatformResolverOptions): BunPlugin {
  const { platform, sourceExts, preferNativePlatform = true } = options;

  return {
    name: 'bungae-platform-resolver',
    setup(build) {
      build.onResolve({ filter: /.*/ }, async (args) => {
        // 이미 절대 경로이거나 확장자가 있으면 Bun의 기본 해석에 위임
        if (args.path.startsWith('/') || args.path.includes('.')) {
          return undefined; // Bun의 기본 해석 사용
        }

        const basePath = args.path;
        const importerDir = args.importer
          ? args.importer.substring(0, args.importer.lastIndexOf('/'))
          : process.cwd();

        // 플랫폼별 확장자 우선순위
        const platformExts = [
          ...sourceExts.map((ext) => `.${platform}${ext}`),
          ...(preferNativePlatform ? sourceExts.map((ext) => `.native${ext}`) : []),
          ...sourceExts,
        ];

        // 각 확장자를 순서대로 시도
        for (const ext of platformExts) {
          const candidate = `${importerDir}/${basePath}${ext}`;
          if (existsSync(candidate)) {
            return { path: candidate };
          }
        }

        // Bun의 기본 해석에 위임
        return undefined;
      });
    },
  };
}
```

### 사용 예시

```typescript
import { createPlatformResolverPlugin } from './plugins/platform-resolver';

const result = await Bun.build({
  entrypoints: ['./src/index.ts'],
  plugins: [
    createPlatformResolverPlugin({
      platform: 'ios',
      sourceExts: ['.tsx', '.ts', '.jsx', '.js'],
      preferNativePlatform: true,
    }),
  ],
  // Bun이 나머지 해석을 자동으로 처리
});
```

## 해석 우선순위

### 플랫폼: `ios`일 때

```typescript
// 1. 플랫폼 특정 확장자
('.ios.tsx', '.ios.ts', '.ios.jsx', '.ios.js');

// 2. 네이티브 공통 확장자 (preferNativePlatform: true일 때)
('.native.tsx', '.native.ts', '.native.jsx', '.native.js');

// 3. 기본 확장자
('.tsx', '.ts', '.jsx', '.js');

// 4. JSON
('.json');
```

### 예시

```typescript
// import './Button' 일 때 (platform: 'ios')
// 시도 순서:
1. './Button.ios.tsx' ✅ 찾으면 이것 사용
2. './Button.ios.ts'
3. './Button.native.tsx'
4. './Button.native.ts'
5. './Button.tsx' ✅ 없으면 이것 사용
6. './Button.ts'
7. './Button.jsx'
8. './Button.js'
```

## 구현 전략 요약

### ✅ 권장 접근 방식

1. **Bun.build() 기본 해석 활용**
   - Node.js 표준 해석은 Bun이 자동 처리
   - Package Exports, node_modules 탐색 등 모두 자동

2. **Platform Resolver Plugin 추가**
   - 플랫폼 확장자만 Plugin으로 처리
   - 최소한의 코드로 React Native 지원

3. **완전히 새로 구현하지 않음**
   - Metro처럼 처음부터 구현할 필요 없음
   - Bun의 성능 이점 그대로 활용

### ❌ 피해야 할 접근

```typescript
// ❌ 나쁜 예: 모든 해석을 직접 구현
function customResolve(specifier: string, from: string) {
  // node_modules 탐색 직접 구현
  // package.json 파싱 직접 구현
  // ... (불필요한 중복 작업)
}

// ✅ 좋은 예: Bun의 해석 활용 + Plugin으로 확장
await Bun.build({
  plugins: [platformResolverPlugin], // 플랫폼 확장자만 추가
  // 나머지는 Bun이 처리
});
```

## Metro와의 차이점

| 항목              | Metro     | Bungae               |
| ----------------- | --------- | -------------------- |
| 기본 해석         | 직접 구현 | Bun.build() 활용     |
| 플랫폼 확장자     | 직접 구현 | Plugin으로 추가      |
| Package Exports   | 직접 구현 | Bun 내장             |
| node_modules 탐색 | 직접 구현 | Bun 내장             |
| 구현 복잡도       | 높음      | 낮음 (Plugin만 추가) |

## 참고 자료

- Bun Plugin API: https://bun.sh/docs/bundler/plugins
- Bun.build() 문서: https://bun.sh/docs/bundler
- Metro Resolver: `reference/metro/packages/metro-resolver/src/resolve.js`
- GitHub Issue: https://github.com/oven-sh/bun/issues/21380
