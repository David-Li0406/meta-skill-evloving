# analyzerアプリケーション アーキテクチャガイド

このドキュメントは、analyzerアプリケーション固有のアーキテクチャパターンを定義します。

## アーキテクチャ概要

analyzerは**ポート&アダプターアーキテクチャ**(ヘキサゴナルアーキテクチャ)を採用しています。

---

## ディレクトリ構造

```
app/analyzer/internal/
├── port/            # インターフェース定義層
├── adapter/         # インターフェース実装層
├── usecase/         # ユースケース層
├── model/           # ドメインモデル層
└── registory/       # 依存性注入コンテナ
```

---

## 各層の役割

### Port層 (`internal/port/`)

**役割**: アプリケーションの境界を定義するインターフェース層

**配置するもの**:
- 外部システムとのインターフェース定義
- ユースケースのインターフェース定義
- **全て関数型(`type Name = func(...)`)で定義**

**例**:
```go
// port/fetcher/entry.go
package fetcher

type FetchLatestEntry = func(context.Context) mo.Result[mo.Option[*model.Entry]]
```

```go
// port/usecase/analyze.go
package usecase

type AnalyzeInput struct {
    Goal model.GoalType
}

type AnalyzeOutput struct {
    IsGoalAchieved bool
}

type Analyze = func(context.Context, *AnalyzeInput) mo.Result[*AnalyzeOutput]
```

**レビューポイント**:
- ✅ 関数型(`type Name = func(...)`)で定義されているか
- ✅ 第一引数が`context.Context`か(必要な場合)
- ✅ 実装コードが含まれていないか(型定義のみ)
- ✅ 必要に応じて入力/出力用の構造体が定義されているか
- ❌ Port層に具体的な実装が含まれていないか

---

### Adapter層 (`internal/adapter/`)

**役割**: Portインターフェースの具体的な実装

**配置するもの**:
- 外部API/DB/ファイルシステムとの通信実装
- Portインターフェースの実装
- `New*`関数でPort型を返す

**ディレクトリ構成**:
```
adapter/
├── fetcher/
│   ├── hatena/      # Hatenaブログ実装
│   ├── zenn/        # Zenn実装
│   └── internal/    # 共通処理
├── notifier/
│   └── discord/     # Discord実装
└── persister/
    └── s3/          # S3実装
```

**例**:
```go
// adapter/fetcher/hatena/hatena.go
package hatena

func NewFetchLatestEntry() fetcher.FetchLatestEntry {
    return func(ctx context.Context) mo.Result[mo.Option[*model.Entry]] {
        return fetchLatestEntry(ctx, config.FeedURLHatena())
    }
}

func fetchLatestEntry(ctx context.Context, url string) mo.Result[mo.Option[*model.Entry]] {
    // 実装
}
```

**レビューポイント**:
- ✅ `New*`という命名規則のコンストラクタがあるか
- ✅ Portインターフェースを実装しているか
- ✅ 外部依存(HTTP、DB、ファイルなど)がこの層に閉じ込められているか
- ✅ 実装関数は非公開(小文字始まり)か
- ❌ ビジネスロジックが含まれていないか

---

### Usecase層 (`internal/usecase/`)

**役割**: アプリケーションのビジネスロジック

**配置するもの**:
- ユースケースの実装
- 複数のPortを組み合わせたワークフロー
- `New*`関数で依存性を注入

**例**:
```go
// usecase/analyze.go
func NewAnalyze(
    latestEntryFetchers []fetcher.FetchLatestEntry,
    printAnalysisReport printer.PrintAnalysisReport,
    notifyAnalysisReport notifier.NotifyAnalysisReport,
    acquireLock locker.Acquire,
    releaseLock locker.Release,
    persistAnalysisReport persister.PersistAnalysisReport,
) usecase.Analyze {
    return func(ctx context.Context, in *usecase.AnalyzeInput) mo.Result[*usecase.AnalyzeOutput] {
        return analyze(ctx, in, latestEntryFetchers, printAnalysisReport,
                      notifyAnalysisReport, acquireLock, releaseLock, persistAnalysisReport)
    }
}
```

**レビューポイント**:
- ✅ `New*`コンストラクタで全ての依存性を注入しているか
- ✅ Portインターフェースのみに依存しているか
- ✅ 実装関数は非公開(小文字始まり)か
- ❌ Adapter層の具体的な実装を直接参照していないか
- ❌ 外部システムに直接アクセスしていないか

---

### Model層 (`internal/model/`)

**役割**: ドメインモデルとビジネスロジック

**配置するもの**:
- ドメインエンティティ
- 値オブジェクト
- ドメインロジック

**レビューポイント**:
- ✅ ドメイン知識を表現する型を定義しているか
- ✅ ドメインロジックがここに集約されているか
- ❌ 外部依存(DB、APIなど)を持っていないか
- ❌ Port/Adapter/Usecaseに依存していないか

---

### Registry層 (`internal/registory/`)

**役割**: 依存性注入コンテナ

**配置するもの**:
- 全てのAdapter層の初期化
- Usecase層への依存性注入
- Entry pointから呼び出される

