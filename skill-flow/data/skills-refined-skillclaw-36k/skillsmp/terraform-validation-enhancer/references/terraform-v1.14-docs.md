# Terraform 1.14 リファレンス

このドキュメントは、Terraform 1.14の依存関係管理とバリデーション機能のリファレンスです。

---

## Variable Validation（変数のバリデーション）

### 概要

`validation`ブロックを使用して、変数値のカスタム検証ルールを定義できます。型制約に加えて、より具体的な条件を指定可能です。

### 基本構文

```hcl
variable "example" {
  type        = string
  description = "説明"

  validation {
    condition     = <条件式>
    error_message = "エラーメッセージ"
  }
}
```

### 主要パラメータ

| パラメータ | 説明 | 必須 |
|----------|------|------|
| `type` | 変数の型制約 | オプション |
| `default` | デフォルト値 | オプション |
| `description` | 変数の説明 | オプション |
| `validation` | 検証ルールブロック | オプション |
| `sensitive` | CLI出力で値を隠すか | オプション |
| `nullable` | `null`を許可するか | オプション |
| `ephemeral` | stateやplanファイルに保存しない | オプション |

### validation ブロック

- **condition**: 検証条件を定義するブール式。変数値は`var.<name>`で参照
- **error_message**: 条件が`false`の場合に表示されるエラーメッセージ
- **複数のvalidationブロック**: 1つの変数に複数の検証ルールを定義可能

### 実用例

#### 数値範囲の検証

```hcl
variable "instance_count" {
  type = number

  validation {
    condition     = var.instance_count >= 1 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}
```

#### 文字列パターンの検証

```hcl
variable "environment" {
  type = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}
```

#### 正規表現による検証

```hcl
variable "project_name" {
  type = string

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "Project name must contain only lowercase letters, numbers, and hyphens."
  }
}
```

#### センシティブな変数

```hcl
variable "db_password" {
  type      = string
  sensitive = true

  validation {
    condition     = length(var.db_password) >= 12
    error_message = "Password must be at least 12 characters."
  }

  validation {
    condition     = can(regex("[A-Z]", var.db_password))
    error_message = "Password must contain at least one uppercase letter."
  }
}
```

### ベストプラクティス

1. **明確なエラーメッセージ**: 何が問題で、どう修正すべきか明確に
2. **型制約と組み合わせ**: `type`で基本的な型チェック、`validation`で詳細なルール
3. **can()関数の活用**: エラーを吐く可能性のある関数は`can()`でラップ
4. **複数の検証**: 関連する複数の条件は別々の`validation`ブロックに分割

---

## Check Blocks（インフラ検証ブロック）

### 概要

`check`ブロックは、Terraformが管理するインフラの継続的な検証を実行します。`terraform apply`後に実行され、失敗してもapply自体は成功します。

### 基本構文

```hcl
check "check_name" {
  data "resource_type" "name" {
    # データソース設定
  }

  assert {
    condition     = <条件式>
    error_message = "エラーメッセージ"
  }
}
```

### 主要要素

- **data ブロック**: 検証対象のデータを取得
- **assert ブロック**: 検証条件を定義（複数可）
- **condition**: 検証する条件式
- **error_message**: 条件が満たされない場合のメッセージ

### 実用例

#### ヘルスチェック

```hcl
check "health_check" {
  data "http" "app_health" {
    url = "https://${aws_instance.app.public_ip}/health"
  }

  assert {
    condition     = data.http.app_health.status_code == 200
    error_message = "Application health check failed with status ${data.http.app_health.status_code}."
  }
}
```

#### セキュリティコンプライアンス

```hcl
check "s3_security" {
  data "aws_s3_bucket" "example" {
    bucket = aws_s3_bucket.example.id
  }

  assert {
    condition     = data.aws_s3_bucket.example.server_side_encryption_configuration != null
    error_message = "S3 bucket must have encryption enabled."
  }

  assert {
    condition     = data.aws_s3_bucket.example.versioning[0].enabled == true
    error_message = "S3 bucket versioning must be enabled."
  }
}
```

#### 環境別要件の検証

```hcl
check "production_requirements" {
  data "aws_db_instance" "example" {
    db_instance_identifier = aws_db_instance.example.id
  }

  assert {
    condition = (
      var.environment != "prod" ||
      (data.aws_db_instance.example.multi_az == true &&
       data.aws_db_instance.example.backup_retention_period >= 30)
    )
    error_message = "Production databases must have Multi-AZ and 30-day backup retention."
  }
}
```

