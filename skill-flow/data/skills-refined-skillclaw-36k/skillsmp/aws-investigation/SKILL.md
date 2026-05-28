---
name: aws-investigation
description: AWS MCPを使用してAWSリソースを調査するスキルです。AWS認証はcopilot-setup-stepsワークフローで自動的に実施されます。AWS環境の調査を依頼された場合に使用してください。
---

# AWS調査スキル

このスキルは、AWS MCPを使用してAWSリソースを調査します。AWS認証は`copilot-setup-steps.yml`ワークフローで自動的に実施され、読み取り専用でAWSに接続します。

## 利用可能なツール

このスキルでは以下のツールを使用します:

- **bash**: AWS CLIコマンドの実行
- **view**: CloudFormationテンプレートやIAM設定の確認
- **grep**: AWS関連の設定ファイルの検索

## 使用すべきタイミング

以下の場合にこのスキルを使用してください:

- AWSリソースの調査を依頼された場合
- デプロイされたインフラの状態確認が必要な場合
- CloudFormationスタックの情報取得が必要な場合
- DynamoDBテーブルやその他のAWSリソースの情報確認が必要な場合

## 前提条件

### 必須

- GitHub Secretsに`AWS_INVESTIGATION_ROLE_ARN`が設定されていること
- CloudFormationで`GitHubCopilotInvestigationRole`が作成されていること
- `copilot-setup-steps.yml`ワークフローが実行されていること（AWS認証が自動的に実施されます）

### 権限

調査用Roleは以下の権限を持ちます:

- **ポリシー**: `ReadOnlyAccess`（AWSマネージドポリシー）
- **目的**: AWSリソースの情報を読み取り専用で取得
- **制限**: リソースの作成・変更・削除は不可

## 実行手順

### 1. AWS認証情報の設定

AWS認証は`copilot-setup-steps.yml`ワークフロー内で自動的に実施されます。

#### 1.1 OIDC認証の実行

`copilot-setup-steps.yml`ワークフローで以下の認証ステップが実行されます:

```yaml
- name: Configure AWS credentials for investigation
  uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ secrets.AWS_INVESTIGATION_ROLE_ARN }}
    aws-region: ap-northeast-1
  continue-on-error: true

- name: Verify AWS access
  run: |
    if aws sts get-caller-identity > /dev/null 2>&1; then
      echo "✓ AWS credentials configured successfully"
      echo "AWS_REGION: $AWS_REGION"
    else
      echo "⚠️  AWS credentials not configured. Set AWS_INVESTIGATION_ROLE_ARN secret to enable AWS MCP."
    fi
  continue-on-error: true
```

**注意**: 
- このスキルはGitHub Actions環境内でのみ実行可能です
- AWS認証は`copilot-setup-steps.yml`ワークフローで自動的に実施されます
- `AWS_INVESTIGATION_ROLE_ARN`シークレットが設定されていない場合、警告が表示されますが処理は続行されます
- 認証情報の詳細（Account ID、Role ARNなど）はセキュリティ上の理由から標準出力に出力されません

### 2. AWSリソースの調査

認証後、以下のようなAWS CLIコマンドを実行してリソースを調査します:

#### 2.1 CloudFormationスタックの確認

```bash
# スタック一覧を取得
aws cloudformation list-stacks \
  --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE \
  --query 'StackSummaries[*].[StackName,StackStatus,CreationTime]' \
  --output table

# 特定のスタックの詳細を取得
aws cloudformation describe-stacks \
  --stack-name AttendanceKit-Dev-Stack \
  --query 'Stacks[0]' \
  --output json
```

#### 2.2 DynamoDBテーブルの確認

```bash
# テーブル一覧を取得
aws dynamodb list-tables --output json

# 特定のテーブルの詳細を取得
aws dynamodb describe-table \
  --table-name attendance-kit-dev-clock \
  --output json
```

#### 2.3 Lambda関数の確認

```bash
# Lambda関数一覧を取得
aws lambda list-functions \
  --query 'Functions[*].[FunctionName,Runtime,LastModified]' \
  --output table

# 特定の関数の詳細を取得
aws lambda get-function \
  --function-name attendance-kit-dev-backend \
  --output json
```

#### 2.4 API Gatewayの確認

```bash
# REST API一覧を取得
aws apigateway get-rest-apis \
  --query 'items[*].[name,id,createdDate]' \
  --output table

# 特定のAPIの詳細を取得
aws apigateway get-rest-api \
  --rest-api-id <api-id> \
  --output json
```

#### 2.5 S3バケットの確認

```bash
# バケット一覧を取得
aws s3 ls

# 特定のバケットの情報を取得
aws s3api get-bucket-location \
  --bucket attendance-kit-dev-frontend \
  --output json
```

#### 2.6 CloudWatchログの確認

```bash
# ロググループ一覧を取得
aws logs describe-log-groups \
  --query 'logGroups[*].[logGroupName,storedBytes,creationTime]' \
  --output table

# 特定のロググループの情報を取得
aws logs describe-log-groups \
  --log-group-name-prefix /aws/lambda/attendance-kit-dev \
  --output json

# ログストリーム一覧を取得
aws logs describe-log-streams \
  --log-group-name /aws/lambda/attendance-kit-dev-backend \
  --order-by LastEventTime \
  --descending \
  --max-items 5 \
  --output table

# 最新のログイベントを取得（直近1時間分）
# 1時間前のタイムスタンプをミリ秒で取得
START_TIME=$(($(date +%s) - 3600))000
aws logs filter-log-events \
  --log-group-name /aws/lambda/attendance-kit-dev-backend \
  --start-time ${START_TIME} \
  --query 'events[*].[timestamp,message]' \
  --output text | head -20
```

