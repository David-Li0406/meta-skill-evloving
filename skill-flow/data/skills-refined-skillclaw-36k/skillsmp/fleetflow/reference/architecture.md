# アーキテクチャ

FleetFlowの内部構造とコンポーネントの説明です。

## プロジェクト構造

```
fleetflow/
├── crates/
│   ├── fleetflow/              # CLIエントリーポイント
│   ├── fleetflow-core/         # KDLパーサー・データモデル
│   │   ├── src/model/          # データ構造
│   │   └── src/parser/         # パーサー
│   ├── fleetflow-config/       # 設定管理
│   ├── fleetflow-container/    # コンテナ操作
│   ├── fleetflow-build/        # Dockerビルド機能
│   ├── fleetflow-mcp/          # MCPサーバー機能
│   ├── fleetflow-cloud/        # クラウドインフラ抽象化
│   ├── fleetflow-cloud-sakura/ # さくらクラウド連携
│   └── fleetflow-cloud-cloudflare/ # Cloudflare連携
├── spec/                       # 仕様書
├── design/                     # 設計書
└── guides/                     # 利用ガイド
```

## クレート概要

### fleetflow

CLIのエントリーポイント。`clap`を使用したコマンド定義とメインロジック。

- コマンドのパース
- ワークフロー制御
- 出力フォーマット

**主要コマンド**:
- `up`, `down`, `deploy` - ステージのライフサイクル管理
- `start`, `stop`, `restart` - サービス単位の操作
- `build` - Dockerイメージビルド
- `cloud up/down` - クラウドインフラ管理
- `ps`, `logs`, `validate` - 状態確認
- `setup` - 環境セットアップ（冪等）
- `play` - Playbook実行
- `mcp` - MCPサーバー起動

### fleetflow-core

KDLパーサーとコアデータモデル。

