---
name: pnpm-workflow
description: |
  pnpmワークフローコマンドを実行します。
  CDKデプロイ、インフラ管理(open/close)、Webビルド・デプロイなどのタスクを実行。
  ユーザーがデプロイ、ビルド、インフラ操作を依頼したときに使用してください。
allowed-tools: Bash
---

# pnpm Workflowスキル

このスキルはプロジェクトのpnpmワークフローコマンドを実行します。

## 利用可能なコマンドカテゴリ

### 1. 統合デプロイ

#### deploy:all - すべてをビルド＆デプロイ ⭐ **推奨**
```bash
pnpm run deploy:all
```
インフラとWebアプリを一括でデプロイする。以下を順次実行：
1. CDKデプロイ（インフラ）
2. Webビルド
3. Webデプロイ

**ユーザーの介入なしで完全なデプロイが完了**します。通常はこのコマンドを使用してください。

### 2. CDK操作

#### cdk:synth - CloudFormationテンプレート生成（デバッグ用）
```bash
pnpm run cdk:synth
```
CDKスタックをCloudFormationテンプレートに変換して確認する。
**注**: `cdk:deploy`は内部で自動的にsynthを実行するため、通常のデプロイでは不要。
デプロイせずにテンプレートだけ確認したい場合や、構文エラーのデバッグ時に使用。

#### cdk:deploy - インフラデプロイ
```bash
pnpm run cdk:deploy
```
CDKスタックをAWSにデプロイする（内部でsynthも実行）。承認なしで自動デプロイ。

#### cdk:destroy - インフラ削除
```bash
pnpm run cdk:destroy
```
デプロイされたCDKスタックを削除する。**慎重に使用**。

#### cdk:diff - 変更差分確認
```bash
pnpm run cdk:diff
```
現在のCDKコードとデプロイ済みスタックの差分を表示。

#### cdk:bootstrap - CDK初期セットアップ
```bash
pnpm run cdk:bootstrap
```
AWS環境でCDKを使用するための初期セットアップ。初回のみ実行。

#### cdk:info - CloudFront情報確認
```bash
pnpm run cdk:info
```
CloudFrontディストリビューションの情報を表示。

### 3. インフラ管理（コスト最適化）

#### infra:close - すべてのインフラを停止
```bash
pnpm run infra:close
```
Lambda、ECS、CloudFrontをすべて停止してコストを削減。

個別に停止する場合:
```bash
pnpm run infra:close:lambda      # Lambda関数の同時実行数を0に
pnpm run infra:close:ecs         # ECSサービスのタスク数を0に
pnpm run infra:close:cloudfront  # CloudFrontを無効化
```

#### infra:open - すべてのインフラを再開
```bash
pnpm run infra:open
```
停止していたLambda、ECS、CloudFrontを再開。

個別に再開する場合:
```bash
pnpm run infra:open:lambda       # Lambda関数の同時実行制限を解除
pnpm run infra:open:ecs          # ECSサービスのタスク数を1に
pnpm run infra:open:cloudfront   # CloudFrontを有効化
```

### 4. Web操作

#### web:build - Webアプリケーションビルド
```bash
pnpm run web:build
```
timtam-webパッケージをビルド。

#### web:deploy - Webアプリケーションデプロイ
```bash
pnpm run web:deploy
```
ビルドしたWebアプリをS3にアップロードしてCloudFrontで配信。

### 5. Orchestratorビルド

#### orchestrator:build - Orchestratorサービスビルド
```bash
pnpm run orchestrator:build
```
orchestratorサービスをビルド。自動的に依存する`@timtam/shared`パッケージも先にビルドされる。

**注**:
- shared パッケージに変更があった場合でも、このコマンド一つで両方ビルドされる
- ビルドが高速なため、毎回 shared を含めてビルドしても問題ない

### 6. テスト

#### test - テスト実行
```bash
pnpm run test
```
orchestratorのテストを実行（Vitest使用）。

**注**:
- 現在、テストはorchestratorサービスにのみ存在します
- `test:watch` と `test:ui` はpackage.jsonに定義されていますが、継続的に実行されるため、Claude Codeでは使用しません（手動実行用）

### 7. その他

