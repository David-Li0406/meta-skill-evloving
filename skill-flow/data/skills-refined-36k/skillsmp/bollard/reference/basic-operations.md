# Bollard基本操作

## 接続

### OS固有のデフォルト設定で接続（推奨）

```rust
use bollard::Docker;

let docker = Docker::connect_with_local_defaults()?;
```

### その他の接続方法

```rust
// Unix socket
let docker = Docker::connect_with_socket_defaults()?;

// HTTP (DOCKER_HOST環境変数 or localhost:2375)
let docker = Docker::connect_with_http_defaults()?;

// SSL/TLS
let docker = Docker::connect_with_ssl_defaults()?;
```

## コンテナ操作

### 1. コンテナの作成

```rust
use bollard::container::{Config, CreateContainerOptions};
use bollard::models::HostConfig;
use std::collections::HashMap;

let config = Config {
    image: Some("postgres:16".to_string()),
    env: Some(vec![
        "POSTGRES_PASSWORD=postgres".to_string(),
    ]),
    exposed_ports: Some({
        let mut ports = HashMap::new();
        ports.insert("5432/tcp".to_string(), HashMap::new());
        ports
    }),
    host_config: Some(HostConfig {
        port_bindings: Some({
            let mut bindings = HashMap::new();
            bindings.insert(
                "5432/tcp".to_string(),
                Some(vec![PortBinding {
                    host_ip: Some("0.0.0.0".to_string()),
                    host_port: Some("11432".to_string()),
                }]),
            );
            bindings
        }),
        binds: Some(vec![
            "/path/to/data:/var/lib/postgresql/data:rw".to_string(),
        ]),
        ..Default::default()
    }),
    ..Default::default()
};

let options = CreateContainerOptions {
    name: "flow-postgres",
    platform: None,
};

let response = docker.create_container(Some(options), config).await?;
println!("Container ID: {}", response.id);
```

### 2. コンテナの起動

```rust
docker.start_container::<String>(&container_id, None).await?;
```

### 3. コンテナの停止

```rust
use bollard::container::StopContainerOptions;

docker.stop_container(
    &container_id,
    Some(StopContainerOptions { t: 10 }) // 10秒のタイムアウト
).await?;
```

### 4. コンテナの削除

```rust
use bollard::container::RemoveContainerOptions;

docker.remove_container(
    &container_id,
    Some(RemoveContainerOptions {
        force: true,    // 強制削除
        v: true,        // ボリュームも削除
        ..Default::default()
    })
).await?;
```

### 5. コンテナ一覧の取得

```rust
use bollard::container::ListContainersOptions;

let containers = docker.list_containers(
    Some(ListContainersOptions::<String> {
        all: true,  // 停止中も含む
        ..Default::default()
    })
).await?;

for container in containers {
    println!("Name: {:?}, Status: {}", container.names, container.status);
}
```

### 6. コンテナログの取得

```rust
use bollard::container::LogsOptions;
use futures_util::stream::TryStreamExt;

let options = Some(LogsOptions::<String> {
    stdout: true,
    stderr: true,
    follow: true,  // ストリーミング
    tail: "100",   // 最後の100行
    ..Default::default()
});

let mut stream = docker.logs(&container_id, options);

while let Some(log) = stream.try_next().await? {
    print!("{}", log);
}
```

## イメージ操作

### イメージのPull

```rust
use bollard::image::CreateImageOptions;
use futures_util::stream::TryStreamExt;

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

### イメージ一覧の取得

```rust
use bollard::image::ListImagesOptions;

let images = docker.list_images(
    Some(ListImagesOptions::<String> {
        all: true,
        ..Default::default()
    })
).await?;
```

## ボリューム操作

### ボリューム作成

```rust
use bollard::volume::CreateVolumeOptions;

let options = CreateVolumeOptions {
    name: "flow_postgres_data",
    driver: "local",
    ..Default::default()
};

let volume = docker.create_volume(options).await?;
```

### ボリューム削除

```rust
docker.remove_volume("flow_postgres_data", None).await?;
```

### ボリューム一覧

```rust
use bollard::volume::ListVolumesOptions;

let volumes = docker.list_volumes(None::<ListVolumesOptions<String>>).await?;
```

## ネットワーク操作

### ネットワーク作成

```rust
use bollard::network::CreateNetworkOptions;

let options = CreateNetworkOptions {
    name: "flow_network",
    driver: "bridge",
    ..Default::default()
};

let network = docker.create_network(options).await?;
```

### ネットワーク削除

```rust
docker.remove_network("flow_network").await?;
```

### ネットワーク一覧

```rust
use bollard::network::ListNetworksOptions;

let networks = docker.list_networks(None::<ListNetworksOptions<String>>).await?;
```
