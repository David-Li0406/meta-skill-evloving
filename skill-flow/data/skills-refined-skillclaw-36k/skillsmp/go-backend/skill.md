---
name: go-backend
description: Goバックエンド開発 - Goイディオム、並行処理、エラーハンドリング、テスト
requires-guidelines:
  - golang
  - common
---

# Goバックエンド開発

## 使用タイミング

- **Go バックエンド実装時**
- **Go コードレビュー時**
- **並行処理・パフォーマンス最適化時**

## 開発観点

### 🔴 Critical（修正必須）

#### 1. エラーハンドリング違反
```go
// ❌ 危険: エラー無視
result, _ := userRepo.Find(id)

// ❌ 危険: panic乱用
if err != nil {
    panic(err)  // サーバークラッシュの原因
}

// ✅ 正しい: エラー適切処理
result, err := userRepo.Find(id)
if err != nil {
    return fmt.Errorf("failed to find user: %w", err)
}
```

#### 2. goroutine リーク
```go
// ❌ 危険: 終了しないgoroutine
func process() {
    ch := make(chan int)
    go func() {
        for v := range ch {  // chがクローズされない
            fmt.Println(v)
        }
    }()
}

// ✅ 正しい: context でキャンセル制御
func process(ctx context.Context) {
    ch := make(chan int)
    go func() {
        defer close(ch)
        for {
            select {
            case <-ctx.Done():
                return
            case v := <-ch:
                fmt.Println(v)
            }
        }
    }()
}
```

#### 3. インターフェース濫用
```go
// ❌ 危険: 不要なインターフェース
type UserRepositoryInterface interface {
    Find(int) (*User, error)
    Save(*User) error
}

// ✅ 正しい: 必要な場所でのみ定義（Accept interfaces）
// domain/repository.go
type UserRepository interface {
    Find(int) (*User, error)
}

// infrastructure/user_repository.go
type userRepositoryImpl struct { ... }
func (r *userRepositoryImpl) Find(id int) (*User, error) { ... }
```

### 🟡 Warning（要改善）

#### 1. context 不使用
```go
// ⚠️ タイムアウト制御がない
func FetchData(url string) ([]byte, error) {
    resp, err := http.Get(url)
    ...
}

// ✅ context でタイムアウト制御
func FetchData(ctx context.Context, url string) ([]byte, error) {
    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
    resp, err := http.DefaultClient.Do(req)
    ...
}
```

#### 2. sync.Mutex の defer 忘れ
```go
// ⚠️ Unlock 忘れのリスク
mu.Lock()
if err := process(); err != nil {
    return err  // Unlock されない
}
mu.Unlock()

// ✅ defer で確実に Unlock
mu.Lock()
defer mu.Unlock()
if err := process(); err != nil {
    return err
}
```

#### 3. テーブル駆動テスト未使用
```go
// ⚠️ 同じテストコードの繰り返し
func TestAdd(t *testing.T) {
    if Add(1, 2) != 3 { t.Error("failed") }
    if Add(0, 0) != 0 { t.Error("failed") }
}

// ✅ テーブル駆動
func TestAdd(t *testing.T) {
    tests := []struct {
        name string
        a, b int
        want int
    }{
        {"positive", 1, 2, 3},
        {"zero", 0, 0, 0},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Add(tt.a, tt.b); got != tt.want {
                t.Errorf("got %d, want %d", got, tt.want)
            }
        })
    }
}
```

## Go イディオムチェック

### 命名規則
- [ ] パッケージ名は小文字・単数形か（`user` not `users`）
- [ ] インターフェース名は動詞+erか（`Reader`, `Finder`）
- [ ] exported names にコメントがあるか

### エラーハンドリング
- [ ] エラーは無視していないか
- [ ] エラーは `fmt.Errorf("%w", err)` でラップしているか
- [ ] sentinel error は `var Err...` で定義しているか

### 並行処理
- [ ] goroutine は終了するか（リークしないか）
- [ ] channel は送信側でクローズしているか
- [ ] context でキャンセル制御しているか
- [ ] sync.Mutex は defer で Unlock しているか

### 設計
- [ ] Accept interfaces, return structs を守っているか
- [ ] 不要な interface{} を使っていないか（ジェネリクス検討）
- [ ] 早期リターンで深いネスト回避しているか

## テストチェックリスト

- [ ] テーブル駆動テストを使用しているか
- [ ] t.Run でサブテストに分けているか
- [ ] モックはインターフェースで定義しているか
- [ ] 標準 testing パッケージを優先しているか

## 出力形式

🔴 **Critical**: `ファイル:行` - エラー処理違反/goroutineリーク - 修正案
🟡 **Warning**: `ファイル:行` - イディオム違反 - 改善案
📊 **Summary**: Critical X件 / Warning Y件

## 関連ガイドライン

開発実施前に以下のガイドラインを参照:
- `~/.claude/guidelines/languages/golang.md`
- `~/.claude/guidelines/common/code-quality-design.md`
- `~/.claude/guidelines/common/testing-guidelines.md`

## 外部知識ベース

最新のGoベストプラクティス確認には context7 を活用:
- Go公式ドキュメント（Effective Go）
- Go標準ライブラリ（net/http, context, sync）
- Go Concurrency Patterns

## プロジェクトコンテキスト

プロジェクト固有のGo実装情報を確認:
- serena memory からディレクトリ構成・命名規則を取得
- プロジェクトの標準的なエラーハンドリングパターンを優先
- 既存の並行処理パターンとの一貫性を確認
