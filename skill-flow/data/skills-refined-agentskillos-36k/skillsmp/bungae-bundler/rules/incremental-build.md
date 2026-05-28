# 증분 빌드 시스템 (Incremental Build)

Bun 네이티브 API를 활용한 증분 빌드 구현 가이드.

---

## 개요

### 왜 직접 구현하는가?

| 도구          | 증분 빌드 | 문제점                          |
| ------------- | --------- | ------------------------------- |
| Bun.build()   | ❌ 미지원 | watch 옵션 없음, 매번 전체 빌드 |
| Rolldown      | ✅ 지원   | 외부 의존성, Bun 네이티브 아님  |
| **직접 구현** | ✅ 가능   | Bun API 최대 활용, ~500줄       |

### 핵심 아이디어

```
파일 변경 → 영향받는 모듈만 찾기 → 해당 모듈만 재변환 → 번들 업데이트
```

Metro의 DeltaBundler 접근 방식을 Bun으로 포팅.

---

## 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                     IncrementalBundler                      │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ FileWatcher │→ │ DeltaCalc   │→ │ TransformCache      │  │
│  │ (fs.watch)  │  │             │  │ (Map<path, code>)   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│         │                │                    │             │
│         ↓                ↓                    ↓             │
│   변경 감지         영향 모듈 계산        변경분만 재변환             │
│                          │                    │             │
│                          ↓                    ↓             │
│                    ┌─────────────────────────────┐          │
│                    │     DependencyGraph         │          │
│                    │  (modules + inverseDeps)    │          │
│                    └─────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

## 핵심 컴포넌트

### 1. DependencyGraph (~150줄)

의존성 관계를 추적하는 그래프 구조.

```typescript
interface Module {
  path: string;
  code: string;
  dependencies: Map<string, Dependency>; // 내가 의존하는 것
  inverseDependencies: Set<string>; // 나를 의존하는 것
  hash: string; // 캐시 무효화용
}

interface Dependency {
  name: string; // import specifier
  absolutePath: string; // 실제 경로
}

class DependencyGraph {
  private modules = new Map<string, Module>();

  // 모듈 추가/업데이트
  setModule(path: string, module: Module): void;

  // 변경된 파일에 영향받는 모듈 찾기 (BFS/DFS)
  getAffectedModules(changedPath: string): Set<string>;

  // 모듈 삭제
  deleteModule(path: string): void;
}
```

**핵심: inverseDependencies**

```
A → B → C
    ↓
    D

B가 변경되면:
- B.inverseDependencies = {A}
- A도 재빌드 필요 (B를 import하므로)
```

### 2. DeltaCalculator (~150줄)

파일 변경을 감지하고 델타(변경분)를 계산.

```typescript
interface DeltaResult {
  added: Map<string, Module>;
  modified: Map<string, Module>;
  deleted: Set<string>;
}

class DeltaCalculator extends EventEmitter {
  private graph: DependencyGraph;
  private modifiedFiles = new Set<string>();
  private deletedFiles = new Set<string>();
  private addedFiles = new Set<string>();

  constructor(entryPoints: string[]) {
    this.setupWatcher();
  }

  // 파일 감시 설정
  private setupWatcher(): void {
    watch(rootDir, { recursive: true }, (event, filename) => {
      this.handleFileChange(event, filename);
      this.emit('change');
    });
  }

  // 델타 계산
  async getDelta(): Promise<DeltaResult> {
    // 1. 변경된 파일 수집
    const modified = new Set(this.modifiedFiles);
    this.modifiedFiles.clear();

    // 2. 영향받는 모듈 찾기
    const affected = new Set<string>();
    for (const path of modified) {
      this.graph.getAffectedModules(path).forEach((p) => affected.add(p));
    }

    // 3. 변경된 모듈만 재변환
    // ...
  }
}
```

### 3. TransformCache (~50줄)

변환 결과를 캐싱하여 불필요한 재변환 방지.

```typescript
class TransformCache {
  private cache = new Map<string, { hash: string; code: string }>();

  get(path: string, currentHash: string): string | null {
    const cached = this.cache.get(path);
    if (cached && cached.hash === currentHash) {
      return cached.code;
    }
    return null;
  }

  set(path: string, hash: string, code: string): void {
    this.cache.set(path, { hash, code });
  }
}
```

### 4. IncrementalBundler (~100줄)

전체를 조율하는 메인 클래스.

```typescript
class IncrementalBundler extends EventEmitter {
  private deltaCalculator: DeltaCalculator;
  private transformCache: TransformCache;
  private moduleCache = new Map<string, string>(); // path → code

  constructor(entryPoints: string[]) {
    this.deltaCalculator.on('change', async () => {
      const delta = await this.rebuild();
      this.emit('update', delta);
    });
  }

  async initialBuild(): Promise<string> {
    // 전체 빌드 후 캐시에 저장
  }

  async rebuild(): Promise<DeltaResult> {
    const delta = await this.deltaCalculator.getDelta();

    // 변경된 모듈만 캐시 업데이트
    for (const [path, module] of delta.modified) {
      this.moduleCache.set(path, module.code);
    }

    return delta;
  }

  getBundle(): string {
    // moduleCache의 모든 모듈 직렬화
  }
}
```

