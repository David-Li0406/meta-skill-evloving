# テンプレート例

## aws_cloudwatch_log_groupの出力例（Provider Version: 6.28.0）

```hcl
#---------------------------------------------------------------
# AWS CloudWatch Log Group
#---------------------------------------------------------------
#
# Amazon CloudWatch Logsのロググループをプロビジョニングするリソースです。
# ロググループは、同じ保持期間・監視・アクセス制御設定を共有するログストリームの
# グループを定義します。
#
# AWS公式ドキュメント:
#   - CloudWatch Logs概要: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html
#   - CloudWatch Logsの概念: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatchLogsConcepts.html
#
# Terraform Registry:
#   - https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group
#
# Provider Version: 6.28.0
# Generated: 2026-01-22
# NOTE: 本テンプレートは生成時点の情報に基づきAIが生成しています。
#       情報が古くなっている可能性、誤りを含む可能性があるため、
#       正確な最新仕様は公式ドキュメントを参照してください。
#
#---------------------------------------------------------------

resource "aws_cloudwatch_log_group" "example" {
  #-------------------------------------------------------------
  # 名前設定
  #-------------------------------------------------------------

  # name (Optional, Forces new resource)
  # 設定内容: ロググループの名前を指定します。
  # 設定可能な値: 1-512文字の文字列
  # 省略時: Terraformがランダムな一意の名前を生成します。
  # 注意: name_prefixと排他的（どちらか一方のみ指定可能）
  name = "/aws/my-application/logs"

  # name_prefix (Optional, Forces new resource)
  # 設定内容: ロググループ名のプレフィックスを指定します。
  # 設定可能な値: 文字列。Terraformが後ろにランダムなサフィックスを追加します。
  # 注意: nameと排他的（どちらか一方のみ指定可能）
  name_prefix = null

  #-------------------------------------------------------------
  # リージョン設定
  #-------------------------------------------------------------

  # region (Optional)
  # 設定内容: このリソースを管理するリージョンを指定します。
  # 設定可能な値: 有効なAWSリージョンコード（例: ap-northeast-1, us-east-1）
  # 省略時: プロバイダー設定のリージョンを使用
  # 参考: https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints
  region = null

  #-------------------------------------------------------------
  # ログクラス設定
  #-------------------------------------------------------------

  # log_group_class (Optional)
  # 設定内容: ロググループのログクラスを指定します。
  # 設定可能な値:
  #   - "STANDARD" (デフォルト): フル機能オプション。リアルタイム監視や頻繁なアクセスに適用
  #   - "INFREQUENT_ACCESS": 低コストオプション。アクセス頻度が低いログ向け。Standardの一部機能のみ
  #   - "DELIVERY": 配信用ログクラス
  # 関連機能: CloudWatch Logs ログクラス
  #   StandardとInfrequent Accessの2つのクラスを提供。用途に応じてコスト最適化が可能。
  #   - https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatchLogsConcepts.html
  log_group_class = "STANDARD"

  #-------------------------------------------------------------
  # 保持期間設定
  #-------------------------------------------------------------

  # retention_in_days (Optional)
  # 設定内容: ログイベントを保持する日数を指定します。
  # 設定可能な値:
  #   0 (無期限), 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365,
  #   400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, 3653
  # 省略時: 0 (ログは無期限に保持され、期限切れになりません)
  # 関連機能: CloudWatch Logs 保持設定
  #   ログイベントの保持期間を設定。期限切れのログは自動的に削除されます。
  #   - https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatchLogsConcepts.html
  # 注意: log_group_classが"DELIVERY"の場合、この引数は無視され強制的に2に設定されます。
  retention_in_days = 30

  #-------------------------------------------------------------
  # 暗号化設定
  #-------------------------------------------------------------

  # kms_key_id (Optional)
  # 設定内容: ログデータの暗号化に使用するKMSキーのARNを指定します。
  # 設定可能な値: 有効なKMSキーARN
  # 関連機能: CloudWatch Logs データ保護
  #   AWS KMS CMKを使用してログデータを暗号化。CMKが関連付け解除された後も、
  #   以前に取り込まれたデータは暗号化されたまま。暗号化されたデータへのアクセス時は
  #   CMKへの権限が必要。
  #   - https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html
  kms_key_id = "arn:aws:kms:ap-northeast-1:123456789012:key/12345678-1234-1234-1234-123456789012"

  #-------------------------------------------------------------
  # 削除保護設定
  #-------------------------------------------------------------

  # deletion_protection_enabled (Optional)
  # 設定内容: ロググループの削除保護を有効にするかを指定します。
  # 設定可能な値:
  #   - true: 削除保護を有効化。明示的に無効化するまで削除操作がブロックされます
  #   - false (デフォルト): 削除保護を無効化
  # 関連機能: CloudWatch Logs 削除保護
  #   ロググループとそのログストリームの誤削除を防止する機能。
  #   監査ログやコンプライアンスデータの保護に有用。
  #   - https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/protecting-log-groups-from-deletion.html
  deletion_protection_enabled = false

  #-------------------------------------------------------------
  # ライフサイクル設定
  #-------------------------------------------------------------

  # skip_destroy (Optional)
  # 設定内容: Terraform destroy時にロググループを削除しないかを指定します。
  # 設定可能な値:
  #   - true: destroy時にロググループ（および含まれるログ）を削除せず、Terraform stateから削除のみ
  #   - false (デフォルト): destroy時にロググループを削除
  # 用途: 重要なログデータを保護したい場合に使用
  skip_destroy = false

  #-------------------------------------------------------------
  # タグ設定
  #-------------------------------------------------------------

  # tags (Optional)
  # 設定内容: リソースに割り当てるタグのマップを指定します。
  # 設定可能な値: キーと値のペアのマップ
  # 関連機能: AWSリソースタグ付け
  #   プロバイダーレベルのdefault_tags設定ブロックで定義されたタグと
  #   一致するキーを持つタグは、プロバイダーレベルで定義されたものを上書きします。
  #   - https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html
  tags = {
    Name        = "my-application-logs"
    Environment = "production"
  }
}

#---------------------------------------------------------------
# Attributes Reference (読み取り専用属性)
#---------------------------------------------------------------
# このリソースは以下の属性をエクスポートします:
#
# - arn: ロググループのAmazon Resource Name (ARN)
#        APIによって追加される `:*` サフィックスは、他のAWSサービスとの
#        互換性のため削除されています。
#
# - tags_all: プロバイダーのdefault_tags設定ブロックから継承されたタグを含む、
#             リソースに割り当てられたすべてのタグのマップ。
#---------------------------------------------------------------
```

