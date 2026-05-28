# CLIコマンドリファレンス

FleetFlowのCLIコマンド一覧と詳細な使い方です。

## コマンド一覧

| コマンド | 説明 |
|---------|------|
| `up` | ステージを起動 |
| `down` | ステージを停止・削除 |
| `deploy` | CI/CD向けデプロイ |
| `ps` | コンテナ一覧 |
| `logs` | ログ表示 |
| `start` | 停止中のサービスを起動 |
| `stop` | サービスを停止 |
| `restart` | サービスを再起動 |
| `build` | イメージをビルド |
| `validate` | 設定を検証 |
| `setup` | ステージの環境をセットアップ |
| `play` | Playbookを実行 |
| `cloud` | クラウドインフラ管理 |
| `mcp` | MCPサーバーを起動 |
| `self-update` | FleetFlow自体を更新 |
| `version` | バージョン表示 |

## 環境変数

| 変数 | 説明 |
|------|------|
| `FLEET_STAGE` | ステージ名を指定（local, dev, pre, live） |
| `FLEETFLOW_CONFIG_PATH` | 設定ファイルの直接パス指定 |
| `CLOUDFLARE_API_TOKEN` | Cloudflare APIトークン（DNS自動管理用） |
| `CLOUDFLARE_ZONE_ID` | Cloudflare Zone ID（DNS自動管理用） |
| `CLOUDFLARE_DOMAIN` | 管理対象ドメイン |

## 詳細

### `fleet up`

指定したステージのコンテナを起動します。

```bash
fleet up -s <stage>
fleet up -s local
fleet up -s local --pull        # イメージを事前にpull
fleet up -s local --build       # ビルドしてから起動
fleet up -s local --build --no-cache  # キャッシュなしでビルド
```

**オプション**:

| オプション | 短縮 | 説明 |
|-----------|------|------|
| `--stage` | `-s` | ステージ名（必須、または`FLEET_STAGE`で指定） |
| `--pull` | | 起動前にイメージをpull |
| `--build` | | 起動前にイメージをビルド |
| `--no-cache` | | キャッシュを使わずにビルド（`--build`と併用） |

**動作**:
1. 設定ファイルを読み込み
2. `--build`指定時はイメージをビルド
3. イメージが無ければ自動pull
4. 依存関係順にコンテナを作成・起動
5. `wait_for`設定がある場合は依存サービスの準備を待機
6. サービスごとに進捗を表示

### `fleet down`

指定したステージのコンテナを停止・削除します。

```bash
fleet down -s <stage>
fleet down -s local
fleet down -s local --remove    # ボリュームも削除
```

**オプション**:

| オプション | 短縮 | 説明 |
|-----------|------|------|
| `--stage` | `-s` | ステージ名（必須、または`FLEET_STAGE`で指定） |
| `--remove` | `-r` | ボリュームも削除 |

**動作**:
1. コンテナを停止
2. コンテナを削除
3. `--remove`指定時のみボリュームを削除

### `fleet deploy`

CI/CDパイプラインからの自動デプロイに最適化されたコマンドです。

```bash
fleet deploy -s <stage> --yes
fleet deploy -s live --yes           # 確認なしでデプロイ
fleet deploy -s live --no-pull --yes # pullをスキップ
```

**オプション**:

| オプション | 短縮 | 説明 |
|-----------|------|------|
| `--stage` | `-s` | ステージ名（必須） |
| `--yes` | `-y` | 確認なしで実行（CI向け） |
| `--no-pull` | | イメージのpullをスキップ（デフォルトはpull） |

**動作**:
1. 既存コンテナを強制停止・削除
2. 最新イメージをpull（`--no-pull`でスキップ可能）
3. コンテナを依存関係順に作成・起動
4. `wait_for`による依存サービス待機

### `fleet ps`

コンテナの状態を表示します。

```bash
fleet ps                 # 実行中のコンテナのみ
fleet ps -s local        # 特定ステージのみ
fleet ps --all           # 停止中も含む
```

**オプション**:

| オプション | 短縮 | 説明 |
|-----------|------|------|
| `--stage` | `-s` | 特定ステージのみ表示 |
| `--all` | `-a` | 停止中のコンテナも表示 |

**表示内容**:
- コンテナ名
- 状態（Running/Stopped）
- ポートマッピング

### `fleet logs`

