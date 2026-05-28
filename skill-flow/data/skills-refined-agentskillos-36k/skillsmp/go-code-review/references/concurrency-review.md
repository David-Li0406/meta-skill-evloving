# 並行処理のレビューガイド

このドキュメントは、Goの並行処理コードをレビューする際の観点とパターンをまとめたものです。

## 目次

- [Goroutineリークの検出](#goroutineリークの検出)
- [Race Conditionの検出](#race-conditionの検出)
- [Channelの適切な使用](#channelの適切な使用)
- [Mutexとsync.Onceの使用](#mutexとsynconceの使用)
- [Contextの適切な伝播](#contextの適切な伝播)

---

## Goroutineリークの検出

### 検出パターン

**1. Goroutineの終了条件が明確でない**

```go
// ❌ 悪い例: goroutineが永遠に終了しない可能性
func process() {
    go func() {
        for {
            // 終了条件なし
            doWork()
        }
    }()
}

// ✅ 良い例: contextで終了を制御
func process(ctx context.Context) {
    go func() {
        for {
            select {
            case <-ctx.Done():
                return
            default:
                doWork()
            }
        }
    }()
}
```

**2. ブロッキングchannelからの読み取り/書き込み**

```go
// ❌ 悪い例: channelが受信されない場合、goroutineがリーク
func leak() {
    ch := make(chan int)
    go func() {
        ch <- 1  // 誰も受信しない場合、永遠にブロック
    }()
}

// ✅ 良い例: バッファ付きchannelまたはtimeout
func noLeak(ctx context.Context) {
    ch := make(chan int, 1)  // バッファ付き
    go func() {
        select {
        case ch <- 1:
        case <-ctx.Done():
            return
        }
    }()
}
```

**3. WaitGroupの不適切な使用**

```go
// ❌ 悪い例: AddとDoneのバランスが取れていない
func badWaitGroup() {
    var wg sync.WaitGroup
    for i := 0; i < 10; i++ {
        wg.Add(1)
        go func() {
            // Done()を呼び忘れる可能性
            doWork()
        }()
    }
    wg.Wait()  // 永遠に待つ可能性
}

// ✅ 良い例: deferでDoneを確実に呼ぶ
func goodWaitGroup() {
    var wg sync.WaitGroup
    for i := 0; i < 10; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            doWork()
        }()
    }
    wg.Wait()
}
```

---

## Race Conditionの検出

### 検出パターン

**1. 共有変数への並行アクセス**

```go
// ❌ 悪い例: race conditionが発生
func raceCondition() {
    counter := 0
    for i := 0; i < 10; i++ {
        go func() {
            counter++  // 複数goroutineから同時アクセス
        }()
    }
}

// ✅ 良い例: mutexで保護
func noRace() {
    var mu sync.Mutex
    counter := 0
    for i := 0; i < 10; i++ {
        go func() {
            mu.Lock()
            counter++
            mu.Unlock()
        }()
    }
}

// ✅ 別の良い例: atomic操作
func noRaceAtomic() {
    var counter int64
    for i := 0; i < 10; i++ {
        go func() {
            atomic.AddInt64(&counter, 1)
        }()
    }
}
```

**2. Mapへの並行アクセス**

```go
// ❌ 悪い例: mapへの並行書き込みでパニック
func mapRace() {
    m := make(map[string]int)
    for i := 0; i < 10; i++ {
        go func(i int) {
            m[fmt.Sprintf("key%d", i)] = i  // concurrent map writes
        }(i)
    }
}

// ✅ 良い例: sync.Mapを使用
func mapNoRace() {
    var m sync.Map
    for i := 0; i < 10; i++ {
        go func(i int) {
            m.Store(fmt.Sprintf("key%d", i), i)
        }(i)
    }
}

// ✅ 別の良い例: mutexで保護
func mapNoRaceWithMutex() {
    var mu sync.Mutex
    m := make(map[string]int)
    for i := 0; i < 10; i++ {
        go func(i int) {
            mu.Lock()
            m[fmt.Sprintf("key%d", i)] = i
            mu.Unlock()
        }(i)
    }
}
```

**3. Sliceへの並行アクセス**

```go
// ❌ 悪い例: sliceへの並行appendでデータ損失
func sliceRace() {
    var results []int
    for i := 0; i < 10; i++ {
        go func(i int) {
            results = append(results, i)  // race condition
        }(i)
    }
}

// ✅ 良い例: channelで結果を集約
func sliceNoRace() {
    resultCh := make(chan int, 10)
    for i := 0; i < 10; i++ {
        go func(i int) {
            resultCh <- i
        }(i)
    }
    results := make([]int, 0, 10)
    for i := 0; i < 10; i++ {
        results = append(results, <-resultCh)
    }
}
```

---

## Channelの適切な使用

### レビューポイント

**1. バッファサイズの適切性**

```go
// ❌ 潜在的な問題: バッファなしchannelで送信側がブロック
func unbuffered() {
    ch := make(chan int)
    for i := 0; i < 10; i++ {
        go func(i int) {
            ch <- i  // 受信側が追いつかないとブロック
        }(i)
    }
}

// ✅ 良い例: 適切なバッファサイズ
func buffered() {
    ch := make(chan int, 10)
    for i := 0; i < 10; i++ {
        go func(i int) {
            ch <- i
        }(i)
    }
}
```

**2. Channelのクローズ**

```go
// ❌ 悪い例: クローズされたchannelに送信
func badClose() {
    ch := make(chan int)
    close(ch)
    ch <- 1  // panic: send on closed channel
}

// ❌ 悪い例: 複数回クローズ
func doubleClose() {
    ch := make(chan int)
    close(ch)
    close(ch)  // panic: close of closed channel
}

// ✅ 良い例: 送信側が1つだけでクローズ
func goodClose() {
    ch := make(chan int)
    go func() {
        defer close(ch)  // 送信完了後にクローズ
        for i := 0; i < 10; i++ {
            ch <- i
        }
    }()
    for v := range ch {
        process(v)
    }
}
```

**3. Selectでのdefault使用**

```go
// ⚠️ 注意: defaultによるbusy loop
func busyLoop() {
    ch := make(chan int)
    for {
        select {
        case v := <-ch:
            process(v)
        default:
            // すぐに次のループへ → CPU使用率100%
        }
    }
}

// ✅ 良い例: ブロッキング待機
func blocking() {
    ch := make(chan int)
    for {
        select {
        case v := <-ch:
            process(v)
        case <-time.After(time.Second):
            // タイムアウト処理
        }
    }
}
```

---

## Mutexとsync.Onceの使用

### レビューポイント

**1. Mutexのロック範囲**

```go
// ❌ 悪い例: ロック範囲が広すぎる
func wideLock() {
    var mu sync.Mutex
    mu.Lock()
    defer mu.Unlock()

    doExpensiveWork()  // 重い処理
    sharedData++       // 実際に保護が必要な部分
}

// ✅ 良い例: 必要最小限のロック
func narrowLock() {
    var mu sync.Mutex

    doExpensiveWork()  // ロック外で実行

    mu.Lock()
    sharedData++       // 保護が必要な部分のみ
    mu.Unlock()
}
```

**2. RWMutexの適切な使用**

```go
// ❌ 非効率: 読み取りだけなのにMutexを使用
func readWithMutex() {
    var mu sync.Mutex
    mu.Lock()
    value := sharedData  // 読み取りのみ
    mu.Unlock()
    return value
}

// ✅ 良い例: 読み取りにはRLock
func readWithRWMutex() {
    var mu sync.RWMutex
    mu.RLock()
    value := sharedData
    mu.RUnlock()
    return value
}
```

**3. sync.Onceの使用**

```go
// ❌ 悪い例: 初期化のrace condition
var instance *Singleton

func GetInstance() *Singleton {
    if instance == nil {  // race condition
        instance = &Singleton{}
    }
    return instance
}

// ✅ 良い例: sync.Onceで安全に初期化
var (
    instance *Singleton
    once     sync.Once
)

func GetInstance() *Singleton {
    once.Do(func() {
        instance = &Singleton{}
    })
    return instance
}

// ✅ さらに良い例: sync.OnceValueを使用 (Go 1.21+)
var getInstance = sync.OnceValue(func() *Singleton {
    return &Singleton{}
})
```

---

## Contextの適切な伝播

### レビューポイント

**1. Contextの伝播**

```go
// ❌ 悪い例: contextを伝播しない
func noContextPropagation() {
    go func() {
        // 新しいcontext → 親のキャンセルが伝わらない
        result := doWork(context.Background())
    }()
}

// ✅ 良い例: contextを伝播
func withContextPropagation(ctx context.Context) {
    go func() {
        result := doWork(ctx)  // 親のcontextを使用
    }()
}
```

**2. Context.Valueの使用**

```go
// ❌ 悪い例: 必須パラメータをContextで渡す
func badContextValue(ctx context.Context) {
    userID := ctx.Value("userID").(string)  // 型アサーション失敗の可能性
    process(userID)
}

// ✅ 良い例: 必須パラメータは引数で渡す
func goodParameter(ctx context.Context, userID string) {
    process(userID)
}

// ⚠️ Contextの適切な使用: リクエストスコープのデータのみ
func appropriateContextValue(ctx context.Context) {
    // トレースIDなどのリクエストスコープデータはOK
    traceID := ctx.Value(traceIDKey).(string)
}
```

**3. Contextのキャンセル確認**

```go
// ❌ 悪い例: contextのキャンセルを確認しない
func ignoreCancel(ctx context.Context) {
    for i := 0; i < 1000000; i++ {
        doWork()  // キャンセルされても継続
    }
}

// ✅ 良い例: 定期的にキャンセルを確認
func checkCancel(ctx context.Context) error {
    for i := 0; i < 1000000; i++ {
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
        }
        doWork()
    }
    return nil
}
```

---

## テストでの検証

### race detectorの使用

```bash
# テスト実行時にrace detectorを有効化
go test -race ./...

# ビルド時にrace detectorを有効化
go build -race
```

### Goroutineリーク検出

```go
// goleak を使ったgoroutineリーク検出
import "go.uber.org/goleak"

func TestMain(m *testing.M) {
    goleak.VerifyTestMain(m)
}
```

### 静的解析ツール

- `go vet`: 基本的な問題を検出
- `staticcheck`: より高度な静的解析
- `golangci-lint`: 複数のlinterを統合
