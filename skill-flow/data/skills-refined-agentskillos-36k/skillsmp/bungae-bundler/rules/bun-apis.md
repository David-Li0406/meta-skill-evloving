# Bun APIs

Bungae에서 활용할 Bun API 가이드.

---

## 파일 I/O

### Bun.file()

```typescript
const file = Bun.file('path/to/file.ts');

// 읽기
const content = await file.text();
const bytes = await file.arrayBuffer();

// 메타데이터
const exists = await file.exists();
const size = file.size;
```

### Bun.write()

```typescript
await Bun.write('output.js', content);
await Bun.write('output.js', Bun.file('input.js'));
```

---

## HTTP 서버

### Bun.serve()

```typescript
const server = Bun.serve({
  port: 8081,
  hostname: 'localhost',

  fetch(req) {
    const url = new URL(req.url);
    return new Response('Hello');
  },

  websocket: {
    message(ws, message) {},
    open(ws) {},
    close(ws) {},
  },
});

// WebSocket 업그레이드
if (server.upgrade(req)) {
  return; // 업그레이드 성공
}
```

---

## 번들링

### Bun.build()

```typescript
const result = await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  target: 'browser',
  format: 'esm',
  minify: true,
  sourcemap: 'external',
  define: {
    'process.env.NODE_ENV': '"production"',
  },
});

if (!result.success) {
  console.error(result.logs);
}
```

---

## 트랜스파일러

### Bun.Transpiler

```typescript
const transpiler = new Bun.Transpiler({
  loader: 'tsx',
  target: 'browser',
  define: {
    __DEV__: 'true',
  },
});

// 동기 변환
const output = transpiler.transformSync(code);

// import 스캔
const imports = transpiler.scanImports(code);
// [{ path: './utils', kind: 'import-statement' }, ...]
```

---

## 해싱

### Bun.hash()

```typescript
const hash = Bun.hash(content); // number (64-bit)
const hashStr = hash.toString(16); // hex string

// 특정 알고리즘
const sha256 = Bun.sha(content, 'sha256');
```

---

## 워커

### Bun Worker

```typescript
const worker = new Worker('./worker.ts');

worker.postMessage({ type: 'transform', code });

worker.onmessage = (event) => {
  const result = event.data;
};
```

---

## 프로세스

### Bun.spawn()

```typescript
const proc = Bun.spawn(['node', 'script.js'], {
  cwd: '/path/to/dir',
  env: { NODE_ENV: 'production' },
  stdout: 'pipe',
});

const output = await new Response(proc.stdout).text();
await proc.exited;
```

---

## 유틸리티

```typescript
// 경로 해석
import.meta.resolve('./module');

// 현재 파일 경로
import.meta.path; // 절대 경로
import.meta.dir; // 디렉토리

// sleep
await Bun.sleep(100); // ms
```