コンテナのログを表示します。

```bash
fleet logs -s <stage>             # 全サービス
fleet logs -s local -n <service>  # 特定サービス
fleet logs -s local -f            # リアルタイム表示
fleet logs -s local --lines 100   # 行数指定
fleet logs -s local -f -n web     # 組み合わせ
```

**オプション**:

| オプション | 短縮 | 説明 |
|-----------|------|------|
| `--stage` | `-s` | ステージ名 |
| `--name` | `-n` | サービス名 |
| `--follow` | `-f` | リアルタイムで追従 |
| `--lines` | | 表示する行数（デフォルト: 100） |

### `flow start`

停止中のサービスを起動します（コンテナは既に存在している場合）。

```bash
flow start -s <stage>              # ステージ内の全サービス
flow start -s <stage> -n <service> # 特定サービスのみ
flow start -s local -n db
```

**オプション**:

| オプション | 短縮 | 説明 |
|-----------|------|------|
| `--stage` | `-s` | ステージ名（必須） |
| `--name` | `-n` | サービス名 |

**動作**:
- `docker start` 相当
- コンテナが存在しない場合はエラー

### `flow stop`

サービスを停止します（コンテナは保持）。

```bash
flow stop -s <stage>              # ステージ内の全サービス
flow stop -s <stage> -n <service> # 特定サービスのみ
flow stop -s local -n db
```

**オプション**:

| オプション | 短縮 | 説明 |
|-----------|------|------|
| `--stage` | `-s` | ステージ名（必須） |
| `--name` | `-n` | サービス名 |

**動作**:
- `docker stop` 相当
- コンテナは削除されない
- `start` で再起動可能

### `fleet restart`

サービスを再起動します。

```bash
fleet restart -s <stage>              # ステージ内の全サービス
fleet restart -s <stage> -n <service> # 特定サービスのみ
fleet restart -s local -n web
```

**オプション**:

| オプション | 短縮 | 説明 |
|-----------|------|------|
| `--stage` | `-s` | ステージ名（必須） |
| `--name` | `-n` | サービス名 |

**動作**:
- `docker restart` 相当
- 停止 → 起動を実行

### `fleet build`

イメージをビルドします（コンテナは起動しない）。

```bash
fleet build -s <stage>                   # ステージ内の全サービス
fleet build -s <stage> -n <service>      # 特定サービスのみ
fleet build -s local -n api
fleet build -s local --no-cache          # キャッシュなしでビルド

# レジストリにプッシュ
fleet build -s local -n api --push
fleet build -s local -n api --push --tag v1.0.0

# クロスビルド
fleet build -s local -n api --push --platform linux/amd64
```

**オプション**:

| オプション | 短縮 | 説明 |
|-----------|------|------|
| `--stage` | `-s` | ステージ名（必須） |
| `--name` | `-n` | サービス名 |
| `--no-cache` | | キャッシュを使わずにビルド |
| `--push` | | ビルド後にレジストリへプッシュ |
| `--tag` | | イメージタグを指定（`--push`と併用） |
| `--platform` | | ターゲットプラットフォーム（クロスビルド用） |

**プッシュ時の認証**:

Docker標準の認証方式を使用：
- `~/.docker/config.json` から認証情報を取得
- credential helper（osxkeychain, desktop）も自動対応
- 環境変数 `DOCKER_CONFIG` でパスをカスタマイズ可能

**タグ解決の優先順位**:
1. `--tag` CLIオプション
2. KDL設定の `image` フィールドのタグ
3. デフォルト: `latest`

### `fleet validate`

設定ファイルの構文チェックを行います。

```bash
fleet validate
fleet validate -s local    # 特定ステージを検証
```

**オプション**:

| オプション | 短縮 | 説明 |
|-----------|------|------|
| `--stage` | `-s` | 特定ステージを検証 |

**チェック内容**:
- KDL構文エラー
- 必須フィールドの欠落（image等）
- 論理的な矛盾

### `fleet setup`

ステージの環境をセットアップします（冪等）。

```bash
fleet setup -s <stage>
fleet setup -s dev
```

**オプション**:

| オプション | 短縮 | 説明 |
|-----------|------|------|
| `--stage` | `-s` | ステージ名（必須） |

**動作**:
- 必要なディレクトリやボリュームの作成
- 設定ファイルの配置
- 冪等性を保証（何度実行しても同じ結果）