---

## 고급 기능 (엣지 케이스)

### 순환 참조 GC (~150줄)

Bacon-Rajan 알고리즘 기반 순환 참조 감지 및 정리.

```typescript
// 색상 기반 마킹
type NodeColor = 'black' | 'gray' | 'white' | 'purple';

class Graph {
  private colors = new Map<string, NodeColor>();
  private possibleCycleRoots = new Set<string>();

  // 순환 참조 수집
  collectCycles(): void {
    // 1. markGray: 가능한 순환 루트에서 시작해 gray로 마킹
    // 2. scan: 참조 카운트 확인, 살아있으면 black으로 복원
    // 3. collectWhite: white인 모듈 제거 (순환 참조로 인한 고아)
  }
}
```

**참고**: Metro의 `Graph.js` 700-930줄

### 롤백 시스템 (~80줄)

에러 발생 시 이전 상태로 복원.

```typescript
class DeltaCalculator {
  async getDelta(): Promise<DeltaResult> {
    // 스냅샷 저장
    const snapshot = this.graph.snapshot();

    try {
      // 변환 수행
      return await this.calculateDelta();
    } catch (error) {
      // 롤백
      this.graph.restore(snapshot);
      throw error;
    }
  }
}
```

### require.context (~80줄)

동적 require 패턴 지원.

```typescript
// 사용 예
const components = require.context('./components', true, /\.tsx$/);

// 구현
class Graph {
  private resolvedContexts = new Map<string, RequireContext>();

  markModifiedContextModules(filePath: string, modified: Set<string>): void {
    // 파일이 어떤 context에 매칭되는지 확인
    // 매칭되면 해당 context 모듈을 modified에 추가
  }
}
```

### Lazy/Async 모듈 (~80줄)

`import()`로 로드되는 모듈 별도 관리.

```typescript
class Graph {
  private importBundleNodes = new Map<
    string,
    {
      inverseDependencies: Set<string>;
    }
  >();

  // async import는 별도 번들로 분리
  // Code Splitting의 기반
}
```

---

## HMR 통합

증분 빌드 결과를 HMR로 전송.

```typescript
class DevServer {
  private bundler: IncrementalBundler;
  private clients = new Set<ServerWebSocket>();

  constructor() {
    this.bundler.on('update', (delta: DeltaResult) => {
      const message = {
        type: 'hmr:update',
        modules: [...delta.modified.entries()].map(([path, mod]) => ({
          id: path,
          code: mod.code,
        })),
      };

      for (const client of this.clients) {
        client.send(JSON.stringify(message));
      }
    });
  }
}
```

---

## 구현 순서

| 단계     | 내용                   | 예상 코드량 |
| -------- | ---------------------- | ----------- |
| 1        | DependencyGraph (기본) | ~100줄      |
| 2        | DeltaCalculator        | ~100줄      |
| 3        | TransformCache         | ~50줄       |
| 4        | IncrementalBundler     | ~100줄      |
| 5        | 순환 참조 GC           | ~150줄      |
| 6        | 롤백 시스템            | ~80줄       |
| 7        | require.context        | ~80줄       |
| 8        | Lazy 모듈              | ~80줄       |
| **총합** |                        | **~740줄**  |

MVP (1-4단계): ~350줄
전체 구현 (1-8단계): ~740줄

---

## Bun API 활용

```typescript
// 파일 감시
import { watch } from 'fs';
watch(dir, { recursive: true }, callback);

// 파일 읽기
const file = Bun.file(path);
const code = await file.text();

// 변환 + 의존성 추출
const transpiler = new Bun.Transpiler({ loader: 'tsx' });
const result = transpiler.transformSync(code);
const imports = transpiler.scanImports(code);

// 해시 생성 (캐시 키)
const hash = Bun.hash(code).toString();
```

---

## 참고 코드

- Metro DeltaBundler: `reference/metro/packages/metro/src/DeltaBundler.js`
- Metro DeltaCalculator: `reference/metro/packages/metro/src/DeltaBundler/DeltaCalculator.js`
- Metro Graph: `reference/metro/packages/metro/src/DeltaBundler/Graph.js`
- Rollipop BundlerPool: `reference/rollipop/packages/rollipop/src/server/bundler-pool.ts`

---

## Rolldown vs 직접 구현 비교

| 항목      | Rolldown                 | Bun 직접 구현             |
| --------- | ------------------------ | ------------------------- |
| 증분 빌드 | `incrementalBuild: true` | DeltaCalculator           |
| HMR       | `devMode` + 콜백         | WebSocket 직접            |
| 의존성    | @rollipop/rolldown       | 없음 (Bun 내장만)         |
| 코드량    | 설정 ~50줄               | 구현 ~740줄               |
| 장점      | 검증됨, 빠름             | Bun 네이티브, 의존성 없음 |
| 단점      | 외부 의존성              | 직접 유지보수             |

**결론**: Bun 네이티브 철학에 맞게 직접 구현. Metro 참고하면 충분히 가능.
