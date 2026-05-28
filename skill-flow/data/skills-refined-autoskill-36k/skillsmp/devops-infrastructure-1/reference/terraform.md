# Terraform パターン集

## 目次
- プロジェクト構成
- モジュール設計
- 状態管理
- 変数とアウトプット
- よく使うリソースパターン
- トラブルシューティング

## プロジェクト構成

### 推奨ディレクトリ構造

```
infrastructure/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ecs/
│   └── rds/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── production/
└── shared/
    └── ecr/
```

### backend.tf

```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "env/dev/terraform.tfstate"
    region         = "ap-northeast-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}
```

## モジュール設計

### 入力変数

```hcl
# modules/vpc/variables.tf
variable "name" {
  description = "VPC名"
  type        = string
}

variable "cidr" {
  description = "VPC CIDR"
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.cidr, 0))
    error_message = "有効なCIDRブロックを指定してください"
  }
}

variable "azs" {
  description = "使用するAZ"
  type        = list(string)
}

variable "tags" {
  description = "共通タグ"
  type        = map(string)
  default     = {}
}
```

### アウトプット

```hcl
# modules/vpc/outputs.tf
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "プライベートサブネットID"
  value       = aws_subnet.private[*].id
}

output "public_subnet_ids" {
  description = "パブリックサブネットID"
  value       = aws_subnet.public[*].id
}
```

## 状態管理

### リモート状態参照

```hcl
data "terraform_remote_state" "vpc" {
  backend = "s3"
  config = {
    bucket = "company-terraform-state"
    key    = "env/prod/vpc/terraform.tfstate"
    region = "ap-northeast-1"
  }
}

resource "aws_instance" "app" {
  subnet_id = data.terraform_remote_state.vpc.outputs.private_subnet_ids[0]
}
```

### 状態操作

```bash
# リソースをモジュールに移動
terraform state mv aws_instance.app module.compute.aws_instance.app

# リソース名変更
terraform state mv aws_s3_bucket.old aws_s3_bucket.new

# 状態からリソース削除（実リソースは残る）
terraform state rm aws_instance.temp

# インポート
terraform import aws_s3_bucket.existing bucket-name
```

## よく使うリソースパターン

### ECS Fargate

```hcl
resource "aws_ecs_cluster" "main" {
  name = "${var.name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "app" {
  family                   = "${var.name}-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([
    {
      name  = "app"
      image = "${aws_ecr_repository.app.repository_url}:latest"
      portMappings = [
        {
          containerPort = 8080
          hostPort      = 8080
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.app.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "ecs"
        }
      }
      environment = [
        { name = "ENV", value = var.environment }
      ]
      secrets = [
        { name = "DB_PASSWORD", valueFrom = aws_secretsmanager_secret.db.arn }
      ]
    }
  ])
}

resource "aws_ecs_service" "app" {
  name            = "${var.name}-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = 8080
  }
}
```

### RDS Aurora

```hcl
resource "aws_rds_cluster" "main" {
  cluster_identifier      = "${var.name}-cluster"
  engine                  = "aurora-postgresql"
  engine_version          = "15.4"
  database_name           = var.database_name
  master_username         = var.master_username
  master_password         = var.master_password
  backup_retention_period = 7
  preferred_backup_window = "03:00-04:00"
  vpc_security_group_ids  = [aws_security_group.rds.id]
  db_subnet_group_name    = aws_db_subnet_group.main.name
  skip_final_snapshot     = var.environment != "production"

  serverlessv2_scaling_configuration {
    min_capacity = 0.5
    max_capacity = 16
  }
}

resource "aws_rds_cluster_instance" "main" {
  count               = var.instance_count
  identifier          = "${var.name}-instance-${count.index}"
  cluster_identifier  = aws_rds_cluster.main.id
  instance_class      = "db.serverless"
  engine              = aws_rds_cluster.main.engine
  engine_version      = aws_rds_cluster.main.engine_version
  publicly_accessible = false
}
```

## トラブルシューティング

### よくあるエラー

```bash
# 状態ロック解除
terraform force-unlock LOCK_ID

# 依存関係の問題
terraform apply -target=module.vpc
terraform apply

# プラン差分が消えない
terraform refresh
terraform plan
```

### デバッグ

```bash
# 詳細ログ
TF_LOG=DEBUG terraform plan

# プロバイダーデバッグ
TF_LOG_PROVIDER=DEBUG terraform apply
```
