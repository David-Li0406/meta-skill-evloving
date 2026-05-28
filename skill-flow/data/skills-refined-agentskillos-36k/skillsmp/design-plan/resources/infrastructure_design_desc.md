# クラウドインフラ構築: インフラ設計

クラウドインフラ構築における設計ドキュメントの作成ガイドです。

## 作成する設計ドキュメント

`docs/design/infrastructure-specification.md` および IaCファイルを作成:

- **システムアーキテクチャ図**: 全体構成の俯瞰図
- **リソース構成**: コンピュート、ストレージ、データベース等
- **ネットワーク設計**: VPC、サブネット、ルーティング
- **セキュリティ設計**: IAM、セキュリティグループ、暗号化
- **可用性・スケーラビリティ**: 冗長化、オートスケーリング
- **コスト見積もり**: 月額コストの試算
- **運用・監視設計**: ログ、メトリクス、アラート

## 補助ツール（基本: Terraform / OpenTofu）

### IaC（Infrastructure as Code）ツール

- **Terraform / OpenTofu**: マルチクラウド対応IaC（基本）
- **AWS CloudFormation / AWS CDK**: AWS特化のIaC
- **Azure Resource Manager (ARM) / Bicep**: Azure特化のIaC
- **Google Cloud Deployment Manager**: GCP特化のIaC
- **Pulumi**: 複数プログラミング言語対応のIaC

### アーキテクチャ図作成

- **Diagrams (Python diagrams)**: コードベースのアーキテクチャ図生成
- **Cloudcraft**: AWS/Azure/GCPアーキテクチャ図作成
- **draw.io / Lucidchart**: 汎用的なアーキテクチャ図作成

### 検証・分析ツール

- **Checkov / tfsec / terrascan**: IaCセキュリティスキャン
- **Infracost**: クラウドコスト見積もり
- **Terraform Docs**: Terraformドキュメント自動生成
- **Rover**: Terraformの可視化ツール

## Terraform設計例

### ディレクトリ構造

```
docs/design/terraform/
├── main.tf           # メインのリソース定義
├── variables.tf      # 変数定義
├── outputs.tf        # 出力値定義
├── terraform.tfvars  # 変数の値
├── versions.tf       # Terraformとプロバイダーバージョン
├── modules/          # 再利用可能なモジュール
│   ├── vpc/
│   ├── compute/
│   └── database/
└── environments/     # 環境別の設定
    ├── dev/
    ├── staging/
    └── production/
```

### main.tf

```hcl
# VPC設定
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-vpc"
    }
  )
}

# パブリックサブネット
resource "aws_subnet" "public" {
  count                   = length(var.availability_zones)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-public-subnet-${count.index + 1}"
      Type = "public"
    }
  )
}

# プライベートサブネット
resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone = var.availability_zones[count.index]

  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-private-subnet-${count.index + 1}"
      Type = "private"
    }
  )
}

# インターネットゲートウェイ
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-igw"
    }
  )
}

# NATゲートウェイ
resource "aws_eip" "nat" {
  count  = length(var.availability_zones)
  domain = "vpc"

  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-nat-eip-${count.index + 1}"
    }
  )
}

resource "aws_nat_gateway" "main" {
  count         = length(var.availability_zones)
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-nat-${count.index + 1}"
    }
  )
}

# セキュリティグループ（Web）
resource "aws_security_group" "web" {
  name        = "${var.project_name}-web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-web-sg"
    }
  )
}

# セキュリティグループ（Database）
resource "aws_security_group" "database" {
  name        = "${var.project_name}-database-sg"
  description = "Security group for database"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "PostgreSQL from web servers"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-database-sg"
    }
  )
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = var.enable_deletion_protection

  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-alb"
    }
  )
}

# RDS Database
resource "aws_db_instance" "main" {
  identifier             = "${var.project_name}-db"
  engine                 = "postgres"
  engine_version         = "15.3"
  instance_class         = var.db_instance_class
  allocated_storage      = var.db_allocated_storage
  storage_encrypted      = true
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.database.id]
  multi_az               = var.db_multi_az
  backup_retention_period = var.db_backup_retention_period
  skip_final_snapshot    = var.skip_final_snapshot

  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-db"
    }
  )
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = aws_subnet.private[*].id

  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-db-subnet-group"
    }
  )
}
```

### variables.tf

```hcl
variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["ap-northeast-1a", "ap-northeast-1c"]
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Allocated storage for RDS (GB)"
  type        = number
  default     = 20
}

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "db_username" {
  description = "Database master username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

variable "db_multi_az" {
  description = "Enable Multi-AZ for RDS"
  type        = bool
  default     = false
}

variable "db_backup_retention_period" {
  description = "Backup retention period in days"
  type        = number
  default     = 7
}

variable "enable_deletion_protection" {
  description = "Enable deletion protection for ALB"
  type        = bool
  default     = true
}

variable "skip_final_snapshot" {
  description = "Skip final snapshot on RDS deletion"
  type        = bool
  default     = false
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}
```