## コメントフォーマット

各プロパティには以下の形式でコメントを記載:

```hcl
  # {プロパティ名} ({Optional/Required}{, Forces new resource があれば追記})
  # 設定内容: {何を設定するためのプロパティかの説明}
  # 設定可能な値:
  #   - {値1}: {説明}
  #   - {値2}: {説明}
  # 省略時: {デフォルト値や動作の説明}（オプショナルの場合）
  # 関連機能: {機能名} (名称のある機能に関連する場合のみ)
  #   {機能の簡単な説明}
  #   - {公式ドキュメントのURL}
  # 注意: {注意事項}（必要な場合のみ）
  property_name = "value"
```

**グルーピングルール:**
- 「必須設定」「オプション設定」ではなく、機能カテゴリ別にグループ化
- 例: 「基本設定」「ネットワーク設定」「暗号化設定」「タグ設定」等

## ファイルヘッダーフォーマット

```hcl
#---------------------------------------------------------------
# {リソース表示名}
#---------------------------------------------------------------
#
# {どのようなAWSリソースをプロビジョニングするかの説明}
#
# AWS公式ドキュメント:
#   - {ドキュメント名}: {URL}
#
# Terraform Registry:
#   - {URL}
#
# Provider Version: {version}
# Generated: {YYYY-MM-DD}
# NOTE: 本テンプレートは生成時点の情報に基づきAIが生成しています。
#       情報が古くなっている可能性、誤りを含む可能性があるため、
#       正確な最新仕様は公式ドキュメントを参照してください。
#
#---------------------------------------------------------------
```

## 属性の除外ルール

以下の属性はテンプレートから除外（Attributes Referenceセクションに記載）:

- `computed: true` かつ `optional` がない属性
- 例: `arn`, `id`, `tags_all`
