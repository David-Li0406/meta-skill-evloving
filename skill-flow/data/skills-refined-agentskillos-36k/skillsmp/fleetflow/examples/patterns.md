# 設定パターン集

FleetFlowの実践的な設定パターンです。

## フルスタックWebアプリケーション

フロントエンド + バックエンド + データベース + キャッシュの構成です。

```kdl
project "webapp"

stage "local" {
    service "frontend"
    service "backend"
    service "db"
    service "redis"
}

// フロントエンド（React/Vue/Next.js等）
service "frontend" {
    image "node:20-alpine"
    ports {
        port 3000 3000
    }
    env {
        NODE_ENV "development"
        NEXT_PUBLIC_API_URL "http://localhost:8080"
    }
    volumes {
        volume "./frontend" "/app"
    }
    command "npm run dev"
    depends_on "backend"
}

// バックエンドAPI
service "backend" {
    image "node:20-alpine"
    ports {
        port 8080 8080
    }
    env {
        NODE_ENV "development"
        DATABASE_URL "postgres://user:pass@db:5432/app"
        REDIS_URL "redis://redis:6379"
    }
    volumes {
        volume "./backend" "/app"
    }
    command "npm run dev"
    depends_on "db" "redis"
    wait_for {
        max_retries 10
        initial_delay 1000
    }
}

// PostgreSQL
service "db" {
    image "postgres:16-alpine"
    restart "unless-stopped"
    ports {
        port 5432 5432
    }
    env {
        POSTGRES_DB "app"
        POSTGRES_USER "user"
        POSTGRES_PASSWORD "pass"
    }
    volumes {
        volume "./data/postgres" "/var/lib/postgresql/data"
    }
    healthcheck {
        test "pg_isready -U user"
        interval 10
        timeout 5
        retries 5
    }
}

// Redis
service "redis" {
    image "redis:7-alpine"
    restart "unless-stopped"
    ports {
        port 6379 6379
    }
    healthcheck {
        test "redis-cli ping"
    }
}
```

## マイクロサービス構成

複数のサービスがAPI Gatewayを通じて連携する構成です。

```kdl
project "microservices"

stage "local" {
    service "gateway"
    service "user-service"
    service "order-service"
    service "db-users"
    service "db-orders"
}

// API Gateway
service "gateway" {
    image "nginx:alpine"
    ports {
        port 80 80
    }
    volumes {
        volume "./gateway/nginx.conf" "/etc/nginx/nginx.conf" read_only=true
    }
    depends_on "user-service" "order-service"
}

// ユーザーサービス
service "user-service" {
    image "myapp/user-service:latest"
    dockerfile "services/user/Dockerfile"
    ports {
        port 8001 8000
    }
    env {
        DATABASE_URL "postgres://user:pass@db-users:5432/users"
    }
    depends_on "db-users"
}

// 注文サービス
service "order-service" {
    image "myapp/order-service:latest"
    dockerfile "services/order/Dockerfile"
    ports {
        port 8002 8000
    }
    env {
        DATABASE_URL "postgres://user:pass@db-orders:5432/orders"
        USER_SERVICE_URL "http://user-service:8000"
    }
    depends_on "db-orders" "user-service"
}

// ユーザーDB
service "db-users" {
    image "postgres:16-alpine"
    restart "unless-stopped"
    ports {
        port 5433 5432
    }
    env {
        POSTGRES_DB "users"
        POSTGRES_USER "user"
        POSTGRES_PASSWORD "pass"
    }
}

// 注文DB
service "db-orders" {
    image "postgres:16-alpine"
    restart "unless-stopped"
    ports {
        port 5434 5432
    }
    env {
        POSTGRES_DB "orders"
        POSTGRES_USER "user"
        POSTGRES_PASSWORD "pass"
    }
}
```

## Rustバックエンド + SurrealDB

Rust APIサーバーとSurrealDBの構成です。

```kdl
project "rust-api"

stage "local" {
    service "api"
    service "surrealdb"
}

// Rust APIサーバー
service "api" {
    image "myapp/api:latest"
    dockerfile "Dockerfile"
    target "development"
    ports {
        port 3000 3000
    }
    env {
        RUST_LOG "debug"
        DATABASE_URL "ws://surrealdb:8000"
        DATABASE_NS "app"
        DATABASE_DB "main"
    }
    volumes {
        volume "./src" "/app/src"
        volume "./Cargo.toml" "/app/Cargo.toml" read_only=true
    }
    depends_on "surrealdb"
    wait_for {
        max_retries 15
        initial_delay 2000
    }
}

// SurrealDB
service "surrealdb" {
    image "surrealdb/surrealdb:latest"
    restart "unless-stopped"
    ports {
        port 8000 8000
    }
    command "start --user root --pass root file:/data/database.db"
    volumes {
        volume "./data/surreal" "/data"
    }
}
```

## 静的サイト + リバースプロキシ

静的ファイル配信とSSL終端の構成です。

```kdl
project "static-site"

stage "local" {
    service "nginx"
}

service "nginx" {
    image "nginx:alpine"
    restart "unless-stopped"
    ports {
        port 80 80
        port 443 443
    }
    volumes {
        volume "./public" "/usr/share/nginx/html" read_only=true
        volume "./nginx.conf" "/etc/nginx/nginx.conf" read_only=true
        volume "./certs" "/etc/nginx/certs" read_only=true
    }
}
```