### `flow play`

Playbookを実行します。リモートサーバーでのサービス起動などに使用します。

```bash
flow play <playbook>
flow play deploy-live.kdl
```

### `flow cloud`

クラウドインフラを管理します。

```bash
# クラウド環境を構築
flow cloud up -s <stage>
flow cloud up -s dev --yes  # 確認をスキップ

# クラウド環境を削除
flow cloud down -s <stage>
flow cloud down -s dev --yes

# サーバー操作
flow cloud server list
flow cloud server create --name my-server
flow cloud server delete --name my-server --yes
flow cloud server start --name my-server
flow cloud server stop --name my-server

# 認証確認
flow cloud auth
```

**サブコマンド**:

| サブコマンド | 説明 |
|-------------|------|
| `up` | クラウド環境を構築（サーバー作成 + DNS設定） |
| `down` | クラウド環境を削除（サーバー削除 + DNS削除） |
| `server list` | サーバー一覧 |
| `server create` | サーバー作成 |
| `server delete` | サーバー削除 |
| `server start` | サーバー起動 |
| `server stop` | サーバー停止 |
| `auth` | 認証状態を確認 |

**オプション**:

| オプション | 説明 |
|-----------|------|
| `--stage` | 対象のステージ名 |
| `--yes` | 確認をスキップ |
| `--name` | サーバー名 |

**DNS自動管理**:

環境変数が設定されている場合、`cloud up`/`cloud down`時にDNSレコードを自動管理：

| 環境変数 | 説明 |
|---------|------|
| `CLOUDFLARE_API_TOKEN` | Cloudflare APIトークン |
| `CLOUDFLARE_ZONE_ID` | ドメインのZone ID |
| `CLOUDFLARE_DOMAIN` | 管理対象ドメイン |

### `fleet mcp`

Model Context Protocol (MCP) サーバーを起動します。

```bash
fleet mcp
```

AI/LLMアシスタントとの連携に使用します。

### `fleet self-update`

FleetFlow自体を最新バージョンに更新します。

```bash
fleet self-update
```

### `fleet version`

バージョン情報を表示します。

```bash
fleet version
# 出力: fleetflow 0.4.2
```

## 終了コード

| コード | 説明 |
|--------|------|
| 0 | 成功 |
| 1 | 一般エラー |
| 2 | 設定エラー |

## トラブルシューティング

### 設定ファイルが見つからない

```
エラー: Flow設定ファイルが見つかりません
```

**解決方法**:
1. カレントディレクトリに`fleet.kdl`があるか確認
2. 環境変数`FLEETFLOW_CONFIG_PATH`を確認
3. `fleet validate`で検証

### イメージが見つからない

```
エラー: イメージが見つかりません: xxx:yyy
```

**解決方法**:
1. イメージ名とタグが正しいか確認
2. 手動でpull: `docker pull image:tag`
3. プライベートレジストリの認証を確認

### ポートが使用中

```
エラー: ポート xxxx は既に使用されています
```

**解決方法**:
1. 他のコンテナを確認: `docker ps`
2. ホストのプロセスを確認: `lsof -i :xxxx`
3. fleet.kdlで別のポート番号を指定

### コンテナが起動しない

**解決方法**:
1. ログを確認: `fleet logs -s <stage>` または `docker logs {container}`
2. 環境変数が正しいか確認
3. ボリュームマウントのパスを確認
4. コマンドが正しいか確認

### ビルドが失敗する

```
エラー: ビルドに失敗しました
```

**解決方法**:
1. Dockerfileのパスが正しいか確認
2. ビルドコンテキストが正しいか確認
3. `.dockerignore`で必要なファイルが除外されていないか確認
4. `--no-cache`でキャッシュをクリアしてリビルド

### プッシュが失敗する

```
エラー: プッシュに失敗しました
```

**解決方法**:
1. レジストリへのログインを確認: `docker login <registry>`
2. `~/.docker/config.json` に認証情報があるか確認
3. 認証情報の有効期限を確認（特にGHCR、ECRなど）
4. イメージ名がレジストリの形式に合っているか確認:
   - GHCR: `ghcr.io/owner/image:tag`
   - Docker Hub: `username/image:tag`
   - ECR: `123456789.dkr.ecr.region.amazonaws.com/image:tag`