### outputs.tf

```hcl
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "alb_dns_name" {
  description = "ALB DNS name"
  value       = aws_lb.main.dns_name
}

output "database_endpoint" {
  description = "Database endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}
```

### terraform.tfvars

```hcl
project_name = "myapp"
environment  = "production"

vpc_cidr           = "10.0.0.0/16"
availability_zones = ["ap-northeast-1a", "ap-northeast-1c"]

db_instance_class           = "db.t3.medium"
db_allocated_storage        = 100
db_name                     = "myapp"
db_username                 = "admin"
db_multi_az                 = true
db_backup_retention_period  = 30
enable_deletion_protection  = true
skip_final_snapshot         = false

common_tags = {
  Project     = "myapp"
  Environment = "production"
  ManagedBy   = "Terraform"
}
```

## アーキテクチャ図生成（Python Diagrams）

### インストール

```bash
pip install diagrams
```

### 基本的な3層アーキテクチャ

`docs/design/architecture_diagram.py`:

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, AutoScaling
from diagrams.aws.network import ELB, VPC, Route53
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.security import IAM, SecretsManager
from diagrams.aws.management import Cloudwatch

with Diagram("Web Service Architecture", show=False, direction="TB"):
    dns = Route53("Route53")

    with Cluster("VPC"):
        lb = ELB("Application\nLoad Balancer")

        with Cluster("Public Subnet"):
            nat = EC2("NAT Gateway")

        with Cluster("Private Subnet - Web"):
            web_group = [
                EC2("Web Server 1"),
                EC2("Web Server 2"),
            ]
            asg = AutoScaling("Auto Scaling")

        with Cluster("Private Subnet - Database"):
            db_master = RDS("RDS Master")
            db_replica = RDS("RDS Replica")

    storage = S3("S3 Bucket")
    secrets = SecretsManager("Secrets Manager")
    monitoring = Cloudwatch("CloudWatch")

    # Connections
    dns >> lb
    lb >> web_group
    web_group >> db_master
    db_master >> Edge(label="replication") >> db_replica
    web_group >> storage
    web_group >> secrets
    web_group >> monitoring
    asg >> web_group
```

### マイクロサービスアーキテクチャ

```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS, Fargate
from diagrams.aws.network import APIGateway, CloudFront
from diagrams.aws.database import Dynamodb, ElastiCache
from diagrams.aws.integration import SQS, SNS

with Diagram("Microservices Architecture", show=False):
    cdn = CloudFront("CloudFront")
    api = APIGateway("API Gateway")

    with Cluster("ECS Cluster"):
        services = [
            Fargate("User Service"),
            Fargate("Order Service"),
            Fargate("Payment Service"),
        ]

    cache = ElastiCache("Redis Cache")
    db = Dynamodb("DynamoDB")
    queue = SQS("SQS Queue")
    topic = SNS("SNS Topic")

    cdn >> api >> services
    services >> cache
    services >> db
    services >> queue
    services >> topic
```

実行:

```bash
python architecture_diagram.py
# web_service_architecture.png が生成される
```

## インフラ仕様書テンプレート

`docs/design/infrastructure-specification.md`:

```markdown
# インフラ仕様: [プロジェクト名]

## システムアーキテクチャ概要

[全体構成の説明]

### アーキテクチャ図

![Architecture Diagram](./architecture_diagram.png)

## 環境

| 環境        | 用途             | URL                         |
| ----------- | ---------------- | --------------------------- |
| Development | 開発環境         | https://dev.example.com     |
| Staging     | ステージング環境 | https://staging.example.com |
| Production  | 本番環境         | https://example.com         |

## リソース構成

### コンピュート

| リソース    | スペック                   | 数量                | 用途                |
| ----------- | -------------------------- | ------------------- | ------------------- |
| EC2 (Web)   | t3.medium (2vCPU, 4GB RAM) | 2-10 (Auto Scaling) | Webアプリケーション |
| EC2 (Batch) | t3.large (2vCPU, 8GB RAM)  | 1                   | バッチ処理          |
| ECS Fargate | 0.5vCPU, 1GB RAM           | 動的                | マイクロサービス    |

### ストレージ

| リソース    | 容量               | 用途                       |
| ----------- | ------------------ | -------------------------- |
| EBS (gp3)   | 100GB × サーバー数 | OS・アプリケーション       |
| S3 Standard | 無制限             | 静的ファイル、バックアップ |
| S3 Glacier  | 無制限             | 長期アーカイブ             |

### データベース