**注意**: ログには機密情報が含まれる可能性があるため、出力する際は適切にフィルタリングしてください。

### 3. 調査結果のまとめ

調査結果は以下の形式でまとめて報告します:

```markdown
## AWS調査結果

### 調査日時
YYYY-MM-DD HH:MM:SS UTC

### 調査リージョン
ap-northeast-1

### 調査対象リソース

#### CloudFormationスタック
- スタック名: AttendanceKit-Dev-Stack
- ステータス: CREATE_COMPLETE
- 作成日時: YYYY-MM-DD HH:MM:SS

#### DynamoDBテーブル
- テーブル名: attendance-kit-dev-clock
- ステータス: ACTIVE
- アイテム数: XXX
- サイズ: XXX MB

#### CloudWatchログ
- ロググループ: /aws/lambda/attendance-kit-dev-backend
- 最新ログ: YYYY-MM-DD HH:MM:SS
- ストレージサイズ: XXX MB

### 推奨事項
（必要に応じて）
```

**注意**: 調査結果にはAccount IDやRole ARNなどの認証情報を含めないでください。

## 使用例

### 例1: 開発環境のリソース状態確認

```bash
# CloudFormationスタックの確認
aws cloudformation describe-stacks \
  --stack-name AttendanceKit-Dev-Stack \
  --query 'Stacks[0].{Name:StackName,Status:StackStatus,Outputs:Outputs}' \
  --output json

# DynamoDBテーブルの確認
aws dynamodb describe-table \
  --table-name attendance-kit-dev-clock \
  --query 'Table.{Name:TableName,Status:TableStatus,ItemCount:ItemCount}' \
  --output json
```

### 例2: デプロイされたLambda関数の確認

```bash
# Lambda関数の一覧を取得
aws lambda list-functions \
  --query 'Functions[?starts_with(FunctionName, `attendance-kit-dev`)].[FunctionName,Runtime,LastModified]' \
  --output table

# 環境変数の確認（センシティブ情報は除外）
aws lambda get-function-configuration \
  --function-name attendance-kit-dev-backend \
  --query '{FunctionName:FunctionName,Runtime:Runtime,Timeout:Timeout,MemorySize:MemorySize}' \
  --output json
```

### 例3: Lambda関数のCloudWatchログ確認

```bash
# Lambda関数のロググループを確認
aws logs describe-log-groups \
  --log-group-name-prefix /aws/lambda/attendance-kit-dev-backend \
  --query 'logGroups[*].{Name:logGroupName,Size:storedBytes}' \
  --output table

# 最新のログストリームを確認
aws logs describe-log-streams \
  --log-group-name /aws/lambda/attendance-kit-dev-backend \
  --order-by LastEventTime \
  --descending \
  --max-items 1 \
  --query 'logStreams[0].{Stream:logStreamName,LastEvent:lastEventTimestamp}' \
  --output json

# エラーログのみをフィルタリング
# 24時間前のタイムスタンプをミリ秒で取得
START_TIME=$(($(date +%s) - 86400))000
aws logs filter-log-events \
  --log-group-name /aws/lambda/attendance-kit-dev-backend \
  --filter-pattern "ERROR" \
  --start-time ${START_TIME} \
  --query 'events[*].[timestamp,message]' \
  --output text | head -10
```

## トラブルシューティング

### AWS認証エラー

**症状**: `aws sts get-caller-identity`が失敗する

**原因**:
1. `AWS_INVESTIGATION_ROLE_ARN`がGitHub Secretsに設定されていない
2. CloudFormationで`GitHubCopilotInvestigationRole`が作成されていない
3. OIDC認証の設定が正しくない

**対処**:
1. GitHub SecretsでシークレットID `AWS_INVESTIGATION_ROLE_ARN`を確認
2. CloudFormationスタック `AttendanceKit-Setup-Stack`が正しくデプロイされているか確認
3. OIDC認証のステップが正しく実行されているか確認

### 権限エラー

**症状**: `AccessDenied`エラーが発生する

**原因**:
- 調査用RoleにReadOnlyAccess権限しかないため、書き込み操作を実行しようとしている

**対処**:
- このスキルは読み取り専用です。書き込み操作が必要な場合は別のワークフローを使用してください

## セキュリティ考慮事項

- このスキルはReadOnlyAccess権限のみを持つRoleを使用します
- リソースの作成・変更・削除は実行できません
- **認証情報の取り扱い**:
  - Account ID、Role ARN、UserIdなどの認証情報は標準出力に出力しないでください
  - `aws sts get-caller-identity`の結果は、成功/失敗の判定のみに使用し、詳細は出力しないでください
- **ログの取り扱い**:
  - CloudWatchログには機密情報（APIキー、パスワード、個人情報など）が含まれる可能性があります
  - ログを出力する際は、機密情報が含まれていないことを確認してください
  - 必要に応じて、ログのフィルタリングやマスキングを行ってください
- **調査結果の共有**:
  - 調査結果を共有する際は、アカウントIDなどの機密情報を適切にマスクしてください
  - センシティブな情報（パスワード、APIキーなど）は絶対に出力しないでください

## 関連ドキュメント

- [初回セットアップ](../../../infrastructure/setup/README.md)
- [CloudFormationテンプレート](../../../infrastructure/setup/attendance-kit-setup.yaml)
- [Agent開発ガイドライン](../../agents/AGENTS.md)
