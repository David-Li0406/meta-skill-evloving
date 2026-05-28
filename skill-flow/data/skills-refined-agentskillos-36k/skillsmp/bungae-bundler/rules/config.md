# Config System

## 구현 현황

### ✅ 완료된 기능 (Phase 1-1)

- [x] Config 파일 로딩 (`bungae.config.ts/js/json`, `package.json`)
- [x] Config 병합 및 기본값 처리
- [x] Config 검증 로직 (타입 및 값 검증)
- [x] Server config 추가 (port, useGlobalHotkey, forwardClientLogs 등)
- [x] Metro-compatible API (`loadConfig({ config, cwd })`)
- [x] Metro 스타일 테스트 코드 (11개 테스트 케이스 모두 통과)

### Metro 호환성

Bungae는 Metro의 config API와 호환되도록 구현되었습니다:

- ✅ `loadConfig({ config: path })` - 명시적 config 파일 경로
- ✅ `loadConfig({ cwd: dir })` - 디렉토리에서 config 검색
- ✅ Function export 지원: `module.exports = (defaultConfig) => ({ ... })`
- ✅ Promise export 지원: `module.exports = Promise.resolve({ ... })`
- ✅ Config chaining: `mergeConfig(defaults, config1, config2, ...)`

### Metro에서 제외된 기능

다음 기능들은 Metro에 있지만 Bungae에서는 구현하지 않습니다:

#### cacheStores (callback 패턴)

**제외 이유**:

- Bun은 자체 캐시 시스템을 제공
- 롤리팝도 자체 캐시 시스템을 사용하며 Metro의 `cacheStores` 패턴을 사용하지 않음
- Bun의 내장 기능을 활용하는 것이 더 효율적

#### YAML config 지원

**제외 이유**:

- Metro에서도 deprecated 상태
- 레거시 지원이 필요 없음 (새로운 프로젝트)
- JavaScript/TypeScript config만 지원해도 충분
- 롤리팝도 YAML을 지원하지 않음

# Config System

설정 파일 스키마 및 Metro 마이그레이션 가이드.

---

## 설정 파일

지원 형식 (우선순위 순):

```
bungae.config.ts   (권장)
bungae.config.js
bungae.config.json
package.json의 "bungae" 필드
```

---

## 전체 스키마

```typescript
import { defineConfig } from 'bungae';

export default defineConfig({
  // ========== 기본 ==========
  root: string;                    // 프로젝트 루트 (기본: cwd)
  entry: string;                   // 진입점 (기본: 'index.js')
  outDir: string;                  // 출력 디렉토리 (기본: 'dist')
  platform: 'ios' | 'android' | 'web';
  mode: 'development' | 'production';

  // ========== Resolver ==========
  resolver: {
    sourceExts: string[];          // ['tsx','ts','jsx','js','json']
    assetExts: string[];           // ['png','jpg','gif','webp',...]
    platforms: string[];           // ['ios','android','native']
    extraNodeModules: Record<string, string>;
    nodeModulesPaths: string[];
    blockList: RegExp[];
    resolveRequest: CustomResolver;
  };

  // ========== Transformer ==========
  transformer: {
    babel: {
      include: string[];           // glob 패턴
      plugins: string[];
      presets: string[];
    };
    minifier: 'bun' | 'terser' | 'esbuild';
    inlineRequires: boolean;
  };

  // ========== Serializer ==========
  serializer: {
    polyfills: string[];
    prelude: string[];
    bundleType: 'plain' | 'ram-indexed' | 'ram-file';
    createModuleIdFactory: () => (path: string) => number;
    processModuleFilter: (module: Module) => boolean;
  };

  // ========== Server ==========
  server: {
    port: number;                  // 기본: 8081
    host: string;                  // 기본: 'localhost'
    https: boolean | TLSConfig;
  };

  // ========== DevMode ==========
  devMode: {
    hmr: boolean | HmrConfig;
    fastRefresh: boolean;
  };

  // ========== Watcher ==========
  watcher: {
    ignore: string[];
    usePolling: boolean;
    debounce: number;
  };

  // ========== Cache ==========
  cache: {
    enabled: boolean;
    directory: string;             // node_modules/.cache/bungae
    version: string;
  };

  // ========== Plugins ==========
  plugins: Plugin[];
});
```

---

## 설정 예시

### 기본

```typescript
import { defineConfig } from 'bungae';

export default defineConfig({
  entry: 'index.js',
  platform: 'ios',
});
```

### Reanimated 사용

```typescript
import { defineConfig } from 'bungae';

export default defineConfig({
  entry: 'index.js',
  transformer: {
    babel: {
      include: ['**/node_modules/react-native-reanimated/**'],
      plugins: ['react-native-reanimated/plugin'],
    },
  },
});
```

### 모노레포

```typescript
import { defineConfig } from 'bungae';
import path from 'path';

export default defineConfig({
  entry: 'index.js',
  resolver: {
    extraNodeModules: {
      '@shared/utils': path.resolve(__dirname, '../shared/utils'),
    },
    nodeModulesPaths: [path.resolve(__dirname, '../../node_modules')],
  },
});
```

### 환경별 분기

```typescript
import { defineConfig } from 'bungae';

export default defineConfig(({ mode, platform }) => ({
  entry: 'index.js',
  platform,
  ...(mode === 'production' && {
    transformer: {
      minifier: 'bun',
      inlineRequires: true,
    },
  }),
}));
```

---

## Metro 마이그레이션

| Metro                              | Bungae                 | 비고       |
| ---------------------------------- | ---------------------- | ---------- |
| `resolver.sourceExts`              | `resolver.sourceExts`  | 동일       |
| `resolver.assetExts`               | `resolver.assetExts`   | 동일       |
| `resolver.blockList`               | `resolver.blockList`   | 동일       |
| `transformer.babelTransformerPath` | `transformer.babel`    | 구조 변경  |
| `transformer.minifierPath`         | `transformer.minifier` | 단순화     |
| `server.port`                      | `server.port`          | 동일       |
| `cacheVersion`                     | `cache.version`        | 구조 변경  |
| `resetCache`                       | CLI `--reset-cache`    | CLI로 이동 |
