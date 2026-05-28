# パフォーマンスパターン

## React最適化

### メモ化とコールバック

```tsx
// ❌ 問題: 毎回新しい配列とコールバックを生成
const ExpensiveComponent = ({ data, onUpdate }) => {
  const processedData = data.map((item) => ({
    ...item,
    processed: true,
  }));

  return (
    <div>
      {processedData.map((item) => (
        <Item key={item.id} item={item} onClick={() => onUpdate(item)} />
      ))}
    </div>
  );
};

// ✅ 改善: useMemo, useCallback, React.memo
const ExpensiveComponent = React.memo(({ data, onUpdate }) => {
  const processedData = useMemo(
    () =>
      data.map((item) => ({
        ...item,
        processed: true,
      })),
    [data]
  );

  const handleItemClick = useCallback(
    (item) => {
      onUpdate(item);
    },
    [onUpdate]
  );

  return (
    <div>
      {processedData.map((item) => (
        <Item key={item.id} item={item} onClick={handleItemClick} />
      ))}
    </div>
  );
});
```

## データベース最適化

### N+1問題

```typescript
// ❌ 問題: N+1クエリ
const users = await User.findAll();
for (const user of users) {
  user.posts = await Post.findAll({ where: { userId: user.id } });
}

// ✅ 改善: JOIN使用
const users = await User.findAll({
  include: [{ model: Post }],
  attributes: ["id", "name", "email"],
});
```

## キャッシュ実装

```typescript
// ❌ 問題: 毎回DBアクセス
const getData = async (key: string) => {
  return await fetchFromDatabase(key);
};

// ✅ 改善: キャッシュ利用
const cache = new Map();
const getData = async (key: string) => {
  if (cache.has(key)) {
    return cache.get(key);
  }

  const data = await fetchFromDatabase(key);
  cache.set(key, data);
  return data;
};
```

## 非同期処理

```typescript
// ❌ 問題: CPUブロッキング
app.get("/process", (req, res) => {
  const result = heavyComputation(req.body.data);
  res.json(result);
});

// ✅ 改善: ワーカースレッド
import { Worker } from "worker_threads";

app.get("/process", async (req, res) => {
  const worker = new Worker("./heavy-computation-worker.js");
  worker.postMessage(req.body.data);

  worker.on("message", (result) => {
    res.json(result);
    worker.terminate();
  });
});
```

## パフォーマンス測定

### バックエンド

```typescript
import { performance } from "perf_hooks";

const measurePerformance = (fn: Function, name: string) => {
  return async (...args: any[]) => {
    const start = performance.now();
    const result = await fn(...args);
    const end = performance.now();

    console.log(`${name} took ${end - start} milliseconds`);
    metrics.timing(`${name}.duration`, end - start);

    return result;
  };
};
```

### フロントエンド（Web Vitals）

```typescript
import { getCLS, getFID, getFCP, getLCP, getTTFB } from "web-vitals";

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);
```

## CI/CD統合

```yaml
# GitHub Actions
name: Performance Tests
on: [push, pull_request]

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun
      - name: Run load tests
        run: |
          npm run test:load
```