**model/**:
- `flow.rs` - Flow（設定全体）
- `stage.rs` - Stage（環境）
- `service.rs` - Service, BuildConfig, HealthCheck
- `port.rs` - Port, Protocol
- `volume.rs` - Volume
- `process.rs` - Process, ProcessState

**parser/**:
- `mod.rs` - メインパース関数、サービスマージロジック
- `stage.rs` - stageノードパース
- `service.rs` - serviceノードパース（image必須バリデーション）
- `port.rs` - portノードパース
- `volume.rs` - volumeノードパース

**重要な仕様**:
- `image`フィールドは必須（v0.2.4以降）
- 同名サービスは自動マージ（`Service::merge()`）

### fleetflow-container

Docker操作を担当。`bollard`クレートでDocker APIと通信。

- コンテナのライフサイクル管理
- イメージのpull
- ポート/ボリュームマッピング
- 依存サービス待機（Exponential Backoff）

### fleetflow-build

Dockerイメージのビルド機能。

- **resolver**: Dockerfile検出と変数展開
- **context**: ビルドコンテキスト作成
- **builder**: Bollard APIでのビルド実行
- **progress**: 進捗表示
- **push**: レジストリへのイメージプッシュ

**規約ベース検出**:
1. `./services/{service-name}/Dockerfile`
2. `./{service-name}/Dockerfile`
3. `./Dockerfile.{service-name}`

### fleetflow-mcp

Model Context Protocol (MCP) サーバー機能。

AI/LLMアシスタントとの連携を可能にするMCPサーバーを提供。
- JSON-RPCベースの通信
- コンテナ操作のツール提供
- 設定情報の公開

### fleetflow-cloud

クラウドインフラ管理の抽象化レイヤー。

- `CloudProvider`トレイト
- Action/Plan/ApplyResultパターン
- 状態管理（ファイルロック付き）

### fleetflow-cloud-sakura

さくらクラウドプロバイダー（usacloud CLI ラッパー）。

- サーバー作成・削除・起動・停止
- ディスク管理
- SSH鍵設定
- スタートアップスクリプト

### fleetflow-cloud-cloudflare

Cloudflareプロバイダー。

- DNS管理（Aレコード CRUD）
- サーバー作成/削除時の自動DNS登録
- R2バケット管理（実装中）
- Workers管理（予定）

## 技術スタック

| カテゴリ | ライブラリ |
|---------|-----------|
| 言語 | Rust (Edition 2024) |
| CLI | clap |
| KDLパース | kdl |
| Docker API | bollard |
| 非同期 | tokio |
| エラー | anyhow, thiserror |
| シリアライズ | serde, serde_json |
| ログ | tracing |

## コンテナ命名規則

```
{project}-{stage}-{service}
```

例: `myapp-local-db`

### Dockerラベル

| ラベル | 値 | 用途 |
|--------|-----|------|
| `com.docker.compose.project` | `{project}-{stage}` | OrbStackグループ化 |
| `com.docker.compose.service` | `{service}` | サービス識別 |
| `fleetflow.project` | プロジェクト名 | メタデータ |
| `fleetflow.stage` | ステージ名 | メタデータ |
| `fleetflow.service` | サービス名 | メタデータ |

## OrbStack連携

FleetFlowは主にmacOSのローカル開発環境での利用を想定しており、OrbStackと連携します。

- `com.docker.compose.project`ラベルでグループ化
- プロジェクト・ステージごとに整理された表示
- Docker Composeとの互換性

## DNS自動管理

`cloud up`/`cloud down`時にCloudflare DNSを自動管理：

**サブドメイン命名規則**:
```
{service}-{stage}.{domain}
```

例: `api-prod.example.com`

**動作**:
- `cloud up`: サーバー作成後にAレコードを自動追加
- `cloud down`: サーバー削除前にDNSレコードを自動削除
- `dns_aliases`: 追加のCNAMEエイリアスを自動作成

**必要な環境変数**:
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_ZONE_ID`
- `CLOUDFLARE_DOMAIN`

## ドキュメント構造

### spec/ - 仕様書（What & Why）

機能の目的と仕様を定義。

- `01-core-concepts.md` - コアコンセプト
- `02-kdl-parser.md` - KDLパーサー仕様
- `03-cli-commands.md` - CLIコマンド仕様
- `06-orbstack-integration.md` - OrbStack連携
- `07-docker-build.md` - Dockerビルド
- `08-cloud-infrastructure.md` - クラウドインフラ
- `09-dns-integration.md` - DNS連携

### design/ - 設計書（How）

実装の詳細設計。

- `01-kdl-parser.md` - パーサー設計
- `02-orbstack-integration.md` - OrbStack連携設計
- `03-docker-build.md` - ビルド機能設計
- `04-cloud-infrastructure.md` - クラウド設計
- `05-dns-integration.md` - DNS連携設計

### guides/ - 利用ガイド（Usage）

ユースケース別の使い方。

- `01-orbstack-integration.md` - OrbStack連携ガイド
- `02-docker-build.md` - Dockerビルドガイド
- `03-cloud-platforms.md` - 外部プラットフォーム対応状況

## 開発フェーズ

### Phase 1: MVP ✅
- KDLパーサー
- 基本CLI（up/down/ps/logs）
- Docker API統合
- OrbStack連携

### Phase 2: ビルド機能 ✅
- Dockerビルド
- 個別サービス操作
- 複数設定ファイル対応
- マルチステージビルド対応
- イメージプッシュ

### Phase 3: クラウドインフラ ✅
- クラウドプロバイダー抽象化
- さくらクラウド連携
- Cloudflare DNS連携
- CLI統合

### Phase 4: 高度な機能 ✅
- MCP（Model Context Protocol）サーバー
- Playbook機能
- CI/CDデプロイコマンド
- セルフアップデート

### Phase 5: 拡張機能（予定）
- 環境変数参照
- 変数展開
- ヘルスチェック強化
- Cloudflare R2/Workers連携
