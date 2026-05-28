---
name: kubectl-localmesh-envoy-protocols
description: kubectl-localmeshにおけるEnvoy HTTPプロトコル設定の実装パターンとトラブルシューティング
allowed-tools: ["Bash", "Read", "Glob"]
---

# kubectl-localmesh Envoy プロトコル設定

このskillは、kubectl-localmeshにおけるEnvoy HTTPプロトコル設定の実装パターンとトラブルシューティングを支援します。

## 対象プロジェクト

- kubectl-localmesh
- EnvoyベースのHTTP/gRPCプロキシ

## HTTPプロトコルオプションの理解

kubectl-localmeshでは、Envoyの`typed_extension_protocol_options`を使用して、各サービスのHTTPプロトコルバージョンを制御します。

### HTTP/1.1設定（protocol: http）

```yaml
typed_extension_protocol_options:
  envoy.extensions.upstreams.http.v3.HttpProtocolOptions:
    "@type": "type.googleapis.com/envoy.extensions.upstreams.http.v3.HttpProtocolOptions"
    explicit_http_config:
      http_protocol_options: {}
```

**用途:**
- 従来のREST API
- HTTP/1.1のみ対応のレガシーシステム
- HTTP/2に対応していないサービス

### HTTP/2設定（protocol: http2）

```yaml
typed_extension_protocol_options:
  envoy.extensions.upstreams.http.v3.HttpProtocolOptions:
    "@type": "type.googleapis.com/envoy.extensions.upstreams.http.v3.HttpProtocolOptions"
    explicit_http_config:
      http2_protocol_options: {}
```

**用途:**
- HTTP/2対応のモダンなHTTP API
- パフォーマンス重視（多重化、ヘッダー圧縮）
- h2c（HTTP/2 cleartext）対応サービス

### gRPC設定（protocol: grpc）

gRPCはHTTP/2を必須とするため、`protocol: grpc`は内部的に`http2_protocol_options`を使用します。

**重要なポイント:**
- `http_protocol_options`と`http2_protocol_options`は排他的（同時使用不可）
- `explicit_http_config`で明示的にプロトコルを指定
- gRPCサービスは必ずHTTP/2が必要

## protocol設定の使い分け

services.yamlでの設定とEnvoyの動作:

| protocol値 | Envoy設定 | 対象サービス |
|-----------|----------|------------|
| `http` | `http_protocol_options` | HTTP/1.1専用REST API |
| `http2` | `http2_protocol_options` | HTTP/2対応HTTP API |
| `grpc` | `http2_protocol_options` | gRPCサービス |

### デフォルト動作

- `protocol`を省略した場合、デフォルトは`http`（HTTP/1.1）
- 明示的に指定することを推奨

### 設定例

```yaml
services:
  # HTTP/1.1専用サービス（レガシーAPI）
  - kind: kubernetes
    host: legacy-api.localhost
    namespace: default
    service: legacy-api
    protocol: http

  # HTTP/2対応モダンAPI
  - kind: kubernetes
    host: modern-api.localhost
    namespace: default
    service: modern-api
    protocol: http2

  # gRPCサービス
  - kind: kubernetes
    host: grpc-api.localhost
    namespace: default
    service: grpc-api
    protocol: grpc
```

## サービス互換性の判断

新しいサービスを追加する際のプロトコル選択方法:

### HTTP/1.1のみ対応のサービスの見分け方

```bash
# 1. まずHTTP/1.1で接続テスト
curl -v http://localhost:<port>/health

# 2. HTTP/2で接続テスト
curl -v --http2-prior-knowledge http://localhost:<port>/health

# HTTP/2で接続できない場合 → protocol: http
```

### HTTP/2対応の確認方法

```bash
# HTTP/2対応サービスは両方成功する
curl -v http://localhost:<port>/health                        # 成功
curl -v --http2-prior-knowledge http://localhost:<port>/health  # 成功

# この場合 → protocol: http2 が使用可能
```

### gRPCサービスの識別

```bash
# grpcurlでサービスリスト取得
grpcurl -plaintext localhost:<port> list

# gRPCサービスの場合 → protocol: grpc
```

### プロトコル選択の決定フロー