#### sso:admin - AWS SSO管理者権限取得 ⚠️ **重要**
```bash
pnpm run sso:admin
```
AWS SSO経由で管理者権限を取得。

**すべてのAWS操作の前に実行が必要**:
- CDK操作（deploy, diff, info等）
- インフラ管理（open/close）
- Web deploy

認証エラーが出た場合は、このコマンドを実行してから再試行する。

#### infra:synth-deploy - 合成とデプロイを一括実行
```bash
pnpm run infra:synth-deploy
```
CDKの合成とデプロイを連続実行。

## 使用シナリオ

### 🔐 AWS認証（必須の初回ステップ）

**すべてのワークフローの最初に実行**:
```bash
pnpm run sso:admin
```

このコマンドでAWS管理者権限を取得してから、以降の操作を実行する。

### デプロイの基本フロー

#### 推奨：一括デプロイ
```bash
pnpm run deploy:all
```
インフラとWebアプリを一度にデプロイ。**通常はこれを使用**。

#### 個別デプロイ（トラブルシューティング時）

1. **インフラのみデプロイ**
   ```bash
   pnpm run cdk:deploy
   ```

2. **Webアプリのみビルド・デプロイ**
   ```bash
   pnpm run web:build
   pnpm run web:deploy
   ```

### コスト削減フロー（開発中断時）

```bash
pnpm run infra:close
```

### 開発再開フロー

```bash
pnpm run infra:open
```

## ベストプラクティス

### デプロイ前の確認
- ✅ `cdk:diff`で変更内容を確認してからデプロイ
- ✅ 本番環境への変更は慎重に
- ✅ CloudFrontの変更は反映に時間がかかることを認識

### コスト管理
- ✅ 開発を中断する時は`infra:close`でリソースを停止
- ✅ 長期間使わない場合は`cdk:destroy`を検討
- ⚠️ `infra:close:cloudfront`は反映に15-20分かかる

### トラブルシューティング
- 🔧 デプロイエラーが出たら`cdk:synth`で構文確認
- 🔧 CloudFront情報が必要なら`cdk:info`
- 🔧 AWS認証エラーが出たら`sso:admin`で再認証

## ユーザー依頼例

- 「すべてデプロイして」 → `deploy:all` ⭐ **推奨**
- 「インフラだけデプロイして」 → `cdk:deploy`
- 「Webアプリだけデプロイ」 → `web:build` → `web:deploy`
- 「orchestratorをビルドして」 → `orchestrator:build`
- 「テストを実行して」 → `test`
- 「今日の作業は終了」 → `infra:close`
- 「開発を再開したい」 → `infra:open`
- 「変更内容を確認したい」 → `cdk:diff`
- 「CloudFrontの情報を見せて」 → `cdk:info`
- 「すべて削除したい」 → `cdk:destroy` (**要確認**)

## 注意事項

### AWS Profile
すべてのコマンドは`--profile admin`を使用しています。AWS SSO設定が必要です。

### 破壊的な操作
以下のコマンドは元に戻せないので注意:
- `cdk:destroy` - スタック全体を削除
- `infra:close` - リソースを停止（データは保持）

### 実行時間
- `deploy:all` - 7-12分程度（CDK + Webビルド + デプロイ）
- `cdk:deploy` - 5-10分程度
- `web:deploy` - 1-2分程度
- `infra:close:cloudfront` / `infra:open:cloudfront` - 15-20分程度

## コマンド実行時の注意

1. **AWS認証の確認**: AWS操作の前に必ず `pnpm run sso:admin` で認証されていることを確認。認証エラーが出た場合は、まず `sso:admin` を実行してから再試行
2. **エラーハンドリング**: コマンド失敗時は出力を確認してユーザーに報告
3. **進捗報告**: 長時間かかるコマンドは実行中であることをユーザーに伝える
4. **確認**: 破壊的な操作は実行前にユーザーに確認を求める
5. **日本語出力**: 実行結果は日本語で要約してユーザーに報告

## パス・環境情報

- ワーキングディレクトリ: `/home/yattom/work/timtam`
- AWS Profile: `admin`
- インフラパッケージ: `timtam-infra`
- Webパッケージ: `timtam-web`
- Orchestratorサービス: `services/orchestrator`
- Sharedパッケージ: `packages/shared`