### 重要な特徴

1. **apply後の検証**: `terraform apply`の後に実行
2. **非ブロッキング**: チェック失敗してもapplyは成功
3. **継続的な検証**: `terraform plan`で警告として表示
4. **実行時状態の確認**: 実際のインフラ状態を検証

---

## Depends On（明示的な依存関係）

### 概要

`depends_on`メタ引数は、リソース間の明示的な依存関係を定義します。通常、Terraformは参照から暗黙的な依存関係を自動的に判断しますが、それでは不十分な場合に使用します。

### 基本構文

```hcl
resource "resource_type" "name" {
  # ... 設定 ...

  depends_on = [
    resource_type.other_resource,
    module.other_module,
  ]
}
```

### 使用場面

#### リソースレベルの依存

```hcl
resource "aws_iam_role" "example" {
  name = "example-role"
}

resource "aws_iam_role_policy" "example" {
  role   = aws_iam_role.example.id
  policy = "..."
}

resource "aws_instance" "example" {
  ami                  = "ami-12345678"
  instance_type        = "t2.micro"
  iam_instance_profile = aws_iam_instance_profile.example.name

  # IAMロールのポリシーが完全に設定されるまで待つ
  depends_on = [
    aws_iam_role_policy.example,
  ]
}
```

#### モジュールレベルの依存

```hcl
module "database" {
  source = "./modules/database"
  vpc_id = module.vpc.vpc_id
}

module "application" {
  source = "./modules/application"

  # データベースが完全にプロビジョニングされてから
  depends_on = [
    module.database,
  ]
}
```

### 使用上の注意

1. **最小限に抑える**: 暗黙的な依存関係で十分な場合は不要
2. **循環依存を避ける**: 相互に依存するリソースは作成できない
3. **パフォーマンス**: 過度な使用は並列実行を妨げる
4. **明確な理由**: なぜ必要かをコメントで記載

### 暗黙的依存 vs 明示的依存

**暗黙的依存（推奨）**:
```hcl
resource "aws_subnet" "example" {
  vpc_id = aws_vpc.example.id  # 暗黙的依存が自動作成される
}
```

**明示的依存（必要な場合のみ）**:
```hcl
resource "aws_instance" "example" {
  # タイミング依存があり、参照だけでは不十分な場合
  depends_on = [aws_iam_role_policy.example]
}
```

---

## Lifecycle（ライフサイクル管理）

### 概要

`lifecycle`メタ引数は、リソースのライフサイクル動作をカスタマイズします。

### 基本構文

```hcl
resource "resource_type" "name" {
  # ... 設定 ...

  lifecycle {
    create_before_destroy = <true|false>
    prevent_destroy       = <true|false>
    ignore_changes        = [<属性リスト>]
    replace_triggered_by  = [<リソース参照リスト>]
    precondition {
      condition     = <条件式>
      error_message = "エラーメッセージ"
    }
    postcondition {
      condition     = <条件式>
      error_message = "エラーメッセージ"
    }
  }
}
```

### 主要オプション

#### create_before_destroy

リソースを置き換える際、新しいリソースを先に作成してから古いリソースを削除します。

```hcl
resource "aws_autoscaling_group" "example" {
  # ... 設定 ...

  lifecycle {
    create_before_destroy = true  # ダウンタイムを回避
  }
}
```

**用途**: ダウンタイムを避けたいリソース（ASG、LB等）

#### prevent_destroy

リソースの削除を防止します。削除を試みるとエラーになります。

```hcl
resource "aws_db_instance" "production" {
  # ... 設定 ...

  lifecycle {
    prevent_destroy = true  # 本番DBを保護
  }
}
```

**用途**: 重要なリソース（DB、S3バケット等）

#### ignore_changes

指定した属性の変更を無視します。Terraform外で変更される属性に使用。

```hcl
resource "aws_instance" "example" {
  ami           = data.aws_ami.latest.id
  instance_type = var.instance_type
  tags          = var.tags

  lifecycle {
    ignore_changes = [
      tags,  # タグはTerraform外で管理
    ]
  }
}
```

**注意**: 過度な使用は構成ドリフトを隠蔽するため、慎重に使用

#### replace_triggered_by

指定したリソースが置き換えられた際に、このリソースも置き換えます。

```hcl
resource "aws_instance" "example" {
  # ... 設定 ...

  lifecycle {
    replace_triggered_by = [
      aws_security_group.example.id
    ]
  }
}
```

### ベストプラクティス

