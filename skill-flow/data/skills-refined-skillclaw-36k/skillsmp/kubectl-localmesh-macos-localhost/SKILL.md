---
name: kubectl-localmesh-macos-localhost
description: macOSにおける.localhostドメインの特殊な挙動と、TCPサービス設定時の注意点を提供します
allowed-tools: ["Bash", "Read"]
---

# macOSにおける.localhostドメインの挙動

このskillは、macOSが`.localhost`ドメインを特別に扱う挙動と、kubectl-localmeshのTCPサービス設定への影響について説明します。

## 概要

macOSはRFC 6761に基づき、`.localhost` TLDを予約済みドメインとして特別扱いします。
その結果、`.localhost`のサブドメインは**`/etc/hosts`の設定を無視**して、常に`127.0.0.1`または`::1`に解決されます。

## 問題が発生するケース

### TCPサービス（DB接続など）で.localhostを使用した場合

```yaml
# 設定ファイル（services.yaml）
services:
  - kind: tcp
    host: db.localhost      # ← これは動かない
    ssh_bastion: primary
    target_host: 10.0.0.1
    target_port: 5432
```

**期待される動作**:
- kubectl-localmeshが`/etc/hosts`に`127.0.0.2 db.localhost`を追加
- クライアントが`db.localhost:5432`に接続
- `127.0.0.2:5432`（Envoy）に到達

**実際の動作（macOS）**:
- `/etc/hosts`に`127.0.0.2 db.localhost`が追加される
- クライアントが`db.localhost:5432`に接続
- **macOSが`/etc/hosts`を無視**し、`127.0.0.1:5432`に接続しようとする
- Envoyは`127.0.0.2:5432`でリッスンしているため接続失敗

## 確認方法

```bash
# /etc/hostsの内容を確認
$ cat /etc/hosts | grep db
127.0.0.2 db.localhost

# macOSのDNS解決を確認
$ python3 -c "import socket; print(socket.gethostbyname('db.localhost'))"
127.0.0.1

# pingでも確認可能
$ ping -c 1 db.localhost
PING localhost (127.0.0.1): 56 data bytes
```

`/etc/hosts`には`127.0.0.2`と書いてあるのに、`127.0.0.1`に解決されているのが問題です。

## 解決方法

### TCPサービスには.localhost以外のTLDを使用する

```yaml
# OK: .localdomain を使用
services:
  - kind: tcp
    host: db.localdomain   # ← これは動く
    ssh_bastion: primary
    target_host: 10.0.0.1
    target_port: 5432
```

### 推奨TLD

| TLD | 説明 |
|-----|------|
| `.localdomain` | 一般的なローカル用TLD |
| `.local` | mDNS/Bonjourでも使用されるが、/etc/hostsが優先される |
| `.dev` | 開発用（ただしHTTPS強制される場合あり） |
| `.test` | RFC 2606で予約されたテスト用TLD |

### 自動警告

kubectl-localmeshは、TCPサービスで`.localhost`ドメインが使用された場合、起動時に警告を出力します：

```
Warning: TCP service 'db.localhost' uses .localhost domain (db.localhost)
  macOS ignores /etc/hosts for .localhost subdomains and resolves them to 127.0.0.1
  This may cause connection failures. Consider using .localdomain or another TLD instead.
```

## なぜHTTP/gRPCサービスは.localhostで動くのか

HTTP/gRPCサービスは仕組みが異なります：

- Envoyが`0.0.0.0:80`（全インターフェース）でリッスン
- ホストヘッダー（`Host: users-api.localhost`）でルーティング
- macOSが`.localhost`を`127.0.0.1`に解決しても、`127.0.0.1:80`でEnvoyに到達
- Envoyがホストヘッダーを見て正しいバックエンドにルーティング

**結論**: HTTP/gRPCは`.localhost`で問題なし、TCPは`.localhost`を避けること

## 技術的背景

### RFC 6761 - Special-Use Domain Names

RFC 6761は、以下のドメインを「特別な用途」として定義しています：

- `.localhost` - ローカルホスト用
- `.invalid` - 明らかに無効なドメイン
- `.test` - テスト用
- `.example` - ドキュメント例示用

### macOSの実装

macOS（Darwin）は、`localhost`およびその全てのサブドメインを、DNSクエリやhostsファイル参照なしに、直接`127.0.0.1`/`::1`に解決します。

これはセキュリティ上の理由（DNSリバインディング攻撃の防止など）からの設計判断です。

## 診断コマンド

```bash
# /etc/hostsの確認
cat /etc/hosts

# macOSのDNS解決確認
python3 -c "import socket; print(socket.gethostbyname('your-host.localhost'))"

# dscacheutilでの確認
dscacheutil -q host -a name your-host.localhost

# Envoyのリッスン状態確認
sudo lsof -i :5432

# loopbackエイリアス確認
ifconfig lo0 | grep inet
```

## 参考情報

- [RFC 6761 - Special-Use Domain Names](https://www.rfc-editor.org/rfc/rfc6761)
- [macOS Network Configuration](https://developer.apple.com/documentation/systemconfiguration)

## 関連Skills

- `kubectl-localmesh-operations`: 起動・運用全般
- `kubectl-envoy-debugging`: Envoy設定のデバッグ