**例**:
```go
// registory/usecase.go
func NewAnalyzeUsecase(ctx context.Context) (usecaseport.Analyze, error) {
    awsConfig, err := config.LoadDefaultConfig(ctx)
    if err != nil {
        return nil, err
    }

    return usecaseadapter.NewAnalyze(
        []fetcher.FetchLatestEntry{
            hatena.NewFetchLatestEntry(),
            zenn.NewFetchLatestEntry(),
        },
        stdout.PrintAnalysisReport,
        discord.NewNotifyAnalysisReport(),
        cfworker.NewAcquire(),
        cfworker.NewRelease(),
        s3.NewPersistAnalysisReport(awsConfig),
    ), nil
}
```

**レビューポイント**:
- ✅ 全ての依存性の組み立てがここで行われているか
- ✅ 具体的な実装の選択がここで行われているか
- ✅ Entry point(`cmd/`)から呼び出されているか
- ❌ ビジネスロジックが含まれていないか

---

## 依存関係のルール

### 依存の方向

```
Adapter → Port ← Usecase
             ↓       ↓
           Model   Model
```

**許可される依存**:
1. Usecase → Port
2. Usecase → Model
3. Adapter → Port
4. Adapter → Model
5. Port → Model(必要に応じて)

**禁止される依存**:
- ❌ Port → Usecase
- ❌ Port → Adapter
- ❌ Usecase → Adapter
- ❌ Model → Port/Usecase/Adapter

### importの確認

**Usecaseの正しいimport例**:
```go
import (
    "github.com/ss49919201/keeput/app/analyzer/internal/port/fetcher"
    "github.com/ss49919201/keeput/app/analyzer/internal/port/locker"
    "github.com/ss49919201/keeput/app/analyzer/internal/model"
)
```

**Adapterの正しいimport例**:
```go
import (
    "github.com/ss49919201/keeput/app/analyzer/internal/port/fetcher"
    "github.com/ss49919201/keeput/app/analyzer/internal/model"
)
```

---

## 命名規則

### New*関数のパターン

**Port型をそのまま返す**:
```go
func NewFetchLatestEntry() fetcher.FetchLatestEntry {
    return func(ctx context.Context) mo.Result[mo.Option[*model.Entry]] {
        return fetchLatestEntry(ctx, config.FeedURLHatena())
    }
}
```

**外部依存を受け取る**:
```go
func NewPersistAnalysisReport(config aws.Config) persister.PersistAnalysisReport {
    initS3Client(config)
    return persistAnalysisReport
}
```

**レビューポイント**:
- ✅ `New*`という命名になっているか
- ✅ Port型を返しているか
- ✅ 設定値はクロージャでキャプチャしているか

---

## パッケージ構成ルール

### Port層パッケージ

- ファイル: `internal/port/{port名}/{port名}.go`
- 責務: インターフェース定義のみ

### Adapter層パッケージ

- ディレクトリ: `internal/adapter/{port名}/{具体実装}/`
- ファイル: `{具体実装}.go`
- 責務: Port型の実装、New関数

### Usecase層パッケージ

- ディレクトリ: `internal/usecase/`
- ファイル: `{usecase名}.go`
- 責務: ビジネスロジック、New関数

### Model層パッケージ

- ディレクトリ: `internal/model/`
- ファイル: `{entity名}.go`
- 責務: データ構造、純粋なビジネスロジック

---

## アーキテクチャ違反の例

### ❌ 悪い例1: UsecaseがAdapterに依存

```go
// usecase/analyze.go
import (
    "github.com/ss49919201/keeput/app/analyzer/internal/adapter/fetcher/hatena"  // NG!
)

func NewAnalyze() usecase.Analyze {
    fetcher := hatena.NewFetchLatestEntry()  // NG: Adapterを直接参照
    // ...
}
```

**問題点**: UsecaseがAdapter層の具体的な実装に依存している

**修正方法**: Registry層で依存性を注入する

---

### ❌ 悪い例2: Port層に実装を含める

```go
// port/fetcher/entry.go
package fetcher

type FetchLatestEntry = func(context.Context) mo.Result[mo.Option[*model.Entry]]

// NG: Port層に実装を含めてはいけない
func DefaultFetchLatestEntry() FetchLatestEntry {
    return func(ctx context.Context) mo.Result[mo.Option[*model.Entry]] {
        // 実装
    }
}
```

**問題点**: Port層に実装が含まれている

**修正方法**: Adapter層に実装を移動する

---

### ❌ 悪い例3: Modelが外部依存を持つ

```go
// model/entry.go
package model

import "github.com/aws/aws-sdk-go-v2/service/s3"  // NG!

func (e *Entry) Save(s3Client *s3.Client) error {  // NG: 外部依存
    // S3への保存処理
}
```

**問題点**: ModelがAWS SDKに依存している

**修正方法**: Persister Adapterに処理を移動する

---

## レビュー時の確認事項

### 新しいPortの追加

1. 関数型で定義されているか
2. `internal/port/{port名}/`に配置されているか
3. 実装コードが含まれていないか

### 新しいAdapterの追加

1. `internal/adapter/{port名}/{具体実装}/`に配置されているか
2. `New*`関数があるか
3. Port型を返しているか
4. 外部依存がこの層に閉じ込められているか

### 新しいUsecaseの追加

1. `internal/usecase/`に配置されているか
2. `New*`コンストラクタで依存性を注入しているか
3. Portインターフェースのみに依存しているか
4. Adapter層を直接参照していないか

### 循環依存のチェック

```bash
# 循環依存がないか確認
go mod graph | grep cycle
```
