# Bollardベストプラクティス

## 1. 接続管理

### Docker接続の再利用

Docker接続インスタンスは複数の操作で再利用すべきです：

```rust
// ✅ 良い例：接続を再利用
let docker = Docker::connect_with_local_defaults()?;

docker.create_container(...).await?;
docker.start_container(...).await?;
docker.list_containers(...).await?;
```

```rust
// ❌ 悪い例：毎回接続を作成
for container in containers {
    let docker = Docker::connect_with_local_defaults()?; // 無駄
    docker.start_container(&container.id, None).await?;
}
```

### 接続の共有

アプリケーション全体でDocker接続を共有：

```rust
use std::sync::Arc;

pub struct ContainerManager {
    docker: Arc<Docker>,
}

impl ContainerManager {
    pub fn new() -> Result<Self> {
        Ok(Self {
            docker: Arc::new(Docker::connect_with_local_defaults()?),
        })
    }

    pub async fn create_container(&self, ...) -> Result<String> {
        // self.dockerを使用
    }
}
```

## 2. エラーハンドリング

### ステータスコードによる分岐

```rust
use bollard::errors::Error;

match docker.create_container(options, config).await {
    Ok(response) => { /* 成功 */ }
    Err(Error::DockerResponseServerError { status_code: 404, .. }) => {
        // イメージが見つからない → pull
    }
    Err(Error::DockerResponseServerError { status_code: 409, .. }) => {
        // 既に存在 → 起動試行
    }
    Err(Error::DockerResponseServerError { status_code: 500, .. }) => {
        // サーバーエラー → ログ記録、リトライ
    }
    Err(e) => {
        // その他のエラー → 適切な処理
    }
}
```

### コンテキストの追加

```rust
use anyhow::{Context, Result};

docker
    .start_container::<String>(&container_id, None)
    .await
    .with_context(|| format!("コンテナ '{}' の起動に失敗", container_id))?;
```

## 3. 非同期処理

### Tokioランタイムの使用

```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let docker = Docker::connect_with_local_defaults()?;
    // 非同期操作
    Ok(())
}
```

### 並列実行

複数のコンテナを並列に起動：

```rust
use futures::future::try_join_all;

async fn start_containers_parallel(
    docker: &Docker,
    container_ids: Vec<String>,
) -> Result<()> {
    let futures = container_ids
        .iter()
        .map(|id| docker.start_container::<String>(id, None));

    try_join_all(futures).await?;
    Ok(())
}
```

### ストリームの処理

```rust
use futures_util::stream::TryStreamExt;

// イメージのpull進捗を表示
let mut stream = docker.create_image(options, None, None);

while let Some(info) = stream.try_next().await? {
    if let Some(status) = info.status {
        print!("\r{}", status);
    }
}
println!(); // 改行
```

## 4. リソース管理

### クリーンアップ

```rust
async fn cleanup_containers(
    docker: &Docker,
    project_name: &str,
) -> Result<()> {
    let containers = list_project_containers(docker, project_name, None).await?;

    for container in containers {
        if let Some(names) = container.names {
            if let Some(name) = names.first() {
                let name = name.trim_start_matches('/');

                // 停止
                let _ = docker
                    .stop_container(name, Some(StopContainerOptions { t: 10 }))
                    .await;

                // 削除
                docker
                    .remove_container(
                        name,
                        Some(RemoveContainerOptions {
                            force: true,
                            v: true,
                            ..Default::default()
                        }),
                    )
                    .await?;
            }
        }
    }

    Ok(())
}
```

### タイムアウトの設定

```rust
use tokio::time::{timeout, Duration};

// 30秒のタイムアウト
let result = timeout(
    Duration::from_secs(30),
    docker.start_container::<String>(&container_id, None)
).await??;
```

## 5. デバッグとロギング

### 詳細なログ出力