## ローカルDockerビルド

Dockerfileからビルドするパターンです。

### 規約ベース（自動検出）

```kdl
// services/api/Dockerfile が自動検出される
service "api" {
    image "myapp/api:latest"  // imageは必須
    ports {
        port 3000 3000
    }
}
```

### 明示的なビルド設定

```kdl
service "api" {
    image "myapp/api:v1.0.0"
    dockerfile "docker/api.Dockerfile"
    context "."
    target "production"
    build_args {
        RUST_VERSION "1.75"
        BUILD_MODE "release"
    }
    ports {
        port 3000 3000
    }
}
```

## 複数ステージ構成

開発・ステージング・本番で異なるサービス構成を持つパターンです。

```kdl
project "multi-stage"

// ローカル開発環境
stage "local" {
    service "web"
    service "db"
    service "mailhog"  // メールテスト用
}

// プレ本番環境
stage "pre" {
    service "web"
    service "db"
}

// ライブ環境
stage "live" {
    service "web"
    service "db"
    service "cdn"
}

service "web" {
    image "node:20-alpine"
    restart "unless-stopped"
    ports {
        port 3000 3000
    }
    depends_on "db"
}

service "db" {
    image "postgres:16-alpine"
    restart "unless-stopped"
    ports {
        port 5432 5432
    }
    healthcheck {
        test "pg_isready -U postgres"
        interval 10
        timeout 5
        retries 5
    }
}

// ローカル開発用メールサーバー
service "mailhog" {
    image "mailhog/mailhog:latest"
    ports {
        port 1025 1025  // SMTP
        port 8025 8025  // Web UI
    }
}

// 本番用CDN/リバースプロキシ
service "cdn" {
    image "nginx:alpine"
    restart "unless-stopped"
    ports {
        port 80 80
        port 443 443
    }
    depends_on "web"
}
```

## クラウドインフラ構成

さくらのクラウドでサーバーを作成し、Cloudflare DNSで管理するパターンです。

```kdl
project "myapp"

providers {
    sakura-cloud { zone "tk1a" }
    cloudflare { account-id env="CF_ACCOUNT_ID" }
}

stage "dev" {
    server "app-server" {
        provider "sakura-cloud"
        plan core=2 memory=4
        disk size=40 os="ubuntu-24.04"
        ssh-key "~/.ssh/id_ed25519.pub"
        dns_aliases "app" "api"
    }

    service "api"
    service "db"
}

service "api" {
    image "myapp/api:latest"
    ports {
        port 3000 3000
    }
}

service "db" {
    image "postgres:16-alpine"
    restart "unless-stopped"
    ports {
        port 5432 5432
    }
}
```

## ベストプラクティス

### 命名規則

- プロジェクト名: 短く、ハイフン区切り（`my-app`）
- ステージ名: 用途を表す（`local`, `dev`, `pre`, `live`）
- サービス名: 役割を表す（`db`, `api`, `web`）

### ポート管理

| サービス | デフォルトポート |
|---------|----------------|
| PostgreSQL | 5432 |
| MySQL | 3306 |
| Redis | 6379 |
| SurrealDB | 8000 |
| HTTP | 80, 3000, 8080 |
| HTTPS | 443 |

### ボリューム管理

```kdl
// 開発用: ソースコードをマウント
volumes {
    volume "./src" "/app/src"
}

// データ永続化
volumes {
    volume "./data/postgres" "/var/lib/postgresql/data"
}

// 設定ファイル（読み取り専用）
volumes {
    volume "./config.yml" "/etc/app/config.yml" read_only=true
}
```

### 環境変数

```kdl
env {
    // データベース接続
    DATABASE_URL "postgres://user:pass@db:5432/app"

    // 開発モード
    NODE_ENV "development"
    RUST_LOG "debug"

    // サービス間通信
    API_URL "http://api:3000"
}
```

### 依存関係と待機

```kdl
// 起動順序の制御
service "web" {
    depends_on "db" "redis"

    // Exponential Backoffで依存サービスの準備を待機
    wait_for {
        max_retries 23        // 最大リトライ回数
        initial_delay 1000    // 初回待機時間（ミリ秒）
        max_delay 30000       // 最大待機時間（ミリ秒）
        multiplier 2.0        // 待機時間の増加倍率
    }
}
```

### ヘルスチェック

```kdl
// データベースのヘルスチェック
service "db" {
    image "postgres:16-alpine"
    healthcheck {
        test "pg_isready -U postgres"
        interval 10      // チェック間隔（秒）
        timeout 5        // タイムアウト（秒）
        retries 5        // リトライ回数
        start_period 10  // 起動待機時間（秒）
    }
}

// Redisのヘルスチェック
service "redis" {
    image "redis:7-alpine"
    healthcheck {
        test "redis-cli ping"
    }
}
```

### 再起動ポリシー

```kdl
service "db" {
    image "postgres:16-alpine"
    restart "unless-stopped"  // ホスト再起動後も自動復旧
}
```

| 値 | 説明 |
|----|------|
| `no` | 再起動しない（デフォルト） |
| `always` | 常に再起動 |
| `on-failure` | 異常終了時のみ再起動 |
| `unless-stopped` | 明示的に停止されない限り再起動（推奨） |