```
サービスを追加する
  ↓
gRPCサービスか？
  Yes → protocol: grpc
  No → ↓
HTTP/2に対応しているか？
  Yes → protocol: http2 （パフォーマンス重視）
  No → protocol: http （互換性重視）
```

## 実装パターン

internal/envoy/config.goでの実装パターン:

### Route構造体

```go
type Route struct {
    Host        string
    LocalPort   int
    ClusterName string
    Type        string   // "http" or "tcp" (サービス分類)
    Protocol    string   // "http" | "http2" | "grpc" (HTTPプロトコルバージョン)
    ListenPort  int      // TCP用
}
```

### プロトコルオプションの組み込み

```go
// HTTP/gRPCサービスの場合
if r.Type != "tcp" {
    var httpConfig map[string]any

    if r.Protocol == "grpc" || r.Protocol == "http2" {
        // gRPC / HTTP/2: HTTP/2（h2c）
        httpConfig = map[string]any{
            "http2_protocol_options": map[string]any{},
        }
    } else {
        // HTTP/1.1（デフォルト、protocol: http または未指定）
        httpConfig = map[string]any{
            "http_protocol_options": map[string]any{},
        }
    }

    cluster["typed_extension_protocol_options"] = map[string]any{
        "envoy.extensions.upstreams.http.v3.HttpProtocolOptions": map[string]any{
            "@type": "type.googleapis.com/envoy.extensions.upstreams.http.v3.HttpProtocolOptions",
            "explicit_http_config": httpConfig,
        },
    }
}
```

### 設計のポイント

- `Type`フィールド: サービスの分類（http vs tcp）
- `Protocol`フィールド: HTTPプロトコルバージョン（http vs http2 vs grpc）
- 分離することで、TCP、HTTP/1.1、HTTP/2、gRPCを明確に区別

## よくあるエラーと解決策

### 502 Bad Gateway with "protocol error"

**症状:**
```
$ curl http://users-api.localhost/health
502 Bad Gateway
```

Envoyログに`protocol error`が記録される。

**原因:**
HTTP/1.1のみ対応のサービスに対して、EnvoyがHTTP/2で接続しようとしている。

**診断方法:**

1. Envoy設定をダンプ:
```bash
kubectl localmesh dump-envoy-config -f services.yaml > /tmp/envoy-config.yaml
```

2. 問題のclusterを検索:
```bash
grep -A 20 "name: <cluster_name>" /tmp/envoy-config.yaml
```

3. `http2_protocol_options`が使用されているか確認:
```yaml
# HTTP/2が設定されている場合、以下が含まれる
explicit_http_config:
  http2_protocol_options: {}
```

**解決策:**

services.yamlで`protocol: http`に変更:

```yaml
services:
  - kind: kubernetes
    host: users-api.localhost
    namespace: users
    service: users-api
    protocol: http  # http2 → http に変更
```

### gRPC接続エラー

**症状:**
```bash
$ grpcurl -plaintext grpc-api.localhost list
Failed to dial target host "grpc-api.localhost:80": ...
```

**原因:**
`protocol: http2`を使用している（gRPC特有の設定が不足）。

**診断方法:**

services.yamlの設定を確認:
```bash
grep -A 5 "host: grpc-api.localhost" services.yaml
```

`protocol: http2`になっている場合、これが原因。

**解決策:**

`protocol: grpc`に変更:

```yaml
services:
  - kind: kubernetes
    host: grpc-api.localhost
    namespace: default
    service: grpc-api
    protocol: grpc  # http2 → grpc に変更
```

### Envoy起動失敗（プロトコル設定関連）

**症状:**
```
error initializing configuration: no such field: 'http1_protocol_options'
```

**原因:**
無効なフィールド名を使用（正しくは`http_protocol_options`）。

**解決策:**

internal/envoy/config.goで正しいフィールド名を使用:

```go
// 誤り
httpConfig = map[string]any{
    "http1_protocol_options": map[string]any{},  // ❌
}

// 正しい
httpConfig = map[string]any{
    "http_protocol_options": map[string]any{},   // ✅
}
```

## デバッグワークフロー

プロトコル関連の問題を診断する手順:

### 1. Envoy設定のダンプ