1. **本番環境**: `prevent_destroy = true`を設定
2. **ダウンタイム回避**: `create_before_destroy = true`を使用
3. **ignore_changes**: 必要最小限に、理由をコメント
4. **組み合わせ**: 複数のオプションを同時に使用可能

---

## Preconditions と Postconditions（事前/事後条件）

### 概要

`precondition`と`postcondition`は、リソース、データソース、出力に対して条件チェックを実行します。

### 基本構文

```hcl
resource "resource_type" "name" {
  # ... 設定 ...

  lifecycle {
    precondition {
      condition     = <条件式>
      error_message = "エラーメッセージ"
    }

    postcondition {
      condition     = <条件式>
      error_message = "エラーメッセージ"
    }
  }
}
```

### Precondition（事前条件）

リソース作成**前**に検証します。データソースや他のリソースの属性をチェック。

#### データソースの検証

```hcl
data "aws_ami" "example" {
  most_recent = true
  owners      = ["self"]

  lifecycle {
    precondition {
      condition     = self.architecture == "x86_64"
      error_message = "AMI must be x86_64 architecture."
    }

    precondition {
      condition     = self.root_device_type == "ebs"
      error_message = "AMI must use EBS root device."
    }
  }
}
```

#### リソースの事前条件

```hcl
resource "aws_instance" "example" {
  ami           = data.aws_ami.example.id
  instance_type = var.instance_type

  lifecycle {
    precondition {
      condition     = data.aws_ami.example.state == "available"
      error_message = "AMI must be in available state."
    }

    precondition {
      condition     = var.instance_type != "t2.micro" || var.environment == "dev"
      error_message = "t2.micro is only allowed in dev environment."
    }
  }
}
```

### Postcondition（事後条件）

リソース作成**後**に検証します。作成されたリソースの属性をチェック。

```hcl
resource "aws_db_instance" "example" {
  # ... 設定 ...

  lifecycle {
    postcondition {
      condition     = self.backup_retention_period >= 7
      error_message = "Backup retention must be at least 7 days, got ${self.backup_retention_period}."
    }

    postcondition {
      condition     = self.multi_az == true
      error_message = "Database must be configured for Multi-AZ."
    }

    postcondition {
      condition     = self.storage_encrypted == true
      error_message = "Database storage must be encrypted."
    }
  }
}
```

### Output の条件

```hcl
output "instance_ip" {
  value = aws_instance.example.public_ip

  precondition {
    condition     = aws_instance.example.public_ip != ""
    error_message = "Instance must have a public IP address."
  }
}
```

### 使い分け

| 条件 | タイミング | 用途 | 参照 |
|------|----------|------|------|
| **precondition** | 作成/更新前 | 前提条件の検証 | 他リソース、データソース |
| **postcondition** | 作成/更新後 | 結果の検証 | `self`（自身の属性） |

### ベストプラクティス

1. **具体的なメッセージ**: 何が問題で、どうすべきか明記
2. **早期失敗**: preconditionで問題を早期検出
3. **重要な属性**: セキュリティや可用性に関わる属性を検証
4. **変数補間**: エラーメッセージに実際の値を含める
5. **複数の条件**: 関連する条件は別々のブロックに

---

## 関数リファレンス

### validation で使用する主要関数

#### can()

エラーを返す可能性のある式を安全に評価します。

```hcl
validation {
  condition     = can(regex("^[a-z]+$", var.name))
  error_message = "Name must contain only lowercase letters."
}
```

#### contains()

リストに値が含まれるかチェックします。

```hcl
validation {
  condition     = contains(["dev", "prod"], var.environment)
  error_message = "Environment must be dev or prod."
}
```

#### length()

文字列、リスト、マップの長さを返します。

```hcl
validation {
  condition     = length(var.password) >= 12
  error_message = "Password must be at least 12 characters."
}
```

#### regex()

正規表現にマッチするかチェックします。

```hcl
validation {
  condition     = can(regex("^[0-9]{3}-[0-9]{4}$", var.zip_code))
  error_message = "Zip code must be in format XXX-XXXX."
}
```

---

## 参考リンク

- [Terraform Language Documentation](https://developer.hashicorp.com/terraform/language)
- [Input Variables](https://developer.hashicorp.com/terraform/language/values/variables)
- [Custom Condition Checks](https://developer.hashicorp.com/terraform/language/expressions/custom-conditions)
- [Resource Behavior](https://developer.hashicorp.com/terraform/language/resources/behavior)
