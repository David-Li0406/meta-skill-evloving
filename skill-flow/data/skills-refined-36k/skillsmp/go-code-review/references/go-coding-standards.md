# Go コーディング規約

このドキュメントは、一般的なGoのコーディング規約とベストプラクティスをまとめたものです。

## 参考資料

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md)

---

## 目次

- [フォーマットと構成](#フォーマットと構成)
- [命名規則](#命名規則)
- [エラーハンドリング](#エラーハンドリング)
- [関数とメソッド](#関数とメソッド)
- [制御構造](#制御構造)
- [パッケージ設計](#パッケージ設計)

---

## フォーマットと構成

### gofmtの使用

```bash
# 必ず実行
gofmt -w .

# またはgoimports（推奨）
goimports -w .
```

**レビューポイント**:
- ✅ 全てのコードが `gofmt` でフォーマットされているか
- ✅ インポート文が整理されているか

---

### インポート文の整理

```go
// ✅ 良い例: グループ分けして整理
import (
    // 標準ライブラリ
    "context"
    "fmt"
    "time"

    // 外部パッケージ
    "github.com/pkg/errors"
    "go.uber.org/zap"

    // 内部パッケージ
    "myproject/internal/model"
    "myproject/internal/service"
)

// ❌ 悪い例: グループ分けなし
import (
    "context"
    "myproject/internal/model"
    "github.com/pkg/errors"
    "fmt"
)
```

---

## 命名規則

### パッケージ名

```go
// ✅ 良い例: 短く、小文字、単数形
package user
package httputil
package ioutil

// ❌ 悪い例
package users          // 複数形は避ける
package user_service   // アンダースコア避ける
package UserService    // 大文字は使わない
```

---

### 変数名

```go
// ✅ 良い例: スコープに応じた長さ
func processUser(u *User) error {
    // 短いスコープでは短い名前
    for i := 0; i < len(u.Items); i++ {
        // ...
    }
    return nil
}

var defaultTimeout = 30 * time.Second  // パッケージレベルは明示的

// ❌ 悪い例
func processUser(user *User) error {
    for index := 0; index < len(user.Items); index++ {  // 長すぎ
        // ...
    }
    return nil
}

var t = 30 * time.Second  // パッケージレベルで短すぎ
```

---

### 関数名

```go
// ✅ 良い例
func NewUser() *User
func GetUserByID(id int) (*User, error)
func IsValid() bool
func HasPermission() bool

// ❌ 悪い例
func get_user_by_id(id int) (*User, error)  // スネークケース
func userByID(id int) (*User, error)        // 曖昧
```

---

### 定数名

```go
// ✅ 良い例
const MaxRetries = 3
const defaultTimeout = 30 * time.Second  // 非公開

// 列挙型
const (
    StatusPending = iota
    StatusActive
    StatusInactive
)

// ❌ 悪い例
const MAX_RETRIES = 3      // スネークケース
const max_retries = 3      // スネークケース
```

---

## エラーハンドリング

### エラーチェック

```go
// ✅ 良い例: 必ずエラーチェック
result, err := doSomething()
if err != nil {
    return fmt.Errorf("failed to do something: %w", err)
}

// ❌ 悪い例: エラー無視
result, _ := doSomething()  // エラーを無視
```

---

### エラーのラップ

```go
// ✅ 良い例: %w でラップ
if err != nil {
    return fmt.Errorf("failed to process user %d: %w", userID, err)
}

// ❌ 悪い例: %v で情報を失う
if err != nil {
    return fmt.Errorf("failed to process user %d: %v", userID, err)
}
```

---

### カスタムエラー型

```go
// ✅ 良い例
type ValidationError struct {
    Field string
    Err   error
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error on field %s: %v", e.Field, e.Err)
}

func (e *ValidationError) Unwrap() error {
    return e.Err
}

// 使用例
if err != nil {
    var validationErr *ValidationError
    if errors.As(err, &validationErr) {
        // バリデーションエラー固有の処理
    }
}
```

---

### panicの使用

```go
// ✅ 良い例: panicは初期化時のみ
func init() {
    if config == nil {
        panic("config must not be nil")
    }
}

// ❌ 悪い例: 通常処理でpanic
func GetUser(id int) *User {
    user, err := fetchUser(id)
    if err != nil {
        panic(err)  // NG: エラーを返すべき
    }
    return user
}
```

---

## 関数とメソッド

### 関数の長さ

```go
// ✅ 良い例: 1つの関数は1つの責務
func ProcessOrder(order *Order) error {
    if err := validateOrder(order); err != nil {
        return err
    }
    if err := calculateTotal(order); err != nil {
        return err
    }
    if err := saveOrder(order); err != nil {
        return err
    }
    return nil
}

// ❌ 悪い例: 長すぎる関数（100行以上）
func ProcessOrder(order *Order) error {
    // バリデーション 30行
    // 計算 40行
    // 保存 30行
    // ...
}
```

---

### 戻り値

```go
// ✅ 良い例: 名前付き戻り値（deferと組み合わせる場合）
func Open(name string) (f *File, err error) {
    f, err = os.Open(name)
    if err != nil {
        return nil, err
    }
    defer func() {
        if err != nil {
            f.Close()
        }
    }()
    // ...
    return f, nil
}

// ✅ 良い例: 通常は名前なし
func GetUser(id int) (*User, error) {
    // ...
}

// ❌ 悪い例: 不要な名前付き戻り値
func GetUser(id int) (user *User, err error) {
    // deferを使っていない場合は不要
}
```

---

### レシーバー名

```go
// ✅ 良い例: 一貫した短い名前
type User struct {
    Name string
}

func (u *User) SetName(name string) {
    u.Name = name
}

func (u *User) GetName() string {
    return u.Name
}

// ❌ 悪い例: 不一致
func (u *User) SetName(name string) {
    u.Name = name
}

func (user *User) GetName() string {  // レシーバー名が違う
    return user.Name
}

func (this *User) Save() error {  // "this"は避ける
    return nil
}
```

---

## 制御構造

### if文

```go
// ✅ 良い例: 早期リターン
func Divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

// ❌ 悪い例: ネストが深い
func Divide(a, b int) (int, error) {
    if b != 0 {
        return a / b, nil
    } else {
        return 0, errors.New("division by zero")
    }
}
```

---

### for文

```go
// ✅ 良い例: rangeの使用
for i, v := range slice {
    process(i, v)
}

for key, value := range m {
    process(key, value)
}

// ✅ 良い例: 無限ループ
for {
    select {
    case <-ctx.Done():
        return
    default:
        doWork()
    }
}

// ❌ 悪い例
for i := 0; i < len(slice); i++ {  // rangeを使うべき
    v := slice[i]
    process(i, v)
}
```

---

### switch文

```go
// ✅ 良い例: 型スイッチ
switch v := value.(type) {
case int:
    fmt.Printf("Integer: %d\n", v)
case string:
    fmt.Printf("String: %s\n", v)
default:
    fmt.Printf("Unknown type\n")
}

// ✅ 良い例: 条件なしswitch
switch {
case age < 18:
    return "minor"
case age < 65:
    return "adult"
default:
    return "senior"
}
```

---

## パッケージ設計

### パッケージ構成

```
myproject/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── domain/
│   ├── service/
│   └── repository/
└── pkg/
    └── utils/
```

**レビューポイント**:
- ✅ `internal/` には外部に公開しないコード
- ✅ `pkg/` には再利用可能なライブラリ
- ✅ `cmd/` にはエントリーポイント

---

### 循環依存の回避

```go
// ❌ 悪い例: 循環依存
// package a
import "myproject/b"

// package b
import "myproject/a"  // 循環依存!

// ✅ 良い例: インターフェースで分離
// package a
type UserRepository interface {
    GetUser(id int) (*User, error)
}

// package b
import "myproject/a"

type UserService struct {
    repo a.UserRepository
}
```

---

## その他のベストプラクティス

### deferの使用

```go
// ✅ 良い例: リソース解放
func ReadFile(name string) ([]byte, error) {
    f, err := os.Open(name)
    if err != nil {
        return nil, err
    }
    defer f.Close()  // 必ず閉じる

    return io.ReadAll(f)
}

// ✅ 良い例: mutexのアンロック
func (s *Service) Update() {
    s.mu.Lock()
    defer s.mu.Unlock()

    // 処理
}
```

---

### コメント

```go
// ✅ 良い例: 公開APIにGoDoc
// GetUser retrieves a user by ID.
// It returns an error if the user is not found.
func GetUser(id int) (*User, error) {
    // ...
}

// ❌ 悪い例: 自明なコメント
// SetName sets the name
func (u *User) SetName(name string) {
    u.Name = name  // nameをセット
}
```

---

### ゼロ値の活用

```go
// ✅ 良い例: ゼロ値で有効な構造体
type Buffer struct {
    buf []byte
}

func (b *Buffer) Write(p []byte) {
    if b.buf == nil {
        b.buf = make([]byte, 0, 64)
    }
    b.buf = append(b.buf, p...)
}

// 使用例
var b Buffer
b.Write([]byte("hello"))  // newなしで使える
```

---

### インターフェースの定義

```go
// ✅ 良い例: 小さいインターフェース
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// ✅ 良い例: 使う側で定義
// package consumer
type DataSource interface {
    GetData() ([]byte, error)
}

// ❌ 悪い例: 大きすぎるインターフェース
type Repository interface {
    GetUser(id int) (*User, error)
    CreateUser(u *User) error
    UpdateUser(u *User) error
    DeleteUser(id int) error
    ListUsers() ([]*User, error)
    SearchUsers(query string) ([]*User, error)
    // ... 10個以上のメソッド
}
```

---

## まとめ

Goのコーディング規約:

1. **gofmtを使う**: フォーマットは自動化
2. **短く明確な名前**: スコープに応じた長さ
3. **エラーは必ずチェック**: `_`でエラーを無視しない
4. **早期リターン**: ネストを浅く
5. **小さいインターフェース**: 使う側で定義
6. **deferでリソース解放**: 確実にクリーンアップ

これらの規約に従うことで、読みやすく保守しやすいGoコードを書くことができます。