| リソース          | スペック                      | 構成                        | 用途                   |
| ----------------- | ----------------------------- | --------------------------- | ---------------------- |
| RDS PostgreSQL    | db.t3.medium (2vCPU, 4GB RAM) | Multi-AZ                    | メインデータベース     |
| RDS Read Replica  | db.t3.medium                  | 2台                         | 読み取り専用レプリカ   |
| ElastiCache Redis | cache.t3.micro                | 2ノード（レプリケーション） | セッション・キャッシュ |

## ネットワーク設計

### VPC

- **CIDR**: 10.0.0.0/16
- **リージョン**: ap-northeast-1 (東京)
- **アベイラビリティーゾーン**: 2 AZ構成 (1a, 1c)

### サブネット

| 名前              | CIDR         | AZ  | 用途                   |
| ----------------- | ------------ | --- | ---------------------- |
| public-subnet-1   | 10.0.0.0/24  | 1a  | ALB, NAT Gateway       |
| public-subnet-2   | 10.0.1.0/24  | 1c  | ALB, NAT Gateway       |
| private-subnet-1  | 10.0.10.0/24 | 1a  | Web Server, App Server |
| private-subnet-2  | 10.0.11.0/24 | 1c  | Web Server, App Server |
| database-subnet-1 | 10.0.20.0/24 | 1a  | RDS, ElastiCache       |
| database-subnet-2 | 10.0.21.0/24 | 1c  | RDS, ElastiCache       |

### ルーティング

**パブリックルートテーブル**:

- 0.0.0.0/0 → Internet Gateway

**プライベートルートテーブル**:

- 0.0.0.0/0 → NAT Gateway

## セキュリティ設計

### IAM

#### ロール一覧

| ロール名              | 信頼エンティティ | ポリシー                       | 用途        |
| --------------------- | ---------------- | ------------------------------ | ----------- |
| ec2-web-role          | EC2              | S3ReadOnly, SecretsManagerRead | Webサーバー |
| ecs-task-role         | ECS Task         | DynamoDBFullAccess             | ECSタスク   |
| lambda-execution-role | Lambda           | CloudWatchLogs, S3ReadWrite    | Lambda関数  |

#### ポリシー原則

- 最小権限の原則（Principle of Least Privilege）
- ロールベースのアクセス制御（RBAC）
- MFA（多要素認証）の強制

### セキュリティグループ

| 名前     | インバウンド                    | アウトバウンド | 用途         |
| -------- | ------------------------------- | -------------- | ------------ |
| alb-sg   | 80 (0.0.0.0/0), 443 (0.0.0.0/0) | All            | ALB          |
| web-sg   | 80 (alb-sg), 443 (alb-sg)       | All            | Webサーバー  |
| app-sg   | 8080 (web-sg)                   | All            | Appサーバー  |
| db-sg    | 5432 (app-sg)                   | All            | データベース |
| redis-sg | 6379 (app-sg)                   | All            | Redis        |

### 暗号化

| リソース   | 暗号化方式 | 鍵管理        |
| ---------- | ---------- | ------------- |
| EBS        | AES-256    | AWS KMS       |
| S3         | AES-256    | AWS KMS       |
| RDS        | AES-256    | AWS KMS       |
| データ転送 | TLS 1.3    | ACM（証明書） |

### WAF（Web Application Firewall）

- SQLインジェクション対策
- XSS（Cross-Site Scripting）対策
- レート制限（1000リクエスト/5分/IP）

## 可用性・スケーラビリティ

### 高可用性

| コンポーネント | 冗長化                  | RPO | RTO  |
| -------------- | ----------------------- | --- | ---- |
| Webサーバー    | Multi-AZ + Auto Scaling | -   | 5分  |
| データベース   | Multi-AZ + Read Replica | 5分 | 15分 |
| ストレージ     | S3（標準で11 9's）      | -   | -    |

- **RPO（Recovery Point Objective）**: データ損失許容時間
- **RTO（Recovery Time Objective）**: サービス復旧目標時間

### Auto Scaling

**スケールアウト条件**:

- CPU使用率 > 70% が 5分継続
- または、リクエスト数 > 1000/分

**スケールイン条件**:

- CPU使用率 < 30% が 10分継続

**設定**:

- 最小: 2台
- 最大: 10台
- 希望: 2台

### ロードバランシング

- **タイプ**: Application Load Balancer (ALB)
- **ヘルスチェック**: HTTP GET / (30秒間隔)
- **スティッキーセッション**: 有効（Cookie based）

## コスト見積もり

### 月額コスト（本番環境）

| リソース         | 詳細                     | 月額コスト（USD） |
| ---------------- | ------------------------ | ----------------- |
| EC2 (Web)        | t3.medium × 2台 (平均)   | $60               |
| RDS (PostgreSQL) | db.t3.medium (Multi-AZ)  | $150              |
| RDS Read Replica | db.t3.medium × 2台       | $150              |
| ElastiCache      | cache.t3.micro × 2ノード | $30               |
| ALB              | 1台                      | $20               |
| S3               | 100GB ストレージ + 転送  | $10               |
| データ転送       | 500GB/月                 | $45               |
| CloudWatch       | ログ・メトリクス         | $15               |
| **合計**         |                          | **$480**          |

