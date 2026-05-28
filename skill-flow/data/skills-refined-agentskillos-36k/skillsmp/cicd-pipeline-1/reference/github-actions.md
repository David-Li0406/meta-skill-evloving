# GitHub Actions 詳細リファレンス

## 目次
- ワークフロー構文
- マトリックスビルド
- キャッシュ戦略
- シークレット管理
- 再利用可能ワークフロー
- 自己ホストランナー

## ワークフロー構文

### トリガー設定

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - '!**.md'
  pull_request:
    types: [opened, synchronize, reopened]
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy environment'
        required: true
        default: 'staging'
        type: choice
        options: [staging, production]
```

### 条件付き実行

```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    steps:
      - name: Deploy to production
        if: success()
        run: ./deploy.sh
```

## マトリックスビルド

```yaml
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest]
        node: [18, 20, 22]
        exclude:
          - os: macos-latest
            node: 18
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

## キャッシュ戦略

### npm

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
```

### pip

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

### Docker レイヤーキャッシュ

```yaml
- uses: docker/build-push-action@v5
  with:
    context: .
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## シークレット管理

```yaml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  
steps:
  - name: Deploy
    env:
      AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
      AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    run: aws s3 sync ./dist s3://my-bucket
```

### 環境別シークレット

```yaml
jobs:
  deploy:
    environment: production
    steps:
      - run: echo "${{ secrets.PROD_API_KEY }}"
```

## 再利用可能ワークフロー

### 定義（.github/workflows/reusable-deploy.yml）

```yaml
name: Reusable Deploy
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy_key:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh ${{ inputs.environment }}
        env:
          DEPLOY_KEY: ${{ secrets.deploy_key }}
```

### 呼び出し

```yaml
jobs:
  call-deploy:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
    secrets:
      deploy_key: ${{ secrets.DEPLOY_KEY }}
```

## 自己ホストランナー

```yaml
jobs:
  build:
    runs-on: [self-hosted, linux, x64]
    steps:
      - uses: actions/checkout@v4
      - run: ./build.sh
```

### ラベル設定例
- `self-hosted`: 自己ホスト
- `linux` / `windows` / `macos`: OS
- `x64` / `arm64`: アーキテクチャ
- `gpu`: GPU搭載マシン
