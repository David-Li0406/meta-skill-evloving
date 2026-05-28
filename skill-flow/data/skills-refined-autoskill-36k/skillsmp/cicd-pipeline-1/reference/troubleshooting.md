# CI/CD トラブルシューティング

## 目次
- ビルド失敗
- テスト失敗
- デプロイ失敗
- パフォーマンス問題
- 権限・認証エラー

## ビルド失敗

### 依存関係エラー

**症状**: `npm ci` や `pip install` が失敗

```bash
# npm: package-lock.json と package.json の不整合
npm ci
# エラー: npm ERR! `npm ci` can only install packages when...

# 解決
rm package-lock.json
npm install
git add package-lock.json
```

```bash
# pip: 依存関係の競合
pip install -r requirements.txt
# エラー: ERROR: Cannot install...

# 解決: pip-tools で依存解決
pip install pip-tools
pip-compile requirements.in
pip-sync requirements.txt
```

### メモリ不足

**症状**: ビルドプロセスがkillされる

```yaml
# GitHub Actions: larger runner
jobs:
  build:
    runs-on: ubuntu-latest-8-cores  # より大きなランナー
```

```yaml
# Node.js: ヒープサイズ増加
env:
  NODE_OPTIONS: "--max-old-space-size=4096"
```

### キャッシュ破損

**症状**: 古いキャッシュが原因で失敗

```yaml
# キャッシュキーにハッシュを含める
- uses: actions/cache@v4
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}-v2  # バージョン更新
```

## テスト失敗

### Flaky テスト

**症状**: 同じコードでテストが不安定

```yaml
# リトライ設定（Jest）
jest --testRetries 3

# GitHub Actions でリトライ
- uses: nick-fields/retry@v2
  with:
    timeout_minutes: 10
    max_attempts: 3
    command: npm test
```

### タイムアウト

**症状**: テストがタイムアウト

```yaml
# タイムアウト延長
jobs:
  test:
    timeout-minutes: 30  # デフォルト360分
    steps:
      - run: npm test -- --testTimeout=60000
```

### 環境依存

**症状**: ローカルで通るがCIで失敗

```bash
# タイムゾーン
TZ=UTC npm test

# ロケール
LC_ALL=C.UTF-8 npm test

# CI環境検出
if [ "$CI" = "true" ]; then
  npm test -- --ci
fi
```

## デプロイ失敗

### 認証エラー

```yaml
# AWS認証（OIDC推奨）
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789:role/GitHubActionsRole
    aws-region: ap-northeast-1
```

```bash
# Docker Hub認証
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
```

### ヘルスチェック失敗

**症状**: デプロイ後にサービスが起動しない

```bash
# ログ確認
kubectl logs deployment/my-app --tail=100

# イベント確認
kubectl describe pod -l app=my-app

# よくある原因
# 1. ポート不一致
# 2. 環境変数不足
# 3. シークレット未設定
# 4. リソース不足（CPU/Memory）
```

### ロールバック

```bash
# Kubernetes
kubectl rollout undo deployment/my-app

# ECS
aws ecs update-service \
  --cluster my-cluster \
  --service my-service \
  --task-definition my-task:PREVIOUS_VERSION
```

## パフォーマンス問題

### ビルド時間短縮

```yaml
# 1. 並列実行
jobs:
  lint:
    runs-on: ubuntu-latest
  test:
    runs-on: ubuntu-latest
  # lint と test が並列実行される

# 2. 変更検出
- uses: dorny/paths-filter@v2
  id: changes
  with:
    filters: |
      backend:
        - 'backend/**'
      frontend:
        - 'frontend/**'

- name: Test backend
  if: steps.changes.outputs.backend == 'true'
  run: cd backend && npm test
```

### キャッシュ最適化

```yaml
# 複数キャッシュ
- uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      ~/.cache/pip
      node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json', '**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-deps-
```

## 権限・認証エラー

### GitHub Actions 権限

```yaml
permissions:
  contents: read
  packages: write
  id-token: write  # OIDC用
```

### シークレットスコープ

```yaml
# リポジトリシークレット
${{ secrets.MY_SECRET }}

# 環境シークレット（environment指定必須）
jobs:
  deploy:
    environment: production
    steps:
      - run: echo "${{ secrets.PROD_SECRET }}"

# Organization シークレット
# Settings > Secrets > Actions で設定
```

## デバッグ手法

### SSH デバッグ（GitHub Actions）

```yaml
- uses: mxschmitt/action-tmate@v3
  if: failure()
  timeout-minutes: 15
```

### 詳細ログ

```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

### ローカル実行

```bash
# act を使用してローカルで GitHub Actions を実行
brew install act
act -j build
```
