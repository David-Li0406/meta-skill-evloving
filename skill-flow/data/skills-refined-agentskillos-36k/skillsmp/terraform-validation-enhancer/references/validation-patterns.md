# Terraform Validation Patterns

このドキュメントは、Terraform構成の依存関係管理とバリデーションの評価・強化パターンを提供します。

## 目次

1. [Variable Validation Patterns](#variable-validation-patterns)
2. [Resource Dependencies (depends_on)](#resource-dependencies-depends_on)
3. [Lifecycle Management](#lifecycle-management)
4. [Preconditions and Postconditions](#preconditions-and-postconditions)
5. [Check Blocks](#check-blocks)

---

## Variable Validation Patterns

### 基本パターン

#### パターン1: 値の範囲チェック

```hcl
variable "instance_count" {
  type        = number
  description = "Number of instances to create"

  validation {
    condition     = var.instance_count >= 1 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}
```

#### パターン2: 文字列パターンマッチ

```hcl
variable "environment" {
  type        = string
  description = "Deployment environment"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

#### パターン3: 正規表現による検証

```hcl
variable "project_name" {
  type        = string
  description = "Project name (alphanumeric and hyphens only)"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.project_name))
    error_message = "Project name must contain only lowercase letters, numbers, and hyphens."
  }
}
```

#### パターン4: 複数の検証ルール

```hcl
variable "db_password" {
  type        = string
  sensitive   = true
  description = "Database password"

  validation {
    condition     = length(var.db_password) >= 12
    error_message = "Password must be at least 12 characters long."
  }

  validation {
    condition     = can(regex("[A-Z]", var.db_password))
    error_message = "Password must contain at least one uppercase letter."
  }

  validation {
    condition     = can(regex("[0-9]", var.db_password))
    error_message = "Password must contain at least one number."
  }
}
```

### 評価観点

- [ ] 全ての重要な入力変数にvalidationブロックが設定されているか
- [ ] error_messageが具体的で理解しやすいか
- [ ] 正規表現を使用する場合、can()関数で適切にラップされているか
- [ ] センシティブな値には`sensitive = true`が設定されているか

---

## Resource Dependencies (depends_on)

### 基本パターン

#### パターン1: 明示的な依存関係

```hcl
resource "aws_iam_role" "example" {
  name = "example-role"
  # ...
}

resource "aws_iam_role_policy" "example" {
  role = aws_iam_role.example.id
  # ...

  # Implicit dependency through aws_iam_role.example.id is sufficient
  # depends_on is NOT needed here
}

resource "aws_instance" "example" {
  # ...
  iam_instance_profile = aws_iam_instance_profile.example.name

  # Explicit dependency needed if IAM role needs to be fully configured
  depends_on = [
    aws_iam_role_policy.example,
  ]
}
```

#### パターン2: 複数リソースへの依存

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "private" {
  count      = 2
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.${count.index}.0/24"
}

resource "aws_instance" "app" {
  # ...

  # All subnets must be created before this instance
  depends_on = [
    aws_subnet.private,
  ]
}
```

#### パターン3: モジュール間の依存関係

```hcl
module "vpc" {
  source = "./modules/vpc"
  # ...
}

module "database" {
  source = "./modules/database"
  vpc_id = module.vpc.vpc_id
  # Implicit dependency through module.vpc.vpc_id
}

module "application" {
  source = "./modules/application"
  # ...

  # Ensure database is fully provisioned before deploying app
  depends_on = [
    module.database,
  ]
}
```

### 評価観点

- [ ] depends_onは本当に必要か（暗黙的な依存関係で十分でないか）
- [ ] 循環依存が発生していないか
- [ ] タイミング依存のあるリソース間で適切に設定されているか
- [ ] モジュール間の依存関係が明確に表現されているか

---

## Lifecycle Management

### 基本パターン

#### パターン1: リソースの再作成防止

```hcl
resource "aws_instance" "example" {
  # ...

  lifecycle {
    # Prevent accidental resource destruction
    prevent_destroy = true
  }
}
```

#### パターン2: 新規リソース作成後の置換

```hcl
resource "aws_autoscaling_group" "example" {
  # ...

  lifecycle {
    # Create new ASG before destroying old one
    create_before_destroy = true
  }
}
```

#### パターン3: 特定属性の変更を無視

```hcl
resource "aws_instance" "example" {
  ami           = data.aws_ami.latest.id
  instance_type = var.instance_type
  tags          = var.tags

  lifecycle {
    # Ignore changes to tags made outside Terraform
    ignore_changes = [
      tags,
    ]
  }
}
```

#### パターン4: 条件付きリソース置換

```hcl
resource "aws_db_instance" "example" {
  # ...

  lifecycle {
    # Only recreate if major version changes
    replace_triggered_by = [
      aws_db_parameter_group.example.id,
    ]
  }
}
```

### 評価観点

- [ ] 本番環境リソースには`prevent_destroy`が設定されているか
- [ ] ダウンタイムを避けるべきリソースに`create_before_destroy`が設定されているか
- [ ] ignore_changesの使用が適切か（過度な使用は構成ドリフトを隠蔽する）
- [ ] replace_triggered_byが意図した動作をするか

---

## Preconditions and Postconditions

### 基本パターン

#### パターン1: Data Source Precondition

```hcl
data "aws_ami" "example" {
  most_recent = true
  owners      = ["self"]

  filter {
    name   = "name"
    values = ["my-app-*"]
  }

  lifecycle {
    precondition {
      condition     = self.architecture == "x86_64"
      error_message = "AMI must be x86_64 architecture."
    }
  }
}
```

#### パターン2: Resource Precondition

```hcl
resource "aws_instance" "example" {
  ami           = data.aws_ami.example.id
  instance_type = var.instance_type

  lifecycle {
    precondition {
      condition     = data.aws_ami.example.root_device_type == "ebs"
      error_message = "AMI must use EBS root device."
    }

    precondition {
      condition     = var.instance_type != "t2.micro" || var.environment == "dev"
      error_message = "t2.micro instances are only allowed in dev environment."
    }
  }
}
```

#### パターン3: Resource Postcondition

```hcl
resource "aws_db_instance" "example" {
  # ...

  lifecycle {
    postcondition {
      condition     = self.backup_retention_period >= 7
      error_message = "Database backup retention must be at least 7 days."
    }

    postcondition {
      condition     = self.multi_az == true
      error_message = "Database must be configured for Multi-AZ deployment."
    }
  }
}
```

#### パターン4: Output Precondition

```hcl
output "instance_ip" {
  value = aws_instance.example.public_ip

  precondition {
    condition     = aws_instance.example.public_ip != ""
    error_message = "Instance must have a public IP address."
  }
}
```

### 評価観点

- [ ] データソースの前提条件が検証されているか
- [ ] リソース作成前の条件チェックが適切か
- [ ] リソース作成後の検証が必要な属性に対してpostconditionが設定されているか
- [ ] エラーメッセージが問題の原因と解決方法を示しているか

---

## Check Blocks

### 基本パターン

#### パターン1: 基本的なインフラ検証

```hcl
check "health_check" {
  data "http" "example" {
    url = "https://${aws_instance.example.public_ip}/health"
  }

  assert {
    condition     = data.http.example.status_code == 200
    error_message = "Health check endpoint returned ${data.http.example.status_code}."
  }
}
```

#### パターン2: 複数条件のチェック

```hcl
check "security_compliance" {
  data "aws_s3_bucket" "example" {
    bucket = aws_s3_bucket.example.id
  }

  assert {
    condition     = data.aws_s3_bucket.example.server_side_encryption_configuration != null
    error_message = "S3 bucket must have encryption enabled."
  }

  assert {
    condition     = data.aws_s3_bucket.example.versioning[0].enabled == true
    error_message = "S3 bucket must have versioning enabled."
  }

  assert {
    condition     = data.aws_s3_bucket.example.logging != null
    error_message = "S3 bucket must have access logging enabled."
  }
}
```

#### パターン3: 環境別のチェック

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

#### パターン4: 外部システムの検証

```hcl
check "dns_resolution" {
  data "dns_a_record_set" "example" {
    host = "${var.app_name}.${var.domain}"
  }

  assert {
    condition     = length(data.dns_a_record_set.example.addrs) > 0
    error_message = "DNS record for ${var.app_name}.${var.domain} must resolve to at least one IP address."
  }

  assert {
    condition     = contains(data.dns_a_record_set.example.addrs, aws_instance.example.public_ip)
    error_message = "DNS must point to the instance public IP ${aws_instance.example.public_ip}."
  }
}
```

### 評価観点

- [ ] 重要なインフラの稼働状態を検証しているか
- [ ] セキュリティ要件が満たされているか確認しているか
- [ ] 環境別の要件が適切にチェックされているか
- [ ] 外部依存関係が正しく構成されているか検証しているか
- [ ] check blocksはapply後の検証に使用され、apply自体は失敗しない点を理解しているか

---

## 総合評価チェックリスト

### Variable Validation
- [ ] 全ての公開変数にdescriptionが設定されている
- [ ] 重要な変数にvalidationブロックが設定されている
- [ ] センシティブな変数に`sensitive = true`が設定されている

### Dependencies
- [ ] depends_onは必要最小限に抑えられている
- [ ] 暗黙的な依存関係で不十分な箇所のみdepends_onを使用
- [ ] モジュール間の依存関係が明確

### Lifecycle
- [ ] 本番リソースに`prevent_destroy`が設定されている
- [ ] ダウンタイムを避けるため`create_before_destroy`が適切に使用されている
- [ ] `ignore_changes`の使用が正当化されている

### Conditions
- [ ] 重要なdata sourceにpreconditionが設定されている
- [ ] リソース作成の前提条件がpreconditionで検証されている
- [ ] リソースの重要な属性がpostconditionで検証されている

### Checks
- [ ] インフラの稼働状態を検証するcheck blockが存在する
- [ ] セキュリティ要件を検証するcheck blockが存在する
- [ ] 環境別の要件がcheck blockで検証されている
