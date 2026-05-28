# KDL構文リファレンス

FleetFlowの設定ファイル（fleet.kdl）の構文詳細です。

## 基本構造

```kdl
// プロジェクト名（必須）
project "project-name"

// ステージ定義
stage "stage-name" {
    service "service-name"
}

// サービス詳細定義
service "service-name" {
    image "image-name:tag"  // 必須
    // ...
}

// クラウドインフラ（オプション）
providers { ... }
server "server-name" { ... }
```

## プロジェクト宣言

```kdl
project "myapp"
```

- **必須**: すべての設定ファイルで最初に宣言
- **用途**: コンテナ命名規則、ラベル付けに使用
- **命名規則**: `{project}-{stage}-{service}`

## ステージ定義

```kdl
stage "local" {
    service "db"
    service "redis"
    service "web"
}

stage "live" {
    service "db"
    service "redis"
    service "web"
    service "cdn"
}
```

- **複数定義可能**: 環境ごとに異なるサービス構成
- **サービスは共通定義**: `service`ブロックで詳細を定義

## サービス定義

### イメージ指定（必須）

```kdl
service "db" {
    image "postgres:16"
    // imageフィールドは必須です
}

service "custom" {
    image "ghcr.io/org/app:v1.0.0"
    // レジストリ付きイメージも使用可能
}
```

**重要**: `image`フィールドは**必須**です。省略するとエラーになります：

```kdl
// エラー: imageが必須
service "db" {
    version "16"
}
// Error: サービス 'db' に image が指定されていません
```

### ポート設定

```kdl
ports {
    port 8080 3000                    // host:8080 → container:3000
    port 5432 5432                    // host:5432 → container:5432
    port 53 53 protocol="udp"         // UDPプロトコル
    port 8443 443 host_ip="127.0.0.1" // ローカルホストのみ
}
```

**構文**: `port <host_port> <container_port> [options]`

| パラメータ | 必須 | 説明 |
|-----------|------|------|
| 第1引数 | Yes | ホスト側のポート番号 |
| 第2引数 | Yes | コンテナ内のポート番号 |
| `protocol` | - | `tcp`（デフォルト）または `udp` |
| `host_ip` | - | バインドするホストIP |

### 環境変数

```kdl
env {
    DATABASE_URL "postgres://localhost:5432/mydb"
    DEBUG "true"
    NODE_ENV "development"
}
```

- キーと値をペアで指定
- 複数行で定義可能
- **マージ時は両方の値が結合される**（後の定義が優先）

### ボリュームマウント

```kdl
volumes {
    volume "./data" "/var/lib/postgresql/data"
    volume "/config" "/etc/config" read_only=true
}
```

**構文**: `volume <host_path> <container_path> [options]`

| パラメータ | 必須 | 説明 |
|-----------|------|------|
| 第1引数 | Yes | ホスト側のパス（相対パスは自動で絶対パスに変換） |
| 第2引数 | Yes | コンテナ内のパス |
| `read_only` | - | 読み取り専用（デフォルト: false） |

### コマンド実行

```kdl
service "db" {
    image "postgres:16"
    command "postgres -c max_connections=200"
}
```

- コンテナ起動時のコマンドを上書き
- スペースで自動的に引数分割

### 依存関係

```kdl
service "web" {
    image "node:20-alpine"
    depends_on "db" "redis"
}
```

- 起動順序の制御に使用
- スペース区切りで複数指定可能

### 依存サービス待機（Exponential Backoff）

```kdl
service "api" {
    image "myapp/api:latest"
    depends_on "db" "redis"
    wait_for {
        max_retries 23        // 最大リトライ回数
        initial_delay 1000    // 初回待機時間（ミリ秒）
        max_delay 30000       // 最大待機時間（ミリ秒）
        multiplier 2.0        // 待機時間の増加倍率
    }
}
```

K8sのReadiness Probeコンセプトを取り入れた、依存サービスの準備完了待機機能です。

| パラメータ | デフォルト | 説明 |
|-----------|-----------|------|
| `max_retries` | 23 | 最大リトライ回数 |
| `initial_delay` | 1000 | 初回待機時間（ミリ秒） |
| `max_delay` | 30000 | 最大待機時間（ミリ秒） |
| `multiplier` | 2.0 | 待機時間の増加倍率 |

**待機時間の計算**（Exponential Backoff）:
```
delay = initial_delay * multiplier^attempt
```

デフォルト設定での待機パターン: 1秒→2秒→4秒→8秒→16秒→30秒（上限）...

```kdl
// デフォルト設定を使用
service "api" {
    depends_on "db"
    wait_for  // 全てデフォルト値
}
```

### 再起動ポリシー

```kdl
service "db" {
    image "postgres:16"
    restart "unless-stopped"
}
```

**対応する値**:

| 値 | 説明 |
|----|------|
| `no` | 再起動しない（デフォルト） |
| `always` | 常に再起動 |
| `on-failure` | 異常終了時のみ再起動 |
| `unless-stopped` | 明示的に停止されない限り再起動（推奨） |

**用途**: ホスト再起動後にコンテナを自動復旧させる場合に使用

### Dockerビルド設定

```kdl
service "api" {
    image "myapp/api:latest"  // ビルド後のイメージタグ

    // 明示的なビルド設定
    dockerfile "services/api/Dockerfile"
    context "."
    target "production"

    build_args {
        RUST_VERSION "1.75"
        NODE_VERSION "20"
    }
}
```

| パラメータ | 説明 |
|-----------|------|
| `dockerfile` | Dockerfileのパス |
| `context` | ビルドコンテキスト（デフォルト: プロジェクトルート） |
| `target` | マルチステージビルドのターゲット |
| `build_args` | ビルド引数 |

