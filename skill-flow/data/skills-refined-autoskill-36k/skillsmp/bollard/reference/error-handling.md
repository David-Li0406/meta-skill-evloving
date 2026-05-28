# Bollardエラーハンドリング

## エラータイプ

Bollardの主なエラーは`bollard::errors::Error`として返されます。

```rust
use bollard::errors::Error;
```

## 主なHTTPステータスコード

### 404 Not Found

イメージやコンテナが見つからない場合：

```rust
match docker.create_container(options, config).await {
    Err(Error::DockerResponseServerError {
        status_code: 404,
        message,
    }) => {
        println!("Image not found: {}", message);
        // イメージをpull
    }
    Ok(response) => { /* ... */ }
    Err(e) => { /* ... */ }
}
```

### 409 Conflict

コンテナが既に存在する場合：

```rust
match docker.create_container(options, config).await {
    Err(Error::DockerResponseServerError {
        status_code: 409,
        message,
    }) => {
        println!("Container already exists: {}", message);
        // 既存コンテナを起動
    }
    Ok(response) => { /* ... */ }
    Err(e) => { /* ... */ }
}
```

### 500 Internal Server Error

サーバーエラー（ポート競合、リソース不足など）：

```rust
match docker.start_container::<String>(&container_id, None).await {
    Err(Error::DockerResponseServerError {
        status_code: 500,
        message,
    }) => {
        eprintln!("Server error: {}", message);
        // ポート競合やリソース不足の可能性
    }
    Ok(_) => { /* ... */ }
    Err(e) => { /* ... */ }
}
```

## 包括的なエラーハンドリング

```rust
use bollard::errors::Error;

match docker.create_container(options, config).await {
    Ok(response) => {
        println!("Created: {}", response.id);
    }
    Err(Error::DockerResponseServerError { status_code, message }) => {
        match status_code {
            404 => println!("Not found: {}", message),
            409 => println!("Conflict: {}", message),
            500 => println!("Server error: {}", message),
            _ => println!("HTTP error {}: {}", status_code, message),
        }
    }
    Err(Error::DockerConnectionError { error }) => {
        eprintln!("Connection error: {}", error);
    }
    Err(e) => {
        eprintln!("Unexpected error: {}", e);
    }
}
```

## FleetFlowでの実装パターン

### 既存コンテナの処理

```rust
match docker.create_container(Some(create_options.clone()), container_config.clone()).await {
    Ok(response) => {
        println!("  ✓ コンテナ作成: {}", response.id);

        // コンテナ起動
        docker.start_container::<String>(&response.id, None).await?;
        println!("  ✓ 起動完了");
    }
    Err(bollard::errors::Error::DockerResponseServerError { status_code: 409, .. }) => {
        // コンテナが既に存在する場合
        println!("  ℹ コンテナは既に存在します");
        let container_name = &create_options.name;

        // 既存コンテナを起動
        match docker.start_container::<String>(container_name, None).await {
            Ok(_) => println!("  ✓ 既存コンテナを起動"),
            Err(e) => println!("  ⚠ 起動エラー: {}", e),
        }
    }
    Err(e) => {
        return Err(anyhow::anyhow!("コンテナ作成エラー: {}", e));
    }
}
```

### イメージ自動Pull

```rust
use bollard::image::CreateImageOptions;
use futures_util::stream::TryStreamExt;

match docker.create_container(options, config).await {
    Err(Error::DockerResponseServerError { status_code: 404, .. }) => {
        println!("イメージが見つかりません。pullします...");

        let image_options = Some(CreateImageOptions {
            from_image: "postgres",
            tag: "16",
            ..Default::default()
        });

        let mut stream = docker.create_image(image_options, None, None);
        while let Some(info) = stream.try_next().await? {
            if let Some(status) = info.status {
                println!("  {}", status);
            }
        }

        // 再度コンテナ作成を試行
        docker.create_container(options, config).await?
    }
    result => result?,
}
```

## エラーメッセージのカスタマイズ

```rust
use anyhow::{Context, Result};

async fn create_and_start_container(
    docker: &Docker,
    name: &str,
    config: Config<String>
) -> Result<String> {
    let options = CreateContainerOptions { name, ..Default::default() };

    let response = docker
        .create_container(Some(options), config)
        .await
        .with_context(|| format!("コンテナ '{}' の作成に失敗", name))?;

    docker
        .start_container::<String>(&response.id, None)
        .await
        .with_context(|| format!("コンテナ '{}' の起動に失敗", name))?;

    Ok(response.id)
}
```

## リトライロジック

```rust
use std::time::Duration;
use tokio::time::sleep;

async fn start_container_with_retry(
    docker: &Docker,
    container_id: &str,
    max_retries: u32
) -> Result<(), Error> {
    let mut retries = 0;

    loop {
        match docker.start_container::<String>(container_id, None).await {
            Ok(_) => return Ok(()),
            Err(e) if retries < max_retries => {
                retries += 1;
                eprintln!("起動失敗 (試行 {}/{}): {}", retries, max_retries, e);
                sleep(Duration::from_secs(2)).await;
            }
            Err(e) => return Err(e),
        }
    }
}
```
