# Optimization

캐싱 및 성능 최적화 구현 가이드.

---

## 캐싱 시스템

### 캐시 대상

| 대상       | 키                         | 값              |
| ---------- | -------------------------- | --------------- |
| Transform  | 파일경로 + 내용해시 + 옵션 | 변환된 코드     |
| Resolution | 모듈경로 + 컨텍스트        | 해석된 파일경로 |
| Bundle     | 엔트리 + 의존성해시        | 번들 결과       |

### 캐시 키 생성

```typescript
function createCacheKey(filePath: string, content: string): string {
  return Bun.hash(
    JSON.stringify({
      path: filePath,
      content: Bun.hash(content),
      version: config.cache.version,
      platform: config.platform,
      dev: config.mode === 'development',
    }),
  ).toString(16);
}
```

### 파일 기반 캐시

```typescript
class FileCache {
  private cacheDir: string;

  constructor(cacheDir: string) {
    this.cacheDir = cacheDir;
  }

  async get(key: string): Promise<string | null> {
    const file = Bun.file(`${this.cacheDir}/${key}`);
    if (await file.exists()) {
      return file.text();
    }
    return null;
  }

  async set(key: string, value: string): Promise<void> {
    await Bun.write(`${this.cacheDir}/${key}`, value);
  }
}
```

---

## 증분 빌드

변경된 파일만 재빌드.

### 의존성 그래프

```typescript
interface DependencyGraph {
  dependencies: Map<string, Set<string>>; // 파일 → 의존 모듈
  dependents: Map<string, Set<string>>; // 파일 → 역의존 모듈
}
```

### 변경 전파

```typescript
function getAffectedModules(changedFile: string): Set<string> {
  const affected = new Set<string>();
  const queue = [changedFile];

  while (queue.length > 0) {
    const file = queue.shift()!;
    if (affected.has(file)) continue;
    affected.add(file);

    const dependents = graph.dependents.get(file);
    if (dependents) {
      queue.push(...dependents);
    }
  }
  return affected;
}
```

---

## Minification

### Bun 내장

```typescript
const result = await Bun.build({
  entrypoints: ['./index.js'],
  minify: true,
});
```

---

## Tree-shaking

`package.json`의 `sideEffects` 필드 존중:

```json
{ "sideEffects": false }
```

---

## Inline Requires

```typescript
// 변환 전
import { heavy } from './heavy';
onClick={() => heavy()}

// 변환 후
onClick={() => require('./heavy').heavy()}
```
