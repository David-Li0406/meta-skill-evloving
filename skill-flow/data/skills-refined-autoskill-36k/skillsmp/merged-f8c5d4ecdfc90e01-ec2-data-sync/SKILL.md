---
name: ec2-data-sync
description: Use this skill to simplify data synchronization and code updates for JRA-VAN on EC2 instances using AWS SSM.
---

# EC2データ同期・コード更新

## 概要

JRA-VANデータの同期とEC2インスタンスへのコード更新を簡単なコマンドで実行します。AWS SSMを利用して、複雑なコマンドをシンプルなインターフェースでラップし、ミスを防止します。

## 主要機能

1. **ファイルアップロード**: Base64エンコードを自動化し、EC2にファイルを送信。
2. **データ差分同期**: 最新データのみを取得。
3. **指定日からの完全同期**: 特定日以降のデータを再取得。
4. **ログ確認**: リアルタイムでCloudWatch Logsからログを表示。
5. **EC2インスタンス状態確認**: インスタンスの状態とSSMエージェントの接続状態を確認。

## 入力形式

```
/ec2-sync <操作>

操作:
  upload <ファイル名>       - ファイルをEC2に送信
  sync                      - 差分同期を実行
  sync-from <YYYYMMDD>      - 指定日からの完全同期
  logs                      - ログ確認
  status                    - EC2インスタンス状態確認
```

## 実行プロセス

### 操作1: ファイルアップロード

**コマンド**:
```
/ec2-sync upload <ファイル名>
```

**実行内容**:
1. EC2インスタンスIDを自動取得。
2. ファイルをBase64エンコード。
3. SSM経由でEC2に送信。
4. 送信完了を確認。

**内部コマンド**:
```bash
INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=*jravan*" \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text)

FILE_B64=$(base64 jravan-api/<ファイル名> | tr -d '\n')
aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters "commands=[\"[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('$FILE_B64')) | Out-File -FilePath C:\\jravan-api\\<ファイル名> -Encoding UTF8 -Force\"]"

echo "✅ <ファイル名> を送信しました"
```

### 操作2: データ差分同期

**コマンド**:
```
/ec2-sync sync
```

**実行内容**:
1. EC2で指定のスクリプトを実行。
2. 最新データのみを取得。
3. 進捗をログで確認。

**内部コマンド**:
```bash
aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters 'commands=["cd C:\\jravan-api; python sync_jvlink.py"]'

echo "✅ データ差分同期を開始しました"
echo "ログ確認: /ec2-sync logs"
```

### 操作3: 指定日からの完全同期

**コマンド**:
```
/ec2-sync sync-from <YYYYMMDD>
```

**実行内容**:
1. 指定日以降のデータを完全に再取得。
2. 既存データは上書き。
3. 大量データの場合は時間がかかる。

**内部コマンド**:
```bash
aws ssm send-command \
  --instance-ids "$INSTANCE_ID" \
  --document-name "AWS-RunPowerShellScript" \
  --parameters 'commands=["cd C:\\jravan-api; python sync_jvlink.py --from <YYYYMMDD>"]'

echo "✅ <YYYYMMDD> からの完全同期を開始しました"
echo "⚠️ 大量データのため、完了まで数時間かかる場合があります"
echo "ログ確認: /ec2-sync logs"
```

### 操作4: ログ確認

**コマンド**:
```
/ec2-sync logs
```

**実行内容**:
1. CloudWatch Logsから最新ログを取得。
2. リアルタイムでログをフォロー。

**内部コマンド**:
```bash
aws logs tail /aws/ec2/jravan --follow
```

### 操作5: EC2インスタンス状態確認

**コマンド**:
```
/ec2-sync status
```

**実行内容**:
1. EC2インスタンスの状態を確認。
2. SSMエージェントの接続状態を確認。

**内部コマンド**:
```bash
aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[].Instances[].[InstanceId,State.Name,LaunchTime]' \
  --output table

aws ssm describe-instance-information \
  --filters "Key=InstanceIds,Values=$INSTANCE_ID" \
  --query 'InstanceInformationList[].[InstanceId,PingStatus,LastPingDateTime]' \
  --output table
```

## エラーハンドリング

### よくあるエラー

1. **インスタンスIDが見つからない**
   ```
   Error: No instances found with tag 'jravan'
   ```
   - 対処: EC2インスタンスが起動しているか確認。

2. **SSMエージェント未接続**
   ```
   Error: TargetNotConnected
   ```
   - 対処: SSMエージェントの起動を確認。

3. **ファイルが見つからない**
   ```
   Error: File not found: jravan-api/<ファイル名>
   ```
   - 対処: カレントディレクトリを確認。

4. **同期スクリプトエラー**
   ```
   Error in sync_jvlink.py
   ```
   - 対処: ログを確認してスクリプトを修正。

## セキュリティ

- **認証**: AWS認証情報が必要（`aws configure`）。
- **IAM権限**: EC2, SSM, CloudWatch Logsの読み取り・書き込み権限。
- **データ保護**: スクリプト内に機密情報をハードコードしない。

## 対象ファイル

### アップロード可能なファイル
- `sync_jvlink.py` - データ同期スクリプト（メイン）
- `race_api.py` - FastAPIサーバー
- `config.py` - 設定ファイル
- `requirements.txt` - Python依存関係

## 使用例

### 例1: スクリプト更新と同期

```
/ec2-sync upload sync_jvlink.py

/ec2-sync sync

/ec2-sync logs
```

### 例2: 特定日からの再同期

```
/ec2-sync sync-from 20260115

/ec2-sync logs
```

## 注意事項

- **同期時間**: 大量データは数時間かかる。
- **データ上書き**: 完全同期は既存データを上書き。
- **SSM制限**: コマンド実行は最大30分でタイムアウト。
- **ログ保持**: CloudWatch Logsは7日間保持。

## 参照

- **AWS SSM**: https://docs.aws.amazon.com/systems-manager/
- **CloudWatch Logs**: https://docs.aws.amazon.com/cloudwatch/