```rust
use tracing::{info, warn, error};

match docker.create_container(options, config).await {
    Ok(response) => {
        info!("コンテナ作成成功: {}", response.id);
    }
    Err(e) => {
        error!("コンテナ作成失敗: {:?}", e);
    }
}
```

### コンテナ情報の表示

```rust
async fn inspect_container(docker: &Docker, container_id: &str) -> Result<()> {
    let info = docker.inspect_container(container_id, None).await?;

    println!("ID: {}", info.id.unwrap_or_default());
    println!("Name: {}", info.name.unwrap_or_default());
    println!("State: {:?}", info.state);

    Ok(())
}
```

## 6. パフォーマンス最適化

### バッチ操作

```rust
// ✅ 良い例：バッチで処理
let containers = docker.list_containers(options).await?;
for container in containers {
    // 処理
}
```

```rust
// ❌ 悪い例：1つずつ問い合わせ
for id in container_ids {
    let container = docker.inspect_container(&id, None).await?;
    // 処理
}
```

### フィルタの活用

```rust
use std::collections::HashMap;

// Docker側でフィルタ（効率的）
let mut filters = HashMap::new();
filters.insert("label", vec!["com.docker.compose.project=myproject"]);

let containers = docker.list_containers(Some(ListContainersOptions {
    all: true,
    filters,
    ..Default::default()
})).await?;
```

## 7. テスト

### モックの使用

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_create_container() {
        // テスト用のコンテナ作成
        let docker = Docker::connect_with_local_defaults().unwrap();

        let config = Config {
            image: Some("alpine:latest".to_string()),
            ..Default::default()
        };

        let options = CreateContainerOptions {
            name: "test-container",
            ..Default::default()
        };

        let response = docker.create_container(Some(options), config).await.unwrap();

        // クリーンアップ
        docker.remove_container(&response.id, Some(RemoveContainerOptions {
            force: true,
            ..Default::default()
        })).await.unwrap();
    }
}
```

### テスト後のクリーンアップ

```rust
use tempfile::TempDir;

#[tokio::test]
async fn test_with_cleanup() -> Result<()> {
    let docker = Docker::connect_with_local_defaults()?;
    let container_name = "test-cleanup";

    // コンテナ作成・テスト...

    // 確実にクリーンアップ
    let _ = docker.remove_container(
        container_name,
        Some(RemoveContainerOptions { force: true, ..Default::default() })
    ).await;

    Ok(())
}
```

## 8. セキュリティ

### 環境変数の安全な扱い

```rust
// ✅ 良い例：環境変数からシークレットを読み込む
let password = std::env::var("DB_PASSWORD")
    .context("DB_PASSWORD環境変数が設定されていません")?;

let config = Config {
    env: Some(vec![format!("POSTGRES_PASSWORD={}", password)]),
    ..Default::default()
};
```

```rust
// ❌ 悪い例：ハードコード
let config = Config {
    env: Some(vec!["POSTGRES_PASSWORD=hardcoded_password".to_string()]),
    ..Default::default()
};
```

### ボリュームの権限

```rust
// 読み取り専用マウント
let config = Config {
    host_config: Some(HostConfig {
        binds: Some(vec![
            "/host/path:/container/path:ro".to_string(), // :ro = 読み取り専用
        ]),
        ..Default::default()
    }),
    ..Default::default()
};
```

## まとめ

FleetFlowでBollardを使う際の重要なポイント：

1. **接続の再利用** - Docker接続インスタンスを使い回す
2. **適切なエラーハンドリング** - ステータスコードで分岐
3. **非同期処理の活用** - Tokioで効率的な並列実行
4. **リソース管理** - 適切なクリーンアップとタイムアウト
5. **ロギング** - デバッグ情報の適切な記録
6. **パフォーマンス** - バッチ処理とフィルタの活用
7. **テスタビリティ** - テスト後のクリーンアップ
8. **セキュリティ** - シークレットの安全な扱い
