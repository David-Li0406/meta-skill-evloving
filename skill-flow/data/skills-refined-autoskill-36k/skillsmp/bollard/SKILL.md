---
name: bollard
description: Rust製非同期Docker APIクライアント「Bollard」の使い方と実装パターン
tags: [docker, rust, async, container]
version: 1.0.0
---

# Bollard Skill

Rust製非同期Docker APIクライアント「Bollard」の実装ガイドです。

## 概要

**Bollard**は、Rust製の非同期Docker API クライアントライブラリです。
HyperとTokioを使用し、futuresとasync/awaitパラダイムで実装されています。

- **公式ドキュメント**: https://docs.rs/bollard/
- **GitHub**: https://github.com/fussybeaver/bollard
- **Docker API バージョン**: 1.49（最新）

## スキルの起動タイミング

このスキルは以下の場合に活用してください：

- ✅ Docker操作を実装する際
- ✅ コンテナ、イメージ、ボリューム、ネットワーク操作
- ✅ Bollardのエラーハンドリング
- ✅ Rustでコンテナ管理機能を実装する際
- ✅ Docker APIを使ったツール開発

## クイックリファレンス

### 基本的な接続

```rust
use bollard::Docker;

// OS固有のデフォルト設定で接続（推奨）
let docker = Docker::connect_with_local_defaults()?;
```

### コンテナ操作

```rust
use bollard::container::{Config, CreateContainerOptions};

// 作成
let response = docker.create_container(Some(options), config).await?;

// 起動
docker.start_container::<String>(&container_id, None).await?;

// 停止
docker.stop_container(&container_id, Some(StopContainerOptions { t: 10 })).await?;

// 削除
docker.remove_container(&container_id, Some(RemoveContainerOptions {
    force: true,
    v: true,
    ..Default::default()
})).await?;

// 一覧
let containers = docker.list_containers(Some(ListContainersOptions::<String> {
    all: true,
    ..Default::default()
})).await?;
```

### イメージ操作

```rust
use bollard::image::CreateImageOptions;
use futures_util::stream::TryStreamExt;

// Pull
let options = Some(CreateImageOptions {
    from_image: "postgres",
    tag: "16",
    ..Default::default()
});

let mut stream = docker.create_image(options, None, None);
while let Some(info) = stream.try_next().await? {
    println!("{:?}", info);
}
```

### エラーハンドリング

```rust
use bollard::errors::Error;

match docker.create_container(options, config).await {
    Ok(response) => { /* 成功 */ }
    Err(Error::DockerResponseServerError { status_code: 409, .. }) => {
        // コンテナが既に存在
    }
    Err(Error::DockerResponseServerError { status_code: 404, .. }) => {
        // イメージが見つからない
    }
    Err(e) => { /* その他のエラー */ }
}
```

## 実装パターン

### Docker Composeライクなラベル設定

```rust
use bollard::container::{Config, CreateContainerOptions};
use bollard::models::HostConfig;
use std::collections::HashMap;

let config = Config {
    image: Some("postgres:16".to_string()),
    labels: Some({
        let mut labels = HashMap::new();
        // Docker Compose互換のラベル
        labels.insert("com.docker.compose.project".to_string(),
                     format!("{}-{}", project_name, stage_name));
        labels.insert("com.docker.compose.service".to_string(),
                     service_name.to_string());
        // カスタムラベル
        labels.insert("app.project".to_string(), project_name.to_string());
        labels.insert("app.stage".to_string(), stage_name.to_string());
        labels
    }),
    host_config: Some(HostConfig {
        port_bindings: Some(port_bindings),
        binds: Some(volumes),
        ..Default::default()
    }),
    ..Default::default()
};

let options = CreateContainerOptions {
    name: format!("{}-{}-{}", project_name, stage_name, service_name),
    ..Default::default()
};
```

### エラーハンドリングと既存コンテナの処理

```rust
match docker.create_container(Some(create_options.clone()), config.clone()).await {
    Ok(response) => {
        println!("  ✓ コンテナ作成: {}", response.id);
        docker.start_container::<String>(&response.id, None).await?;
        println!("  ✓ 起動完了");
    }
    Err(bollard::errors::Error::DockerResponseServerError { status_code: 409, .. }) => {
        println!("  ℹ コンテナは既に存在します");
        match docker.start_container::<String>(&container_name, None).await {
            Ok(_) => println!("  ✓ 既存コンテナを起動"),
            Err(e) => println!("  ⚠ 起動エラー: {}", e),
        }
    }
    Err(e) => {
        return Err(anyhow::anyhow!("コンテナ作成エラー: {}", e));
    }
}
```

## ベストプラクティス

### 1. 接続の再利用

Docker接続インスタンスは複数の操作で再利用できます：

```rust
let docker = Docker::connect_with_local_defaults()?;

// 同じインスタンスを使い回す
docker.create_container(...).await?;
docker.start_container(...).await?;
docker.list_containers(...).await?;
```

### 2. エラーの詳細な分類

ステータスコードで適切にハンドリング：

```rust
match result {
    Err(Error::DockerResponseServerError { status_code: 404, .. }) => {
        // イメージが見つからない → pull
    }
    Err(Error::DockerResponseServerError { status_code: 409, .. }) => {
        // 既に存在 → 起動試行
    }
    Err(Error::DockerResponseServerError { status_code: 500, .. }) => {
        // サーバーエラー（ポート競合など）
    }
    Ok(result) => { /* 成功 */ }
    Err(e) => { /* その他 */ }
}
```

### 3. 非同期処理の適切な使用

```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let docker = Docker::connect_with_local_defaults()?;
    let containers = docker.list_containers(None).await?;
    Ok(())
}
```

## 詳細リファレンス

詳細な実装例とパターンについては、以下のリファレンスを参照してください：

- [基本操作](reference/basic-operations.md) - コンテナ、イメージ、ボリューム、ネットワーク操作
- [エラーハンドリング](reference/error-handling.md) - エラーの種類と処理パターン
- [ベストプラクティス](reference/best-practices.md) - パフォーマンスと保守性の向上

## 外部リンク

- [Bollard公式ドキュメント](https://docs.rs/bollard/)
- [Docker Engine API](https://docs.docker.com/engine/api/)
- [Tokio非同期ランタイム](https://tokio.rs/)

## よくある実装機能

Bollardを使って実装できる機能：

- イメージの自動pull
- コンテナログのストリーミング表示
- ヘルスチェック
- 依存関係順の起動制御
- リソース制限設定
- ネットワーク自動作成・管理
- ボリューム自動管理
