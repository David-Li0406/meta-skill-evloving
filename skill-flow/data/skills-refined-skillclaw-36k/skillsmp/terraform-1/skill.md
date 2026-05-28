---
name: terraform
description: Terraform IaC設計 - モジュール設計、状態管理、セキュリティベストプラクティス
requires-guidelines:
  - terraform
  - common
---

# Terraform IaC設計

## 使用タイミング

- **インフラ構築・変更時**
- **IaC コードレビュー時**
- **モジュール設計時**
- **状態管理の見直し時**

## 設計パターン

### 🔴 Critical（修正必須）

#### 1. バージョン固定なし
```hcl
# ❌ 危険: バージョン未固定
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

# ✅ 正しい: バージョン固定
terraform {
  required_version = "~> 1.9.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

#### 2. ハードコードされたシークレット
```hcl
# ❌ 危険: シークレットをハードコード
resource "aws_db_instance" "main" {
  username = "admin"
  password = "hardcoded_password"  # 絶対禁止！
}

# ✅ 正しい: Secrets Manager から取得
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "db-password"
}

resource "aws_db_instance" "main" {
  username = "admin"
  password = jsondecode(data.aws_secretsmanager_secret_version.db_password.secret_string)["password"]
}
```

#### 3. リモートステート未使用
```hcl
# ❌ 危険: ローカルステート（チーム開発不可）
# terraform.tfstate がローカルに保存される

# ✅ 正しい: S3 + DynamoDB でリモートステート
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "environments/dev/terraform.tfstate"
    region         = "ap-northeast-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

#### 4. 過度に permissive な IAM ポリシー
```hcl
# ❌ 危険: 全権限付与
resource "aws_iam_role_policy" "bad" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}

# ✅ 正しい: 最小権限の原則
resource "aws_iam_role_policy" "good" {
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject"
      ]
      Resource = "arn:aws:s3:::my-bucket/*"
    }]
  })
}
```

### 🟡 Warning（要改善）

#### 1. モジュール化されていない
```hcl
# ⚠️ 改善推奨: すべてのリソースを main.tf に記述
# main.tf (500行超え)
resource "aws_vpc" "main" { ... }
resource "aws_subnet" "public_1" { ... }
resource "aws_subnet" "public_2" { ... }
# ... 多数のリソース

# ✅ モジュール化
# modules/vpc/main.tf
resource "aws_vpc" "main" { ... }
resource "aws_subnet" "public" {
  for_each = var.public_subnets
  ...
}

# environments/dev/main.tf
module "vpc" {
  source = "../../modules/vpc"

  public_subnets = {
    "public-1" = { cidr = "10.0.1.0/24", az = "ap-northeast-1a" }
    "public-2" = { cidr = "10.0.2.0/24", az = "ap-northeast-1c" }
  }
}
```

#### 2. タグ付けなし
```hcl
# ⚠️ 改善推奨: タグなし
resource "aws_instance" "app" {
  ami           = "ami-xxxxx"
  instance_type = "t3.micro"
}

# ✅ 必須タグを設定
resource "aws_instance" "app" {
  ami           = "ami-xxxxx"
  instance_type = "t3.micro"

  tags = {
    Environment = "dev"
    Project     = "my-app"
    Terraform   = "true"
    ManagedBy   = "platform-team"
  }
}

# ✅ 更に良い: 共通タグをローカル変数で定義
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    Terraform   = "true"
    ManagedBy   = "platform-team"
  }
}

resource "aws_instance" "app" {
  ami           = "ami-xxxxx"
  instance_type = "t3.micro"
  tags          = merge(local.common_tags, { Name = "app-server" })
}
```

#### 3. 公式モジュール未使用
```hcl
# ⚠️ 改善推奨: スクラッチで VPC を構築
resource "aws_vpc" "main" { ... }
resource "aws_subnet" "public" { ... }
resource "aws_route_table" "public" { ... }
# 多数のリソース定義が必要

# ✅ 公式モジュールを活用
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["ap-northeast-1a", "ap-northeast-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = false

  tags = local.common_tags
}
```

## モジュール設計

### ディレクトリ構成
```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── production/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── eks/
│   └── rds/
└── shared/
    └── iam/
```

### モジュールベストプラクティス
| 項目 | 推奨事項 | チェック |
|-----|---------|---------|
| 命名 | リソースタイプを反映（vpc, eks, rds） | [ ] |
| 変数 | description 必須、type 明示 | [ ] |
| 出力 | 他モジュールで使う値を output | [ ] |
| バージョン | メジャーバージョン固定 (version = "~> 5.0") | [ ] |

## チェックリスト

### セキュリティ
- [ ] シークレットはハードコード禁止（Secrets Manager / SSM 連携）
- [ ] IAM ポリシーは最小権限
- [ ] S3 バケットは暗号化有効
- [ ] パブリックアクセス禁止（必要な場合のみ許可）
- [ ] VPC エンドポイント活用

### 状態管理
- [ ] S3 バケット + DynamoDB でリモートステート
- [ ] 環境ごとにステートファイル分離
- [ ] 暗号化有効（encrypt = true）
- [ ] バージョニング有効

### コード品質
- [ ] terraform fmt でフォーマット
- [ ] terraform validate で検証
- [ ] 変数に description と type を設定
- [ ] 必須タグを全リソースに設定

### モジュール
- [ ] terraform-aws-modules 活用
- [ ] バージョン固定（~> X.Y）
- [ ] 環境ごとに tfvars で変数管理

### ワークフロー
- [ ] terraform plan で事前確認
- [ ] PR で plan 結果を共有
- [ ] apply 前にレビュー実施

## 出力形式

🔴 **Critical**: `ファイル:行` - セキュリティリスク/バージョン未固定 - 修正案
🟡 **Warning**: `ファイル:行` - 設計改善推奨 - 改善案
📊 **Summary**: Critical X件 / Warning Y件

## 関連ガイドライン

レビュー実施前に以下のガイドラインを参照:
- `~/.claude/guidelines/infrastructure/terraform.md`

## 外部知識ベース

最新の Terraform ベストプラクティス確認には context7 を活用:
- Terraform 公式ドキュメント
- terraform-aws-modules GitHub
- Terraform Best Practices Guide

## プロジェクトコンテキスト

プロジェクト固有の Terraform 構成を確認:
- serena memory から既存モジュール構成を取得
- プロジェクトの命名規則・タグ体系を優先
- 既存のディレクトリ構造との一貫性を確認