### コスト削減策

- Reserved Instances（1年契約）: 30-40% 削減
- Savings Plans: 柔軟な割引
- S3 ライフサイクルポリシー: 古いデータをGlacierへ移動

## 運用・監視設計

### ログ管理

| ログタイプ             | 保存先          | 保存期間 |
| ---------------------- | --------------- | -------- |
| アプリケーションログ   | CloudWatch Logs | 30日     |
| アクセスログ           | S3              | 90日     |
| VPC Flow Logs          | CloudWatch Logs | 7日      |
| CloudTrail（監査ログ） | S3              | 7年      |

### メトリクス

| メトリクス        | 収集間隔 | アラート閾値     |
| ----------------- | -------- | ---------------- |
| CPU使用率         | 1分      | > 80%            |
| メモリ使用率      | 1分      | > 90%            |
| ディスク使用率    | 5分      | > 85%            |
| RDSコネクション数 | 1分      | > 80% (最大数の) |
| ALBエラーレート   | 1分      | > 5%             |
| レスポンスタイム  | 1分      | > 1秒 (P95)      |

### アラート

| アラート名      | 条件            | 通知先           | アクション   |
| --------------- | --------------- | ---------------- | ------------ |
| High CPU        | CPU > 80% (5分) | Slack, Email     | Auto Scaling |
| Database Down   | RDS Unavailable | PagerDuty, Phone | 即時対応     |
| High Error Rate | Error Rate > 5% | Slack            | 調査         |
| Disk Full       | Disk > 85%      | Email            | ディスク拡張 |

### バックアップ

| リソース | バックアップ方法     | 頻度         | 保持期間 |
| -------- | -------------------- | ------------ | -------- |
| RDS      | 自動スナップショット | 毎日         | 30日     |
| EBS      | AWS Backup           | 毎日         | 7日      |
| S3       | バージョニング       | リアルタイム | 90日     |

## ディザスタリカバリ

### バックアップリージョン

- **プライマリ**: ap-northeast-1 (東京)
- **セカンダリ**: ap-northeast-3 (大阪)

### リカバリ手順

1. セカンダリリージョンでRDSスナップショットから復元
2. S3バケットのレプリケーションデータを使用
3. Route53でDNSフェイルオーバー
4. トラフィックをセカンダリリージョンへ切り替え

## セキュリティ監査

### コンプライアンス

- [ ] CIS AWS Foundations Benchmark
- [ ] PCI DSS（決済情報を扱う場合）
- [ ] SOC 2 Type II

### 脆弱性スキャン

- **ツール**: AWS Inspector, Checkov
- **頻度**: 週次
- **対応**: Critical/Highは24時間以内

## Terraformコマンド

### 初期化

\`\`\`bash
terraform init
\`\`\`

### プラン確認

\`\`\`bash
terraform plan
\`\`\`

### 適用

\`\`\`bash
terraform apply
\`\`\`

### 破棄

\`\`\`bash
terraform destroy
\`\`\`

### セキュリティスキャン

\`\`\`bash

# Checkov

checkov -d .

# tfsec

tfsec .

# terrascan

terrascan scan
\`\`\`

### コスト見積もり

\`\`\`bash
infracost breakdown --path .
\`\`\`

### ドキュメント生成

\`\`\`bash
terraform-docs markdown table . > README.md
\`\`\`
```

## テスト設計の考慮事項

1. **構文チェック**

   - `terraform validate`: Terraform構文チェック
   - `terraform fmt`: フォーマットチェック

2. **セキュリティテスト**

   - Checkov, tfsec, terrascan でスキャン
   - IAMポリシーの最小権限確認

3. **コストテスト**

   - Infracost でコスト見積もり
   - 予算を超えていないか確認

4. **統合テスト**
   - Terratest（Go）でインフラのテスト
   - 実際にリソースを作成して動作確認

## 設計チェックリスト

- [ ] アーキテクチャ図が作成されているか
- [ ] リソース構成が明確に定義されているか
- [ ] ネットワーク設計（VPC、サブネット）が適切か
- [ ] セキュリティグループが最小権限の原則に従っているか
- [ ] IAMロールとポリシーが適切に設計されているか
- [ ] 暗号化が適切に実装されているか
- [ ] Multi-AZ構成で高可用性が確保されているか
- [ ] Auto Scalingが適切に設定されているか
- [ ] バックアップ戦略が定義されているか
- [ ] 監視・アラート設定が適切か
- [ ] コスト見積もりが行われているか
- [ ] ディザスタリカバリ計画が策定されているか