```bash
kubectl localmesh dump-envoy-config -f services.yaml > /tmp/envoy-config.yaml
```

### 2. cluster設定の確認

問題のサービスに対応するclusterを検索:

```bash
# clusterセクションを表示
grep -A 30 "clusters:" /tmp/envoy-config.yaml

# 特定のclusterを検索
grep -A 20 "name: <cluster_name>" /tmp/envoy-config.yaml
```

### 3. typed_extension_protocol_optionsの検証

```bash
# プロトコルオプションを確認
grep -A 10 "typed_extension_protocol_options" /tmp/envoy-config.yaml
```

期待される構造:

```yaml
typed_extension_protocol_options:
  envoy.extensions.upstreams.http.v3.HttpProtocolOptions:
    "@type": "type.googleapis.com/envoy.extensions.upstreams.http.v3.HttpProtocolOptions"
    explicit_http_config:
      http_protocol_options: {}      # HTTP/1.1の場合
      # または
      http2_protocol_options: {}     # HTTP/2の場合
```

### 4. プロトコルオプションの確認

- `http_protocol_options`が存在 → HTTP/1.1設定
- `http2_protocol_options`が存在 → HTTP/2設定
- どちらも存在しない → 設定エラー

### 5. 設定修正と再試行

services.yamlの`protocol`フィールドを修正し、再起動:

```bash
# 設定を修正（エディタで編集）

# 再起動
sudo kubectl localmesh up -f services.yaml
```

## 使用方法（ユースケース別）

### ケース1: 502エラーが発生した場合

```bash
# 1. Envoy設定をダンプ
kubectl localmesh dump-envoy-config -f services.yaml > /tmp/envoy-config.yaml

# 2. 問題のclusterを検索
grep -A 20 "<cluster_name>" /tmp/envoy-config.yaml

# 3. http2_protocol_optionsが使用されているか確認
# → あればHTTP/1.1のみ対応のサービスの可能性

# 4. services.yamlでprotocol: httpに変更
vi services.yaml  # protocol: http2 → protocol: http

# 5. 再起動して確認
sudo kubectl localmesh up -f services.yaml
curl http://<service-name>.localhost/health
```

### ケース2: gRPC接続が失敗する場合

```bash
# 設定でprotocol: grpcが指定されているか確認
grep -A 5 "host: <service-name>" services.yaml

# protocol: http2になっている場合 → protocol: grpcに変更
vi services.yaml  # protocol: http2 → protocol: grpc

# 再起動
sudo kubectl localmesh up -f services.yaml

# gRPCクライアントでテスト
grpcurl -plaintext <service-name>.localhost list
```

### ケース3: 新しいサービスを追加する際のプロトコル選択

```bash
# 1. kubectl port-forwardで直接アクセスしてテスト
kubectl port-forward -n <namespace> svc/<service> 8080:80 &

# 2. HTTP/1.1で接続
curl -v http://localhost:8080/health

# 3. HTTP/2で接続
curl -v --http2-prior-knowledge http://localhost:8080/health

# 4. 結果に基づいて設定
# - HTTP/1.1のみ成功 → protocol: http
# - 両方成功 → protocol: http2
# - gRPCサービス → protocol: grpc

# 5. services.yamlに追加
cat >> services.yaml <<EOF
  - kind: kubernetes
    host: <service-name>.localhost
    namespace: <namespace>
    service: <service>
    protocol: http  # または http2, grpc
EOF
```

## 関連リソース

- **kubectl-envoy-debugging skill**: Envoy設定のデバッグツール
  - 設定ダンプ（`dump-envoy-config`）
  - オフラインモード（`--mock-config`）
  - デバッグログ（`--log-level debug`）

- **README.md**: Protocol Selection Guide
  - プロトコル選択の概要
  - ユーザー向けの使い方ガイド

- **internal/envoy/config.go**: 実装コード
  - `BuildConfig()`関数
  - `Route`構造体
  - プロトコルオプション生成ロジック

- **Envoy公式ドキュメント**:
  - [HTTP Protocol Options](https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/upstreams/http/v3/http_protocol_options.proto)
  - [HTTP/2 Protocol Options](https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/core/v3/protocol.proto#config-core-v3-http2protocoloptions)