**規約ベース検出**: `services/{name}/Dockerfile` が自動検出されます。

**検索順序**:
1. `./services/{service-name}/Dockerfile`
2. `./{service-name}/Dockerfile`
3. `./Dockerfile.{service-name}`

### ヘルスチェック設定

```kdl
service "db" {
    image "postgres:16"
    healthcheck {
        test "pg_isready -U postgres"
        interval 30
        timeout 3
        retries 3
        start_period 10
    }
}
```

| パラメータ | デフォルト | 説明 |
|-----------|-----------|------|
| `test` | - | ヘルスチェックコマンド（必須） |
| `interval` | 30 | チェック間隔（秒） |
| `timeout` | 3 | タイムアウト（秒） |
| `retries` | 3 | リトライ回数 |
| `start_period` | 10 | 起動待機時間（秒） |

## クラウドインフラ定義

### プロバイダー設定

```kdl
providers {
    sakura-cloud {
        zone "tk1a"
        // 認証はusacloud configから自動取得
    }

    cloudflare {
        account-id env="CF_ACCOUNT_ID"
        // 認証は環境変数から
    }
}
```

### サーバー定義（ステージ内）

```kdl
stage "dev" {
    server "app-server" {
        provider "sakura-cloud"
        plan core=4 memory=4
        disk size=100 os="ubuntu-24.04"
        ssh-key "~/.ssh/id_ed25519.pub"

        // DNSエイリアス（オプション）
        dns_aliases "app" "api" "www"
    }
}
```

| パラメータ | 説明 |
|-----------|------|
| `provider` | 使用するクラウドプロバイダー |
| `plan` | サーバースペック（コア数、メモリ） |
| `disk` | ディスクサイズとOS |
| `ssh-key` | SSH公開鍵のパス |
| `dns_aliases` | DNSエイリアス（CNAMEレコード） |

## サービスマージ機能

複数ファイルで同じサービスを定義した場合、設定がマージされます：

```kdl
// fleet.kdl（ベース設定）
service "api" {
    image "myapp:latest"
    ports { port 8080 3000 }
    env { NODE_ENV "production" }
}

// flow.local.kdl（ローカルオーバーライド）
service "api" {
    env { DATABASE_URL "localhost:5432" }
}

// 結果:
// - image: "myapp:latest" (保持)
// - ports: [8080:3000] (保持)
// - env: { NODE_ENV: "production", DATABASE_URL: "localhost:5432" } (マージ)
```

**マージルール**:

| フィールドタイプ | ルール | 例 |
|----------------|--------|-----|
| `Option<T>` | 後の定義が`Some`なら上書き | image, command, build, healthcheck |
| `Vec<T>` | 後の定義が空でなければ上書き | ports, volumes, depends_on |
| `HashMap<K, V>` | 両方をマージ（後の定義が優先） | env (environment) |

## 設定ファイル検索順序

FleetFlowは以下の優先順位で設定ファイルを検索します：

1. 環境変数 `FLEETFLOW_CONFIG_PATH`
2. カレントディレクトリ:
   - `flow.local.kdl` (ローカル専用)
   - `.flow.local.kdl`
   - `fleet.kdl` (標準)
   - `.fleet.kdl`
3. `.fleetflow/` ディレクトリ
4. `~/.config/fleetflow/fleet.kdl` (グローバル)

## 完全な例

### ローカル開発環境

```kdl
project "myapp"

// ステージ定義
stage "local" {
    service "db"
    service "redis"
    service "web"
}

stage "live" {
    service "db"
    service "redis"
    service "web"
    service "cdn"
}

// PostgreSQL
service "db" {
    image "postgres:16-alpine"
    restart "unless-stopped"
    ports {
        port 5432 5432
    }
    env {
        POSTGRES_DB "myapp"
        POSTGRES_USER "myapp"
        POSTGRES_PASSWORD "secret"
    }
    volumes {
        volume "./data/postgres" "/var/lib/postgresql/data"
    }
    healthcheck {
        test "pg_isready -U myapp"
        interval 10
        timeout 5
        retries 5
    }
}

// Redis
service "redis" {
    image "redis:7-alpine"
    ports {
        port 6379 6379
    }
    healthcheck {
        test "redis-cli ping"
    }
}

// Webアプリ
service "web" {
    image "node:20-alpine"
    ports {
        port 3000 3000
    }
    env {
        NODE_ENV "development"
        DATABASE_URL "postgres://myapp:secret@db:5432/myapp"
        REDIS_URL "redis://redis:6379"
    }
    volumes {
        volume "./app" "/app"
    }
    command "npm run dev"
    depends_on "db" "redis"
    wait_for {
        max_retries 10
        initial_delay 1000
    }
}

// CDN（本番のみ）
service "cdn" {
    image "nginx:alpine"
    ports {
        port 80 80
        port 443 443
    }
    volumes {
        volume "./nginx.conf" "/etc/nginx/nginx.conf" read_only=true
    }
}
```

### クラウドインフラ設定

```kdl
project "myapp"

providers {
    sakura-cloud { zone "tk1a" }
    cloudflare { account-id env="CF_ACCOUNT_ID" }
}

stage "dev" {
    // さくらのクラウドでサーバー作成
    server "app-server" {
        provider "sakura-cloud"
        plan core=4 memory=4
        disk size=100 os="ubuntu-24.04"
        ssh-key "~/.ssh/id_ed25519.pub"
        dns_aliases "app" "api"
    }

    service "api"
    service "db"
}

service "api" {
    image "myapp/api:latest"
    ports { port 3000 3000 }
}

service "db" {
    image "postgres:16"
    ports { port 5432 5432 }
}
```
